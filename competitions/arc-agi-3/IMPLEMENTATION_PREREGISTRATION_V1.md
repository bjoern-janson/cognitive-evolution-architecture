# ARC-AGI-3 Implementation Preregistration v1

Status: **FROZEN BEFORE FIRST IMPLEMENTATION**.

This document freezes the first mechanism-isolation implementation. It is a specification, not code, verification, an empirical result, a component witness, a composition witness, or a benchmark result.

If an item below proves infeasible, the failure must be recorded as a typed implementation/specification failure and a new preregistration version must be created before altered results are observed. Implementation convenience does not silently modify this document.

## Empirical basis

The specification is constrained by black-box V1 and V2 only.

V1 established that visible frame change is not an authorized synonym for progress and visible no-op is not an authorized synonym for uselessness.

V2 established transition-relevant observational aliasing: measured trajectories include `O(s0) = O(s1)` while the same action has different observed future transition behavior. V2 also measured two-step context effects and coordinate dependence for ACTION6 in a subset of development games.

Therefore the first implementation must use bounded interaction history, but V2 does not authorize an unbounded transcript, a hidden-mechanic label, a task-goal label, or a semantic interpretation of any latent distinction.

---

# 0. Shared bounded-history rule

All arms receive the same raw interface exposure.

The raw historical window is frozen as:

`H_raw = 2 completed transitions + current observation`.

The current observation may retain the full current 64x64 visible frame and current interface fields. For each of the previous two completed transitions, the raw window may retain only the typed transition record defined below; it may not retain the full prior frame payload.

A transition record is:

`e_i = (action_token, action_coordinate_or_null, pre_frame_hash, post_frame_hash, z_change, changed_cell_count, changed_count_bucket, state_before, state_after, level_before, level_after, available_action_mask_before, available_action_mask_after, exact_return_flag)`.

`z_change = 1` iff the visible frame after the action differs from the visible frame before the action.

`changed_count_bucket` uses the frozen bins:

- `0`
- `1`
- `2..4`
- `5..16`
- `17..64`
- `65..256`
- `>256`.

`exact_return_flag = 1` iff the post-action frame hash equals either of the frame hashes represented in the bounded raw window before the action.

At a level transition, the raw transition window is cleared. At a game transition, all game-local state is cleared.

No arm may keep older raw observations or raw transition events outside the structures explicitly authorized below.

Rationale: two completed transitions are the smallest bounded raw window that can directly represent all two-step dependencies measured by V2. If this bound proves inadequate, that is an empirical/specification result; it is not permission to enlarge the buffer mid-run.

---

# 1. Exact representational state `R_t`

For every arm, the shared representational substrate is:

`R_t^base = (O_t, phi_t, W_t)`.

Where:

- `O_t` is the current interface-visible observation: current 64x64 frame, environment state, levels completed, and currently available actions.
- `phi_t` is a deterministic non-semantic descriptor of `O_t` containing: frame SHA-256, 16-value color histogram, non-modal color id, count of non-modal cells, and available-action bitmask.
- `W_t` is the ordered `H_raw = 2` transition-record window.

The baseline receives all of `R_t^base`.

For arms containing L, the representational state additionally contains:

`D_t = {d_1, ..., d_k}`

where each `d_j` is a live transition-predictive candidate distinction drawn from the frozen predicate language in section 5. `D_t` contains no semantic mechanic or goal labels.

Thus:

`R_t^L = (R_t^base, D_t)`.

No representation may infer a semantic label solely from predictive success.

---

# 2. Persistent memory schema `M_t`

The first implementation separates ordinary model state shared by all arms from CEA corrective memory.

## 2.1 Shared ordinary predictive state

All arms may maintain the same conventional online transition-statistics state `Theta_t` within a level. `Theta_t` is not counted as C-specific memory and is identically available across arms.

`Theta_t` consists of Beta-Bernoulli counts for `z_change` and Dirichlet counts for `changed_count_bucket`, indexed by the frozen base context:

`c_base = (current_action_token, ACTION6_coordinate_bin_or_null, previous_action_token_or_START, previous_z_change_or_START, available_action_mask)`.

ACTION6 coordinates are quantized into an 8x8 grid over the 64x64 frame; non-ACTION6 actions use `null`.

