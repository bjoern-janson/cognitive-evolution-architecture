# Typed Research Objects — Conception

## Core Idea

CEA should eventually represent research state as distinct object types rather than prose labels that can silently drift in authority.

The provisional type family is:

```text
SourceClaim
VerifiedPhenomenon
Hypothesis
Experiment
Witness
CompositionHypothesis
CompositionExperiment
CompositionWitness
```

The purpose is not bureaucratic classification. It is to make invalid authority promotion explicit.

## Legal Transition Shape

```text
SourceClaim
  │ independent verification
  ▼
VerifiedPhenomenon
  │ relevance + hypothesis construction
  ▼
Hypothesis
  │ discriminating experimental design
  ▼
Experiment
  │ result under declared scope
  ▼
Witness
```

Composition is a separate lane:

```text
Witness[A]
Witness[B]
Witness[C]
  │ composition proposal only
  ▼
CompositionHypothesis
  │ interaction-specific experimental design
  ▼
CompositionExperiment
  │ discriminating result
  ▼
CompositionWitness
```

## Forbidden Coercions

The following promotions are conceptually invalid unless an explicit intermediate transition supplies the missing evidence:

```text
SourceClaim          -> Witness
VerifiedPhenomenon   -> Mechanism
VerifiedPhenomenon   -> Witness
Hypothesis           -> Witness
Witness[]            -> CompositionWitness
ValidatedEvaluation  -> Mutation
```

The exact implementation of these types remains open. The current claim is methodological: research state should preserve distinctions in authority rather than compress them into a single `confidence` field.

## Minimal Metadata Discipline

A research object should eventually preserve enough information to answer:

```text
what proposition does this object establish?
what evidence produced it?
what alternatives did that evidence discriminate?
under what scope and conditions is it valid?
what predecessor objects authorize it?
what would invalidate or reopen it?
what downstream transitions may it authorize?
```

Provenance is therefore part of research state, not decoration.

## Local Authority

A `VerifiedPhenomenon` may establish that an event or pattern occurred under stated conditions. It does not automatically identify mechanism.

A `Witness` may establish only the proposition its experiment was capable of discriminating.

A `CompositionWitness` may establish only the tested interaction regime. It does not license arbitrary extension to different scales, environments, component versions, or future compositions.

```text
authority scope ≤ discrimination scope
```

## Competence Types

CEA must preserve the distinction:

```text
InheritedCompetence
≠ PersistentLearning
≠ OpenEndedImprovement
```

Sophisticated behavior is insufficient to promote a system across these boundaries.

A demonstration of inherited competence establishes only that the current organization can produce some behavior in the tested setting.

Persistent learning additionally requires evidence that consequences alter future state or policy in a retained way.

Open-ended improvement requires a stronger long-horizon proposition: improvements must compound without the demonstrated process collapsing into a fixed ceiling, repeated rediscovery, or externally supplied redesign.

Each requires a separate evidential transition.

## Authority Gradient as Type Capability

```text
interesting < relevant < verified < discriminating < witnessed
```

This ordering should not become a scalar score that erases provenance. The categories name different capabilities:

- relevance authorizes prioritization, not belief;
- verification authorizes an occurrence claim, not mechanism;
- discrimination authorizes relative update among specified alternatives;
- witnessing authorizes the tested proposition within scope.

## Status

This is a conception-level metadata/type discipline. No software type system is yet specified or implemented.
