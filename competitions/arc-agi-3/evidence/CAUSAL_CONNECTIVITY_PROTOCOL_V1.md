# ARC-AGI-3 Experiment 2 — Provisional Probe Causal-Connectivity Protocol v1

Status: **FROZEN BEFORE IMPLEMENTATION OR NEW ARC INTERACTION**.

This protocol tests one and only one newly authorized causal edge:

`provisional L state -> A_probe ranking input`.

It does not authorize `A_plan`, relaxation of canonical X persistence, cross-context generalization, a new CEA component, or any task-semantic goal representation.

## Frozen evidential basis

The experiment is authorized by the already frozen DEVELOPMENT evidence:

- v1.5 implementation artifact: `dc60b57c3d066d3e1f09e34af422061952da60fb`;
- v1.5 matrix: 288/288 completed DEVELOPMENT runs, 0 level completions, 0 wins;
- post-result diagnostic: L/C/X were control-disconnected in v1.5;
- offline provisional rerank protocol freeze: `34be699c6e84efabc6c7a35a129df2789843f684`;
- offline provisional rerank result freeze: `48e9d65525afadc2a8ca1addb47b59d7a9069cc5`;
- offline replay: 2,264/2,264 reconstructed decisions valid, 392 L-eligible points, 205/392 rank-1 changes, zero out-of-scope direct score changes, and an observed rank-1 change rate above all 256 provenance-matched permutation replicates.

The offline result established action discrimination only. It did not establish that any reranked action is environmentally useful.

## Scientific question

Primary question:

`Does allowing the already-frozen provisional L state to influence AIEC information-probe ranking improve subsequent environment-grounded transition prediction relative to an otherwise identical arm in which the same provisional state remains control-disconnected?`

This is an `A_probe` causal-connectivity assay, not a task-goal or persistence assay.

## Experimental arms

Exactly two arms are permitted.

### `E_disconnected`

Mechanistic state is exactly the v1.5 `B+L+A` configuration:

- same ordinary transition model;
- same provisional L hypothesis generation and correction machinery;
- same bounded history;
- same candidate actions;
- same AIEC mode threshold and execution policy;
- provisional L predictions are computed and logged;
- action selection continues to use the ordinary base transition probabilities exactly as v1.5.

`E_disconnected` is the causal control.

### `E_connected`

Identical to `E_disconnected` except for one edge inside **P_INFO candidate ranking only**:

`p_base(a) -> p_probe(a)`

where:

- if the frozen provisional-L selection rule identifies a matching live provisional correction for candidate `a`, `p_probe(a)` is that frozen provisional-L-corrected probability;
- otherwise `p_probe(a) = p_base(a)`.

The information score remains exactly:

`S(a) = H_Bernoulli(p_change(a))`.

No new utility, semantic score, object detector, goal hypothesis, reward model, survival heuristic, or planning term is introduced.

## Isolation of the causal edge

The v1.5 AIEC mode decision remains unchanged in both arms.

For every decision point:

1. enumerate the same legal candidate actions and ACTION6 coordinates;
2. compute ordinary base probabilities for every candidate;
3. compute the **mean base-probability entropy** exactly as v1.5;
4. compare that mean to the frozen `0.55` nat threshold;
5. if the result is `P_EXEC`, both arms use the original deterministic execution cycle and provisional L cannot alter the action;
6. if the result is `P_INFO`:
   - `E_disconnected` ranks candidates by `H(p_base(a))`;
   - `E_connected` ranks candidates by `H(p_probe(a))`;
7. both use the original deterministic action-id/coordinate tie breaking.

Thus connectivity may change **which information-seeking action is selected**, but may not change whether the step is classified as `P_INFO` or `P_EXEC` at the same pre-divergence state.

This prevents the first causal assay from conflating graded action permission with a redesigned explore/exploit allocator.

## What remains fixed

Both arms retain:

- `H_raw = 2 completed transitions + current observation`;
- seed `0`;
- maximum `256` non-RESET actions per game;
- same candidate action enumeration and ACTION6 schedule;
- same `0.55` AIEC entropy threshold;
- same deterministic `P_EXEC` cycle;
- same transition-model priors and updates;
- same non-semantic predicate language;
- same provisional-correction proposal, arbitration, forward-support, and eviction rules;
- same logging and lineage requirements;
- no semantic goal labels;
- no `A_plan`;
- no `A_generalize`;
- no environment source inspection.

The first connectivity assay uses the `B+L+A` substrate specifically to avoid C/X persistence as a causal confound. Existing X thresholds and canonical-persistence rules remain frozen globally but are **not activated in these two assay arms**. Nothing in this protocol relaxes `A_persist`.

## Development corpus and run matrix

Run both arms on all 18 already exposed DEVELOPMENT games, seed 0:

`18 games x 2 arms = 36 runs`.

The seven `SEALED_HOLDOUT` games must remain physically absent from the runtime environment root.

All runs begin from fresh game-local state. No result may be used to alter the second arm during the matrix.

## Predeclared strata

The offline diagnostic identified provisional-L-eligible points on the frozen v1.5 trajectory in exactly six games:

`ar25, g50t, sb26, sc25, sk48, wa30`.

These six form the **primary connectivity stratum**.

The other twelve DEVELOPMENT games form a **negative-control stratum** because the frozen offline replay observed no legal candidate whose prediction was changed by provisional L on the original `B+L+A` trajectory.

The stratum assignment is frozen from prior evidence and may not be changed after the causal run.

## Primary outcome

