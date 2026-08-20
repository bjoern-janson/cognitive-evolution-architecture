# ARC-AGI-3 Implementation Preregistration v1.4

Status: **PRE-EXECUTION MINIMAL REPAIR AMENDMENT**.

This amendment was created before the first ARC environment instantiation by the v1.x implementation and before any comparative arm result. It repairs specification ambiguities exposed by a static execution-readiness audit. It does not tune thresholds, history depth, candidate language, action budgets, action policies, or promotion criteria.

The operative specification becomes:

`V1 + V1.1 + V1.2 + V1.3 + V1.4`.

## SF-004 — observation descriptor color field

V1 named a singular `non-modal color id` while also allowing arbitrary 16-color frames. A frame may contain multiple non-modal colors, so the singular field is not well-defined.

Minimal repair:

- replace `non-modal color id` with `modal_color_id`, the smallest color id among colors tied for maximum cell count;
- retain `non_modal_cells = total_cells - count(modal_color_id)` exactly as before;
- no color descriptor is granted semantic status or added to the frozen transition-predictor context in v1.x.

This clarification does not change action selection or the primary transition model.

## SF-005 — development wall-clock field

V1 placed `remaining_wallclock_budget` in `G_t` but froze no local development wall-clock budget in Section 12.

Minimal repair:

- for mechanism-isolation development execution, `remaining_wallclock_budget = null` (`None`) and is informational only;
- the sole frozen local interaction budget remains 256 non-RESET actions per game;
- no v1.x action or promotion decision may depend on wall-clock time.

A later Kaggle deployment may define a deployment wall-clock field under a separate deployment specification.

## SF-006 — secondary transition-head predictor definition

V1 required prequential scores for every component of `S_t` but did not define the predictive heads precisely enough to implement them without discretion.

Minimal repair:

All secondary heads use the same frozen `c_base` context as the primary predictor, are scored before update, and have unit symmetric priors. They are instrumentation only and do not affect v1.x action selection, hypothesis generation, CLPR correction, or X authorization.

- `changed_count_bucket`: 7-class Dirichlet(1,...,1), already present in the base transition cell;
- `state_delta_class`: 3-class Dirichlet(1,1,1) over `SAME`, `WIN`, `GAME_OVER`;
- `level_delta_positive`: Beta(1,1);
- `action_surface_changed`: Beta(1,1);
- `exact_return_flag`: Beta(1,1).

Categorical NLL is `-log(p_observed)` with the same `[1e-6,1-1e-6]` numerical floor applied to the observed probability before scoring.

Predicate-contingency table `Q_t` remains exactly the v1.1 object and is **not** extended with these secondary heads.

## SF-007 — `F_B` aliasing-trigger counting

V1 did not state whether a context that remains mixed after first satisfying the candidate-generation trigger counts repeatedly.

Minimal repair:

`aliasing_residual_triggers` counts the **first activation only** for each unique `(game_slug, level_index, c_base)` tuple. A context contributes at most one trigger to a level.

This is measurement state only and cannot influence control.

## SF-008 — `F_B` forward-supported candidate threshold

V1 used `authorized_or_forward_supported_candidates` without freezing the support threshold.

Minimal repair:

A candidate is `forward_supported` for `F_B` iff it reaches at least **4 strictly forward in-scope scored events** after proposal, regardless of gain or X outcome. A candidate counts once in the level in which that threshold is first reached. Authorized candidates are included once and are not double-counted.

This definition reuses the already-frozen X forward-support threshold and adds no new promotion authority.

## SF-009 — `P_persistence` cross-arm pairing

V1 required comparison against the matched transient arm's parent prediction but did not freeze the exact event-pairing rule.

Minimal repair:

A persistent-arm canonical-scope encounter is evaluable only when the matched transient run has an event with the exact key:

`(game_slug, seed, level_index, step_within_game, action_token, action_coordinate)`.

The outcome signature must also match. If either key or outcome differs, the event is `NON_EVALUABLE_PAIR` and is excluded from `P_persistence`; it is not force-matched.

For an evaluable pair:

`persistence_nll_difference = NLL(persistent emitted prediction) - NLL(transient parent prediction)`.

Negative values favor the persisted correction.

The primary C pairing is `B+L+C` against `B+L`. `B_PERSIST` remains a descriptive conventional-persistence cross-check, not the transient parent comparator.

## Execution-readiness instrumentation requirement

Before the first ARC execution, the runner must durably log enough typed information to reconstruct the frozen mechanism metrics without retaining prohibited historical frames. At minimum this includes:

- transition/action legality and policy mode;
- prequential primary and all v1.4 secondary predictions/scores;
- first aliasing-trigger activations;
- admitted hypothesis creation and forward-support progress;
- localized correction source and claim id;
- every X evaluation decision, including refusals and reason codes;
- ungated-promotion control decisions;
- canonical entries and level-boundary persistence state;
- complete `Lambda_t` evidence/claim/decision records;
- per-run terminal/action/level summary.

Instrumentation records are read-only outputs and may not feed back into the agent.

## Authority state

Still unchanged:

- `H_raw = 2`;
- action budget = 256 per development game;
- seed policy unchanged;
- eight-predicate candidate language unchanged;
- CLPR correction rule unchanged;
- AIEC threshold/schedules unchanged;
- X thresholds unchanged;
- sealed exposure = 0;
- no ARC behavioral result has yet been produced.
