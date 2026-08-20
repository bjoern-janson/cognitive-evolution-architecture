# Trace the Ace — Results Ledger

## Current Status

```text
No experimental result has yet been recorded in this proving-ground directory.
```

Establishing the protocol is not a result.

```text
proving-ground specification ≠ implementation ≠ experiment ≠ witness
```

## Result Classes

Every result must be marked as exactly one of:

```text
EXPLORATORY
INTERNAL_HELD_OUT
EXTERNAL_LEADERBOARD
COMPONENT_WITNESS_CANDIDATE
COMPONENT_WITNESS
COMPOSITION_WITNESS_CANDIDATE
COMPOSITION_WITNESS
NEGATIVE_RESULT
INVALID_RESULT
```

A leaderboard score normally belongs to `EXTERNAL_LEADERBOARD`; it does not automatically acquire component or composition authority.

## Baseline Results

| Run | Regime | Split | Log loss ↓ | Calibration | Notes | Status |
| --- | --- | --- | ---: | ---: | --- | --- |
| — | — | — | — | — | No runs yet | — |

## Component Results

| Experiment | Component | Target claim | Held-out effect | Uncertainty | Falsifier triggered? | Authority status |
| --- | --- | --- | ---: | --- | --- | --- |
| — | — | — | — | — | — | NOT EARNED |

## Composition Results

| Experiment | Regime | Utility | Pairwise interactions | Three-way `τ_LCA` | Scope | Authority status |
| --- | --- | ---: | --- | ---: | --- | --- |
| — | — | — | — | — | — | NOT EARNED |

## Longitudinal Results

| Epoch | State | Future log loss | `F_B` proxy | Regression | Correction cost | Authority violations |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| — | — | — | — | — | — | — |

## Authority Integrity

| Test family | Attempts | Unauthorized successes | False refusals | Result |
| --- | ---: | ---: | ---: | --- |
| — | — | — | — | NOT RUN |

## Negative Results

Preserve all genuine negatives here with:

```text
hypothesis
experiment
observed failure
failure locus
competing explanations
minimal revision, if any
retest status
```

A failed component or composition experiment is evidence about CEA and may be the legitimate trigger for evidence-pulled architectural revision.
