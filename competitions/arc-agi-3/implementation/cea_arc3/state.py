from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Deque, Iterable, Mapping, Optional

H_RAW = 2
MAX_HYPOTHESES = 32
MAX_CANONICAL = 64


class CanonicalStatus(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"


@dataclass(frozen=True)
class TransitionRecord:
    action_token: int
    action_coordinate: Optional[tuple[int, int]]
    pre_frame_hash: str
    post_frame_hash: str
    z_change: int
    changed_cell_count: int
    changed_count_bucket: int
    state_before: str
    state_after: str
    level_before: int
    level_after: int
    available_action_mask_before: int
    available_action_mask_after: int
    exact_return_flag: int

    def __post_init__(self) -> None:
        if self.z_change not in (0, 1):
            raise ValueError("z_change must be binary")
        if self.changed_count_bucket not in range(7):
            raise ValueError("changed_count_bucket must be in 0..6")
        if self.exact_return_flag not in (0, 1):
            raise ValueError("exact_return_flag must be binary")


class RawHistory:
    """Bounded raw transition window. It can never hold more than H_RAW records."""

    def __init__(self, records: Optional[Iterable[TransitionRecord]] = None) -> None:
        self._records: Deque[TransitionRecord] = deque(maxlen=H_RAW)
        if records:
            for record in records:
                self.append(record)

    def append(self, record: TransitionRecord) -> None:
        self._records.append(record)

    def clear(self) -> None:
        self._records.clear()

    def as_tuple(self) -> tuple[TransitionRecord, ...]:
        return tuple(self._records)

    def __len__(self) -> int:
        return len(self._records)

    def __iter__(self):
        return iter(self._records)

    def hash(self) -> str:
        payload = repr(self.as_tuple()).encode("utf-8")
        return sha256(payload).hexdigest()


@dataclass(frozen=True)
class ObservationDescriptor:
    frame_sha256: str
    color_histogram: tuple[int, ...]
    non_modal_color: int
    non_modal_cells: int
    available_action_mask: int


@dataclass
class RepresentationalState:
    current_frame: Any
    descriptor: ObservationDescriptor
    raw_window: RawHistory
    distinctions: dict[str, "Hypothesis"] = field(default_factory=dict)


@dataclass(frozen=True)
class GoalState:
    environment_state: str
    levels_completed: int
    live_action_mask: int
    remaining_action_budget: int
    remaining_wallclock_budget: float


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    game_slug: str
    level_index: int
    interaction_step: int
    current_frame_hash: str
    raw_window_hash: str
    action_token: int
    action_coordinate: Optional[tuple[int, int]]
    result_signature: tuple[Any, ...]


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    claim_id: str
    evidence_ids_considered: tuple[str, ...]
    proposal_snapshot_hash: str
    metric_values: Mapping[str, float]
    decision: str
    reason_code: str


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    parent_claim_or_null: Optional[str]
    proposal_snapshot_hash: str
    predicate: tuple[str, Any]
    scope: tuple[Any, ...]
    current_status: str


@dataclass
class LineageState:
    evidence: dict[str, EvidenceRecord] = field(default_factory=dict)
    claims: dict[str, ClaimRecord] = field(default_factory=dict)
    decisions: dict[str, DecisionRecord] = field(default_factory=dict)

    def add_evidence(self, record: EvidenceRecord) -> None:
        if record.evidence_id in self.evidence:
            raise ValueError(f"duplicate evidence id: {record.evidence_id}")
        self.evidence[record.evidence_id] = record

    def add_claim(self, record: ClaimRecord) -> None:
        if record.claim_id in self.claims:
            raise ValueError(f"duplicate claim id: {record.claim_id}")
        self.claims[record.claim_id] = record

    def update_claim_status(self, claim_id: str, status: str) -> None:
        current = self.claims[claim_id]
        self.claims[claim_id] = ClaimRecord(
            claim_id=current.claim_id,
            parent_claim_or_null=current.parent_claim_or_null,
            proposal_snapshot_hash=current.proposal_snapshot_hash,
            predicate=current.predicate,
            scope=current.scope,
            current_status=status,
        )

    def add_decision(self, record: DecisionRecord) -> None:
        if record.decision_id in self.decisions:
            raise ValueError(f"duplicate decision id: {record.decision_id}")
        self.decisions[record.decision_id] = record


@dataclass
class Hypothesis:
    claim_id: str
    parent_context: tuple[Any, ...]
    predicate_id: str
    predicate_value: Any
    scope: tuple[Any, ...]
    proposal_gain_nll: float = 0.0
    proposal_snapshot_hash: str = ""
    proposal_snapshot_counts: tuple[Any, ...] = ()
    forward_support: int = 0
    forward_gain_nll: float = 0.0
    forward_event_gains: list[float] = field(default_factory=list)
    sibling_support: int = 0
    evidence_ids: list[str] = field(default_factory=list)
    sibling_evidence_ids: list[str] = field(default_factory=list)
    status: str = "PROVISIONAL"

    @property
    def max_single_gain_fraction(self) -> float:
        if self.forward_gain_nll <= 0:
            return 1.0
        positive = [g for g in self.forward_event_gains if g > 0]
        if not positive:
            return 1.0
        return max(positive) / self.forward_gain_nll


@dataclass(frozen=True)
class CanonicalEntry:
    claim_id: str
    scope_predicate: tuple[Any, ...]
    local_predictive_delta: float
    evidence_ids: tuple[str, ...]
    authorization_id: str
    created_level: int
    created_step: int
    last_verified_level: int
    status: CanonicalStatus = CanonicalStatus.AUTHORIZED


@dataclass
class CanonicalMemory:
    entries: dict[str, CanonicalEntry] = field(default_factory=dict)

    def add(self, entry: CanonicalEntry) -> None:
        if len(self.entries) >= MAX_CANONICAL and entry.claim_id not in self.entries:
            raise OverflowError("canonical memory capacity exhausted")
        self.entries[entry.claim_id] = entry

    def clear(self) -> None:
        self.entries.clear()