All count tables use unit symmetric priors.

`Theta_t` is reset at every level transition for all primary mechanism-isolation arms. A separate strong conventional-persistence control is defined in section 13.

## 2.2 CEA corrective memory

For arms containing C, `M_t` is a bounded canonical correction ledger with at most 64 entries per game.

Each canonical entry is:

`m_j = (claim_id, scope_predicate, local_predictive_delta, evidence_ids, authorization_id, created_level, created_step, last_verified_level, status)`.

`status` is one of `AUTHORIZED`, `SUSPENDED`, `REVOKED`.

`M_t` persists across level transitions within the same game only. It is cleared before a different game slug is entered.

No silent eviction is permitted. If 64 canonical entries are already present, further otherwise-eligible promotions are refused with reason `CAPACITY_REFUSAL`; that event is logged for `F_refusal` analysis.

Arms without C do not persist canonical correction entries across the level boundary.

---

# 3. Goal / constraint state `G_t`

V1/V2 did not identify task semantics. Therefore `G_t` v1 is deliberately restricted to direct interface constraints and externally explicit benchmark progress signals:

`G_t = (environment_state, levels_completed, live_action_mask, remaining_action_budget, remaining_wallclock_budget)`.

The implementation may use an observed positive `levels_completed` delta or transition to `WIN` as an explicit success event because those are interface-provided benchmark signals.

It may not place an inferred visual pattern, object, location, action, or transition into canonical goal state unless a later preregistration explicitly authorizes a discrimination test for that claim.

Candidate goal explanations, if generated, must remain provisional members of `H_t` and have no privileged control authority in v1.

---

# 4. Lineage / provenance state `Lambda_t`

`Lambda_t` is append-only game-local provenance metadata. It stores hashes and typed summaries, not historical full frames.

Every evidence event receives an immutable `evidence_id` and records:

`(game_slug, level_index, interaction_step, current_frame_hash, raw_window_hash, action, result_signature)`.

Every hypothesis receives a `claim_id` and records:

`(parent_claim_or_null, creation_evidence_ids, predicate, scope, current_status)`.

Every correction and authorization decision records:

`(decision_id, claim_id, evidence_ids_considered, frozen_metric_values, decision, reason_code)`.

A canonical memory entry without a complete lineage chain is invalid and counts as unauthorized persistence if it enters `M_t`.

---

# 5. Live hypothesis set `H_t`

`H_t` contains at most 32 provisional transition-predictive hypotheses per game.

A hypothesis has the frozen form:

`H_j = (claim_id, parent_context, extra_predicate, scope, provisional_counts, forward_eval_counts, status)`.

Allowed `extra_predicate` primitives are restricted to the bounded non-semantic history/interface language:

1. previous action token;
2. previous `z_change`;
3. second-previous action token;
4. second-previous `z_change`;
5. previous ACTION6 coordinate bin;
6. second-previous ACTION6 coordinate bin;
7. whether current frame hash equals the immediately preceding post-frame hash;
8. current available-action mask.

No object names, inferred mechanics, inferred goals, manual game labels, source-derived features, or game-specific hand-authored predicates are permitted.

## 5.1 Candidate generation trigger

A candidate may be generated only after the ordinary base predictor has observed an aliasing/residual condition within the current game:

- the same frozen base context has produced both `z_change=0` and `z_change=1`; and
- at least four total observations exist for that base context, with at least one observation of each class.

When triggered, the implementation evaluates each allowed extra predicate that is defined for the stored evidence and creates provisional candidates for predicates that divide the accumulated evidence into at least two non-empty subsets.

Candidate generation may use accumulated within-level evidence for proposal only. Evidence used to create the proposal may not count toward X authorization; authorization uses strictly later forward evidence.

If more than 32 provisional candidates would exist, retain the 32 with highest in-sample binary log-loss reduction versus the parent context. This ranking is proposal management only and grants no authority.

---

# 6. Transition target `T`

## 6.1 Primary target

The primary transition-prediction target for L/C mechanism claims is:

`z_t = 1[O_{t+1} != O_t]`.

Predictions are probabilistic. Primary loss is binary negative log-likelihood with probabilities clipped to `[1e-6, 1-1e-6]`.

