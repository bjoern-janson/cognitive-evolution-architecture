# ARC-AGI-3 Experiment 2 — Execution-Ready Authority State v1.5

Successor checkpoint to the earlier repository-freeze authority records.

## Current state

- `V2 = FROZEN`
- `Operationalization = FROZEN`
- `Operative specification = FROZEN THROUGH v1.5`
- `Specification failures = SF-001..SF-010 PRESERVED`
- `Frozen execution implementation commit = dc60b57c3d066d3e1f09e34af422061952da60fb`
- `Execution verification surface = 32 Python files`
- `Reachable byte identity = 32/32 EXACT`
- `Fresh-materialization conformance = 67/67 PASS`
- `Synthetic non-tuning control = 16/16 arms identical on the tested 100-step synthetic surface`
- `REPOSITORY_IMPLEMENTATION_VERIFIED_v1.5 = EARNED`
- `EXECUTION_READY_v1.5 = EARNED`
- `ARC development execution = NOT STARTED`
- `ARC behavioral result = NOT PRODUCED`
- `CEA component witness = NOT EARNED`
- `CEA composition witness = NOT EARNED`
- `sealed exposure = 0`
- `environment source inspection = 0`

## Conjunctive execution gate

Execution readiness requires all three terms:

`Spec Frozen AND Reachable Byte Identity AND Fresh-Materialization Conformance`.

For v1.5 all three are now earned.

The earlier v1.3 56/56 verification remains valid for its original artifact/invariant scope. The pre-execution conformance audit demonstrated that artifact/invariant verification alone was insufficient for execution authorization. v1.4/v1.5 repaired that gap before any ARC implementation execution.

## Verification provenance

See:

`evidence/IMPLEMENTATION_VERIFICATION_V1_5.md`.

Frozen execution implementation:

`dc60b57c3d066d3e1f09e34af422061952da60fb`.

The branch may contain later evidence/checkpoint documentation commits; those do not alter the frozen execution artifact.

## Next authorized operation

Run the preregistered matched development matrix:

`18 DEVELOPMENT games x 16 frozen arms x maximum 256 non-RESET actions per arm/game pair`.

Execution remains measurement-only:

- no implementation edits during the matrix;
- no threshold/history/budget/predicate changes;
- no development source inspection;
- no sealed-game exposure;
- no Kaggle interaction;
- failures are recorded before any repair decision.

The seven SEALED_HOLDOUT games remain inaccessible until a candidate is frozen under the experiment protocol.
