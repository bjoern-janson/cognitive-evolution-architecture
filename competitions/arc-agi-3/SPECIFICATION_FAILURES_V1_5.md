# ARC-AGI-3 Specification Failure Ledger — v1.5 Successor

This successor preserves the earlier failure ledgers unchanged and records the final pre-execution lineage ambiguity discovered after the v1.4 conformance repair but before the first ARC environment instantiation by the implementation.

## SF-010 — hypothesis lineage `current_status` lifecycle under-specified

Status: **CONFIRMED BEFORE FIRST ARC IMPLEMENTATION EXECUTION**.

### Conflict

The frozen lineage schema calls the hypothesis field `current_status`. The frozen candidate lifecycle can remove a provisional hypothesis in two ways without authorization:

1. eviction by the 32-candidate cap/ranking rule;
2. expiration when provisional `H_t` clears at a level boundary.

The prior implementation logged those removal events but left the persistent claim record with `current_status = PROVISIONAL`. Once the claim is no longer live, that is not a truthful current status.

The earlier specification did not define lifecycle labels for these removals, so selecting labels only in code would silently complete the specification.

### Minimal sufficient revision

`IMPLEMENTATION_PREREGISTRATION_V1_5.md` freezes lineage-only statuses:

- `PROVISIONAL` while live;
- `AUTHORIZED` after canonical promotion;
- `EVICTED` after cap eviction;
- `EXPIRED` after level-boundary provisional clearing.

These statuses are provenance only. They do not alter live-set membership, canonical-memory membership, prediction, action choice, promotion criteria, or any threshold.

### Evidence contamination state

At discovery:

- ARC environment instantiation by the implementation: **NO**;
- ARC development arm execution: **NO**;
- comparative outcome observed: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

Therefore this minimal lineage clarification is admissible before behavioral execution.
