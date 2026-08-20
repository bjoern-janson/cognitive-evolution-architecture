# ARC-AGI-3 Implementation Preregistration v1.5

Status: **PRE-EXECUTION LINEAGE-SEMANTICS CLARIFICATION**.

This amendment was created after the v1.4 static conformance repair and before the first ARC environment instantiation by the implementation. No comparative outcome had been observed. It changes lineage bookkeeping only; it does not change agent control, prediction, action selection, history, candidate generation, correction, persistence eligibility, AIEC, X predicates, or budgets.

The operative specification becomes:

`V1 + V1.1 + V1.2 + V1.3 + V1.4 + V1.5`.

## SF-010 — hypothesis lineage `current_status` lifecycle under-specified

V1 defines each hypothesis lineage record with a `current_status` field. It also freezes two lifecycle operations that remove provisional hypotheses from the live set:

1. proposal-cap eviction when more than 32 provisional candidates would otherwise exist;
2. clearing provisional `H_t` at an ARC level boundary.

The prior implementation emitted audit events for those removals but left the corresponding persistent lineage claim record with `current_status = PROVISIONAL`. After the removal event that value is no longer a truthful current status.

The frozen documents did not name statuses for these two cases, so choosing labels in code would silently complete the specification.

### Minimal repair

For lineage bookkeeping only, provisional claim lifecycle status is frozen as:

- `PROVISIONAL` — claim remains live in `H_t`;
- `AUTHORIZED` — claim was promoted into canonical corrective memory;
- `EVICTED` — claim was removed from live `H_t` solely by the frozen 32-candidate cap/ranking rule;
- `EXPIRED` — claim was still provisional when the frozen level-boundary clearing rule removed it.

Rules:

1. An admitted claim starts `PROVISIONAL`.
2. A cap-evicted admitted claim's `Lambda_t.current_status` becomes `EVICTED` at the same step as eviction.
3. Every still-provisional admitted claim present immediately before a level-boundary clear becomes `EXPIRED` before `H_t` is cleared.
4. An authorized claim remains `AUTHORIZED` in lineage when provisional `H_t` clears.
5. These statuses are audit/provenance fields only and may not be consulted by v1.x action selection or prediction beyond the already-frozen live/canonical membership structures.
6. No new revocation or suspension mechanism is introduced by this clarification.

## Authority state

At this amendment's freeze:

- ARC development execution under the implementation: **NO**;
- comparative outcome observed: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

All non-lineage v1.x definitions remain unchanged.
