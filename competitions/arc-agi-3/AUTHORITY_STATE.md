# ARC-AGI-3 Experiment 2 — Authority State

Frozen on 2026-08-20 before first ARC execution of the preregistered implementation.

This file records authority, not capability. It does not promote local implementation verification into a CEA component witness or empirical benchmark result.

## Frozen state

- `Specification = FROZEN v1.3`
- `Specification failures = 3 PRESERVED (SF-001, SF-002, SF-003)`
- `Local implementation = BUILT`
- `Local invariant verification = 56/56 PASS`
- `Reachable repository implementation = INCOMPLETE` at this checkpoint
- `ARC execution = NOT STARTED`
- `Empirical result = NOT PRODUCED`
- `CEA component witness = NOT EARNED`
- `CEA composition witness = NOT EARNED`
- `sealed exposure = 0`
- `environment source inspection = 0`

## Interpretation boundary

The 56/56 result belongs only in:

`IMPLEMENTATION_VERIFIED_LOCALLY`

It does not imply:

`COMPONENT_VERIFIED`.

The tests establish internal conformance to the operative implementation specification. They do not establish intelligent behavior, task success, component advantage, composition advantage, or benchmark generalization.

## Operative specification lineage

The implementation contract is the cumulative specification:

`V1 + V1.1 + V1.2 + V1.3`.

The preserved typed failures are:

1. `SF-001 -> V1.1`: candidate-generation evidence storage was under-specified. Repair: aggregate non-reconstructive predicate contingencies `Q_t`; no widening of `H_raw`.
2. `SF-002 -> V1.2`: overlapping localized-correction arbitration was under-specified. Repair: explicit non-compositional deterministic arbitration.
3. `SF-003 -> V1.3`: exact proposal event IDs conflicted with non-reconstructive aggregate storage. Repair: proposal snapshot hashes plus individually identified forward authorization evidence.

No comparative ARC implementation result was observed before any of these repairs.

## Minimal-history boundary

`H_raw = 2 completed transitions + current observation`.

This is not claimed to be sufficient for cognition. It is the smallest raw historical window directly required by the two-step transition dependence measured in Black-Box V2.

Older information may survive only through the typed aggregate, hypothesis, provenance, or authorized canonical state explicitly permitted by the operative specification. An unconstrained transcript dump is not authorized.

## Next gate

The next gate is mechanical only:

`locally tested bytes == reachable committed bytes`

followed by:

`frozen repository snapshot -> clean verification run -> repository implementation freeze`.

No ARC development execution is authorized until that gate passes.
