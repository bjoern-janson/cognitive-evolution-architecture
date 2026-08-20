# ARC-AGI-3 Specification Failure Ledger — v1.4 Successor

This successor preserves `SPECIFICATION_FAILURES.md` unchanged and records specification failures discovered by the pre-execution conformance audit after repository verification but before any ARC environment instantiation by the v1.x implementation.

All six failures below were discovered with:

- ARC development arm execution: **NO**;
- comparative outcome observed: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

Their minimal repairs are frozen in `IMPLEMENTATION_PREREGISTRATION_V1_4.md`.

## SF-004 — singular non-modal color id is under-defined

A 16-color frame may contain multiple colors other than the modal color, so a singular `non-modal color id` is not uniquely defined.

Repair: use deterministic `modal_color_id` (smallest id on a frequency tie) plus `non_modal_cells`. The descriptor remains non-semantic and is not added to the frozen transition-predictor context.

## SF-005 — development wall-clock budget missing

`G_t` contained `remaining_wallclock_budget`, but the development budget section froze no wall-clock value.

Repair: development v1.x uses `None`; only the 256 non-RESET action budget governs local mechanism-isolation execution. Wall-clock may not affect v1.x decisions.

## SF-006 — secondary transition heads under-specified

V1 required prequential scores for all fields of `S_t` but did not define their predictor contexts/priors precisely enough to implement without discretion.

Repair: all secondary heads use the same frozen `c_base`, unit priors, and strict prequential scoring; they are instrumentation-only. `Q_t` remains unchanged.

## SF-007 — `F_B` trigger counting ambiguous

V1 did not say whether a context that remains mixed after first meeting the aliasing trigger counts repeatedly.

Repair: count first activation only per `(game_slug, level_index, c_base)`.

## SF-008 — `forward_supported_candidates` threshold undefined

V1 used the term in `F_B` without an exact forward-support threshold.

Repair: a candidate becomes forward-supported at 4 strictly forward in-scope scored events, reusing the already frozen X support threshold and granting no additional authority.

## SF-009 — `P_persistence` pairing key undefined

V1 required comparison against the matched transient arm's parent prediction but did not define exact cross-arm event alignment.

Repair: pair only exact `(game_slug, seed, level_index, step_within_game, action_token, action_coordinate)` matches with matching outcome signature; otherwise mark `NON_EVALUABLE_PAIR`.

## Authority consequence

These failures justify only the v1.4 clarification and corresponding instrumentation repair. They do not authorize changing `H_raw`, policies, thresholds, action budgets, candidate language, CLPR behavior, or X promotion criteria.
