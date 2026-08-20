# ARC-AGI-3 Implementation Preregistration v1.2

Status: **FROZEN BEFORE FIRST ENVIRONMENT EXECUTION OR COMPARATIVE IMPLEMENTATION RESULT**.

This document supersedes implementation preregistration v1.1 only through the explicit correction-arbitration amendment below. All v1 and v1.1 clauses not named here remain unchanged and binding.

Reason for revision: `SF-002` in `SPECIFICATION_FAILURES.md`.

At freeze time, 15 pure unit/invariant tests had run successfully, but no ARC development environment had been executed by the implementation and no comparative arm result had been observed.

---

# Amendment D — localized-correction arbitration is non-compositional

For any emitted primary transition prediction, compute the set of localized corrections whose registered scope matches the current frozen base context and current frozen predicate value.

Exactly **zero or one** localized correction may modify that prediction.

No correction deltas may be summed, averaged, stacked, recursively composed, or otherwise combined in implementation v1.x.

## D.1 Provisional correction selection

Among matching provisional corrections:

1. if a candidate has at least one forward scored event, rank by cumulative `forward_gain_nll`, descending;
2. a candidate with zero forward scored events is ranked by `proposal_gain_nll` instead;
3. ties break by lexicographically smallest `claim_id`.

This selection rule is predictive arbitration only. It does not grant authorization or semantic authority.

## D.2 Canonical correction selection

Every successful X authorization decision must record at least the following frozen metric values in its existing lineage `DecisionRecord.metric_values`:

- `forward_gain_nll`;
- `forward_support`;
- `sibling_support`;
- `max_single_gain_fraction`;
- `local_predictive_delta`.

Among matching canonical corrections, rank by the `forward_gain_nll` stored in the corresponding authorization decision, descending; ties break by lexicographically smallest `claim_id`.

No new canonical-memory field is added.

## D.3 Canonical precedence

If at least one matching canonical correction exists, provisional corrections are ignored for that prediction.

Only if no canonical correction matches may the provisional-selection rule be used.

## D.4 Local predictive delta

For the selected correction only:

`delta = clip(logit(p_local) - logit(p_parent), -4, +4)`.

The emitted corrected primary probability is:

`p_corrected = sigmoid(logit(p_parent) + delta)`.

Since `delta` is defined relative to the selected local predictor, this equals the selected local posterior probability except where clipping is active.

Outside the selected correction's registered scope, emitted probability remains exactly the parent/base probability.

---

# Amendment E — forward-discrimination completeness check

To operationalize the already-frozen X predicate requiring both local and parent predictions for every forward support event, a hypothesis is promotion-eligible only if:

`len(forward_event_gains) == forward_support`.

Every entry in `forward_event_gains` must have been computed prequentially from a parent probability and a local probability emitted before the corresponding result was observed.

This adds no new evidence source or threshold; it makes the existing predicate machine-checkable.

---

# Unchanged constraints

All other v1/v1.1 clauses remain binding, including:

- `H_raw = 2` completed transitions plus current observation;
- aggregate-only `Q_t` historical contingency storage;
- frozen candidate predicate language;
- proposal evidence excluded from forward authorization;
- X thresholds;
- 256-action development budget;
- arm matrix;
- level-boundary persistence semantics;
- no source inspection;
- sealed-holdout firewall;
- typed invalidation and specification-failure handling.

# Authority consequence

v1.2 authorizes only deterministic arbitration among already-authorized correction objects and a machine-checkable forward-discrimination completeness test.

It does not authorize multi-correction composition, semantic interpretation, additional history, new predicates, changed thresholds, or empirical claims before implementation verification and development execution.
