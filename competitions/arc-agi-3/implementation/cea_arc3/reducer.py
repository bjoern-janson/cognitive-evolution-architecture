from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

from .metrics import paired_persistence_summary
from .transition import TransitionModel


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def _one(events: Iterable[dict[str, Any]], kind: str) -> dict[str, Any]:
    matches = [e["payload"] for e in events if e.get("kind") == kind]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {kind}, found {len(matches)}")
    return matches[0]


def run_summary(path: Path) -> dict[str, Any]:
    return _one(load_events(path), "run_summary")


def _transition_key(payload: dict[str, Any]) -> tuple[Any, ...]:
    score = payload["score"]
    coord = payload.get("action_coordinate")
    return (
        payload["game_slug"],
        int(payload["seed"]),
        int(score["level"]),
        int(payload["step"]),
        int(payload["action_token"]),
        tuple(coord) if coord is not None else None,
    )


def _outcome_signature(payload: dict[str, Any]) -> tuple[Any, ...]:
    r = payload["transition"]
    return (
        int(r["z_change"]),
        int(r["changed_count_bucket"]),
        str(r["state_after"]),
        int(r["level_after"]) - int(r["level_before"]),
        int(int(r["available_action_mask_after"]) != int(r["available_action_mask_before"])),
        int(r["exact_return_flag"]),
    )


def index_logs(log_dir: Path) -> dict[tuple[str, str, int], tuple[Path, list[dict[str, Any]]]]:
    out: dict[tuple[str, str, int], tuple[Path, list[dict[str, Any]]]] = {}
    for path in sorted(Path(log_dir).glob("*.jsonl")):
        events = load_events(path)
        start = _one(events, "run_start")
        key = (str(start["game_slug"]), str(start["arm"]), int(start["seed"]))
        if key in out:
            raise ValueError(f"duplicate run log key: {key}")
        out[key] = (path, events)
    return out


def reduce_run(path: Path) -> dict[str, Any]:
    events = load_events(path)
    summary = _one(events, "run_summary")
    transitions = [e["payload"] for e in events if e.get("kind") == "transition"]
    evidence = [e["payload"] for e in events if e.get("kind") == "evidence"]
    claims = [e["payload"] for e in events if e.get("kind") == "claim_created"]
    decisions = [e["payload"] for e in events if e.get("kind") in {"authorization_decision", "ungated_decision"}]
    triggers = [e["payload"] for e in events if e.get("kind") == "aliasing_trigger"]
    forward = [e["payload"] for e in events if e.get("kind") == "forward_supported"]
    levels = [e["payload"] for e in events if e.get("kind") == "level_transition"]

    if len(evidence) != len(transitions):
        raise ValueError(f"lineage evidence/transition mismatch in {path}: {len(evidence)} != {len(transitions)}")
    lineage = _one(events, "lineage_snapshot")
    if len(lineage["evidence"]) != len(evidence):
        raise ValueError("final lineage snapshot is incomplete")
    if len(lineage["claims"]) != len(claims):
        raise ValueError("final claim snapshot is incomplete")
    if len(lineage["decisions"]) != len(decisions):
        raise ValueError("final decision snapshot is incomplete")

    collateral = sum(
        abs(float(t["prediction"]["p_change"]) - float(t["prediction"]["parent_p_change"])) > 1e-12
        and t["prediction"].get("claim_id") is None
        for t in transitions
    )
    return {
        **summary,
        "logged_transitions": len(transitions),
        "logged_evidence": len(evidence),
        "logged_claims": len(claims),
        "logged_decisions": len(decisions),
        "logged_aliasing_triggers": len({(x["level"], json.dumps(x["context"], sort_keys=True)) for x in triggers}),
        "logged_forward_supported_claims": len({x["claim_id"] for x in forward}),
        "level_transitions": len(levels),
        "collateral_violations_reduced": collateral,
    }


