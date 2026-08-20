# ARC-AGI-3 Experiment 2 — Development Matrix v1.5 Raw Result

Status: **FIRST COMPLETE ARC BEHAVIORAL RESULT**.

This file freezes the first complete development execution of the v1.5 mechanism-isolation artifact before any tuning or redesign. It is an empirical development result, not a held-out result, component witness, composition witness, novelty claim, or Kaggle result.

## Frozen execution artifact

Implementation commit:

`dc60b57c3d066d3e1f09e34af422061952da60fb`

Operative specification:

`V1 + V1.1 + V1.2 + V1.3 + V1.4 + V1.5`.

Execution matrix:

- 18 DEVELOPMENT games;
- 16 frozen arms;
- seed 0;
- maximum 256 non-RESET actions per arm/game pair;
- lexicographic game order;
- independent fresh game-local state for every arm/game pair;
- seven SEALED_HOLDOUT games physically absent.

Expected runs: 288.

Completed runs: **288/288**.

## Infrastructure interruption lineage

Four earlier full-matrix attempts were terminated externally by the container command-time limit before completion. They completed 151, 144, 152, and 150 run records respectively.

Those partial matrices were not resumed, spliced, combined, or interpreted as the experiment result. The frozen runner's no-resume rule was preserved.

The fifth attempt ran the same frozen process detached from the short-lived command transport and completed all 288 runs without changing implementation bytes, seed, order, budgets, thresholds, predicates, or environment exposure.

## Raw artifact hashes

Complete run directory: local execution object `arc3_exp2_v15_dev_matrix_run5`.

Top-level result hashes:

- `MANIFEST.json` SHA-256: `14b248de2d0f4168e198d11dae91f11832efeaf209f33e2fef77e95312038cb5`
- `results.partial.jsonl` SHA-256: `1be0a292e19798fed84ff16d6cd0da4ea22ee2986370e28e08bcee27d69e4bf5`
- `results.json` SHA-256: `49d9fc53cc99deee8e47116a2459e98d57cdfbcc4455f3888ca8ca547c1b0ea3`
- `results.csv` SHA-256: `b2f43fc37d31f0c3c1b5316a3b4d69a41f487ccc581dadde3da1710f91731ffa`

Per-run logs:

- log files: **288**;
- uncompressed log bytes: **129,949,039**;
- deterministic per-log SHA-256 manifest aggregate SHA-256: `401caf9c9fba1197bf813223a31587c57f0dbc97b059c32e1e1f3e6029e6507e`;
- local gzip archive SHA-256: `666055b9944ac7abfda2fd1553fee5a7feed0302351188c52beaae0f4ca915dc`.

The large raw JSONL logs are not embedded in this Git repository; their hashes are frozen here. The execution is deterministic under the frozen seed/artifact and can be regenerated from the verified corpus/runtime.

## Structural validation

- result rows: **288**;
- unique `(game_slug, arm, seed)` keys: **288**;
- run logs: **288**;
- reducer-successful logs: **288/288**;
- reducer errors: **0**;
- interface transitions: **37,303**;
- durable lineage evidence records: **37,303**;
- transition/evidence mismatch: **0**;
- logged claims: **596**;
- logged authorization/ungated decisions: **13,805**;
- logged distinct aliasing triggers: **62**;
- logged forward-supported claims: **89**;
- illegal issued actions: **0**;
- reduced outside-scope collateral violations: **0**;
- sealed slugs observed: **0**;
- development slugs observed: **18**;
- maximum non-RESET actions in a run: **256**.

## Direct benchmark progress result

Across all 288 arm/game runs:

- total observed level completions: **0**;
- terminal `WIN`: **0**;
- terminal `GAME_OVER`: **223**;
- terminal `NOT_FINISHED` at budget: **65**.

Therefore the v1.5 mechanism-isolation system produced **no direct ARC task progress** on the 18-game development matrix.

This is a negative benchmark-engagement result. It does not imply that every internal mechanism failed; component-specific transition and governance measurements must be analyzed separately.

## Primary mechanism measurements

### L / localized correction

`B+L` versus `B`:

- mean per-game primary transition NLL: `0.4760143420` vs `0.4868200973`;
- mean paired difference: `-0.0108057553` NLL (lower is better);
- 1 game improved, 17 unchanged, 0 worsened;
- the non-zero difference occurred on `g50t` (`-0.194504` per-game NLL);
- 43 provisional correction-applied scored events;
- all 43/43 had positive local-vs-parent prequential NLL gain;
- cumulative correction gain: `25.2854673780` nats.