The primary outcome is the paired per-game **ordinary parent/base-model primary transition NLL** over the full realized run:

`T_parent(g, arm) = mean_t[-log P_base(z_change_t | context_t)]`.

Primary estimator over the six-game connectivity stratum:

`Delta_parent = mean_g[T_parent(g,E_connected) - T_parent(g,E_disconnected)]`.

Lower is better.

Why parent NLL is primary:

- it is already a frozen v1.5 measurement;
- it is scored prequentially before the transition-model update;
- it does not directly reward the provisional corrected probability that caused the action reranking;
- therefore it asks whether the different probe trajectory buys useful predictive evidence for the shared ordinary transition model, rather than merely whether the L-corrected prediction scores itself well.

No significance threshold or population claim is preregistered. Report the exact six paired game differences, their mean, median, and sign pattern.

Directional interpretation:

- `Delta_parent < 0`: positive DEVELOPMENT causal-connectivity signal for the registered probe objective;
- `Delta_parent > 0`: negative DEVELOPMENT causal-connectivity signal;
- `Delta_parent = 0` within `1e-12`: no measured primary effect.

Magnitude and heterogeneity must be reported even when the sign is clear.

## Required secondary outcomes

Secondary quantities, all explicitly subordinate to the primary outcome:

1. emitted/L-corrected primary transition NLL;
2. number and fraction of steps at which the two arms' issued `(action, coordinate)` differ;
3. number of `P_INFO` and `P_EXEC` steps per run;
4. first action-divergence step per game, if any;
5. level completions;
6. terminal `WIN`, `GAME_OVER`, or budget-exhausted `NOT_FINISHED`;
7. non-RESET actions to termination/budget;
8. changed-cell and exact-return transition signatures already available in v1.5;
9. provisional claims admitted, forward-supported, and actually used for `E_connected` probe ranking;
10. direct ranking-score changes outside registered provisional scope — expected `0`;
11. action-legality violations — expected `0`;
12. any level-boundary event, reported descriptively only; this assay does not activate C persistence.

Task progress is therefore recorded if it occurs, but **level completion is not the primary outcome and cannot retroactively redefine success of the probe-connectivity hypothesis**.

## Negative-control requirements

### Disconnected replay control

Before causal execution, `E_disconnected` must reproduce the frozen v1.5 `B+L+A` policy/state-update behavior under deterministic offline replay.

Required:

- action-coordinate sequence match on frozen logs: exact until logged termination;
- logged parent/emitted probability replay tolerance: `1e-12`;
- same hypothesis/provisional-correction state at replayed decision points.

Failure invalidates implementation authorization until localized.

### Connected offline conformance control

Before environment execution, the implementation of `E_connected` must reproduce the frozen offline rerank result on the original v1.5 logs:

- 2,264 reconstructed decision points;
- 392 L-eligible points;
- 205 rank-1 changes;
- zero direct score changes outside registered provisional scope.

This is implementation conformance, not a new scientific result.

### Twelve-game negative-control stratum

Because connected and disconnected arms are identical until an action divergence, any divergence on a game whose exact frozen prefix contains no provisional-L candidate modification must be investigated against replay before interpretation.

The twelve-game stratum is reported separately and cannot be used post hoc to redefine the six-game primary stratum.

## Anti-laundering constraints

The experiment must preserve:

- `A_probe` permission does not alter hypothesis truth status;
- a selected probe does not become canonical because it was selected;
- successful environment consequence does not automatically authorize `A_persist`;
- task progress, if observed, does not establish that the provisional hypothesis identified the task mechanic;
- probe failure does not automatically retire a hypothesis unless the already-frozen evidence rules warrant it;
- no connectivity result authorizes cross-context or sealed generalization;
- no threshold, predicate, history depth, candidate set, budget, or goal representation may be tuned during the 36-run matrix.

## Implementation gate

This protocol freezes the experiment, not its code.

Before any new ARC interaction, the minimal connectivity implementation must:

1. be derived from the verified v1.5 artifact;
2. expose an explicit `connected/disconnected` probe-ranking switch rather than duplicating unrelated mechanisms;
3. pass all inherited v1.5 invariant/conformance tests;
4. add tests proving that only `P_INFO` ranking may consume provisional L probabilities;
5. prove `P_EXEC` identity across connectivity settings from identical state;
6. prove the base mean-entropy mode threshold is identical across settings from identical state;
7. prove no canonical state affects the first connectivity assay;
8. pass the disconnected replay control;
9. pass the connected offline conformance control;
10. be frozen and byte-verified before the 36-run environment matrix begins.

Implementation failure is not permission to change this protocol. Any impossible or contradictory requirement must be recorded as a typed specification failure and repaired prospectively before environment results exist.

## Interpretation ceiling

A positive primary result may earn only:

`provisional L-informed A_probe connectivity improves the registered DEVELOPMENT transition-prediction consequence relative to the disconnected control under this frozen assay.`

It does not earn:

- task-goal identification;
- `A_plan`;
- `A_persist` relaxation;
- `A_generalize`;
- graded authority as a general CEA law;
- CLPR/AIEC/X component witness;
- CEA composition witness;
- held-out or Kaggle authority.

A negative result falsifies or weakens only this minimal connectivity mechanism under the registered objective. It does not establish that all typed action permission is useless.

## Stopping boundary

After the complete 36-run matrix is frozen, stop before redesign.

Perform result classification and diagnostic discrimination first. Any successor mechanism requires a new preregistration.

Seven `SEALED_HOLDOUT` games remain untouched.