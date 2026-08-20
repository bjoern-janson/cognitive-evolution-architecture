# ARC-AGI-3 Black-Box Probe V2 — Preregistered Measurement Protocol

Status: preregistered before execution.

Purpose: discriminate interface-visible transition structure in the 18 DEVELOPMENT games without promoting any pattern into a goal, mechanic, usefulness judgment, persistent rule, or CEA mechanism.

## Firewall

- Runtime must contain exactly the 18 DEVELOPMENT slugs.
- The 7 SEALED_HOLDOUT slugs must be physically absent.
- Development `*.py` source text may be executed by the official local wrapper but must not be inspected, parsed, searched, displayed, summarized, or supplied as information.
- Seed is fixed to `0`.
- Every planned sequence starts from a fresh environment instance/reset state.

## Raw observables only

At each step record:

- frame SHA-256
- frame shape
- state
- levels completed
- available actions
- selected action and action data
- changed-cell count from immediately prior frame
- changed-cell bounding box
- exact equality to initial frame
- exact equality to immediately prior frame

No raw record field may label a transition as `goal`, `mechanic`, `useful`, `progress`, or `rule`.

## Deterministic probe families

### A. Simple-action repetition

For each initially available simple action in `{1,2,3,4,5,7}` execute:

`[a,a,a]`

stopping only if the environment terminates or `a` is no longer available.

### B. Ordered simple-action composition

For every ordered pair `(a,b)` of initially available simple actions in `{1,2,3,4,5,7}`, execute:

`[a,b]`

This includes `a=b` even though Family A also repeats actions; duplicated measurements are retained as reproducibility checks rather than deduplicated post hoc.

### C. ACTION6 spatial sampling

If ACTION6 is initially available, construct a deterministic coordinate set from the initial 64x64 visible frame:

1. 5x5 fixed lattice with x,y in `{0,16,32,47,63}`.
2. Centroid of each 4-neighbor connected non-modal component, ordered by decreasing component size then `(y,x)`, capped at 12 components.
3. Deduplicate identical coordinates.

For every coordinate `p`, execute `[click(p), click(p)]` from a fresh reset.

### D. Simple-action -> ACTION6 composition

If ACTION6 and simple actions are initially available, use the same coordinate set as Family C. For every simple action `a` and every coordinate `p`, execute:

`[a, click(p)]`

### E. ACTION6 -> simple-action composition

If ACTION6 and simple actions are initially available, for every coordinate `p` and every simple action `a`, execute:

`[click(p), a]`

## Discrimination summaries permitted after execution

Derived summaries may report only structural relations supported by exact observations, including:

- immediate visible effect vs initial no visible effect
- later visible effect after an earlier no-op
- same action producing different transition signatures in different predecessor states
- coordinate-dependent transition signatures for ACTION6
- exact return to a previously observed frame
- action-surface changes
- level/state transitions

These are measurement classifications, not task interpretations.

## Explicitly forbidden V2 promotions

V2 does not authorize definitions or claims about:

- goals
- mechanics
- usefulness/reward
- persistent rules
- CLPR
- Cognitive Core
- AIEC
- Issue #44 / X
- CEA composition
- CEA advantage

The next architectural step remains blocked until V2 evidence is frozen and reviewed.