`B+L+A` versus `B+A`:

- mean per-game primary transition NLL: `0.5815631872` vs `0.5859938760`;
- mean paired difference: `-0.0044306887`;
- 4 games improved, 2 worsened, 12 unchanged;
- 197 correction-applied events;
- 131 positive-gain, 62 negative-gain, 4 zero-gain events;
- cumulative correction gain: `14.7354976850` nats.

This is a positive **development transition-prediction signal** for L. It is not a CLPR component witness and it did not produce task progress.

### C / persistence

No arm completed a level. Therefore the registered level-boundary persistence contrast was never entered.

Preregistered persistence reducer:

- evaluable persisted-scope encounters: **0**;
- `P_persistence n = 0`;
- paired later levels for `F_B`: **0**.

Thus C persistence is **NON-EVALUABLE** in this matrix.

Within-level permissive canonicalization in `B+L+C` produced 4 ungated promotions and a mean NLL `0.0005843035` worse than `B+L`; this is not a level-persistence estimate.

### A / AIEC

Mean per-game primary transition NLL:

- `B+A`: `0.5859938760`;
- `A_fixed_0`: `0.4868200973`;
- `A_fixed_25`: `0.5390853763`;
- `A_fixed_50`: `0.5758831669`;
- `A_fixed_75`: `0.5669081254`;
- `A_fixed_100`: `0.5933211992`.

The adaptive AIEC arm selected `P_INFO` 1,836 times and `P_EXEC` 428 times over 2,264 actions.

Against the frozen fixed-allocation controls, AIEC v1 had worse mean transition NLL than fixed 0%, 25%, 50%, and 75%, and better mean NLL only than fixed 100%.

Therefore the preregistered AIEC v1 transition-prediction hypothesis receives a **negative development result**. No task-performance claim is available because every arm had zero level completion.

### X / authority governance

Under otherwise matched `B+L+C+A` trajectories:

- claims admitted: 196 in both governance arms;
- forward-supported claims: 27 in both;
- permissive `B+L+C+A` promotions: **27**;
- X-gated `B+L+C+A+X` promotions: **2**;
- X eligible-promotion events: **2**;
- X unauthorized-promotion rate: **0**;
- X strict false-refusal rate: **0**.

Mean per-game transition NLL:

- permissive full arm: `0.5821254543`;
- X-gated full arm: `0.5815723946`;
- paired mean difference: `-0.0005530598` in favor of X;
- 4 games improved, 1 worsened, 13 unchanged.

This establishes that X v1 materially restricted canonical promotion while satisfying its frozen integrity predicates on the observed development trajectories. Because no level transition occurred, the consequences of that governance for persistent future-level state are **not evaluated**. No X witness is earned.

## Composition boundary

The full `B+L+C+A+X` arm:

- completed 0 levels;
- won 0 games;
- mean primary transition NLL `0.5815723946`, worse than baseline `B` at `0.4868200973`.

Therefore the v1.5 full composition does **not** demonstrate greater long-horizon competence acquisition than the matched baseline on this development matrix.

No component witness, composition witness, held-out generalization, or benchmark advantage is earned.

## New empirical discrimination

The matrix strengthens an earlier distinction:

`better transition prediction != task progress`.

Localized corrections produced measurable forward transition-prediction gains on development trajectories while all arms still produced zero level completions.

The result therefore creates pressure for a task-relevant consequence / goal-acquisition bridge, but it does not by itself identify the missing representation or mechanism.

## Authority state after result

Earned:

- first complete v1.5 development behavioral result;
- positive L transition-prediction development signal;
- negative AIEC v1 transition-prediction result versus most fixed controls;
- X governance-integrity behavior on observed trajectories;
- direct negative benchmark-engagement result: 0 level completions / 0 wins.

Not earned / non-evaluable:

- C level-persistence effect: **NON-EVALUABLE**;
- task-relevant consequence model;
- goal acquisition mechanism;
- CLPR witness;
- Core witness;
- AIEC task-performance witness;
- X persistent-state witness;
- CEA composition witness;
- held-out result;
- Kaggle result.

The seven SEALED_HOLDOUT games remain untouched.
