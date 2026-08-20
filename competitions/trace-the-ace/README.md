# Trace the Ace — CEA Proving Ground

## Status

This directory operationalizes the frozen CEA conception against the external **Trace the Ace** tutoring-outcomes competition.

It is a proving ground, not a CEA witness.

```text
competition performance ≠ component witness ≠ composition witness
```

The competition provides an externally adjudicated prediction task. CEA supplies the research discipline for deciding which interventions, corrections, and persistent changes are entitled to acquire authority.

## Flagship Question

> **Can an artificial system accumulate justified corrective transformations in a way that increases its future capacity to discover and execute further justified corrections?**

The competition is useful because it exposes a real downstream consequence: given a tutoring dialogue and learning objective, predict the probability that the student answers the next same-topic assessment question correctly.

## Operational Machine

```text
Environment / development stream
→ Observation
→ Representation
→ Prediction
→ Intervention
→ Evaluation
→ Candidate correction
→ Authorization
→ Persistent update
→ new cognitive state
→ next development differential
```

The corresponding CEA responsibilities are:

```text
Cognitive Core → persistent prediction / evaluation / correction loop
CLPR           → correction-localized predictive representation intervention
AIEC           → adaptive allocation of exploration vs exploitation
Issue #44      → provenance, warrant, authorization, commit integrity
```

No component is promoted from useful decomposition to necessary mechanism without an ablation capable of removing or breaking it while preserving relevant alternatives.

## Two Simultaneous Objectives

### Competition objective

Build the strongest rule-compliant predictor possible under the official metric:

```text
minimize held-out log loss
```

Calibration is first-class because the submitted output is a probability and log loss penalizes confident errors.

### CEA objective

Measure whether development-time corrections become:

```text
better prediction
+ persistent learning
+ efficient future correction
+ low collateral damage
+ preserved authority integrity
```

A leaderboard improvement may motivate a hypothesis, but it does not by itself establish a CEA witness.

## Experimental Order

```text
Phase 0 — competition constraints + leakage-safe validation
Phase 1 — strong static baseline
Phase 2 — executable Cognitive Core + typed correction ledger
Phase 3 — CLPR intervention
Phase 4 — AIEC intervention
Phase 5 — component/composition ablation matrix
Phase 6 — longitudinal corrective-capacity experiment
```

The full CEA stack is not built first. Each intervention must earn its place independently.

## Directory

```text
competitions/trace-the-ace/
├── README.md
├── COMPETITION.md
├── OPERATIONALIZATION.md
├── EXPERIMENTS.md
├── LEDGER.md
└── RESULTS.md
```

## Governing Firewalls

```text
source compatibility ↛ evidence
verified phenomenon ↛ mechanism
positive development result ↛ held-out witness
component witness ↛ composition witness
evaluation ↛ mutation
leaderboard score ↛ CEA validation
```

## Current Authority State

```text
Trace the Ace proving-ground specification = ESTABLISHED
competition result                         = NOT YET PRODUCED
CLPR witness                              = NOT EARNED
Cognitive Core witness                    = NOT EARNED
AIEC witness                              = NOT EARNED
CEA composition witness                   = NOT EARNED
```

The next legitimate change is implementation or data-derived evidence, not another conceptual layer.