def persistence_metric(
    log_dir: Path,
    *,
    persistent_arm: str = "B+L+C",
    transient_arm: str = "B+L",
) -> dict[str, Any]:
    logs = index_logs(log_dir)
    differences: list[float] = []
    non_evaluable = 0
    considered = 0

    for (game, arm, seed), (_, p_events) in logs.items():
        if arm != persistent_arm:
            continue
        t_key = (game, transient_arm, seed)
        if t_key not in logs:
            continue
        _, t_events = logs[t_key]
        created_level = {
            e["payload"]["claim_id"]: int(e["payload"]["created_level"])
            for e in p_events if e.get("kind") == "canonical_entry"
        }
        transient_by_key = {
            _transition_key(e["payload"]): e["payload"]
            for e in t_events if e.get("kind") == "transition"
        }
        for e in p_events:
            if e.get("kind") != "transition":
                continue
            p = e["payload"]
            pred = p["prediction"]
            claim = pred.get("claim_id")
            if pred.get("correction_source") != "CANONICAL" or not claim:
                continue
            level = int(p["score"]["level"])
            if claim not in created_level or level <= created_level[claim]:
                continue
            considered += 1
            key = _transition_key(p)
            other = transient_by_key.get(key)
            if other is None or _outcome_signature(other) != _outcome_signature(p):
                non_evaluable += 1
                continue
            z = int(p["transition"]["z_change"])
            transient_parent_nll = TransitionModel.binary_nll(float(other["prediction"]["parent_p_change"]), z)
            persistent_emitted_nll = float(p["score"]["emitted_nll"])
            differences.append(persistent_emitted_nll - transient_parent_nll)

    return {
        **paired_persistence_summary(differences),
        "considered_scope_encounters": considered,
        "non_evaluable_pairs": non_evaluable,
        "persistent_arm": persistent_arm,
        "transient_arm": transient_arm,
    }


def future_correction_capacity(log_dir: Path) -> dict[str, Any]:
    logs = index_logs(log_dir)
    by_run_level: dict[tuple[str, str, int, int], dict[str, Any]] = {}

    for (game, arm, seed), (_, events) in logs.items():
        triggers: dict[int, set[str]] = defaultdict(set)
        supported: dict[int, set[str]] = defaultdict(set)
        correction_nll: dict[int, list[float]] = defaultdict(list)
        persisted_into: dict[int, int] = defaultdict(int)

        for e in events:
            kind = e.get("kind")
            p = e.get("payload", {})
            if kind == "aliasing_trigger":
                triggers[int(p["level"])].add(json.dumps(p["context"], sort_keys=True))
            elif kind == "forward_supported":
                supported[int(p["level"])].add(str(p["claim_id"]))
            elif kind == "transition" and p["prediction"].get("claim_id") is not None:
                correction_nll[int(p["score"]["level"])].append(float(p["score"]["emitted_nll"]))
            elif kind == "level_transition" and p.get("canonical_after"):
                persisted_into[int(p["to_level"])] = len(p["canonical_after"])

        levels = set(triggers) | set(supported) | set(correction_nll) | set(persisted_into)
        for level in levels:
            by_run_level[(game, arm, seed, level)] = {
                "triggers": len(triggers[level]),
                "forward_supported": len(supported[level]),
                "localization_yield": len(supported[level]) / max(1, len(triggers[level])),
                "mean_correction_nll": mean(correction_nll[level]) if correction_nll[level] else float("nan"),
                "persisted_canonical_entries": persisted_into[level],
            }

    paired: list[dict[str, Any]] = []
    for (game, arm, seed, level), vals in sorted(by_run_level.items()):
        if arm != "B+L+C" or level <= 0 or vals["persisted_canonical_entries"] <= 0:
            continue
        other = by_run_level.get((game, "B+L", seed, level))
        if other is None:
            continue
        paired.append({
            "game_slug": game,
            "seed": seed,
            "level": level,
            "persistent_yield": vals["localization_yield"],
            "transient_yield": other["localization_yield"],
            "yield_difference": vals["localization_yield"] - other["localization_yield"],
            "persistent_mean_correction_nll": vals["mean_correction_nll"],
            "transient_mean_correction_nll": other["mean_correction_nll"],
        })

    finite_diffs = [r["yield_difference"] for r in paired if math.isfinite(r["yield_difference"])]
    return {
        "n_paired_later_levels": len(paired),
        "mean_yield_difference": mean(finite_diffs) if finite_diffs else float("nan"),
        "pairs": paired,
    }
