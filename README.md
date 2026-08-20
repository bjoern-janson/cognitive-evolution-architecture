# Cognitive Evolution Architecture

> **Research hypothesis:** a sufficiently capable cognitive core, operating on correction-localized predictive representations and a sustainable adaptive information-expansion cycle, may exhibit sustained capability growth without explicitly simulating biological evolution.

Cognitive Evolution Architecture (CEA) is a research notebook for composing independently testable hypotheses and engineering substrates. The architecture is intentionally provisional: every new framework enters the repository as a **conception version** and is expected to change as evidence accumulates.

## Architecture

CEA currently consists of four independently testable components:

1. **Adaptive Information Expansion Cycle (AIEC)**
   - Governs exploration, information expansion, resolution, prediction, exploitation, and learning.
   - Question: does adaptive regime switching improve long-horizon capability growth?

2. **Correction-Localized Predictive Representation (CLPR)**
   - Hypothesizes that future-relevant distinctions can be represented so that corrections produce localized, predictable trajectory changes.
   - Question: does correction-localized geometry improve predictive and adaptive efficiency?

3. **Cognitive Core**
   - The minimal persistent system that hosts the corrective learning loop.
   - `Represent → Predict → Act → Observe → Evaluate → Correct → Remember`

4. **Issue #44 substrate**
   - Provides authority, provenance, state-transition, canonicalization, persistence, and verification machinery for safely committing validated semantic changes.

## Governing Composition

```text
CLPR
  ↓
Cognitive Core
  ↓
AIEC
  ↓
validated persistent improvement
  ↓
changed future search space
```

The complete composition remains a research hypothesis. Coherence of the stack is not evidence that any component, or the composition itself, is empirically validated.

## Repository Role

This repository defines and tracks the **composition**.

Independent empirical work remains separable:

- [`correction-localized-predictive-representation`](https://github.com/bjoern-janson/correction-localized-predictive-representation) tests CLPR independently.
- [`adaptive-information-expansion-cycle`](https://github.com/bjoern-janson/adaptive-information-expansion-cycle) tests AIEC independently.
- The Issue #44 implementation repository implements and tests the authority substrate independently.

CEA should not absorb independent experiments merely to make the architecture look unified. Composition comes after component-level evidence.

## Notebook Structure

```text
cognitive-evolution-architecture/
├── cognitive_core/
│   ├── CONCEPTION.md
│   ├── state/
│   ├── memory/
│   ├── proposal/
│   └── correction/
├── representation/
│   └── CLPR/
├── cycle/
│   └── AIEC/
└── substrate/
    └── issue_44/
        ├── authority/
        ├── evaluator/
        ├── StateStore/
        ├── MergeIntent/
        ├── DAG/
        ├── codec/
        ├── persistence/
        └── verification/
```

Each conceptual area begins with a `CONCEPTION.md`. These are research snapshots, not stable interfaces. A conception may be revised, split, rejected, or promoted when evidence warrants it.

## Current Status

| Component | Status | Current role |
| --- | --- | --- |
| Issue #44 | Semantic specification frozen; implementation / verification phase | Engineering substrate |
| CLPR | Conception hypothesis; independent empirical testing | Representation-level hypothesis |
| AIEC | Conception hypothesis; independent empirical testing | Process-level hypothesis |
| Cognitive Core | Conception specification | Persistent cognitive loop |
| CEA | Compositional conception | Whole-architecture hypothesis |

## Scientific Rule

```text
Specification ≠ Implementation ≠ Verification Result
```

No component is considered validated merely because the architecture is coherent, implementable, or internally consistent.

Additional governing constraints:

```text
framework assertion ≠ empirical demonstration
prediction ≠ result
validated consequence grants local authority; it does not automatically grant causal authority
```

## Working Rule

Prefer changes directly on `main` while this repository functions as a fast-moving research notebook, unless a change has enough implementation, review, or rollback risk to justify isolation on a branch.
