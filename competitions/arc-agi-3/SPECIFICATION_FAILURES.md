# ARC-AGI-3 Specification Failure Ledger

This ledger records implementation-specification failures discovered before or during implementation. A specification failure is not an empirical result and does not authorize silent redesign.

## SF-001 — candidate-generation evidence storage under-specified

Status: **CONFIRMED BEFORE FIRST IMPLEMENTATION RESULT**.

Affected specification: `IMPLEMENTATION_PREREGISTRATION_V1.md` at commit `a2745c1`.

### Conflict

The frozen v1 candidate-generation rule requires evaluating each allowed `extra_predicate` against accumulated evidence after an aliasing/residual trigger.

However, v1 simultaneously freezes:

- `H_raw = 2 completed transitions + current observation`;
- no older raw transcript retention;
- ordinary predictive state `Theta_t` containing only Beta-Bernoulli and Dirichlet counts indexed by the base context.

Base-context aggregate counts are insufficient to reconstruct how historical outcomes partition under each allowed candidate predicate after the raw events have left `H_raw`.

Therefore implementing candidate generation exactly as written would require at least one unregistered state object:

1. an illegal older raw-event buffer; or
2. predicate-conditioned aggregate statistics not named in v1.

Either choice would silently change the specification.

### Classification

`SPECIFICATION_FAILURE` at the representation/state interface.

This is not an empirical CEA failure, not a benchmark result, and not evidence for or against L/C/A/X.

### Minimal sufficient revision

Create implementation preregistration v1.1 that preserves every v1 rule except that `Theta_t` is explicitly extended with **aggregate, non-reconstructive predicate contingency counts**:

`Q_t[(base_context, predicate_id, predicate_value)] -> (n_change_0, n_change_1, changed_count_bucket_counts)`.

`Q_t` stores counts only. It may not store frame payloads, event objects, coordinates beyond the already quantized predicate value, timestamps, semantic labels, or a reconstructable ordered transcript.

Candidate generation may query `Q_t`; authorization remains strictly forward and continues to use candidate-local forward counts and provenance ids.

`H_raw` remains exactly 2 completed transitions plus current observation.

No other v1 definition changes under SF-001.

### Evidence contamination state

At discovery:

- implementation comparative results observed: **NO**;
- development arm execution under v1: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

Therefore the minimal v1.1 revision is admissible before implementation execution.

---

## SF-002 — overlapping localized-correction arbitration unspecified

Status: **CONFIRMED DURING UNIT IMPLEMENTATION, BEFORE ENVIRONMENT EXECUTION OR COMPARATIVE RESULT**.

Affected specifications: v1 plus v1.1.

### Conflict

The frozen predicate language allows more than one provisional or canonical localized correction to match the same action-prediction context. The specification defines the local correction value for each claim, but does not define whether simultaneous matching corrections are summed, averaged, composed sequentially, selected by evidence, selected by recency, or otherwise arbitrated.

Those choices produce different predictions and therefore different L/C behavior. Choosing one in code would silently define a new mechanism.

### Classification

`SPECIFICATION_FAILURE` at the correction/composition interface.

### Minimal sufficient revision

Create implementation preregistration v1.2 with a **non-compositional correction rule**:

1. At most one localized correction may modify any single primary transition prediction.
2. Among matching provisional corrections, select the claim with greatest cumulative forward primary NLL gain; before any forward event, use proposal-stage gain; ties break by lexicographically smallest `claim_id`.
3. Among matching canonical corrections, select the claim whose authorization decision recorded the greatest forward primary NLL gain at promotion; ties break by lexicographically smallest `claim_id`.
4. Canonical correction has precedence over provisional correction.
5. No correction deltas are added, averaged, stacked, or recursively composed in implementation v1.x.

### Evidence contamination state

At discovery:

- pure unit/invariant tests executed: **YES**;
- unit tests passed before discovery: **15/15**;
- ARC development environment execution under implementation: **NO**;
- comparative arm result observed: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

Therefore a minimal v1.2 clarification remains admissible before empirical implementation execution.

---

## SF-003 — proposal provenance conflicts with non-reconstructive aggregate storage

Status: **CONFIRMED DURING UNIT IMPLEMENTATION, BEFORE ENVIRONMENT EXECUTION OR COMPARATIVE RESULT**.

Affected specifications: v1 lineage schema plus v1.1 aggregate candidate-generation rule.

### Conflict

v1 requires every hypothesis to record creation evidence identifiers. v1.1 then deliberately restricts proposal-stage historical storage to non-reconstructive aggregate contingency counts `Q_t` and forbids recovering older raw events to perform candidate generation.

Once proposal evidence has left `H_raw`, exact per-event creation identifiers cannot be reconstructed from `Q_t` without adding an event index or other reconstructive state that v1.1 explicitly forbids.

Therefore the two requirements cannot both be implemented exactly.

### Classification

`SPECIFICATION_FAILURE` at the provenance/representation interface.

This is not evidence for or against any CEA component.

### Minimal sufficient revision

Create implementation preregistration v1.3 with a two-tier provenance rule:

1. **Proposal-stage provenance** is represented by an immutable snapshot descriptor of the exact aggregate evidence state that generated the candidate:
   - base context;
   - predicate id/value;
   - parent aggregate counts;
   - local aggregate counts;
   - proposal gain;
   - deterministic SHA-256 of that canonicalized snapshot.
2. The hypothesis stores `proposal_snapshot_hash` and `proposal_snapshot_counts`, not historical creation event IDs.
3. **Forward authorization evidence** remains individually identified exactly as frozen: every forward scored event contributing to support/gain receives an `evidence_id`, and those IDs are stored on the hypothesis and in authorization lineage.
4. X lineage completeness is evaluated over forward authorization evidence IDs plus the proposal snapshot hash.
5. No event index, ordered historical event list, or reconstructive transcript is added to `Q_t`.

### Evidence contamination state

At discovery:

- pure unit/invariant tests executed: **YES**;
- latest unit suite before discovery: **20/20 passed**;
- ARC development environment execution under implementation: **NO**;
- comparative arm result observed: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

Therefore a minimal v1.3 provenance repair remains admissible before empirical implementation execution.
