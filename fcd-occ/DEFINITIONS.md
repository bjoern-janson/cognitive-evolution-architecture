# FCD/OCC C0 — Definitions

## Status

```text
DEFINITIONS FOR THE FROZEN C0 CANDIDATE
PROSPECTIVE / UNVERIFIED / NONCANONICAL
```

These definitions constrain the object attacked by the accompanying protocol. They do not constitute an implementation or measurement contract.

## Reference tuple

```text
R_ref = (P, h, B, Ω_(P,h,B), S/E boundary)
```

- `P` — the declared correction, evidence, authority, and loss-authorization contract.
- `h` — the future horizon over which reachability and corrective relevance are evaluated.
- `B` — the declared resource and interaction budget.
- `Ω_(P,h,B)` — the prospective evaluator-defined universe of externally grounded challenge episodes.
- `S/E boundary` — the declared system-plus-authorized-environment boundary used to determine what can cause a challenge episode.

The reference tuple is fixed for an evaluated transition. A change to it produces a successor contract rather than a favorable reinterpretation of the same transition.

## Challenge episode

A challenge episode `ω ∈ Ω_(P,h,B)` specifies enough evaluator-level structure to determine:

- the externally grounded source or intervention opportunity;
- the authorized system/environment interaction path;
- the relevant observation opportunity;
- the scope and provenance conditions;
- the prospectively admitted outcome set `Out_P(ω)` and possible correction-relevant consequences;
- the horizon and resource accounting.

Membership in `Ω` does not imply that the incumbent can reach, recognize, adjudicate, or use the episode. It also does not imply that a particular outcome is true or that a warrant will be granted.

## Filtration predicates

All five sets contain challenge episodes, not downstream epistemic objects.

### Opportunity

```text
Opportunity(ω | P,h,B)
```

`ω` is externally grounded, protocol-authorized, and physically realizable somewhere inside the declared system/environment assemblage within the reference contract.

### Causal reachability

```text
Reachable(ω | K_t, π_t, P,h,B)
```

There exists an authorized causal interaction sequence, available to the declared assemblage within `h` and `B`, through which `ω` can be realized.

Mere API permission, a visible button, an unsolicited observation, or a hidden answer-bearing channel is not automatically causal reachability. The declared protocol must specify whether the system, a wrapper, or the environment causes the episode and whether that cause is relevant to the claim.

### Legibility

```text
Legible(ω | K_t, R_t, P,h,B)
```

The realized consequences of `ω` can enter a representation that preserves the correction-relevant distinction identified by the reference contract.

Reception without discrimination is not legibility.

### Adjudicability

```text
Adjudicable(ω | K_t, P)
```

If `ω` is realized and legible, the prospectively declared evaluation procedure can classify whether its result warrants retention, rescoping, revision, retirement, or unresolved status.

Adjudicability is a route capability. It is not a `ValidatedEvaluation`, warrant, capability, or mutation.

### Effectiveness

```text
EffectiveRoute(ω | K_t, P)
```

If `ω` realizes a warranted result, an authorized causal path exists by which that result can alter persistent future state or authority within scope.

An unused log, advisory message with no policy consequence, challenge generated and judged solely by the incumbent, or stale authority object does not automatically establish effectiveness.

## Filtration

```text
Q^opp
⊇ Q^reach_t
⊇ Q^legible_t
⊇ Q^adjudicable_t
⊇ Q^effective_t
```

This is a filtration. No meet, join, or lattice operation is claimed by C0.

## Realized epistemic chain

The prospective filtration must remain distinct from the realized authority chain:

```text
challenge opportunity
→ realized observation
→ evidence object
→ evaluation
→ warrant, rejection, or unresolved result
→ authority decision
→ attempted transition
→ persistence result
```

No arrow is an equivalence or an automatic authority promotion.

## Episode outcome

```text
o ∈ Out_P(ω)
```

is one prospectively admitted possible outcome of challenge episode `ω`. An episode is an opportunity structure; `o` identifies a possible realized result. Protocol-invalid, fabricated, or provenance-incompatible results are not silently added to `Out_P(ω)`.