This target is selected because V2 directly discriminated observational aliasing using the visible-change/no-change effect class. It is not interpreted as progress or utility.

## 6.2 Secondary signature

The secondary transition signature is:

`S_t = (z_change, changed_count_bucket, state_delta_class, level_delta_positive, action_surface_changed, exact_return_flag)`.

Where:

- `state_delta_class` is `SAME`, `WIN`, or `GAME_OVER` relative to the pre-action state;
- `level_delta_positive` is a Boolean;
- `action_surface_changed` is a Boolean.

Secondary heads are evaluated separately; they are not combined into a semantic reward.

## 6.3 Prequential evaluation

Every prediction must be emitted before the corresponding action result is observed. Update occurs only after scoring that prediction.

`T_transition` is reported as prequential primary NLL plus the per-field secondary predictive scores. No post-hoc refit on the scored event is allowed.

---

# 7. CLPR correction operator `Delta_L`

`Delta_L` is a localized predictive correction, not a semantic reinterpretation.

For a provisional hypothesis `H_j`, the operator constructs a local Beta-Bernoulli predictor for `z_change` scoped by `parent_context AND extra_predicate` and compares it against the frozen parent/base predictor.

The local correction value is the difference in posterior predictive log-odds between local and parent predictors, clipped to `[-4, +4]`.

While provisional, the correction may be used only in the L arm's transition prediction for the exact registered scope. It may not alter unrelated contexts.

A correction is eligible for canonical persistence only through `Gamma_X` in section 10.

Primary L falsifier remains:

`localized corrections fail to improve forward prequential transition NLL relative to the matched nonlocalized parent predictor`.

---

# 8. Canonical persistence boundary `Pi_C`

The canonical persistence boundary is the ARC level boundary.

For `C_persistent`:

- `W_t` clears at level change;
- ordinary `Theta_t` resets at level change;
- provisional `H_t` clears at level change;
- only `AUTHORIZED` entries in `M_t`, together with their `Lambda_t` lineage, persist into the next level of the same game.

For `C_transient`:

- `W_t`, `Theta_t`, provisional `H_t`, and all correction entries clear at level change.

For both arms, every structure clears at game change.

This makes the persistence contrast specifically about validated corrective state rather than raw transcript carryover or generic model carryover.

A separate conventional-persistence control is included to test whether generic persistence alone explains any observed benefit.

---

# 9. AIEC allocation rule `pi_A`

V1/V2 provide no authorized task-utility model. Therefore AIEC v1 is an information-allocation mechanism, not a claim of task-optimal exploration/exploitation.

At every decision, two shared candidate policies are available:

- `P_exec`: deterministic legal-action cycling policy over the current live action set; ACTION6 uses the frozen coordinate schedule below.
- `P_info`: choose the legal action with maximum posterior predictive entropy for primary target `z_change`; ties break deterministically by action id then coordinate order.

ACTION6 coordinate schedule is fixed and game-agnostic: 8x8 bin centers in row-major order, restricted to legal frame coordinates.

`pi_A` chooses `P_info` iff the mean primary predictive entropy over currently legal candidate actions exceeds `0.55` nats; otherwise it chooses `P_exec`.

The fixed-allocation controls use the same `P_info` and `P_exec` implementations with frozen schedules:

- `A_fixed_0`: 0% information-policy selections;
- `A_fixed_25`: every fourth decision uses `P_info`;
- `A_fixed_50`: alternating `P_exec`, `P_info`;
- `A_fixed_75`: every fourth decision uses `P_exec`;
- `A_fixed_100`: 100% information-policy selections.

The AIEC v1 primary outcome is future transition-prediction quality per action, not frame novelty and not task progress.

No AIEC task-performance witness may be claimed from v1 unless direct benchmark progress events occur and the frozen analysis supports that stronger statement.

---

# 10. Issue #44 authorization predicates `Gamma_X`

A provisional correction may enter canonical `M_t` only if all predicates below are satisfied using strictly forward evidence collected after proposal creation.

For claim `H_j`:

