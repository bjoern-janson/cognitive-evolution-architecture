# Cognitive Evolution Architecture

> **Research hypothesis:** a sufficiently capable cognitive core, operating on correction-localized predictive representations and a sustainable adaptive information-expansion cycle, may exhibit sustained capability growth without explicitly simulating biological evolution.

Cognitive Evolution Architecture (CEA) is a research notebook for composing independently testable hypotheses, engineering substrates, and the epistemic rules that govern what the project is allowed to conclude from them.

Every new framework enters the repository as a **conception version**. Conceptions are research checkpoints, not validation events: they may be revised, split, rejected, or promoted only when evidence warrants it.

## Two Architectures

CEA is intentionally a paired system:

```text
CEA = Computational Architecture + Epistemic Architecture
```

The computational architecture asks:

> **How can capability accumulate?**

The epistemic architecture asks:

> **What entitles us to say that it accumulated?**

The master law connecting them is:

> **Capability may accumulate; authority must be earned at every transition.**

Equivalently:

```text
A precursor cannot manufacture the authority of its successor.
```

## Computational Architecture

CEA currently composes four independently testable components:

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

The current compositional hypothesis is:

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

This composition remains a hypothesis about interaction. A coherent architecture does not establish that its components are individually correct, jointly sufficient, synergistic, or capable of sustained improvement.

## Epistemic Architecture

CEA treats research state as a sequence of authority-limited transitions:

```text
SourceClaim
  ↓ verification
VerifiedPhenomenon
  ↓ hypothesis construction
Hypothesis
  ↓ discriminating experiment
Witness
  ↓ composition proposal
CompositionHypothesis
  ↓ composition-specific discriminating experiment
CompositionWitness
```

No arrow is an equivalence, and no stage inherits the authority of a later stage.

The three primary firewalls are:

```text
Ingestion:   conceptual compatibility ↛ authority
Composition: component witness ↛ composition witness
Execution:   validated evaluation ↛ mutation
```

These are instances of the same conservation rule: **the presence of a precursor is insufficient to authorize the successor transition.**

## CEA Methodological Kernel

The current kernel consists of four governing distinctions:

```text
K1: Specification ≠ Implementation ≠ Verification Result
K2: Conceptual compatibility ↛ authority
K3: Component witness ↛ composition witness
K4: Evaluation ↛ mutation
```

Together they prevent analogy inflation, compositional inflation, and operational inflation.

Additional protected distinctions include:

```text
framework assertion ≠ empirical demonstration
prediction ≠ result
verified phenomenon ≠ mechanism
inherited competence ≠ persistent learning ≠ open-ended improvement
validated consequence grants local authority; it does not automatically grant causal authority
```

## Authority Gradient

CEA uses the following ordering as different epistemic capabilities, not merely prose confidence labels:

```text
interesting < relevant < verified < discriminating < witnessed
```

A source may be relevant without being verified. A verified phenomenon may establish occurrence without identifying mechanism. A witness has authority only over the proposition its experiment discriminated. A composition witness has authority only over the tested interaction regime.

## Repository Role

This repository defines and tracks the **composition and epistemic methodology**.

Independent empirical work remains separable:

- [`correction-localized-predictive-representation`](https://github.com/bjoern-janson/correction-localized-predictive-representation) tests CLPR independently.
- [`adaptive-information-expansion-cycle`](https://github.com/bjoern-janson/adaptive-information-expansion-cycle) tests AIEC independently.
- The Issue #44 implementation repository implements and tests the authority substrate independently.

CEA must not become evidential authority for its children merely because it composes them.

```text
CEA ↛ CLPR truth
CEA ↛ AIEC truth
CEA ↛ Issue #44 correctness
```

Likewise, independent component success does not establish architectural success:

```text
Witness[A] + Witness[B] + ... ↛ CompositionWitness
```

A composition is a hypothesis about interaction, not a certificate of its components or of itself.

## Notebook Structure

```text
cognitive-evolution-architecture/
├── README.md
├── methodology/
│   ├── CONCEPTION.md
│   ├── research_objects/
│   │   └── CONCEPTION.md
│   └── composition/
│       └── CONCEPTION.md
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

Each conceptual area begins with a `CONCEPTION.md`. These are research snapshots, not stable interfaces.

## Current Evidential Hierarchy

```text
Source claim
→ verified phenomenon
→ component hypothesis
→ component experiment
→ component witness
→ composition hypothesis
→ composition experiment
→ composition witness
```

Authority is earned locally at every transition. No inference leap is licensed between stages.

## Current Status

| Object | Status | Current role |
| --- | --- | --- |
| CEA methodological kernel | Conception frozen | Governs research authority transitions |
| Issue #44 | Semantic specification frozen; implementation / verification phase | Engineering substrate |
| CLPR | Conception hypothesis; independent empirical testing | Representation-level hypothesis |
| AIEC | Conception hypothesis; independent empirical testing | Process-level hypothesis |
| Cognitive Core | Conception specification | Persistent cognitive loop |
| CEA composition | Conception frozen | Whole-architecture hypothesis |

The active engineering bottleneck remains:

```text
Issue #44 → implementation → verification → first witness
```

Component witnesses, when earned, do not automatically promote the CEA composition. The composition must eventually survive its own ablations, negative controls, and interaction-specific falsification experiment.

## Working Rule

Prefer `main` while this repository functions as a fast-moving research notebook. Use branches when implementation, review, rollback, or repository safety warrants isolation.
