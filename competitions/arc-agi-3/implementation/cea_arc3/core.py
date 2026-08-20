from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from .arms import ArmConfig
from .authority import AuthorityGate
from .corrections import apply_delta, clipped_delta, select_canonical, select_provisional
from .hypotheses import HypothesisManager
from .metrics import MetricsLedger, PredictionEvent
from .policies import AIECPolicy, FixedAllocationPolicy, candidate_actions
from .state import (
    CanonicalEntry,
    CanonicalMemory,
    ClaimRecord,
    DecisionRecord,
    EvidenceRecord,
    LineageState,
    RawHistory,
    TransitionRecord,
)
from .transition import STATE_DELTA_CLASSES, TransitionModel, action_mask, state_delta_class


@dataclass(frozen=True)
class Prediction:
    probability_change: float
    parent_probability: float
    secondary_probabilities: dict[str, Any]
    claim_id: Optional[str]
    correction_source: Optional[str]
    context: tuple[Any, ...]
    predicate_values: dict[str, Any]


AuditEvent = tuple[str, Any]


class MechanismCore:
    """Stateful implementation of the operative v1+v1.1+v1.2+v1.3+v1.4 substrate.

    Audit events returned by `observe` are read-only execution outputs. They are
    not retained as control state and never feed back into action selection.
    """

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

    def choose_action(self, current_frame_hash: str, available_actions: Iterable[int]) -> tuple[int, Optional[tuple[int, int]], str]:
        available = tuple(sorted(int(a) for a in available_actions if int(a) != 0))
        if not available:
            return 0, None, "RESET"
        if self.policy is not None:
            return self.policy.choose(history=self.history, current_frame_hash=current_frame_hash, available_actions=available)
        candidates = candidate_actions(available)
        choice = candidates[self.step % len(candidates)]
        return choice[0], choice[1], "P_EXEC"

    def predict_action(
        self,
        *,
        action_token: int,
        action_coordinate: Optional[tuple[int, int]],
        current_frame_hash: str,
        available_actions: Iterable[int],
    ) -> Prediction:
        mask = action_mask(available_actions)
        context = self.model.base_context(action_token, action_coordinate, self.history, mask)
        pred_values = self.model.predicate_values(self.history, current_frame_hash, mask)
        parent_p, _ = self.model.predict(context)
        secondary = self.model.predict_secondary(context)
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

        # Scope-gated corrections must never perturb an unmatched prediction.
        if claim_id is None and abs(emitted - parent_p) > 1e-15:
            self.metrics.localization_violations += 1

        return Prediction(emitted, parent_p, secondary, claim_id, source, context, pred_values)

    def observe(
        self,
        *,
        prediction: Prediction,
        record: TransitionRecord,
        current_frame_hash_before: str,
    ) -> list[AuditEvent]:
        """Score prequential predictions, then update evidence/model/corrections.

        Returned audit records are durable-output material for the runner; they
        are not retained by the core and cannot influence future behavior.
        """
        audit: list[AuditEvent] = []
        z = record.z_change
        state_delta = state_delta_class(record.state_before, record.state_after)
        level_positive = int(record.level_after > record.level_before)
        surface_changed = int(record.available_action_mask_after != record.available_action_mask_before)

        parent_nll = self.model.binary_nll(prediction.parent_probability, z)
        emitted_nll = self.model.binary_nll(prediction.probability_change, z)
        bucket_nll = self.model.categorical_nll(
            prediction.secondary_probabilities["changed_count_bucket"], record.changed_count_bucket
        )
        state_nll = self.model.categorical_nll(
            prediction.secondary_probabilities["state_delta_class"], STATE_DELTA_CLASSES.index(state_delta)
        )
        level_nll = self.model.binary_nll(prediction.secondary_probabilities["level_delta_positive"], level_positive)
        surface_nll = self.model.binary_nll(prediction.secondary_probabilities["action_surface_changed"], surface_changed)
        return_nll = self.model.binary_nll(prediction.secondary_probabilities["exact_return_flag"], record.exact_return_flag)

        pe = PredictionEvent(
            self.game_slug,
            self.level,
            self.step,
            self.arm.name,
            parent_nll,
            emitted_nll,
            z,
            bucket_nll,
            state_nll,
            level_nll,
            surface_nll,
            return_nll,
            prediction.claim_id,
            prediction.correction_source,
            prediction.claim_id is not None,
        )
        self.metrics.predictions.append(pe)
        if prediction.correction_source == "CANONICAL":
            self.metrics.canonical_applications += 1
        elif prediction.correction_source == "PROVISIONAL":
            self.metrics.provisional_applications += 1
        audit.append(("prediction_score", pe))

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
            result_signature=(
                record.z_change,
                record.changed_count_bucket,
                state_delta,
                level_positive,
                surface_changed,
                record.exact_return_flag,
            ),
        )
        self.lineage.add_evidence(ev)
        audit.append(("evidence", ev))

        # Strictly forward evaluation of candidates that existed before this event.
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
                    if h.forward_support == 4:
                        self.metrics.forward_supported_claims.add(h.claim_id)
                        audit.append(("forward_supported", {
                            "claim_id": h.claim_id,
                            "level": self.level,
                            "step": self.step,
                            "forward_support": h.forward_support,
                            "forward_gain_nll": h.forward_gain_nll,
                        }))
                else:
                    h.sibling_support += 1
                    h.sibling_evidence_ids.append(evidence_id)
                audit.append(("hypothesis_progress", {
                    "claim_id": h.claim_id,
                    "level": self.level,
                    "step": self.step,
                    "forward_support": h.forward_support,
                    "forward_gain_nll": h.forward_gain_nll,
                    "sibling_support": h.sibling_support,
                }))

        # Update ordinary model only after every prequential score above is frozen.
        self.model.update(
            context=prediction.context,
            predicate_values=prediction.predicate_values,
            z_change=z,
            bucket=record.changed_count_bucket,
            state_delta=state_delta,
            level_delta_positive=level_positive,
            action_surface_changed=surface_changed,
            exact_return_flag=record.exact_return_flag,
        )

        if self.arm.L:
            trigger_key = (self.game_slug, self.level, prediction.context)
            if self.hypotheses.trigger_met(self.model.base[prediction.context]) and trigger_key not in self.metrics.aliasing_trigger_keys:
                self.metrics.aliasing_trigger_keys.add(trigger_key)
                audit.append(("aliasing_trigger", {
                    "game_slug": self.game_slug,
                    "level": self.level,
                    "context": prediction.context,
                    "step": self.step,
                }))

            before_live = set(self.hypotheses.live)
            self.hypotheses.propose_from_q(self.model, prediction.context)
            after_live = set(self.hypotheses.live)
            new_ids = sorted(after_live - before_live)
            evicted_ids = sorted(before_live - after_live)
            for claim_id in new_ids:
                h = self.hypotheses.live[claim_id]
                self.lineage.add_claim(ClaimRecord(
                    claim_id=h.claim_id,
                    parent_claim_or_null=None,
                    proposal_snapshot_hash=h.proposal_snapshot_hash,
                    predicate=(h.predicate_id, h.predicate_value),
                    scope=h.scope,
                    current_status=h.status,
                ))
                self.metrics.admitted_claims.add(h.claim_id)
                audit.append(("claim_created", h))
            for claim_id in evicted_ids:
                if claim_id in self.lineage.claims:
                    self.lineage.update_claim_status(claim_id, "EVICTED")
                audit.append(("hypothesis_evicted", {"claim_id": claim_id, "level": self.level, "step": self.step, "status": "EVICTED"}))

            audit.extend(self._maybe_promote_all())

        self.history.append(record)
        self.step += 1

        if record.level_after > record.level_before:
            canonical_before = tuple(sorted(self.memory.entries))
            live_before = tuple(sorted(self.hypotheses.live))
            theta_present_before = bool(self.model.base)
            self.on_level_transition(record.level_after)
            audit.append(("level_transition", {
                "from_level": int(record.level_before),
                "to_level": int(record.level_after),
                "canonical_before": canonical_before,
                "canonical_after": tuple(sorted(self.memory.entries)),
                "provisional_cleared": live_before,
                "theta_present_before": theta_present_before,
                "theta_present_after": bool(self.model.base),
                "persist_theta": bool(self.arm.persist_theta),
                "persist_canonical": bool(self.arm.C),
            }))

        return audit

    def _decision_record(self, h, decision, delta: float, label: str, reason: str) -> DecisionRecord:
        return DecisionRecord(
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
            decision=label,
            reason_code=reason,
        )

    def _maybe_promote_all(self) -> list[AuditEvent]:
        audit: list[AuditEvent] = []
        for h in list(self.hypotheses.live.values()):
            if h.status != "PROVISIONAL":
                continue
            if self.arm.X:
                parent_p = self.model.base[h.parent_context].binary.p_one
                local_p = self.model.predict_local(h.parent_context, h.predicate_id, h.predicate_value)
                delta = clipped_delta(parent_p, local_p)
                decision = self.authority.evaluate(
                    h,
                    self.lineage,
                    self.memory,
                    created_level=self.level,
                    created_step=self.step,
                    local_predictive_delta=delta,
                )
                if decision.eligible:
                    self.metrics.eligible_promotion_events += 1
                if decision.eligible and not decision.authorize:
                    if decision.reason_code == "CAPACITY_REFUSAL":
                        self.metrics.capacity_refusals += 1
                    else:
                        self.metrics.false_refusals += 1

                dr = self._decision_record(
                    h,
                    decision,
                    delta,
                    "AUTHORIZED" if decision.authorize else "REFUSED",
                    decision.reason_code,
                )
                self.lineage.add_decision(dr)
                audit.append(("authorization_decision", dr))

                if decision.authorize:
                    entry = CanonicalEntry(
                        claim_id=h.claim_id,
                        scope_predicate=h.scope,
                        local_predictive_delta=delta,
                        evidence_ids=tuple(h.evidence_ids),
                        authorization_id=decision.decision_id,
                        created_level=self.level,
                        created_step=self.step,
                        last_verified_level=self.level,
                    )
                    self.memory.add(entry)
                    h.status = "AUTHORIZED"
                    self.lineage.update_claim_status(h.claim_id, "AUTHORIZED")
                    self.metrics.total_promotions += 1
                    # Independent post-insertion integrity check for U_unauthorized.
                    stored = self.memory.entries.get(h.claim_id)
                    if (
                        stored is None
                        or not decision.eligible
                        or not decision.authorize
                        or stored.scope_predicate != h.scope
                        or stored.authorization_id != decision.decision_id
                        or stored.evidence_ids != tuple(h.evidence_ids)
                    ):
                        self.metrics.unauthorized_promotions += 1
                    audit.append(("canonical_entry", entry))
                    audit.append(("claim_status", {"claim_id": h.claim_id, "status": "AUTHORIZED"}))

            elif self.arm.C and h.forward_support >= 4:
                parent_p = self.model.base[h.parent_context].binary.p_one
                local_p = self.model.predict_local(h.parent_context, h.predicate_id, h.predicate_value)
                delta = clipped_delta(parent_p, local_p)
                decision_id = f"UNGATED:{next(self._decision_counter):08d}"
                if len(self.memory.entries) >= 64 and h.claim_id not in self.memory.entries:
                    dr = DecisionRecord(
                        decision_id=decision_id,
                        claim_id=h.claim_id,
                        evidence_ids_considered=tuple(h.evidence_ids + h.sibling_evidence_ids),
                        proposal_snapshot_hash=h.proposal_snapshot_hash,
                        metric_values={"forward_gain_nll": float(h.forward_gain_nll)},
                        decision="UNGATED_REFUSAL",
                        reason_code="CAPACITY_REFUSAL",
                    )
                    self.lineage.add_decision(dr)
                    audit.append(("ungated_decision", dr))
                    continue

                dr = DecisionRecord(
                    decision_id=decision_id,
                    claim_id=h.claim_id,
                    evidence_ids_considered=tuple(h.evidence_ids + h.sibling_evidence_ids),
                    proposal_snapshot_hash=h.proposal_snapshot_hash,
                    metric_values={"forward_gain_nll": float(h.forward_gain_nll)},
                    decision="UNGATED_PROMOTION",
                    reason_code="FOUR_FORWARD_OBSERVATIONS",
                )
                self.lineage.add_decision(dr)
                entry = CanonicalEntry(
                    claim_id=h.claim_id,
                    scope_predicate=h.scope,
                    local_predictive_delta=delta,
                    evidence_ids=tuple(h.evidence_ids),
                    authorization_id=decision_id,
                    created_level=self.level,
                    created_step=self.step,
                    last_verified_level=self.level,
                )
                self.memory.add(entry)
                h.status = "AUTHORIZED"
                self.lineage.update_claim_status(h.claim_id, "AUTHORIZED")
                self.metrics.total_promotions += 1
                self.metrics.ungated_promotions += 1
                audit.append(("ungated_decision", dr))
                audit.append(("canonical_entry", entry))
                audit.append(("claim_status", {"claim_id": h.claim_id, "status": "AUTHORIZED"}))
        return audit

    def on_level_transition(self, new_level: int) -> None:
        self.history.clear()
        if not self.arm.persist_theta:
            self.model.reset()
        for h in self.hypotheses.live.values():
            if h.status == "PROVISIONAL" and h.claim_id in self.lineage.claims:
                self.lineage.update_claim_status(h.claim_id, "EXPIRED")
        self.hypotheses.clear()
        if not self.arm.C:
            self.memory.clear()
        self.level = int(new_level)

    def reset_game(self, game_slug: str) -> None:
        self.game_slug = game_slug
        self.history.clear()
        self.model.reset()
        self.hypotheses.clear()
        self.memory.clear()
        self.lineage = LineageState()
        self.metrics = MetricsLedger()
        self.level = 0
        self.step = 0