1. **Scope predicate exists and is non-empty.**
2. **Forward support:** at least 4 forward scored events fall inside the candidate scope.
3. **Forward discrimination:** both the local candidate and parent predictor emitted prequential probabilities for every scored support event.
4. **Predictive gain:** cumulative forward primary NLL improvement of local over parent is at least `2.0` nats.
5. **Non-singleton gain:** no single forward event contributes more than 75% of the cumulative NLL improvement.
6. **Collateral check:** at least 4 forward events have been scored in the sibling/parent context outside the candidate scope; applying the candidate correction outside its declared scope is prohibited, therefore collateral predictive change outside scope must be exactly zero by construction.
7. **Lineage completeness:** all proposal and forward evidence ids are present in `Lambda_t`.
8. **No semantic promotion:** the canonical claim text remains a transition-predictive scoped predicate; no mechanic/goal/usefulness label is attached.
9. **Capacity available:** fewer than 64 canonical entries exist.

If all predicates hold, X authorizes promotion. Otherwise the candidate remains provisional or expires at the next level boundary.

`Gamma_X` uses no benchmark score, frame-novelty reward, hand-authored game knowledge, or source information.

## 10.1 Unauthorized-persistence definition

For v1, an entry is `unauthorized` if it appears in canonical `M_t` without satisfying all frozen predicates at its promotion step, or if its stored scope/evidence/claim differs from the authorized object.

`U_unauthorized = unauthorized_promotions / max(1, total_promotions)`.

## 10.2 False-refusal definition

A `false refusal` occurs when all frozen predicates are satisfied for a provisional claim at a decision point but X does not authorize it for a reason other than explicit capacity exhaustion.

Capacity refusals are reported separately and also included in a second conservative refusal rate.

`F_refusal_strict = false_refusals / max(1, eligible_promotion_events)`.

`F_refusal_including_capacity` additionally counts `CAPACITY_REFUSAL`.

---

# 11. Frozen metric definitions

## 11.1 `T_transition`

Primary: mean prequential binary NLL for `z_change`, reported overall, per game, per level, and before/after each localized correction.

Secondary: mean prequential loss for each component of `S_t`.

Lower is better.

## 11.2 `P_persistence`

For every canonical correction promoted in level `l`, compare its forward primary NLL contribution in the next level in which its registered scope is encountered against the matched transient arm's parent prediction.

Report:

- number of corrections with a subsequent evaluable scope encounter;
- mean paired NLL difference;
- median paired NLL difference;
- fraction with improvement.

No persistence effect is claimed for corrections never re-encountered.

## 11.3 `F_B` — future correction capacity

`F_B` v1 is the rate of successful localization on later independent residual events.

For each level, define:

`localization_yield = authorized_or_forward_supported_candidates / max(1, aliasing_residual_triggers)`.

Compare this rate in later levels after persistent corrections against the transient matched arm, together with the forward NLL of those later corrections.

An increase in count alone is insufficient; later localized candidates must also improve forward predictive loss.

## 11.4 `D_collateral`

Because v1 local corrections are scope-gated, direct predictive collateral is measured as any difference in emitted transition probabilities outside the correction's registered scope compared with its parent arm.

Expected value under a correct implementation is exactly zero.

Any non-zero outside-scope difference is a localization violation and is recorded separately as an implementation defect before being interpreted scientifically.

## 11.5 `U_unauthorized` and `F_refusal`

Defined in section 10.

## 11.6 `A_actions`

Record every non-RESET action issued, per game and per level, plus actions until any observed level completion or terminal state.

## 11.7 Benchmark outcome

Record observed level completions, terminal state, and the operative ARC/Kaggle score when available. Benchmark outcome is secondary for mechanism-isolation v1 and cannot replace component-specific metrics.

---

# 12. Budgets

## 12.1 Development action budget

For mechanism-isolation v1, each arm receives a maximum of **256 non-RESET actions per development game**.

The budget is shared across levels encountered within that game. If the environment terminates earlier, the run stops.

RESET actions used only to initialize a game do not count; any deliberate RESET after initialization does count as one action-equivalent and must be logged.

## 12.2 Model/update budget

All arms use the same count-based predictive substrate and the same unit-prior updates. No arm may use external models, pretrained game knowledge, internet access, or source inspection.

Candidate enumeration is restricted to the eight frozen predicate primitives and 32 provisional-candidate cap.

Canonical memory is capped at 64 entries.

