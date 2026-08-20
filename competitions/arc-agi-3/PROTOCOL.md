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
- observational aliasing != task-semantic aliasing
- transition predictiveness != usefulness
- implementation convenience != specification change

Authority scope may not exceed discrimination scope.

## ARC-specific scientific question

Primary strong null:

`H0: CEA corrective machinery provides no advantage over a strong matched reactive/reflection/world-model agent under matched model, compute, action budgets, and environment exposure.`

Component nulls remain open for L / C / A / X and their composition.

## Development sequence

1. Freeze public provenance and sealed split. **DONE**
2. Build development-only runtime root. **DONE**
3. Inventory development metadata. **DONE**
4. Black-box interface probing before source inspection. **V1 + V2 DONE**
5. Freeze observed pressure surface. **DONE THROUGH V2**
6. Freeze ARC3 operationalization contract. **DONE — `fac9362`**
7. Freeze exact implementation schema, metrics, matched baseline, arm matrix, and evaluation procedure. **DONE — v1 `a2745c1`; v1.1 repair `6e4dfe2` after SF-001**
8. Implement the preregistered mechanism-isolation baseline and CEA component/composition arms. **NEXT**
9. Verify implementation invariants before comparative execution.
10. Run matched development experiments and component ablations.
11. Freeze first candidate.
12. One-shot seven-game sealed evaluation.
13. Generate Kaggle notebook.
14. External 110-game competition evaluation.

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

## ARC3 operationalization contract v1

Commit `fac9362` freezes the first ARC3 operationalization contract.

It defines operational requirements and falsifiers for:

- L / CLPR;
- C / Cognitive Core;
- A / AIEC;
- X / authority substrate;
- matched non-CEA control;
- component/composition arms;
- transition, persistence, future-correction, collateral-damage, and authority-integrity measurements.

Experimental-fairness tightening: the matched control receives the same raw interaction transcript/history exposure as CEA arms. CEA must therefore earn any advantage from structured correction, persistence, adaptive allocation, and authority control rather than from privileged memory access.

V2 forces history into the first transition-relevant Core representation but does not authorize naming the hidden distinction. Competing latent explanations may remain explicitly unresolved.

## Implementation preregistration

Commit `a2745c1` froze implementation preregistration v1 before code or comparative results.

During implementation preparation, v1 was found internally incomplete: candidate generation required predicate-conditioned accumulated evidence, while the only authorized long-lived ordinary model state contained base-context counts and `H_raw` prohibited older raw events. This was recorded as `SPECIFICATION_FAILURE SF-001` at commit `3b86f8c` before any implementation result.

Commit `6e4dfe2` freezes the minimal v1.1 repair. It adds only non-reconstructive aggregate predicate-contingency counts `Q_t` to the ordinary predictive state. `H_raw` remains exactly two completed transitions plus the current observation; no raw transcript widening, semantic feature addition, threshold change, budget change, or arm change was authorized.

The operative implementation specification is therefore:

`IMPLEMENTATION_PREREGISTRATION_V1.md + IMPLEMENTATION_PREREGISTRATION_V1_1.md`.

Key frozen choices include:

- raw history bound `H_raw = 2 completed transitions + current observation`;
- no historical full-frame transcript outside the current frame;
- exact schemas for `R_t`, `M_t`, `G_t`, `Lambda_t`, and `H_t`;
- ordinary base predictive counts plus v1.1 aggregate predicate contingencies `Q_t`;
- primary transition target `z_t = 1[O_{t+1} != O_t]` with prequential binary NLL;
- bounded non-semantic hypothesis predicate language;
- localized CLPR correction operator;
- level-boundary persistence contrast;
- AIEC v1 information-allocation rule and fixed-allocation controls;
- frozen X authorization predicates;
- exact metric definitions and a 256-action development budget per game;
- arm matrix including a conventional generic-persistence control;
- typed `IMPLEMENTATION_INVALID` and `SPECIFICATION_FAILURE` handling.

## Current authority state

Earned:

- public membership/version/byte provenance for uploaded Kaggle bundle
- frozen 18/7 split
- development-only runtime isolation
- development metadata inventory
- black-box one-step interface evidence
- black-box short-sequence transition evidence
- transition-relevant observational aliasing for the visible-frame interface in at least 3 development games
- ARC3 operationalization contract v1
- implementation preregistration v1 plus admissible pre-result v1.1 repair
- requirement that first transition-relevant state representation include bounded interaction history

Authorized next:

- code implementation against the operative v1+v1.1 specification
- unit/invariant verification of that implementation
- development-only matched execution only after verification passes

Not earned:

- implementation verification result
- task-relevant consequence model
- goal/mechanic identification
- CLPR witness
- Core witness
- AIEC witness
- X witness
- CEA benchmark advantage
- composition witness
- novelty claim
- sealed-holdout result
- external 110-game result
