# Adaptive Information Expansion Cycle — Conception

## Core Hypothesis

Sustained capability growth may arise from a recurrent cycle in which a system converts environmental differentials into new information, resolves that information into actionable distinctions, predicts consequences, exploits discovered opportunities, and uses the resulting state change to generate new differentials.

```text
Differential
→ Explore
→ Information Expansion
→ Resolve
→ Predict
→ Exploit
→ Learn
→ New Differential
```

This is a research hypothesis, not an established law.

## Definitions

**Differential** — A measurable mismatch, uncertainty, opportunity, constraint, or pressure capable of producing a state change.

**Exploration** — Actions that enter insufficiently known regions of state space to obtain information unavailable from current knowledge.

**Information expansion** — An increase in usable, decision-relevant information or reachable state/action space.

**Resolution** — Refinement of representation so previously collapsed states become distinguishable when the distinction affects future prediction or action.

**Prediction** — Estimation of how candidate actions or state changes alter future trajectories.

**Exploitation** — Applying discovered structure to realize value from the currently available state space.

**Learn** — Persisting useful information, representations, policies, or state changes so they affect future behavior.

## Regime-Switching Principle

Let `C_E` and `C_X` denote resources allocated to exploration and exploitation, and let:

```text
M_E = ∂V/∂C_E
M_X = ∂V/∂C_X
```

The hypothesis predicts adaptive allocation:

```text
M_E > M_X → increase exploration
M_X > M_E → increase exploitation
```

As one regime saturates, its marginal return should fall, potentially producing a transition toward the complementary regime.

## Key Mechanistic Claim

Exploration alone is insufficient because discovered information must be converted into realized value. Exploitation alone should eventually exhaust the currently accessible opportunity space.

```text
sustained adaptation requires both frontier expansion and frontier harvesting
```

Exploitation can also generate new observations, resources, constraints, and unmet opportunities, thereby creating the next differential.

## Predicted Consequences

If the hypothesis is correct:

1. continuous exploration should accumulate unrealized information and underperform adaptive alternation;
2. continuous exploitation should eventually plateau;
3. adaptive switching based on marginal return should outperform fixed schedules in changing environments;
4. preserving discoveries across cycles should improve long-horizon capability;
5. better state resolution should improve cycle efficiency;
6. environments that continue generating differentials should sustain growth longer when discoveries can be retained and exploited.

## Falsification

A particularly strong negative result would be:

```text
alternating Explore/Exploit
not >
single-regime optimization
```

across held-out environments with changing opportunity structures.

## Relationship to CLPR

AIEC is a process-level hypothesis. CLPR is a representation-level hypothesis. They should be tested independently before composition is treated as evidence.

Independent experiment repository: https://github.com/bjoern-janson/adaptive-information-expansion-cycle
