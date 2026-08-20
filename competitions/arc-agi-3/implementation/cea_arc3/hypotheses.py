from __future__ import annotations

import itertools
from typing import Any

from .state import Hypothesis, MAX_HYPOTHESES
from .transition import AggregateCell, TransitionModel
from .provenance import proposal_snapshot, proposal_snapshot_hash, observed_counts


class HypothesisManager:
    """Proposal manager for the frozen v1.1 non-semantic predicate language."""

    def __init__(self) -> None:
        self.live: dict[str, Hypothesis] = {}
        self._counter = itertools.count(1)

    @staticmethod
    def trigger_met(cell: AggregateCell) -> bool:
        observed_zero = cell.binary.zero - 1
        observed_one = cell.binary.one - 1
        total = observed_zero + observed_one
        return total >= 4 and observed_zero >= 1 and observed_one >= 1

    def propose_from_q(self, model: TransitionModel, context: tuple[Any, ...]) -> list[Hypothesis]:
        parent = model.base[context]
        if not self.trigger_met(parent):
            return []

        candidates: list[Hypothesis] = []
        for pid in TransitionModel.PREDICATE_IDS:
            values = []
            for key, cell in model.q.items():
                c, qpid, qval = key
                if c == context and qpid == pid:
                    observed = (cell.binary.zero - 1) + (cell.binary.one - 1)
                    if observed > 0:
                        values.append((qval, cell))
            if len(values) < 2:
                continue
            for value, local in values:
                gain = self._in_sample_gain(parent, local)
                claim_id = f"H{next(self._counter):06d}"
                snap = proposal_snapshot(
                    base_context=context, predicate_id=pid, predicate_value=value,
                    parent_cell=parent, local_cell=local, proposal_gain_nll=gain,
                )
                candidates.append(
                    Hypothesis(
                        claim_id=claim_id,
                        parent_context=context,
                        predicate_id=pid,
                        predicate_value=value,
                        scope=(context, pid, value),
                        proposal_gain_nll=gain,
                        proposal_snapshot_hash=proposal_snapshot_hash(snap),
                        proposal_snapshot_counts=(
                            observed_counts(parent), observed_counts(local)
                        ),
                    )
                )

        # Proposal management only; not authority. Do not duplicate an already-live scope.
        live_scopes = {h.scope for h in self.live.values()}
        candidates = [h for h in candidates if h.scope not in live_scopes]
        candidates.sort(key=lambda h: (-h.proposal_gain_nll, h.claim_id))
        for h in candidates:
            self.live[h.claim_id] = h
        self._trim()
        return candidates

    @staticmethod
    def _in_sample_gain(parent: AggregateCell, local: AggregateCell) -> float:
        # Compare posterior-mean probabilities on local observed counts only.
        z0 = local.binary.zero - 1
        z1 = local.binary.one - 1
        if z0 + z1 <= 0:
            return 0.0
        parent_p = parent.binary.p_one
        local_p = local.binary.p_one
        loss_parent = z1 * TransitionModel.binary_nll(parent_p, 1) + z0 * TransitionModel.binary_nll(parent_p, 0)
        loss_local = z1 * TransitionModel.binary_nll(local_p, 1) + z0 * TransitionModel.binary_nll(local_p, 0)
        return loss_parent - loss_local

    def _trim(self) -> None:
        if len(self.live) <= MAX_HYPOTHESES:
            return
        ranked = sorted(self.live.values(), key=lambda h: (-h.proposal_gain_nll, h.claim_id))[:MAX_HYPOTHESES]
        self.live = {h.claim_id: h for h in ranked}

    def clear(self) -> None:
        self.live.clear()
