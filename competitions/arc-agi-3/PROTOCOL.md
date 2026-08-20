# ARC-AGI-3 Experiment 2 Protocol

Status: active proving-ground protocol on branch `arc3-exp2`.

## Scope

ARC-AGI-3 is used as a full agentic proving ground for the frozen Cognitive Evolution Architecture conception. The experiment must distinguish benchmark performance from evidence for CEA-specific mechanisms.

## Corpus firewall

Public corpus:

- 25 public ARC-AGI-3 games from the Kaggle competition bundle.
- 18 DEVELOPMENT games.
- 7 SEALED_HOLDOUT games.

Frozen holdout slugs:

`cn04`, `dc22`, `lf52`, `lp85`, `m0r0`, `tn36`, `tr87`.

The sealed holdout must not be used for source inspection, metadata inspection, manual play, replay inspection, solver research, tuning, or development feedback before the first frozen candidate evaluation.

Development runtime construction must physically exclude the seven sealed slugs before the ARC toolkit scans `metadata.json`.

## Epistemic firewall

Maintain:

- framework assertion != empirical demonstration
- specification != implementation != verification result
- component witness != composition witness
- evaluation != mutation
- frame change != progress
- no-op != uselessness
- visible frame equality != transition-state identity

Authority scope may not exceed discrimination scope.

## ARC-specific scientific question

Primary strong null:

`H0: CEA corrective machinery provides no advantage over a strong matched reactive/reflection/world-model agent under matched model, compute, and action budgets.`

Component nulls remain open for L / C / A / X and their composition.

## Development sequence

1. Freeze public provenance and sealed split. **DONE**
2. Build development-only runtime root. **DONE**
3. Inventory development metadata. **DONE**
4. Black-box interface probing before source inspection. **V1 + V2 DONE**
5. Freeze observed pressure surface. **DONE THROUGH V2**
6. Build strong non-CEA baseline. **NEXT**
7. Specify the minimal ARC-specific L+C+A+X implementation forced by development evidence.
8. Run matched component ablations.
9. Freeze first candidate.
10. One-shot seven-game sealed evaluation.
11. Generate Kaggle notebook.
12. External 110-game competition evaluation.

## Black-box probe rule

Development game implementation files may be executed by the official local environment wrapper because this is necessary to instantiate the environment, but their source text must not be inspected, parsed, searched, displayed, summarized, or supplied to the agent as information during the black-box phase.

Only interface-visible evidence is admissible:

- observations / frames
- state
- levels completed
- available actions
- chosen action and coordinate data
- resulting observation/state
- reset behavior
- recordings produced from interface-visible interactions

## Black-box V1 result

Commit `6dc9fb6` records the first interface probe artifacts:

- 18/18 development games characterized
- 84 fresh-reset one-step interventions
- 57/84 visible frame changes
- 27/84 visible no-ops
- 0/84 one-step level completions
- all post-probe states remained `NOT_FINISHED`
- same-seed RESET initial-frame repeatability 18/18

The V1 evidence directly rejects treating `frame_changed` as an authorized synonym for usefulness/progress. It also leaves preconditioned, delayed, coordinate-sensitive, and multi-step effects open.

## Black-box V2 result

Protocol was preregistered at commit `e68e121`; executable probe implementation was frozen at `f95bcc5`; empirical summary was frozen at `3c7569b`; per-game measurements were frozen at `f996776`.

V2 executed 2,800 fresh-reset sequences and 5,658 action steps across all 18 development games:

- 3,216 steps with visible frame change
- 2,442 steps with no visible frame change
- 0 level-completion deltas
- 0 state changes away from initial `NOT_FINISHED`
- 0 available-action-surface changes

V2 provides a direct transition-dynamics witness that visible frame equality is not sufficient for transition-state identity. In 11 repeated-identical-action cases across `g50t`, `sc25`, and `wa30`, the first action left the visible frame exactly unchanged while the same action repeated immediately afterward produced a visible change.

Formally, the measured trajectories include successive latent states `s0,s1` and action `a` for which:

`O(s0) = O(s1)` while `O(T(s0,a)) != O(T(s1,a))`.

This establishes transition-relevant observational aliasing. It does not establish task-relevant aliasing, goal structure, usefulness, or a CEA component witness.

V2 also measured sampled ACTION6 coordinate dependence in 6/13 ACTION6 games and exact frame-return transitions in 10 sequences across 2 games.

## Current authority state

Earned:

- public membership/version/byte provenance for uploaded Kaggle bundle
- frozen 18/7 split
- development-only runtime isolation
- development metadata inventory
- black-box one-step interface evidence
- black-box short-sequence transition evidence
- transition-relevant observational aliasing for the visible-frame interface in at least 3 development games

Not earned:

- task-relevant consequence model
- goal/mechanic identification
- ARC-specific CEA mechanism necessity
- CEA benchmark advantage
- component witnesses
- composition witness
- novelty claim
- sealed-holdout result
- external 110-game result
