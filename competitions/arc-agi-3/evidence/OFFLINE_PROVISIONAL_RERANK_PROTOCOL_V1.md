# ARC-AGI-3 Experiment 2 — Offline Provisional Rerank Protocol v1

Status: **FROZEN BEFORE OFFLINE COUNTERFACTUAL EXECUTION**.

This protocol tests whether already-observed provisional L state could have changed AIEC probe-action ranking if the frozen v1.5 action policy had been allowed to consume that state. It uses only frozen DEVELOPMENT logs and deterministic replay of the already verified v1.5 state-update code. It performs no ARC environment interaction, no source inspection, no sealed exposure, no v2 implementation, and no policy mutation.

## Scientific question

Primary question:

`Does provisional L state contain enough action-discriminating information to change the ordering of legal AIEC probe candidates under the same transition-entropy objective used in v1.5?`

This is a connectivity diagnostic, not a task-competence test.

A positive result does not establish that the reranked action is useful, goal-directed, or superior in the environment. A negative result does not establish that all possible A_probe mechanisms are impossible.

## Frozen data surface

Primary replay arm: `B+L+A`, seed 0, all 18 DEVELOPMENT games from the complete v1.5 development matrix.

Reason: this arm contains provisional L corrections and the adaptive AIEC policy but no C/X persistence/governance confound.

Frozen execution artifact: `dc60b57c3d066d3e1f09e34af422061952da60fb`.

Only logged observations/transitions from the complete frozen run are replayed. No counterfactual action is sent to any environment.

## Decision reconstruction

Before replaying each logged transition result:

1. reconstruct the exact v1.5 core state from all preceding logged transitions using the frozen state-update implementation;
2. recover the current frame hash and live action mask from the logged transition record;
3. enumerate the same legal candidate action-coordinate set used by v1.5 `candidate_actions`;
4. compute candidate predictions from a disposable copy of the reconstructed state so enumeration cannot mutate the replay state;
5. discard the copy after ranking;
6. replay only the actually logged transition into the authoritative replay state.

Replay validity requires that the reconstructed prediction for the actually logged action matches the logged v1.5 parent and emitted primary probabilities to numerical tolerance `1e-12`. Any mismatch invalidates the affected game for interpretation until localized.

## Base ranking

For every legal candidate `a`, let

`p_base(a)` be the ordinary parent probability for `z_change` before any localized correction.

The frozen v1.5 AIEC information score is retained exactly:

`S_base(a) = H_Bernoulli(p_base(a))`.

Candidates rank by descending `S_base`; ties use the frozen deterministic ordering: action id, then coordinate order.

## Provisional-informed ranking

For every legal candidate `a`, let

`p_L(a)` be the primary probability emitted by the frozen L correction machinery at that same reconstructed decision state. Canonical state is absent in the primary `B+L+A` arm, so any difference from `p_base(a)` is provisional L influence only.

The counterfactual uses the **same** AIEC information objective and changes only which predictive probability the objective consumes:

`S_L(a) = H_Bernoulli(p_L(a))`.

Candidates rank by descending `S_L` with the same deterministic tie breaking.

This does not define a new utility function. It is the smallest missing-edge test:

`provisional L prediction -> existing AIEC ranking function`.

## Eligible decision point

A decision point is `L-eligible` iff at least one legal candidate has

`|p_L(a) - p_base(a)| > 1e-12`.

All decision points are counted, but ranking-change metrics are reported both:

- over all reconstructed decision points;
- conditionally over L-eligible points.

## Frozen metrics

For each decision point:

- `any_rank_change`: whether the complete candidate ordering differs;
- `top_action_change`: whether rank-1 `(action, coordinate)` differs;
- `mean_abs_rank_displacement`: mean absolute candidate rank movement;
- `max_abs_rank_displacement`;
- `top_margin_base`: score(rank1)-score(rank2) under base ranking;
- `top_margin_L`: same under provisional-informed ranking;
- `directly_modified_candidates`: count of candidates with changed predictive probability;
- `new_top_directly_modified`: whether a changed top action, if any, is itself a candidate whose probability was directly changed by L;
- `outside_scope_direct_score_changes`: count of candidates whose probability changed despite no matching provisional correction. Expected value under a correct localized implementation: zero.

Aggregate quantities:

- `N_decisions`;
- `N_eligible` and eligible fraction;
- `N_changed`: fraction with any ranking change;
- `N_top`: fraction with top-action change;
- mean and median absolute rank displacement;
- mean top-margin change;
- scope-consistency rate;
- per-game versions of all primary counts.

### Action-policy entropy

No `Delta H_pi` is introduced in v1 because the frozen AIEC ranking is deterministic. Assigning a stochastic softmax policy or temperature would create an unregistered mechanism. Top-margin change is used instead.

## Provenance-matched negative control

At every L-eligible decision point, preserve exactly:

- the candidate set;
- the base scores;
- the number of directly modified candidates;
- the multiset of provisional probability deltas `p_L(a)-p_base(a)`.

Break only the association between each L-derived delta and its actual candidate by deterministic pseudorandom permutation over candidate indices.

Null procedure:

- 256 permutations per eligible decision point;
- seed for permutation replicate `r` is SHA-256 of `"ARC3_OFFLINE_RERANK_NULL_V1|game|step|r"`, interpreted deterministically;
- each permuted probability is clipped to `[1e-6,1-1e-6]` before entropy scoring;
- rankings use the same deterministic tie breaking.

For each of 256 global null replicates, use the corresponding per-point permutation replicate and aggregate `N_changed`, `N_top`, and mean absolute rank displacement over the whole corpus.

Report the actual statistic, null mean, null 2.5/50/97.5 percentiles, and empirical upper-tail percentile. These are descriptive randomization diagnostics, not preregistered significance tests for a population claim.

## Interpretation gates

### Outcome A — effectively no reranking

If `N_eligible` is negligible or eligible-point `N_top` and rank displacement are approximately zero, infer only:

`the v1.5 provisional L state, when minimally connected to the existing entropy ranking, does not materially discriminate probe actions`.

This weakens the exact minimal A_probe bridge but does not falsify every possible graded-authority mechanism.

### Outcome B — structured reranking

If provisional-informed scores produce reproducible ranking changes materially above the provenance-matched null while outside-scope direct score changes remain zero, infer only:

`provisional L state contains action-discriminating information under the existing transition-entropy objective`.

This authorizes consideration of a small causal-connectivity experiment. It does not establish task value or A_plan.

### Outcome C — reranking indistinguishable from provenance-matched state

If observed ranking changes are comparable to the permutation null, infer that the action discrimination may be attributable to adding/reassigning predictive perturbations rather than to the learned scope linkage itself.

## Authority ceiling

This offline analysis cannot earn:

- task competence;
- A_probe benefit;
- A_plan;
- persistence benefit;
- graded authority as a CEA law;
- v2 implementation authorization by itself;
- sealed-holdout authorization.

It may only discriminate whether the already-frozen provisional L state has a structured causal route into the existing probe-ranking objective when that route is evaluated counterfactually.

Seven SEALED_HOLDOUT games remain untouched.
