# ARC-AGI-3 Experiment 2 — Post-Result Diagnostic v1.5

Status: **POST-RESULT DEVELOPMENT DIAGNOSTIC**.

This document analyzes only the already frozen v1.5 DEVELOPMENT matrix logs plus previously exposed DEVELOPMENT metadata and the already frozen v1.5 implementation/specification. It introduces no new environment interaction, no source inspection, no sealed exposure, no threshold tuning, and no v2 implementation.

It is an interpretation/discrimination layer over `DEVELOPMENT_MATRIX_V1_5_RAW_RESULT.md`; it does not mutate or replace that raw empirical result.

## Frozen basis

Execution artifact:

`dc60b57c3d066d3e1f09e34af422061952da60fb`

Frozen behavioral result:

- 288/288 runs complete;
- 37,303 transitions;
- 0 level completions;
- 0 wins;
- positive development transition-prediction signal for L;
- C persistence non-evaluable;
- AIEC v1 negative against fixed 0/25/50/75 transition-NLL controls;
- X admitted 2 canonical promotions versus 27 permissive promotions under matched full-arm trajectories.

Seven SEALED_HOLDOUT games remain untouched.

---

# 1. New diagnostic discrimination: L/C/X were control-disconnected

The frozen logs were compared pairwise at the exact `(action_token, ACTION6_coordinate)` sequence and visible-frame trajectory level.

## Non-A action group

For every DEVELOPMENT game, the following arms emitted exactly the same action-coordinate sequence and therefore traversed exactly the same visible trajectory:

`B`, `B+L`, `B+C`, `B+X`, `B+L+C`.

Pairwise against `B`:

- `B` vs `B+L`: actions identical **18/18**, frame trajectories identical **18/18**;
- `B` vs `B+C`: **18/18**, **18/18**;
- `B` vs `B+X`: **18/18**, **18/18**;
- `B` vs `B+L+C`: **18/18**, **18/18**.

## A-bearing mechanism group

Likewise, every DEVELOPMENT game had an identical action-coordinate sequence and visible trajectory across:

`B+A`, `B+L+A`, `B+C+A`, `B+L+C+A`, `B+L+C+A+X`.

Pairwise against `B+A`:

- `B+A` vs `B+L+A`: actions identical **18/18**, frame trajectories identical **18/18**;
- `B+A` vs `B+C+A`: **18/18**, **18/18**;
- `B+A` vs `B+L+C+A`: **18/18**, **18/18**;
- `B+A` vs `B+L+C+A+X`: **18/18**, **18/18**.

Therefore, in v1.5, L/C/X changed prediction, hypothesis, memory, and governance state but did not change issued actions on any observed DEVELOPMENT trajectory.

This is consistent with the frozen implementation: `choose_action` dispatches either a task-agnostic deterministic candidate cycle or an AIEC/fixed policy backed by the ordinary `TransitionModel`; localized/canonical corrected predictions are emitted later by `predict_action` and are not consumed by the action policy.

The AIEC policy itself scores ordinary base-context `z_change` entropy. It does not consume CLPR-corrected probabilities, canonical memory, task-goal hypotheses, or visual descriptors beyond the action surface/history variables already in the base model.

## Consequence

The earlier statement

`L_task_competence = negative`

must be narrowed.

The v1.5 matrix establishes zero task progress under L-bearing arms, but it did **not** create a causal action contrast for L. The correct state is:

`L transition-prediction effect = POSITIVE DEVELOPMENT SIGNAL`

while

`L task-control effect = NON-IDENTIFIABLE / CONTROL-DISCONNECTED in v1.5`.

The same restriction applies to X task competence: strict and permissive X trajectories were behaviorally identical at the action/environment level. X governance integrity was evaluated; X task-control benefit was not.

For the full composition, the task trajectory was determined by the A-bearing action policy. L/C/X additions did not alter that trajectory. Therefore the v1.5 matrix does not identify a task-level L×C×A×X composition effect.

No composition witness remains earned.

---

# 2. Diagnostic of the “guardrails too tight” hypothesis

Observed governance contrast:

- permissive full arm canonical promotions: **27**;
- X-gated full arm canonical promotions: **2**.

However, strict and permissive full arms issued identical actions and traversed identical visible trajectories in **18/18** DEVELOPMENT games.

Thus the hypothesis

`strict X prevented useful actions`

