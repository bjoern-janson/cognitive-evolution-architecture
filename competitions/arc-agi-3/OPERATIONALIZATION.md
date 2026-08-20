# ARC-AGI-3 Operationalization Contract v1

Status: **SPECIFICATION FROZEN FOR FIRST IMPLEMENTATION**.

This document is an operationalization contract. It is not an implementation, verification result, empirical component witness, composition witness, or benchmark result.

## Empirical pressure authorizing this contract

Black-box V1 established:

- visible frame change is not an authorized synonym for progress;
- visible no-op is not an authorized synonym for uselessness.

Black-box V2 established transition-relevant observational aliasing in the development corpus. Measured trajectories include successive latent states `s0,s1` and the same action `a` for which:

`O(s0) = O(s1)` while `O(T(s0,a)) != O(T(s1,a))`.

Therefore a controller state of the form

`K_t = f(current visible frame)`

is not sufficient to predict all measured future transition behavior.

This does **not** establish task-semantic aliasing, goal structure, usefulness, or the identity of any hidden variable.

## Governing boundary

Maintain throughout implementation and evaluation:

- observational aliasing != task-semantic aliasing
- transition predictiveness != usefulness
- frame novelty != progress
- candidate distinction != semantic fact
- specification != implementation != verification result
- component witness != composition witness
- evaluation != mutation

Authority scope may not exceed discrimination scope.

---

## L — CLPR operationalization

### Requirement

The representation must be able to maintain future-transition-relevant distinctions that are not necessarily recoverable from the current visible frame alone.

At minimum, the representational state must permit access to:

`R_t ⊇ {observation history, action history, transition evidence, candidate latent distinctions}`.

History is required by V2 evidence. The implementation is not authorized to assign semantic meaning to a latent distinction merely because it predicts a visible transition.

### Candidate-hypothesis state

The implementation may maintain an unresolved hypothesis set:

`H_t = {H_1, H_2, ..., H_n}`

with scoped support, contradiction, and uncertainty rather than collapsing immediately to one hidden-state explanation.

### Legitimate localized correction

A CLPR correction is legitimate only when a candidate representational distinction is subjected to controlled discrimination and produces measurable improvement in subsequent transition prediction, with bounded collateral degradation on unrelated predictions or behaviors.

Operational chain:

`candidate distinction -> controlled intervention -> predictive improvement -> scoped retention`.

### Primary falsifier

`H0,L: localized representation corrections do not improve prediction of subsequent transitions relative to matched nonlocalized representations.`

A score gain alone does not satisfy the CLPR witness criterion.

---

## C — Cognitive Core operationalization

### Requirement

The Core must maintain interaction state across time and explicitly separate epistemic stages.

Minimum persistent state schema:

`K_t = (R_t, M_t, G_t, Lambda_t)`

where the implementation must define each term before evaluation and must not silently merge evidence with authorized state.

The update cycle must preserve the distinction:

`observation -> hypothesis -> prediction -> action -> consequence -> correction`.

A correction must be capable of changing future prediction or action behavior. Logging without changed future weighting is not a correction witness.

### Persistence comparison

Primary controlled comparison:

`C_persistent` versus `C_transient`.

The persistent arm may retain validated corrective state across the authorized interaction horizon. The transient arm receives matched raw observations/history/exposure but cannot carry the structured corrective state across the matched boundary.

### Primary falsifier

`H0,C: persistent corrective state provides no measurable improvement in later states or levels after controlling for model, compute, interaction budget, and raw exposure.`

Persistence itself is not evidence; benefit must be measured longitudinally.

---

## A — AIEC operationalization

### Requirement

AIEC allocates scarce interaction budget between information acquisition and current-plan execution.

It must not receive privileged labels declaring an action "exploratory", "useful", "goal-directed", or "informative".

Candidate decision objective:

`a* = argmax_a E[Delta U_future | a, K_t] / C(a)`.

`Delta U_future` must be operationally defined before comparative evaluation. It cannot default to visible-frame novelty because V1 rejected `Delta O != 0 => progress` as an authorized identity.

### Primary control

Compare adaptive allocation against matched fixed allocation policies under identical model, compute, action budget, and environment exposure.

### Primary falsifier

`H0,A: adaptive allocation <= matched fixed allocation`.

AIEC is not licensed merely because it explores more or produces more frame changes.

---

## X — authority substrate operationalization

### Requirement

X governs promotion from tentative evidence into persistent canonical state.

Required promotion chain:

`observation -> candidate rule -> discriminating evidence -> scoped warrant -> authorization -> persistent state`.

The implementation must preserve at least the following non-promotions:

- one unexplained no-op does not authorize `action useless`;
- one successful transition does not authorize a global action rule;
- one transition-predictive distinction does not authorize task-semantic meaning;
- component-local evidence does not authorize composition-level claims.

### Primary X hypothesis

The X hypothesis is not simply "X improves score".

`H_X: X reduces unsupported generalization entering persistent canonical state without collapsing useful learning.`

### Required integrity metrics

Measure separately:

- `U_unauthorized`: unauthorized-persistence rate;
- `F_refusal`: false-refusal rate for claims that satisfy the frozen authorization criteria.

Targeting only `U_unauthorized = 0` is insufficient because a system that never authorizes anything trivially satisfies that condition.

