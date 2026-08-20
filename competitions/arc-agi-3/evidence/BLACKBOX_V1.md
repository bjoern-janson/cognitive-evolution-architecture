# ARC-AGI-3 Development Black-Box Probe V1

Status: **empirical development-interface evidence**, not CEA evidence and not a solver result.

## Boundary

- Runtime contained exactly the 18 DEVELOPMENT games.
- The 7 SEALED_HOLDOUT games were physically absent.
- Development game source was executed by the official local wrapper as environment runtime, but was not inspected, parsed, searched, displayed, or supplied to the probe as information.
- Probe seed: `0`.
- Each intervention was performed from a fresh reset state.

## Probe

For each development game: record initial interface state; test same-seed RESET repeatability; apply each initially available simple action once from a fresh reset; for ACTION6 test the grid center and, when distinct, the centroid of the largest visible non-modal connected component.

## Results

- Games characterized: **18/18**.
- One-step interventions: **84**.
- Visible frame changes: **57/84**.
- Interface-visible no-ops: **27/84**.
- One-step level completions: **0/84**.
- Post-probe states: **all `NOT_FINISHED`**.
- Same-seed RESET initial frame repeatability: **18/18**.
- Initial visible grid shape: **64×64 for 18/18**.

## Immediate pressure surface

1. **Action availability is strongly game-local.** Initial action sets range from click-only `{6}` through keyboard-only `{1,2,3,4}` to the full `{1,2,3,4,5,6,7}`. A policy must gate on the live action surface rather than assume a fixed global action set.

2. **Frame change is not progress.** 57 interventions changed visible state, but none completed a level. This directly rejects `frame_changed => useful/progress` as a warranted reward identity.

3. **No-op does not identify uselessness.** Several games expose available actions that are inert from the initial state; three development games (`ft09`, `sb26`, `sc25`) yielded no visible change for any V1 canonical probe. This leaves preconditions, coordinate targeting, delayed effects, and multi-step dependencies open.

4. **ACTION6 is coordinate-sensitive in some games and sparse/inert in others.** The same coordinate-action identifier ranges from large visible transitions to one-cell changes to zero effect, depending on game and click point. Globalizing an ACTION6 semantic is therefore unsupported.

5. **Single-step intervention is insufficient for goal acquisition.** V1 deliberately found no level completion. The next probe must test short controlled sequences and prediction/retrodiction, not increase architecture complexity yet.

## Authority consequence

The evidence licenses only local interface claims. It does **not** establish CLPR, Cognitive Core, AIEC, Issue #44, CEA composition, novelty, or benchmark advantage.

## Next authorized probe

Run short, bounded, development-only action sequences chosen from interface-visible candidates to distinguish: immediate-effect actions, preconditioned actions, coordinate-sensitive actions, reversible actions, and delayed/multi-step effects. Preserve fresh-reset controls and do not inspect environment source.
