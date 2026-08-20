from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from .arms import ArmConfig
from .authority import AuthorityGate
from .corrections import apply_delta, clipped_delta, select_canonical, select_provisional
from .hypotheses import HypothesisManager
from .metrics import MetricsLedger, PredictionEvent
from .policies import AIECPolicy, FixedAllocationPolicy, candidate_actions
from .state import (
    CanonicalMemory,
    ClaimRecord,
    DecisionRecord,
    EvidenceRecord,
    GoalState,
    LineageState,
    RawHistory,
    TransitionRecord,
)
from .transition import TransitionModel, action_mask


@dataclass(frozen=True)
class Prediction:
    probability_change: float
    parent_probability: float
    claim_id: Optional[str]
    correction_source: Optional[str]
    context: tuple[Any, ...]
    predicate_values: dict[str, Any]


class MechanismCore:
    """Stateful implementation of the frozen v1+v1.1+v1.2+v1.3 mechanism substrate."""

    def __init__(self, arm: ArmConfig, game_slug: str) -> None:
        self.arm = arm
        self.game_slug = game_slug
        self.history = RawHistory()
        self.model = TransitionModel()
        self.hypotheses = HypothesisManager()
        self.memory = CanonicalMemory()
        self.lineage = LineageState()
        self.authority = AuthorityGate()
        self.metrics = MetricsLedger()
        self.level = 0
        self.step = 0
        self._evidence_counter = itertools.count(1)
        self._decision_counter = itertools.count(1)
        if arm.fixed_info_percent is not None:
            self.policy = FixedAllocationPolicy(arm.fixed_info_percent, self.model)
        elif arm.A:
            self.policy = AIECPolicy(self.model)
        else:
            self.policy = None

    def choose_action(self, current_frame_hash: str, available_actions: Iterable[int]) -> tuple[int, Optional[tuple[int,int]], str]:
        available = tuple(sorted(int(a) for a in available_actions if int(a) != 0))
        if not available:
            return 0, None, "RESET"
        if self.policy is not None:
            return self.policy.choose(history=self.history, current_frame_hash=current_frame_hash, available_actions=available)
        # P_exec: deterministic legal-action cycling; keep simple per-core step index.
        candidates = candidate_actions(available)
        choice = candidates[self.step % len(candidates)]
        return choice[0], choice[1], "P_EXEC"

    def predict_action(
        self,
        *,
        action_token: int,
        action_coordinate: Optional[tuple[int,int]],
        current_frame_hash: str,
        available_actions: Iterable[int],
    ) -> Prediction:
        mask = action_mask(available_actions)
        context = self.model.base_context(action_token, action_coordinate, self.history, mask)
        pred_values = self.model.predicate_values(self.history, current_frame_hash, mask)
        parent_p, _ = self.model.predict(context)
        emitted = parent_p
        claim_id = None
        source = None

        if self.arm.L:
            canonical = select_canonical(self.memory.entries.values(), self.lineage, context, pred_values)
            if canonical is not None:
                emitted = apply_delta(parent_p, canonical.local_predictive_delta)
                claim_id = canonical.claim_id
                source = "CANONICAL"
            else:
                provisional = select_provisional(self.hypotheses.live.values(), context, pred_values)
                if provisional is not None:
                    local_p = self.model.predict_local(context, provisional.predicate_id, provisional.predicate_value)
                    emitted = apply_delta(parent_p, clipped_delta(parent_p, local_p))
                    claim_id = provisional.claim_id
                    source = "PROVISIONAL"

        return Prediction(emitted, parent_p, claim_id, source, context, pred_values)

    def observe(
        self,
        *,
        prediction: Prediction,
        record: TransitionRecord,
        current_frame_hash_before: str,
    ) -> None:
        """Score prequential prediction, update forward evidence, then update model and propose."""
        z = record.z_change
        parent_nll = self.model.binary_nll(prediction.parent_probability, z)
        emitted_nll = self.model.binary_nll(prediction.probability_change, z)
        self.metrics.predictions.append(PredictionEvent(
            self.game_slug, self.level, self.step, self.arm.name,
            parent_nll, emitted_nll, z, prediction.claim_id, prediction.claim_id is not None,
        ))

        evidence_id = f"{self.game_slug}:E{next(self._evidence_counter):08d}"
        ev = EvidenceRecord(
            evidence_id=evidence_id,
            game_slug=self.game_slug,
            level_index=self.level,
            interaction_step=self.step,
            current_frame_hash=current_frame_hash_before,
            raw_window_hash=self.history.hash(),
            action_token=record.action_token,
            action_coordinate=record.action_coordinate,
            result_signature=(record.z_change, record.changed_count_bucket, record.state_after, record.level_after-record.level_before, int(record.available_action_mask_after != record.available_action_mask_before), record.exact_return_flag),
        )
        self.lineage.add_evidence(ev)

        # Strictly forward evaluation of candidates that already existed before this event.
        if self.arm.L:
            for h in list(self.hypotheses.live.values()):
                if h.parent_context != prediction.context:
                    continue
                value = prediction.predicate_values.get(h.predicate_id)
                if value == h.predicate_value:
                    local_p = self.model.predict_local(prediction.context, h.predicate_id, h.predicate_value)
                    gain = self.model.binary_nll(prediction.parent_probability, z) - self.model.binary_nll(local_p, z)
                    h.forward_support += 1
                    h.forward_gain_nll += gain
                    h.forward_event_gains.append(gain)
                    h.evidence_ids.append(evidence_id)
                else:
                    h.sibling_support += 1
                    h.sibling_evidence_ids.append(evidence_id)

        # Update ordinary model after scoring.
        self.model.update(
            context=prediction.context,
            predicate_values=prediction.predicate_values,
            z_change=z,
            bucket=record.changed_count_bucket,
        )

        # Proposal uses accumulated aggregate evidence, never this event as forward authorization evidence.
        if self.arm.L:
            new_h = self.hypotheses.propose_from_q(self.model, prediction.context)
            for h in new_h:
                self.lineage.add_claim(ClaimRecord(
                    claim_id=h.claim_id,
                    parent_claim_or_null=None,
                    proposal_snapshot_hash=h.proposal_snapshot_hash,
                    predicate=(h.predicate_id, h.predicate_value),
                    scope=h.scope,
                    current_status=h.status,
                ))
            self._maybe_promote_all()

        self.history.append(record)
        self.step += 1

        if record.level_after > record.level_before:
            self.on_level_transition(record.level_after)

    def _maybe_promote_all(self) -> None:
        for h in list(self.hypotheses.live.values()):
            if h.status != "PROVISIONAL":
                continue
            if self.arm.X:
                parent_p = self.model.base[h.parent_context].binary.p_one
                local_p = self.model.predict_local(h.parent_context, h.predicate_id, h.predicate_value)
                delta = clipped_delta(parent_p, local_p)
                decision = self.authority.evaluate(
                    h, self.lineage, self.memory,
                    created_level=self.level, created_step=self.step,
                    local_predictive_delta=delta,
                )
                if decision.eligible:
                    self.metrics.eligible_promotion_events += 1
                if decision.authorize:
                    # Record frozen authorization metrics before canonical insertion.
                    dr = DecisionRecord(
                        decision_id=decision.decision_id,
                        claim_id=h.claim_id,
                        evidence_ids_considered=tuple(h.evidence_ids + h.sibling_evidence_ids),
                        proposal_snapshot_hash=h.proposal_snapshot_hash,
                        metric_values={
                            "forward_gain_nll": float(h.forward_gain_nll),
                            "forward_support": float(h.forward_support),
                            "sibling_support": float(h.sibling_support),
                            "max_single_gain_fraction": float(h.max_single_gain_fraction),
                            "local_predictive_delta": float(delta),
                        },
                        decision="AUTHORIZED",
                        reason_code="AUTHORIZED",
                    )
                    self.lineage.add_decision(dr)
                    # Use promote now; it will generate a new decision id, so insert canonical directly with our recorded id.
                    from .state import CanonicalEntry
                    self.memory.add(CanonicalEntry(
                        claim_id=h.claim_id,
                        scope_predicate=h.scope,
                        local_predictive_delta=delta,
                        evidence_ids=tuple(h.evidence_ids),
                        authorization_id=decision.decision_id,
                        created_level=self.level,
                        created_step=self.step,
                        last_verified_level=self.level,
                    ))
                    h.status = "AUTHORIZED"
                    self.lineage.update_claim_status(h.claim_id, "AUTHORIZED")
                    self.metrics.total_promotions += 1
                elif decision.reason_code == "CAPACITY_REFUSAL":
                    self.metrics.capacity_refusals += 1
            elif self.arm.C and h.forward_support >= 4:
                # Frozen permissive no-X governance control.
                parent_p = self.model.base[h.parent_context].binary.p_one
                local_p = self.model.predict_local(h.parent_context, h.predicate_id, h.predicate_value)
                delta = clipped_delta(parent_p, local_p)
                from .state import CanonicalEntry
                if len(self.memory.entries) < 64:
                    decision_id = f"UNGATED:{next(self._decision_counter):08d}"
                    self.lineage.add_decision(DecisionRecord(
                        decision_id=decision_id,
                        claim_id=h.claim_id,
                        evidence_ids_considered=tuple(h.evidence_ids + h.sibling_evidence_ids),
                        proposal_snapshot_hash=h.proposal_snapshot_hash,
                        metric_values={"forward_gain_nll": float(h.forward_gain_nll)},
                        decision="UNGATED_PROMOTION",
                        reason_code="FOUR_FORWARD_OBSERVATIONS",
                    ))
                    self.memory.add(CanonicalEntry(
                        claim_id=h.claim_id, scope_predicate=h.scope,
                        local_predictive_delta=delta,
                        evidence_ids=tuple(h.evidence_ids), authorization_id=decision_id,
                        created_level=self.level, created_step=self.step,
                        last_verified_level=self.level,
                    ))
                    h.status = "AUTHORIZED"
                    self.lineage.update_claim_status(h.claim_id, "AUTHORIZED")
                    self.metrics.total_promotions += 1

    def on_level_transition(self, new_level: int) -> None:
        self.history.clear()
        if not self.arm.persist_theta:
            self.model.reset()
        self.hypotheses.clear()
        if not self.arm.C:
            self.memory.clear()
        self.level = int(new_level)

    def reset_game(self, game_slug: str) -> None:
        self.game_slug = game_slug
        self.history.clear(); self.model.reset(); self.hypotheses.clear(); self.memory.clear()
        self.lineage = LineageState(); self.metrics = MetricsLedger(); self.level = 0; self.step = 0
