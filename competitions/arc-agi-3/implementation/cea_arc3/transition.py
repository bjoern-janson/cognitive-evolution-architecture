from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Iterable, Optional

import numpy as np

from .state import RawHistory, TransitionRecord

BUCKET_EDGES = (0, 1, 4, 16, 64, 256)
STATE_DELTA_CLASSES = ("SAME", "WIN", "GAME_OVER")


def frame_sha256(frame: np.ndarray) -> str:
    arr = np.asarray(frame, dtype=np.int16)
    return sha256(arr.tobytes()).hexdigest()


def action_mask(actions: Iterable[int]) -> int:
    mask = 0
    for a in actions:
        i = int(a)
        if i < 0 or i > 7:
            raise ValueError(f"invalid action id: {i}")
        mask |= 1 << i
    return mask


def changed_bucket(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n <= 4:
        return 2
    if n <= 16:
        return 3
    if n <= 64:
        return 4
    if n <= 256:
        return 5
    return 6


def coord_bin(coord: Optional[tuple[int, int]]) -> Optional[int]:
    if coord is None:
        return None
    x, y = coord
    if not (0 <= x <= 63 and 0 <= y <= 63):
        raise ValueError("ACTION6 coordinate outside 64x64 frame")
    return (y // 8) * 8 + (x // 8)


def state_delta_class(state_before: str, state_after: str) -> str:
    before = str(state_before)
    after = str(state_after)
    if after == "WIN" and before != "WIN":
        return "WIN"
    if after == "GAME_OVER" and before != "GAME_OVER":
        return "GAME_OVER"
    return "SAME"


def transition_record_from_arrays(
    *,
    before: np.ndarray,
    after: np.ndarray,
    action_token: int,
    action_coordinate: Optional[tuple[int, int]],
    state_before: str,
    state_after: str,
    level_before: int,
    level_after: int,
    available_actions_before: Iterable[int],
    available_actions_after: Iterable[int],
    prior_hashes: Iterable[str] = (),
) -> TransitionRecord:
    a = np.asarray(before)
    b = np.asarray(after)
    if a.shape != b.shape:
        raise ValueError("v1.x implementation requires stable visible frame shape")
    changed = int(np.count_nonzero(a != b))
    post_hash = frame_sha256(b)
    return TransitionRecord(
        action_token=int(action_token),
        action_coordinate=action_coordinate,
        pre_frame_hash=frame_sha256(a),
        post_frame_hash=post_hash,
        z_change=int(changed > 0),
        changed_cell_count=changed,
        changed_count_bucket=changed_bucket(changed),
        state_before=str(state_before),
        state_after=str(state_after),
        level_before=int(level_before),
        level_after=int(level_after),
        available_action_mask_before=action_mask(available_actions_before),
        available_action_mask_after=action_mask(available_actions_after),
        exact_return_flag=int(post_hash in set(prior_hashes)),
    )


@dataclass
class BinaryCounts:
    zero: int = 1
    one: int = 1

    @property
    def p_one(self) -> float:
        return self.one / (self.zero + self.one)

    def update(self, z: int) -> None:
        if z == 0:
            self.zero += 1
        elif z == 1:
            self.one += 1
        else:
            raise ValueError("binary outcome required")


@dataclass
class BucketCounts:
    counts: list[int] = field(default_factory=lambda: [1] * 7)

    def probabilities(self) -> tuple[float, ...]:
        total = sum(self.counts)
        return tuple(c / total for c in self.counts)

    def update(self, bucket: int) -> None:
        if int(bucket) not in range(7):
            raise ValueError("bucket must be in 0..6")
        self.counts[int(bucket)] += 1


@dataclass
class StateDeltaCounts:
    counts: dict[str, int] = field(default_factory=lambda: {k: 1 for k in STATE_DELTA_CLASSES})

    def probabilities(self) -> tuple[float, ...]:
        total = sum(self.counts.values())
        return tuple(self.counts[k] / total for k in STATE_DELTA_CLASSES)

    def update(self, outcome: str) -> None:
        if outcome not in self.counts:
            raise ValueError(f"unknown state delta class: {outcome}")
        self.counts[outcome] += 1


@dataclass
class AggregateCell:
    """v1/v1.1 base/Q aggregate: primary binary + changed-count bucket only."""

    binary: BinaryCounts = field(default_factory=BinaryCounts)
    buckets: BucketCounts = field(default_factory=BucketCounts)


@dataclass
class SecondaryCell:
    """v1.4 secondary heads; base-context only, never stored in Q_t."""

    state_delta: StateDeltaCounts = field(default_factory=StateDeltaCounts)
    level_delta_positive: BinaryCounts = field(default_factory=BinaryCounts)
    action_surface_changed: BinaryCounts = field(default_factory=BinaryCounts)
    exact_return: BinaryCounts = field(default_factory=BinaryCounts)


class TransitionModel:
    """Conventional count-based predictive substrate shared by all arms.

    `base` and predicate-contingency `q` preserve the v1/v1.1 primary object.
    v1.4 secondary heads live in `secondary_base` keyed by the same base context
    and are instrumentation-only; they are not consulted by action selection,
    hypothesis generation, CLPR, or X.
    """

    PREDICATE_IDS = (
        "prev_action",
        "prev_z",
        "prev2_action",
        "prev2_z",
        "prev_coord_bin",
        "prev2_coord_bin",
        "current_equals_prev_post",
        "available_action_mask",
    )

    def __init__(self) -> None:
        self.base: dict[tuple[Any, ...], AggregateCell] = defaultdict(AggregateCell)
        self.q: dict[tuple[Any, ...], AggregateCell] = defaultdict(AggregateCell)
        self.secondary_base: dict[tuple[Any, ...], SecondaryCell] = defaultdict(SecondaryCell)

    @staticmethod
    def base_context(
        action_token: int,
        coordinate: Optional[tuple[int, int]],
        history: RawHistory,
        available_action_mask: int,
    ) -> tuple[Any, ...]:
        records = history.as_tuple()
        prev = records[-1] if records else None
        return (
            int(action_token),
            coord_bin(coordinate) if int(action_token) == 6 else None,
            prev.action_token if prev else "START",
            prev.z_change if prev else "START",
            int(available_action_mask),
        )

    @staticmethod
    def predicate_values(history: RawHistory, current_frame_hash: str, available_action_mask: int) -> dict[str, Any]:
        records = history.as_tuple()
        prev = records[-1] if len(records) >= 1 else None
        prev2 = records[-2] if len(records) >= 2 else None
        return {
            "prev_action": prev.action_token if prev else "START",
            "prev_z": prev.z_change if prev else "START",
            "prev2_action": prev2.action_token if prev2 else "START",
            "prev2_z": prev2.z_change if prev2 else "START",
            "prev_coord_bin": coord_bin(prev.action_coordinate) if prev and prev.action_token == 6 else None,
            "prev2_coord_bin": coord_bin(prev2.action_coordinate) if prev2 and prev2.action_token == 6 else None,
            "current_equals_prev_post": bool(prev and current_frame_hash == prev.post_frame_hash),
            "available_action_mask": int(available_action_mask),
        }

    def predict(self, context: tuple[Any, ...]) -> tuple[float, tuple[float, ...]]:
        cell = self.base[context]
        return cell.binary.p_one, cell.buckets.probabilities()

    def predict_secondary(self, context: tuple[Any, ...]) -> dict[str, Any]:
        base = self.base[context]
        sec = self.secondary_base[context]
        return {
            "changed_count_bucket": base.buckets.probabilities(),
            "state_delta_class": sec.state_delta.probabilities(),
            "level_delta_positive": sec.level_delta_positive.p_one,
            "action_surface_changed": sec.action_surface_changed.p_one,
            "exact_return_flag": sec.exact_return.p_one,
        }

    def predict_local(self, context: tuple[Any, ...], predicate_id: str, predicate_value: Any) -> float:
        return self.q[(context, predicate_id, self._freeze_value(predicate_value))].binary.p_one

    def update(
        self,
        *,
        context: tuple[Any, ...],
        predicate_values: dict[str, Any],
        z_change: int,
        bucket: int,
        state_delta: str = "SAME",
        level_delta_positive: int = 0,
        action_surface_changed: int = 0,
        exact_return_flag: int = 0,
    ) -> None:
        cell = self.base[context]
        cell.binary.update(z_change)
        cell.buckets.update(bucket)
        for pid in self.PREDICATE_IDS:
            value = self._freeze_value(predicate_values[pid])
            qcell = self.q[(context, pid, value)]
            qcell.binary.update(z_change)
            qcell.buckets.update(bucket)

        sec = self.secondary_base[context]
        sec.state_delta.update(state_delta)
        sec.level_delta_positive.update(int(level_delta_positive))
        sec.action_surface_changed.update(int(action_surface_changed))
        sec.exact_return.update(int(exact_return_flag))

    def reset(self) -> None:
        self.base.clear()
        self.q.clear()
        self.secondary_base.clear()

    @staticmethod
    def _freeze_value(value: Any) -> Any:
        if isinstance(value, list):
            return tuple(value)
        if isinstance(value, dict):
            return tuple(sorted(value.items()))
        return value

    @staticmethod
    def binary_nll(prob: float, outcome: int) -> float:
        p = min(max(float(prob), 1e-6), 1 - 1e-6)
        return -math.log(p if outcome else 1 - p)

    @staticmethod
    def categorical_nll(probabilities: Iterable[float], outcome_index: int) -> float:
        probs = tuple(float(p) for p in probabilities)
        if int(outcome_index) not in range(len(probs)):
            raise ValueError("categorical outcome outside probability vector")
        p = min(max(probs[int(outcome_index)], 1e-6), 1 - 1e-6)
        return -math.log(p)

    @staticmethod
    def entropy(prob: float) -> float:
        p = min(max(float(prob), 1e-12), 1 - 1e-12)
        return -(p * math.log(p) + (1 - p) * math.log(1 - p))
