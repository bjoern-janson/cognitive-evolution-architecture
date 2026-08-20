# ARC-AGI-3 Experiment 2 — Authority State After Development Matrix v1.5

Successor to `AUTHORITY_STATE_EXECUTION_READY_V1_5.md`.

## Observation state

Frozen development result:

`evidence/DEVELOPMENT_MATRIX_V1_5_RAW_RESULT.md`.

Execution artifact:

`dc60b57c3d066d3e1f09e34af422061952da60fb`.

Completed matrix:

`18 DEVELOPMENT games x 16 frozen arms`, seed 0, maximum 256 non-RESET actions per arm/game pair.

## Current authority

- `Specification = FROZEN THROUGH v1.5`
- `Specification failures = SF-001..SF-010 PRESERVED`
- `Repository implementation verification v1.5 = EARNED`
- `Development execution v1.5 = COMPLETE 288/288`
- `ARC behavioral result = PRODUCED`
- `Direct task progress = 0 level completions, 0 wins`
- `L development transition-prediction signal = POSITIVE`
- `C level-persistence effect = NON-EVALUABLE`
- `AIEC v1 transition-prediction result = NEGATIVE versus fixed 0/25/50/75; positive only versus fixed 100`
- `X observed governance integrity = SATISFIED on development trajectories`
- `CEA component witness = NOT EARNED`
- `CEA composition witness = NOT EARNED`
- `held-out evaluation = NOT AUTHORIZED YET`
- `sealed exposure = 0`
- `Kaggle submission = 0 for this experiment`

## New earned distinction

The first behavioral matrix establishes, for this v1.5 implementation:

`transition-prediction improvement != task-progress improvement`.

Localized corrections can improve forward transition prediction while the complete system still fails to reach any level boundary.

This does not identify why task progress failed. Competing explanations remain open.

## Live failure hypotheses

At minimum:

1. the frozen action policies may be insufficient to acquire task goals;
2. the permitted non-semantic transition representation may omit distinctions needed for task-directed control;
3. the interface-provided success signal may be too sparse for the current consequence model;
4. the two-transition raw history may be insufficient for some required control dependencies;
5. the 256-action budget may constrain some games, though this has not yet been established as the dominant cause;
6. combinations of the above may apply differently by game.

No one explanation has authority yet.

## Next authorized operation

Do not tune or widen the implementation immediately.

First perform **post-result diagnostic discrimination using only the already frozen DEVELOPMENT execution logs and previously exposed development metadata**. The diagnostic should determine which failure hypotheses are supported or falsified without new environment interaction where possible.

Any v2 implementation change must be justified by that diagnostic pressure and preregistered before execution.

The seven SEALED_HOLDOUT games remain inaccessible.
