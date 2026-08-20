# ARC-AGI-3 Experiment 2 — Authority State After Repository Freeze

Successor checkpoint to `AUTHORITY_STATE.md`.

The earlier file is intentionally preserved unchanged as the pre-repository-freeze fossilization. This file records the authority state after artifact-identity and clean invariant verification completed.

## Current state

- `Specification = FROZEN v1.3`
- `Specification failures = 3 PRESERVED (SF-001, SF-002, SF-003)`
- `Local implementation = BUILT`
- `Local invariant verification = 56/56 PASS`
- `Frozen implementation commit = 219d80aaf9a72a305fba1db6494402b6ae9f2caa`
- `Repository byte identity = 29/29 EXACT MATCH`
- `Clean byte-equivalent invariant verification = 56/56 PASS`
- `Repository implementation verification = EARNED`
- `ARC execution = NOT STARTED`
- `Empirical ARC result = NOT PRODUCED`
- `CEA component witness = NOT EARNED`
- `CEA composition witness = NOT EARNED`
- `sealed exposure = 0`
- `environment source inspection = 0`

## Verification provenance

Repository verification evidence is frozen in:

`evidence/IMPLEMENTATION_VERIFICATION_V1.md`

The evidence records:

- implementation commit `219d80a...`;
- 29/29 Git-blob equality between locally tested bytes and reachable committed bytes;
- explicit failure of literal network checkout because the execution container could not resolve `github.com`;
- clean byte-equivalent materialization of the verified files;
- fresh invariant result `56 passed in 0.17s`;
- zero ARC environment execution during verification.

## Authority consequence

The mechanical implementation gate is now closed successfully:

`local tested bytes == reachable committed bytes`

and:

`clean verified materialization -> 56/56 PASS`.

This licenses development-only execution of the frozen implementation. It licenses no CEA component or composition claim.

## Next authorized operation

Run the preregistered matched arm matrix on the 18 DEVELOPMENT games only, under the frozen 256-action per-game budget and evaluation procedure.

The seven SEALED_HOLDOUT games remain inaccessible until the first candidate is frozen.
