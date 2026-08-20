# Correction-Localized Predictive Representation — Conception

## Core Hypothesis

A latent representation becomes more **predictively capable** when it preserves future-relevant distinctions in a form where a correction to one semantic factor produces a **localized trajectory change** rather than requiring wholesale recomputation of the representation.

```text
predictive capability ↑
as
future-relevant distinctions preserved
--------------------------------------
latent change required for correction
↑
```

This is a hypothesis, not an established theorem.

## Motivation

Raw observations contain detail irrelevant to future prediction, while aggressive compression can collapse distinctions that determine what happens next.

The desired representation lies between raw preservation and excessive abstraction:

```text
Raw state → structured latent state → future-relevant distinctions
```

## Correction-Localized Dynamics

Let `z_t` denote a latent state and `k` identify a semantic factor. A correction should ideally admit:

```text
z'_t = z_t + Δz_k
```

such that:

```text
Δz_k → ΔTrajectory_(t:t+h)
```

with minimal collateral change to unrelated latent factors.

Rather than learning only:

```text
x_t → x_(t+1)
```

the system should support:

```text
(z_t, Δz_k) → ẑ_(t+h)
```

## Predicted Consequences

If the hypothesis is correct, better factorized semantic structure should yield:

1. better counterfactual prediction;
2. more efficient correction;
3. greater transfer across surface realizations or environments;
4. lower collateral prediction error;
5. improved continual correction.

## Falsification Criterion

The hypothesis is weakened or falsified if increasing semantic/factorized structure does not reliably improve localized counterfactual prediction, or if apparently localized latent changes fail to correspond to stable changes in future trajectories.

Strong negative result:

```text
localized latent perturbation
↛ localized predictable future change
```

across held-out environments.

## Architectural Interpretation

```text
Preserve the distinctions that make future correction predictable.
```

Representation quality is therefore not merely reconstruction or compression. It is the maintenance of a geometry in which warranted corrections are expressible as small, interpretable changes with predictable downstream consequences.

Independent experiment repository: https://github.com/bjoern-janson/correction-localized-predictive-representation