is **not testable from v1.5**, because X had no action-selection pathway through which either a refusal or authorization could change behavior.

Loosening X alone would not have changed any v1.5 action unless the action architecture were also changed.

The stronger diagnostic pressure is therefore not “weaken canonical truth standards.” It is:

`epistemic state needs a scoped route into reversible control before canonical persistence`.

A candidate v2 hypothesis is graded authority:

- `A_probe`: may guide discriminating information-seeking;
- `A_plan`: may guide reversible/local tactical action;
- `A_persist`: may enter canonical cross-boundary memory;
- `A_global`: may generalize beyond the registered local scope.

This is currently a **diagnostic design hypothesis**, not an earned architecture change. It refines the X/A interface rather than adding a new CEA component.

---

# 3. Existing-evidence discrimination of live failure hypotheses

## H1 — task model is weak

Status: **STRONGLY SUPPORTED, more precisely: task-relevant state was absent from the control path.**

The frozen v1 specification deliberately restricted `G_t` to interface constraints and explicit benchmark signals. Inferred visual/task hypotheses had no privileged control authority.

The frozen action policy does not condition decisions on the current visual descriptor, object structure, inferred goal, CLPR-corrected prediction, or canonical claim. `current_frame_hash` is passed into policy APIs but is not used by `AIECPolicy` or `FixedAllocationPolicy` when choosing an action.

Therefore v1.5 did not contain an operational task model capable of mapping current visual/task state to action value.

This supports the missing bridge:

`transition model -> task-relevant consequence -> goal-directed action`.

It does not identify the correct goal representation.

## H2 — action policy is weak

Status: **SUPPORTED, but partially coupled to H1.**

`P_exec` is a deterministic legal-action/coordinate cycle. `P_info` selects the candidate with maximum ordinary `z_change` entropy. Neither uses task semantics or current visual-layout structure.

Across all 288 runs, task progress was zero.

Using DEVELOPMENT metadata, first-level human baseline action counts are between **7 and 78** actions across all 18 games; none exceeds the 256-action agent budget.

Across the 288 agent runs, **272/288** executed at least as many actions as the corresponding human first-level baseline without completing the first level. The 16 exceptions are all `sp80`, where every arm reached `GAME_OVER` after 30 actions versus a first-level human baseline of 39.

This weakens a pure “not enough actions” explanation and supports a task-alignment/action-selection deficiency.

## H3 — `H_raw = 2` is insufficient

Status: **MIXED / NOT ESTABLISHED AS THE NEXT REVISION.**

A post-hoc history-depth diagnostic reconstructed action/outcome context from the frozen logs only.

Retrospectively, deeper history reduces residual mixed transition contexts. For `B+A`, the fraction of events lying in mixed `z_change` contexts fell from approximately **4.0% at depth 2** to **1.2% at depth 5**. For `B`, it fell from approximately **2.1%** to **1.2%**.

But a matched online Beta-Bernoulli prequential diagnostic shows the opposite pressure once sparsity is paid for:

- `B`: depth-2 mean NLL ≈ **0.4767**; depth-5 ≈ **0.4835**;
- `B+A`: depth-2 ≈ **0.6215**; depth-5 ≈ **0.6404**.

Thus longer history can retrospectively partition remaining transition aliasing but did not improve online prediction under the tested tabular count model.

The logs therefore do **not** currently license widening `H_raw` as the primary v2 repair.

## H4 — task consequence signal is too sparse

Status: **STRONGLY SUPPORTED.**

Across 37,303 scored transitions:

- positive level deltas: **0**;
- `WIN`: **0**.

The agent therefore received no positive task-success event from the explicit benchmark consequence channel during the entire matrix.

Negative `GAME_OVER` consequences occurred, but v1 AIEC does not optimize predicted level/win/game-over utility; the relevant secondary heads are measurement outputs rather than action-value inputs.

This establishes extreme sparsity/misalignment of the direct task consequence signal available to the v1 control rule. It does not prove that no useful denser consequence can be inferred from visual structure.

## H5 — AIEC optimizes the wrong information target

Status: **STRONGLY SUPPORTED FOR AIEC v1.**

AIEC v1 optimizes posterior predictive entropy of the non-semantic target:

`z_change = 1[O_{t+1} != O_t]`.

It does not optimize information about task goals, level success, survival, or decision value.

Observed DEVELOPMENT result:

- adaptive `B+A` selected `P_INFO` on **1,836/2,264 ≈ 81.1%** of actions;
- mean primary NLL `0.58599`;
- fixed 0% information NLL `0.48682`;
- fixed 25% `0.53909`;
- fixed 50% `0.57588`;
- fixed 75% `0.56691`;
- fixed 100% `0.59332`.

Across the five fixed controls, information-allocation fraction is strongly positively associated with worse transition NLL (Pearson ≈ **0.916**; descriptive post-hoc statistic only).

Within the adaptive `B+A` trajectory:

- `P_INFO`: 1,836 actions, mean emitted NLL ≈ **0.6314**, `z_change` rate ≈ **0.495**;
- `P_EXEC`: 428 actions, mean emitted NLL ≈ **0.2308**, `z_change` rate ≈ **0.589**.

These within-policy numbers are selection-confounded because AIEC chooses modes based on model uncertainty; they are diagnostic, not a causal comparison.

The licensed conclusion is narrow:

`transition uncertainty != demonstrated task-relevant information value`.

## H6 — 256-action budget prevents competence before persistence can manifest

Status: **WEAKENED AS A CORPUS-WIDE PRIMARY EXPLANATION; remains possible locally.**

Every DEVELOPMENT game's metadata first-level human baseline is below 256 actions (range **7–78**).

`272/288` agent runs lasted at least the corresponding first-level human action count without completing that level.

Therefore simply raising the global action cap is not currently supported as the dominant repair.

`sp80` is the clearest local exception: every arm terminated at 30 actions before the metadata first-level human baseline of 39. Other local budget/survival interactions may exist, but they cannot explain the corpus-wide zero-completion result.

---

# 4. X predictive-quality diagnostic

The strict X gate did not merely refuse claims indiscriminately on the observed trajectories.

Full permissive arm `B+L+C+A`:

- 27 canonical entries;
- 130 canonical-correction applications;
- cumulative canonical local-vs-parent primary NLL gain ≈ **5.4433 nats**;
- mean gain per canonical application ≈ **0.0419 nats**.

X-gated full arm:

- 2 canonical entries;
- 2 canonical-correction applications;
- cumulative canonical gain ≈ **0.7760 nats**;
- mean gain per canonical application ≈ **0.3880 nats**.

This is descriptive development evidence consistent with X selecting a much smaller set of stronger canonical corrections for transition prediction. It does not establish optimal gate strictness, because action value and cross-level persistence were not evaluated.

Therefore the current evidence does **not** support loosening `A_persist`/canonical standards.

---

# 5. Minimal v2 pressure earned by this diagnostic

The strongest pressure is at the interface between epistemic state and action, not at canonical truth standards.

v1.5 demonstrated:

1. localized/provisional epistemic state can improve transition prediction;
2. canonical governance can strongly restrict persistent claims;
3. neither provisional nor canonical corrected state influenced action selection;
4. AIEC was the only CEA factor that changed the task trajectory, and it optimized transition entropy rather than task-relevant consequence;
5. direct positive task consequence was never observed;
6. longer raw history is not yet justified as the primary repair;
7. the global 256-action cap is not supported as the dominant failure cause.

The next architecture/specification problem is therefore:

`How can uncertain, scoped, provenance-bearing hypotheses influence reversible task-directed action without being promoted to canonical truth?`

A candidate graded-authority formulation is scientifically motivated:

`hypothesis -> probe authority -> reversible planning authority -> persistence authority -> wider generalization authority`.

But this remains a **v2 operationalization hypothesis**. It must be specified and falsifiable before implementation.

No existing X threshold is changed by this diagnostic.

---

# 6. Authority update

Earned / strengthened:

- `transition-prediction improvement != task competence`;
- L transition-prediction development signal remains positive;
- v1.5 L/C/X task effects are control-disconnected and therefore task-level causal effects are non-identifiable;
- AIEC v1 negative development result remains valid because AIEC did change action trajectories;
- task-positive consequence sparsity is directly established;
- 256-action global budget hypothesis is weakened;
- deeper-than-2 raw history is not yet licensed as the primary repair;
- graded scoped action authority is a justified **candidate v2 hypothesis**.

Not earned:

- claim that X is too strict;
- claim that permissive persistence would improve competence;
- claim that `H_raw > 2` is needed;
- task-goal identity;
- component witness;
- composition witness;
- held-out evaluation;
- sealed-holdout result.

Sealed exposure remains **0**.