## 12.3 Randomness

Primary runs are deterministic with seed `0`. Where the official environment itself exposes stochasticity despite the seed, repeat seeds `0,1,2,3,4` for all compared arms. The need for the five-seed extension must be decided from observed reset nondeterminism, not comparative arm outcomes.

---

# 13. Frozen arms

Minimum v1 arms:

1. `B` — shared bounded history + ordinary within-level `Theta_t`; no L, C, A, or X.
2. `B_PERSIST` — conventional control: identical to B except ordinary `Theta_t` persists across levels of the same game; no localized correction, hypothesis ledger, AIEC, or authority gate.
3. `B+L`.
4. `B+C`.
5. `B+A`.
6. `B+X` only as an integrity plumbing control; without candidate corrections it is not interpreted as an X capability test.
7. `B+L+C`.
8. `B+L+A`.
9. `B+C+A`.
10. `B+L+C+A`.
11. `B+L+C+A+X`.

For arms without X, any correction used beyond the provisional level is promoted by a deliberately permissive control rule once it has four forward in-scope observations, regardless of predictive gain. This supplies a governance contrast and is logged explicitly as `UNGATED_PROMOTION`; it is not called authorized state.

For arms without A, action selection uses `P_exec` unless the arm is one of the fixed-allocation A controls.

Additional fixed-allocation controls `A_fixed_0/25/50/75/100` are run against the A arm under otherwise matched factors when estimating the A main effect.

The primary C contrast is `B+L+C` versus `B+L` and is cross-checked against `B_PERSIST` to distinguish structured corrective persistence from generic transition-statistics persistence.

The primary X contrast is `B+L+C+A+X` versus `B+L+C+A` with the permissive promotion control.

---

# 14. Evaluation procedure

1. Use only the 18 DEVELOPMENT games. The 7 SEALED_HOLDOUT games remain physically absent.
2. Do not inspect development source files. Environment source may be executed only by the official local wrapper.
3. Run games in lexicographic slug order for bookkeeping, but instantiate independent fresh game-local agent state for every arm/game pair.
4. Every compared arm receives identical seed, action budget, raw interface fields, `H_raw`, and deterministic tie-breaking rules.
5. Predictions are scored prequentially before model updates.
6. Store complete typed event/provenance logs; do not store historical full-frame payloads beyond the current frame and the hashes/summaries authorized in `H_raw`.
7. Compute component metrics only from their preregistered contrasts.
8. Do not modify thresholds, history depth, candidate language, budgets, or metric definitions after seeing comparative outcomes.
9. Any implementation bug that violates the specification is typed `IMPLEMENTATION_INVALID`; fix it in a new commit and rerun all affected arms from scratch.
10. Any specification that cannot be implemented without changing its meaning is typed `SPECIFICATION_FAILURE`; create v2 before execution under altered rules.

## 14.1 Development interpretation boundary

Positive development differences may authorize further testing but do not establish held-out generalization, a component witness, or composition witness.

No sealed game may be touched until a candidate configuration and its complete code/configuration hash are frozen for one-shot holdout evaluation.

---

# 15. First implementation deliverables

Implementation is complete only when the repository contains:

- typed state dataclasses for `R_t, M_t, G_t, Lambda_t, H_t`;
- bounded-history enforcement tests;
- transition-signature extraction tests;
- deterministic base predictor;
- CLPR candidate generator and local correction operator;
- persistent/transient boundary implementation;
- AIEC and fixed-allocation policies;
- X authorization evaluator;
- event/provenance logger;
- arm configuration matrix;
- development runner enforcing the 18-game corpus firewall;
- metric reducer implementing this document exactly;
- unit tests demonstrating that sealed slugs cannot be requested through the development runner.

No benchmark or component result is interpreted until these implementation-level checks pass.

# 16. Authority state after freeze

Authorized after this document is frozen:

- implementation against the exact v1 schema;
- unit/invariant verification;
- development-only matched arm execution after implementation verification passes.

Still not earned:

- task-goal identification;
- hidden-mechanic identification;
- CLPR witness;
- Core witness;
- AIEC task-performance witness;
- X witness;
- composition witness;
- CEA benchmark advantage;
- sealed-holdout result;
- external 110-game result.