## Corrective consequence

```text
WarrantedConsequence_P(x, ω, o)
```

is the evaluator-level, contract-relative consequence that would be warranted for case or state `x` if challenge episode `ω` realized admitted outcome `o` with its declared provenance.

The consequence may be:

```text
retain | rescope | revise | retire | unresolved
```

Equality of consequences is contract-relative. It is not asserted to be decidable by the incumbent.

## Corrective equivalence

```text
x ≡corr_(P,h,B) y
iff
∀ω ∈ Ω_(P,h,B), ∀o ∈ Out_P(ω):
WarrantedConsequence_P(x,ω,o)
= WarrantedConsequence_P(y,ω,o)
```

`x` and `y` are correction-distinguishable when this equality fails for at least one admitted episode.

## Corrective reachability structure

```text
R^corr_t = CorrectiveReachability(K_t, P,h,B)
```

`R^corr_t` is the typed causal route structure induced by the current filtration. It is not a set of challenge episodes and is not interchangeable with any `Q^stage_t`.

A merely hypothetical recovery route is not present in `R^corr_t`. Reacquired, replaced, or newly constructed routes enter `R^corr_(t+1)` only through an explicit candidate transition within the frozen contract.

## Distinguishing coverage

```text
Disc_(P,h,B)(R^corr)
```

is the set of correction-relevant distinctions that the typed paths in `R^corr` can expose and make available to the declared corrective process.

Two route sets may have different implementations or cardinalities while providing the same distinguishing coverage.

C0 does not freeze an estimator, representation, metric, threshold, or completeness theorem for `Disc`.

## Reopenable commitment

```text
u = (c,s,w,ℓ,χ)
```

- `c` — content whose persistent use is proposed or established.
- `s` — scope, conditions, and claim-relative applicability.
- `w` — evidence warrant and authority ceiling.
- `ℓ` — immutable, attributable transition lineage.
- `χ` — executable reopening interface.

### Reopening interface

```text
χ_u : realized admissible challenge
      ⇀ {retain,rescope,revise,retire,unresolved}
```

`χ` is partial because an invalid, irrelevant, or underdetermined challenge need not authorize a state change.

For C0, `χ` is constituted only if an independently grounded challenge can traverse an authorized causal path to a typed consequence. Merely storing instructions for possible future review is not sufficient.

## Candidate and persistent states

```text
K_t          incumbent persistent state
K~_(t+1)     proposed successor before authorized persistence
K_(t+1)      successfully persisted successor
```

```text
proposal ≠ admission ≠ authority ≠ persistence
```

## Coverage loss and gain

```text
L_t^R     routes lost by the proposed transition
G_t^R     routes gained, recovered, or constructed
L_t^auth  correction-relevant coverage whose loss is explicitly authorized
```

A route replacement supplies coverage when:

```text
Disc_(P,h,B)(L_t^R)
⊆
Disc_(P,h,B)(G_t^R).
```

Uncovered loss is not silently converted into authorized loss.

## Candidate theory roles

The following mappings are hypotheses about roles, not claims of implementation:

```text
FS       representation/interface adequacy for future correction
AIEC     budgeted acquisition of correction-relevant distinctions
CLPR     localized representational revision
CCA      causal and epistemic warrant
CARS     authority and controlled persistence
Issue #44 executable authority / lineage substrate
OCC      trajectory-level corrective-coverage condition
CEA      possible developmental organization
```

## Status terms

The following are constitution-level terminal statuses assignable only after a separately frozen finite attack suite is completed.

### `SURVIVED CONSTITUTION ATTACK`

Every instance in the frozen suite was validly completed and no counterexample was established against C0. This establishes no empirical truth or CEA promotion.

### `FAILED CONSTITUTION`

A valid minimal countertrace established inconsistency, vacuity, overconstraint, or a false survivor. A defective trace correctly rejected by C0 is not constitution failure.

### `INVALID / UNDERCONSTITUTED`

At least one load-bearing suite instance could not be prospectively constituted well enough for the suite to support either survival or failure.
