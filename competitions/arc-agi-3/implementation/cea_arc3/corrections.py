from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from .state import CanonicalEntry, Hypothesis, LineageState


def logit(p: float) -> float:
    p = min(max(float(p), 1e-6), 1 - 1e-6)
    return math.log(p / (1 - p))


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)


def clipped_delta(parent_p: float, local_p: float) -> float:
    return max(-4.0, min(4.0, logit(local_p) - logit(parent_p)))


def apply_delta(parent_p: float, delta: float) -> float:
    return sigmoid(logit(parent_p) + float(delta))


def scope_matches(scope: tuple[Any, ...], context: tuple[Any, ...], predicate_values: dict[str, Any]) -> bool:
    if len(scope) != 3:
        return False
    parent, pid, value = scope
    return parent == context and predicate_values.get(pid) == value


def select_provisional(
    hypotheses: Iterable[Hypothesis],
    context: tuple[Any, ...],
    predicate_values: dict[str, Any],
) -> Optional[Hypothesis]:
    matching = [h for h in hypotheses if h.status == "PROVISIONAL" and scope_matches(h.scope, context, predicate_values)]
    if not matching:
        return None
    def rank(h: Hypothesis):
        score = h.forward_gain_nll if h.forward_support > 0 else h.proposal_gain_nll
        return (-score, h.claim_id)
    return sorted(matching, key=rank)[0]


def select_canonical(
    entries: Iterable[CanonicalEntry],
    lineage: LineageState,
    context: tuple[Any, ...],
    predicate_values: dict[str, Any],
) -> Optional[CanonicalEntry]:
    matching = [e for e in entries if e.status.value == "AUTHORIZED" and scope_matches(e.scope_predicate, context, predicate_values)]
    if not matching:
        return None
    def rank(e: CanonicalEntry):
        decision = lineage.decisions.get(e.authorization_id)
        gain = float(decision.metric_values.get("forward_gain_nll", float("-inf"))) if decision else float("-inf")
        return (-gain, e.claim_id)
    return sorted(matching, key=rank)[0]
