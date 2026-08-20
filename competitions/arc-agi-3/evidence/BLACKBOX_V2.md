# ARC-AGI-3 Development Black-Box Probe V2

Status: **empirical development-interface evidence**. This is not a solver result, goal inference, mechanic inference, usefulness/reward judgment, persistent-rule claim, or CEA witness.

## Provenance

- V2 protocol preregistered before execution: Git commit `e68e121`.
- V2 executable implementation frozen before execution: Git commit `f95bcc5`.
- Probe seed: `0`.
- Runtime contained exactly the 18 DEVELOPMENT games.
- The 7 SEALED_HOLDOUT games were physically absent.
- Development environment Python was executed only by the official local wrapper; source text was not inspected, parsed, searched, displayed, summarized, or supplied as information.
- Raw V2 JSON SHA-256: `de1662b2ec1871b359cf58447fe50d72022b8668d3938b5023b81e860a6ceeb4`.
- Frozen probe implementation SHA-256: `479733169692a2213d31c8f2f9b76de0c66a33082289543054b2c48bed10edf4`.
- Preregistered protocol SHA-256: `b8e66a12101f545cb3f9a88063cc2963e998a316840b791c8414bf00780d618e`.

## Execution totals

- Games: **18/18**.
- Fresh-reset sequences: **2,800**.
- Executed action steps: **5,658**.
- Steps with visible frame change: **3,216**.
- Steps with no visible frame change: **2,442**.
- Level-completion deltas: **0**.
- State changes away from initial `NOT_FINISHED`: **0**.
- Available-action-surface changes: **0**.
- Every sequence instance began from the same seed-0 initial frame hash as that game's V2 reference initial frame.

Sequence families:

| Family | Sequences | Steps |
|---|---:|---:|
| A — simple action repeated 3x | 58 | 174 |
| B — ordered simple-action pairs | 264 | 528 |
| C — same ACTION6 coordinate repeated | 412 | 824 |
| D — simple action then ACTION6 | 1,033 | 2,066 |
| E — ACTION6 then simple action | 1,033 | 2,066 |

## Discrimination 1 — visible frame equality does not imply transition-state equality

V2 contains **11 repeated-identical-action cases across 3 development games** where:

1. the first action produces zero visible changed cells and the resulting frame is exactly equal to the initial frame; and
2. applying the identical action again from that observationally identical frame produces a visible change.

Observed cases:

- `g50t`: ACTION1 `0 -> 1` changed cells; ACTION3 `0 -> 1`; ACTION5 `0 -> 1`.
- `sc25`: ACTION1 `0 -> 8`; ACTION2 `0 -> 8`; ACTION3 `0 -> 32`; ACTION4 `0 -> 16`; ACTION6 at `(32,47)` `0 -> 9`; ACTION6 at `(32,63)` `0 -> 9`; ACTION6 at `(30,55)` `0 -> 9`.
- `wa30`: ACTION5 `0 -> 1`.

Thus, for these measured trajectories, there exist successive latent environment states `s0,s1` and the same action `a` such that:

`O(s0) = O(s1)` while `O(T(s0,a)) != O(T(s1,a))`.

This establishes **transition-relevant observational aliasing** for the visible frame interface. It does not establish that the aliased latent distinction is task-relevant, goal-relevant, or useful.

## Discrimination 2 — sampled ACTION6 transition signatures can depend on coordinate

ACTION6 was initially available in **13/18** development games. Under the preregistered 5x5 lattice plus up-to-12 interface-derived component-centroid points:

- **6/13** games produced more than one distinct first-step post-click frame hash across sampled coordinates: `bp35`, `cd82`, `r11l`, `sb26`, `su15`, `vc33`.
- **7/13** did not produce sampled first-step coordinate variation under V2: `ar25`, `ft09`, `ka59`, `s5i5`, `sc25`, `sk48`, `sp80`.

The second statement is only a failure to discriminate coordinate dependence under the sampled points; it is not evidence of global coordinate-insensitivity.

## Discrimination 3 — exact return transitions exist

V2 observed **10 sequences across 2 games** where a changed frame returned exactly to the initial frame on a later action:

- `sb26`: 4 repeated-ACTION6 sequences returned exactly to the initial frame on the second identical click.
- `sk48`: 6 ordered simple-action pairs returned exactly to the initial frame.

This is an exact frame-level return relation only; no semantic label is attached to it.

## Discrimination 4 — transition effect class is context-dependent

Comparing the same action's initial visible-change/no-change class with its class when executed second in a preregistered two-step sequence:

- simple-action effect class differed in at least one measured predecessor context in **8 games**: `ar25`, `bp35`, `cd82`, `g50t`, `sc25`, `sk48`, `su15`, `wa30`;
- ACTION6 effect class at a fixed sampled coordinate differed after a simple predecessor in **4 games**: `bp35`, `cd82`, `ka59`, `sc25`.

A stricter subset holds the visible predecessor frame fixed: **154 two-step contexts across `g50t`, `sc25`, and `wa30`** had a first step with zero visible change, followed by a second action whose visible-change/no-change class differed from that same action applied directly from the initial state. The 11 repeated-identical-action cases above are the simplest witnesses.

## What V2 does not discriminate

V2 observed no level-completion delta, no terminal-state transition, and no available-action-surface change. Therefore V2 does not identify:

- task goal structure;
- task-relevant consequence;
- which transition signatures are beneficial or harmful;
- persistence of any candidate rule across levels;
- whether any observed latent distinction is necessary for task success.

## Authority consequence

V2 licenses a stronger interface statement than V1:

`visible frame equality != transition-state identity`.

It still does **not** license CLPR, Cognitive Core, AIEC, Issue #44/X, CEA composition, or CEA advantage. Architectural operationalization remains blocked until this measurement object is frozen and the minimal requirements are derived without smuggling task semantics into the evidence.