---

## Matched non-CEA control

Primary control: `B_reactive`.

The control must receive the same environment observations, same action interface, same model capacity, same compute budget, same interaction budget, and the same raw interaction transcript/history exposure as the CEA arms.

The control is prohibited from using the mechanisms under test:

- no structured persistent corrective state;
- no CLPR-specific localized correction operator;
- no adaptive AIEC explore/exploit controller;
- no authority-gated promotion into persistent canonical state.

The raw-history matching rule is deliberate: CEA must not win merely because it can remember observations that the control was denied. The experiment is intended to test structured correction, persistence, adaptive allocation, and authority control—not memory access alone.

If a later implementation requires a narrower or wider baseline to isolate a factor cleanly, that change must be preregistered before observing its comparative result.

---

## Component and composition arms

Minimum planned arms are:

- `B` — matched non-CEA control;
- `B+L`;
- `B+C`;
- `B+A`;
- `B+X` where a governance-only comparison is technically meaningful;
- `B+L+C`;
- `B+L+A`;
- `B+C+A`;
- `B+L+C+A`;
- `B+L+C+A+X`.

Additional factorial arms may be added only if needed to estimate interactions cleanly. Adding an arm does not authorize changing the frozen definition of a factor after results are observed.

X is conceptually orthogonal to the capability mechanisms but may participate as a governance factor where the implementation allows matched comparison.

---

## Primary scientific quantities

Official benchmark score is necessary but insufficient.

Record at minimum:

`M = (RHAE, A_actions, T_transition, P_persistence, F_B, D_collateral, U_unauthorized, F_refusal)`.

### `RHAE`

Official ARC-AGI-3 benchmark outcome under the competition's operative scoring implementation.

### `A_actions`

Interaction/action cost. Report raw actions and any benchmark-normalized efficiency quantity used in external evaluation.

### `T_transition`

Transition-model quality: ability to predict `P(O_{t+1} | K_t, a_t)` or the frozen operational equivalent. Compare before/after correction and against matched controls.

### `P_persistence`

Longitudinal effect of validated corrective state on subsequent states/levels under matched exposure.

### `F_B`

Future correction capacity. The implementation must define a measurable estimator before evaluation. The intended question is whether the post-correction state improves the system's ability to detect, localize, discriminate, or repair later failures:

`F_B(K_{t+1}) > F_B(K_t)`.

No increase may be claimed without a preregistered estimator and held-out or forward evidence.

### `D_collateral`

Collateral degradation: change in predictions or behavior outside the scope of the corrected assumption. Local correction is preferred over unnecessary global damage.

### `U_unauthorized`

Rate at which unsupported claims enter persistent canonical state under the frozen X authorization rules.

### `F_refusal`

Rate at which X refuses promotion of claims that satisfy the frozen authorization criteria.

---

## Full CEA composition hypothesis

Primary narrow hypothesis:

`H_CEA: L+C+A+X produces greater long-horizon competence acquisition than matched controls under identical model, compute, interaction budget, and environment exposure.`

A composition claim requires more than a score difference.

Minimum evidence package:

- main-effect accounting;
- interaction evidence;
- longitudinal persistence;
- held-out generalization;
- preservation of authority integrity.

A positive `tau_LCAX` is necessary for a synergy claim under the chosen factorial estimator, but is not sufficient by itself for a composition witness.

Component evidence remains component-local unless and until composition is independently discriminated.

---

## Implementation consequences forced by V2

### History is mandatory in the first Core state

Because V2 observed `O(s0) = O(s1)` with different measured future transition behavior under the same repeated action, the first implementation cannot use current visible frame alone as its complete transition-relevant state.

The implementation must therefore retain enough interaction history to distinguish at least some observationally aliased trajectories.

This requirement is empirical, not semantic: it does not identify what the hidden distinction is.

### Uncertainty over latent explanations is permitted and preferred to premature collapse

The implementation may maintain competing latent explanations in `H_t` and update their weights through discriminating interaction. It must not rename an unobserved variable as a mechanic merely because that naming is convenient.

---

## First implementation gate

Before comparative experiments begin, freeze:

1. exact state schema for `R_t, M_t, G_t, Lambda_t`;
2. candidate-hypothesis representation `H_t`;
3. transition-prediction target and loss/score;
4. CLPR localization and correction operator;
5. persistence boundary for `C_persistent` and `C_transient`;
6. AIEC allocation rule and fixed-allocation controls;
7. X authorization predicates;
8. estimator definitions for `T_transition, P_persistence, F_B, D_collateral, U_unauthorized, F_refusal`;
9. matched compute/model/action/exposure budgets;
10. arm matrix and randomization/evaluation procedure.

Only after those are frozen may implementation results be interpreted against this contract.

## Current authority state

Authorized now:

- implementation of a history-bearing, uncertainty-preserving first ARC3 state representation;
- implementation of matched non-CEA and component arms under this contract;
- preregistration of metrics and ablation procedure.

Still not earned:

- task-goal identification;
- hidden-mechanic identification;
- CLPR witness;
- Core witness;
- AIEC witness;
- X witness;
- CEA composition witness;
- CEA advantage;
- novelty claim;
- sealed-holdout result;
- external 110-game result.
