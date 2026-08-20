# Cognitive Core — Conception

## Core Hypothesis

A **cognitive core** is the smallest persistent computational system capable of maintaining an internal model of its environment, generating and evaluating possible transitions, learning from consequences, and using accumulated state to improve future behavior.

The cognitive core is **not** the body, the environment, the training corpus, or the long-term evolutionary process that produced the substrate.

```text
Cognitive Core =
State Model
+ Prediction
+ Evaluation
+ Action Selection
+ Learning
+ Persistent State
```

Its purpose is to run a continual corrective loop.

## State

The core maintains an authoritative internal state:

```text
K_t = (R_t, M_t, G_t, Λ_t)
```

where:

- `R_t` — current world/self representation;
- `M_t` — persistent learned memory;
- `G_t` — current goals, constraints, or values;
- `Λ_t` — provenance/history of relevant prior transitions.

**Future-relevant distinctions must remain distinguishable.**

## Prediction

The core maps current state and candidate interventions into predicted future states:

```text
(R_t, a) → R̂_(t+h)
```

Prediction need not reconstruct every detail of the world. It should preserve the latent structure necessary to distinguish materially different futures.

## Evaluation

The core compares predicted and observed consequences while preserving the distinctions:

```text
success ≠ failure ≠ uncertainty ≠ novelty
Observation ≠ Interpretation ≠ Correction ≠ Action
```

Information does not automatically become authority.

## Explore / Exploit

The core must be able to shift between discovering unknown structure and harvesting known structure:

```text
Explore ↔ Exploit
```

AIEC is the current process-level hypothesis for how this allocation may be governed.

## Correction

When evidence indicates the current model or policy is inadequate, the core generates a candidate refinement rather than merely memorizing the latest observation.

A correction is valuable when it improves future outcomes while preserving previously valid structure.

## Persistent Learning

Successful corrections become part of future cognitive state:

```text
K_t --validated correction--> K_(t+1)
```

The core should retain enough provenance to distinguish what was learned, why it was learned, under which conditions it remains valid, and what evidence could invalidate it.

```text
memory = persistent state + provenance
```

## Sustainability

Open-ended improvement requires continued operation, state preservation, resource access, and recovery. Evolution may construct such substrates, but biological evolution need not be reproduced inside the cognitive algorithm.

## Minimal Loop

```text
K_t
→ Observe
→ Predict
→ Act
→ Observe Consequence
→ Evaluate
→ Correct
→ K_(t+1)
```

Over long horizons:

```text
K_0 → K_1 → K_2 → ...
```

Each improved state changes the space of future possible improvements.

## Minimal Criterion

A system qualifies as a cognitive core if it can:

```text
represent → predict → act → observe → evaluate → correct → remember
```

The stronger claim remains prospective:

```text
base cognition
+ persistent corrective learning
+ sustainable substrate
→ potential for open-ended capability growth
```

This is a conception hypothesis, not an empirical result.
