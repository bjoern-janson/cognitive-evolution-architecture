from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable

from .state import CanonicalEntry, CanonicalMemory, Hypothesis, LineageState
from .provenance import proposal_snapshot_from_hypothesis, proposal_snapshot_hash


@dataclass(frozen=True)
class AuthorizationDecision:
    eligible: bool
    authorize: bool
    reason_code: str
    decision_id: str


class AuthorityGate:
    FORWARD_SUPPORT_MIN = 4
    GAIN_MIN_NATS = 2.0
    SIBLING_SUPPORT_MIN = 4
    MAX_SINGLE_GAIN_FRACTION = 0.75

    def __init__(self) -> None:
        self._counter = itertools.count(1)

    def evaluate(
        self,
        hypothesis: Hypothesis,
        lineage: LineageState,
        memory: CanonicalMemory,
        *,
        created_level: int,
        created_step: int,
        local_predictive_delta: float,
    ) -> AuthorizationDecision:
        did = f"AUTH{next(self._counter):06d}"
        try:
            recomputed_snapshot_hash = proposal_snapshot_hash(proposal_snapshot_from_hypothesis(hypothesis))
        except Exception:
            recomputed_snapshot_hash = ""
        claim_record = lineage.claims.get(hypothesis.claim_id)
        all_forward_ids = tuple(hypothesis.evidence_ids) + tuple(hypothesis.sibling_evidence_ids)
        eligibility_checks = [
            (bool(hypothesis.scope), "EMPTY_SCOPE"),
            (hypothesis.forward_support >= self.FORWARD_SUPPORT_MIN, "INSUFFICIENT_FORWARD_SUPPORT"),
            (hypothesis.forward_gain_nll >= self.GAIN_MIN_NATS, "INSUFFICIENT_FORWARD_GAIN"),
            (len(hypothesis.forward_event_gains) == hypothesis.forward_support, "INCOMPLETE_FORWARD_DISCRIMINATION"),
            (hypothesis.max_single_gain_fraction <= self.MAX_SINGLE_GAIN_FRACTION, "SINGLE_EVENT_DOMINANCE"),
            (hypothesis.sibling_support >= self.SIBLING_SUPPORT_MIN, "INSUFFICIENT_SIBLING_SUPPORT"),
            (
                bool(hypothesis.proposal_snapshot_hash)
                and recomputed_snapshot_hash == hypothesis.proposal_snapshot_hash
                and claim_record is not None
                and claim_record.proposal_snapshot_hash == hypothesis.proposal_snapshot_hash
                and all(eid in lineage.evidence for eid in all_forward_ids),
                "INCOMPLETE_LINEAGE",
            ),
            (not self._looks_semantic(hypothesis), "SEMANTIC_PROMOTION_FORBIDDEN"),
        ]
        failed = [reason for ok, reason in eligibility_checks if not ok]
        if failed:
            return AuthorizationDecision(False, False, failed[0], did)
        # v1.4: `eligible` means every non-capacity predicate is satisfied.
        # Capacity exhaustion is a separately measured refusal, not an eligibility failure.
        if not (len(memory.entries) < 64 or hypothesis.claim_id in memory.entries):
            return AuthorizationDecision(True, False, "CAPACITY_REFUSAL", did)
        return AuthorizationDecision(True, True, "AUTHORIZED", did)

    @staticmethod
    def _looks_semantic(h: Hypothesis) -> bool:
        forbidden = ("goal", "mechanic", "useful", "progress", "object")
        text = f"{h.predicate_id} {h.scope}".lower()
        return any(tok in text for tok in forbidden)

    def promote(
        self,
        *,
        hypothesis: Hypothesis,
        lineage: LineageState,
        memory: CanonicalMemory,
        created_level: int,
        created_step: int,
        local_predictive_delta: float,
    ) -> AuthorizationDecision:
        decision = self.evaluate(
            hypothesis,
            lineage,
            memory,
            created_level=created_level,
            created_step=created_step,
            local_predictive_delta=local_predictive_delta,
        )
        if decision.authorize:
            memory.add(
                CanonicalEntry(
                    claim_id=hypothesis.claim_id,
                    scope_predicate=hypothesis.scope,
                    local_predictive_delta=float(local_predictive_delta),
                    evidence_ids=tuple(hypothesis.evidence_ids),
                    authorization_id=decision.decision_id,
                    created_level=int(created_level),
                    created_step=int(created_step),
                    last_verified_level=int(created_level),
                )
            )
            hypothesis.status = "AUTHORIZED"
        return decision
