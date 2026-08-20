# ARC-AGI-3 Experiment 2 — Offline Provisional Rerank Result v1

Status: **OFFLINE DEVELOPMENT DIAGNOSTIC RESULT**.

This result executes `OFFLINE_PROVISIONAL_RERANK_PROTOCOL_V1.md` against the already frozen v1.5 DEVELOPMENT logs only. It introduces no new ARC environment interaction, no source inspection, no sealed exposure, no v2 implementation, and no change to the frozen v1.5 action policy.

## Frozen basis

Protocol freeze commit:

`34be699c6e84efabc6c7a35a129df2789843f684`

Behavioral execution artifact replayed:

`dc60b57c3d066d3e1f09e34af422061952da60fb`

Primary replay arm:

`B+L+A`, seed 0, all 18 DEVELOPMENT games.

Frozen v1.5 logs used: the complete `arc3_exp2_v15_dev_matrix_run5` execution object already hashed in `DEVELOPMENT_MATRIX_V1_5_RAW_RESULT.md`.

Offline result JSON SHA-256:

`fa0e2a83ce7da023c922b34a48cf92f8fcde9a0b9cc3ad93aa2ccb970f423b53`

Auxiliary attribution JSON SHA-256:

`da7ee88f5bc01599c7c352a4f94802fc3e31008e65a51b51bec6f89ecbda100b`

## Replay validity

Reconstructed decision-state replay was checked against the logged v1.5 parent and emitted probabilities for the actually executed action at every transition.

- reconstructed decision points: **2,264**;
- replay-valid games: **18/18**;
- parent/emitted probability mismatches above `1e-12`: **0**.

No counterfactual action was executed.

## Primary eligibility result

A point is L-eligible iff at least one legal candidate receives a different primary probability from the frozen provisional L correction machinery.

- all reconstructed decisions: **2,264**;
- L-eligible decisions: **392**;
- eligible fraction: **17.31%**;
- directly modified candidate predictions across eligible decisions: **482**.

L-eligible decisions occurred in **6/18** games:

- `ar25`: 61/256;
- `g50t`: 39/130;
- `sb26`: 120/256;
- `sc25`: 16/139;
- `sk48`: 75/256;
- `wa30`: 81/200.

The remaining 12 games had no decision point at which provisional L state changed any legal candidate's primary probability under the frozen v1.5 representation and trajectory.

## Actual reranking

The counterfactual retained the exact v1.5 AIEC objective:

`S(a) = H_Bernoulli(p_change(a))`.

Only its predictive input changed from the base probability to the already-frozen provisional-L-corrected probability.

Conditional on the 392 L-eligible decision points:

- any complete-order ranking change: **251/392 = 64.03%**;
- rank-1 action-coordinate change: **205/392 = 52.30%**;
- candidate-weighted mean absolute rank displacement: **0.9491 ranks**;
- median decision-level mean absolute displacement: **0.6970 ranks**;
- mean top-margin change: **+0.00961 nats**;
- direct probability changes outside registered provisional scope: **0**.

Every one of the **205** top-action changes touched a directly L-modified candidate at the top boundary: either the old top was directly modified, the new top was directly modified, or both.

- new top directly modified: **139/205**;
- old top directly modified: **72/205**;
- union touching old or new top: **205/205**.

Thus the rank-1 changes are attributable to the scoped L correction surface rather than an unrelated sorting artifact.

## Provenance-matched permutation control

The negative control preserved, at each eligible point:

- candidate set;
- base scores;
- number of modified candidates;
- exact multiset of L-derived probability deltas.

It destroyed only the learned association between each delta and its actual candidate by the frozen deterministic 256-replicate permutation procedure.

### Rank-1 action change rate

Observed:

`0.52296`

Permutation null:

- mean: `0.23879`;
- median: `0.23724`;
- 2.5th percentile: `0.21173`;
- 97.5th percentile: `0.27041`.

Observed rank-1 change exceeded **all 256/256** null replicates.

This is a descriptive randomization diagnostic, not a population-level significance claim.

### Any-ranking-change rate

Observed:

`0.64031`

Permutation null:

- mean: `0.89716`;
- 97.5th percentile: `0.91837`.

Observed diffuse ranking change was **lower** than every null replicate.

### Mean absolute rank displacement

Observed:

`0.94914`

Permutation null:

- mean: `1.19313`;
- 2.5th percentile: `1.12149`;
- 97.5th percentile: `1.24958`.

Observed displacement was **lower** than every null replicate.

## Structural interpretation of the null comparison

The learned provisional state does not behave like generic extra predictive perturbation.

Randomly reassigning the same correction deltas produces broader and more diffuse ranking churn, but substantially fewer rank-1 changes.

The observed learned linkage instead produces a more concentrated pattern:

`less global rank movement + much more frequent top-decision change`.

This is consistent with the learned scopes aligning corrective probability changes with candidates that are decision-critical under the existing entropy ranking.

It does not establish that the new rank-1 action is task-useful.

## Which distinctions drove the modified candidate predictions

Across the 482 directly modified candidate predictions, the selected provisional correction predicate was:

- `prev2_z`: **310**;
- `prev2_action`: **131**;
- `prev_coord_bin`: **40**;
- `prev2_coord_bin`: **1**.

No semantic goal or mechanic predicate is involved. The action-discriminating information arises from the frozen non-semantic bounded-history predicate language.

Directly modified action ids were also localized by game:

- `ar25`: ACTION1;
- `g50t`: ACTION1/ACTION2/ACTION3;
- `sb26`: ACTION6 coordinates;
- `sc25`: ACTION1;
- `sk48`: ACTION1;
- `wa30`: ACTION5.

This establishes structured action discrimination, not task relevance.

## Protocol outcome

The result is not `Outcome A` (effectively no reranking).

The result is also more specific than generic diffuse `Outcome B` because two metric families move in opposite directions relative to the provenance-matched null:

- **decision-boundary/top-action reranking: strongly above null**;
- **diffuse whole-order reranking: below null**.

Therefore the licensed result is:

`provisional L state contains structured action-discriminating information under the existing v1.5 transition-entropy objective, concentrated at the rank-1 decision boundary rather than expressed as generic ranking perturbation.`

This satisfies the protocol's causal-connectivity prerequisite narrowly at the probe-ranking boundary and authorizes preregistration of a **small DEVELOPMENT causal-connectivity experiment** in which an A_probe-like path may consume provisional L predictions while canonical X persistence remains unchanged.

## What is not earned

This result does **not** establish:

- that any counterfactually selected action is useful;
- task-goal identification;
- A_probe benefit in the environment;
- A_plan;
- task competence;
- persistence benefit;
- relaxed X thresholds;
- graded authority as a CEA law;
- a component witness;
- a composition witness;
- held-out generalization.

## Authority update

Earned:

- provisional L state is action-discriminating for the existing AIEC probe-ranking objective at 392 observed DEVELOPMENT decision points;
- the learned scope linkage changes rank-1 actions much more often than provenance-matched reassignment of the same correction deltas;
- the effect is scope-consistent and concentrated at the top decision boundary;
- a small, separately preregistered DEVELOPMENT causal-connectivity test is authorized.

Not earned:

- any particular v2 mechanism beyond the minimal connectivity hypothesis;
- A_plan, A_persist relaxation, or A_generalize;
- sealed evaluation.

Seven SEALED_HOLDOUT games remain untouched.
