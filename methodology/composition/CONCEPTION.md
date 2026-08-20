# Composition Evidence — Conception

## Core Rule

> **A composition is a hypothesis about interaction, not a certificate of its components or of itself.**

The current evidential hierarchy is:

```text
Component hypothesis
→ Component experiment
→ Component witness
→ Composition hypothesis
→ Composition experiment
→ Composition witness
```

No inference leap is permitted between those stages.

## Non-Implication

Let `H_i` be independently tested component hypotheses. Even if each survives:

```text
∧_i Witness(H_i)
```

the architecture-level claim remains unestablished:

```text
∧_i Witness(H_i)
↛
Witness(Compose(H_1, ..., H_n))
```

The reason is structural: a composition introduces new interaction claims that were absent from the component experiments.

## Decomposition Is Not Explanation

CEA currently uses AIEC, CLPR, the Cognitive Core, and Issue #44 as useful hypothesis slots. Their clarity as a decomposition is not evidence that they are the natural, unique, or necessary factors of intelligence.

```text
useful decomposition ≠ necessary mechanism
```

A layer may remain useful for experimentation even if later evidence shows that another factorization explains the same behavior more directly.

The promotion rule is strict:

> **No existing layer is promoted from useful decomposition to necessary mechanism without an ablation.**

The ablation must be capable of removing, disabling, replacing, or breaking the proposed mechanism while preserving relevant alternative explanations strongly enough to test whether the mechanism is causally load-bearing.

## What a Composition Experiment Must Distinguish

A positive composition result is not sufficient if it can be explained by independent or additive component gains.

The eventual CEA composition experiment should distinguish at least:

```text
independent component gains
≠ additive gains
≠ interaction / synergy
≠ sustained architecture-level improvement
```

This requires ablations and negative controls that deliberately disrupt the proposed interaction pathways.

At minimum, the experiment must be able to answer whether the complete composition outperforms simpler explanations because of the proposed interactions rather than because one component dominates or several independent gains accumulate.

## Current CEA Interaction Hypothesis

The present composition suggests a division of labor:

```text
AIEC      → encounter / generate new distinctions
CLPR      → preserve them in correction-efficient predictive geometry
Core      → use them in recurrent cognition and persistent learning
Issue #44 → govern which validated corrections become canonical persistent state
```

This is a **composition hypothesis**. It is not a witness.

## Candidate Negative Controls

The eventual composition benchmark should include variants such as:

```text
AIEC without persistent retention
CLPR without adaptive exploration/exploitation
Core with persistence but no correction-localized representation
Issue #44-like persistence without discriminating evaluation
component outputs shuffled or delayed across interaction boundaries
fixed explore/exploit schedule in place of adaptive switching
representation compression that destroys future-relevant distinctions
validated corrections that cannot influence future policy/state
```

The purpose is to test whether the proposed interaction is causally load-bearing rather than merely co-present.

## Joint Sufficiency Boundary

Even complete component-level success establishes at most:

```text
these component propositions survived independently
```

It does not establish:

```text
the components are jointly sufficient
```

Nor does one successful composition experiment establish open-ended capability growth beyond the tested horizon.

The composition claim must remain scoped to the interaction regime, environment family, duration, component versions, and measured outcome actually tested.

## Open-Endedness Boundary

Repeated improvement is not itself evidence of open-ended improvement.

```text
continued improvement ≠ open-ended improvement
```

A system can improve across many cycles while remaining inside a bounded task family or fixed representational interface.

Evidence for the stronger claim would need to show that successful improvements repeatedly expand the space of subsequent improvements the system can discover, express, or exploit—not merely that a fixed objective continues to rise for a finite horizon.

## Current Engineering Priority

The architecture should not be implemented wholesale merely because the composition is conceptually attractive.

The current bottleneck remains:

```text
Issue #44
→ implementation
→ verification
→ first witness
```

CLPR and AIEC remain independent experimental objects. The Cognitive Core remains a conceptual specification. CEA remains the map of how independently surviving objects might later compose.

## Conception Freeze

Composition methodology is now frozen until evidence creates a deficiency the present structure cannot represent.

```text
CEA frozen
→ independent experiments
→ witnesses / failures
→ evidence-pulled revision
```

Additional conceptual layers are not warranted merely because they make the architecture more complete. Future structural changes should be responses to observed failure, contradiction, or established evidence.

## Status

This is a conception-level composition methodology. It defines what future CEA composition evidence would need to establish; it does not establish that evidence itself.
