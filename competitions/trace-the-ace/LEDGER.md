# CEA Research / Update Ledger

## Purpose

The ledger prevents development convenience from silently becoming epistemic authority.

Every meaningful experiment, model change, external resource, correction, promotion, rejection, and competition submission receives a durable record.

## Research Object Types

```text
SourceClaim
VerifiedPhenomenon
Hypothesis
Experiment
Result
Witness
CompositionHypothesis
CompositionExperiment
CompositionResult
CompositionWitness
```

`Result` is explicit because an experiment can produce a result without earning a witness.

## Experiment Record

Minimum schema:

```yaml
experiment_id: exp-...
parent_state_id: state-...
hypothesis_id: hyp-...
research_object_type: Experiment
status: planned | running | complete | invalidated
scope:
  dataset_version: ...
  split_id: ...
  session_grouped: true
  environment: ...
intervention:
  component: baseline | core | clpr | aiec | authority | composition
  description: ...
implementation:
  code_commit: ...
  config_hash: ...
  data_hash: ...
  random_seeds: [...]
  compute_budget: ...
acceptance_predicate: ...
falsifier: ...
metrics:
  primary: ...
  collateral: [...]
provenance:
  sources: [...]
  external_models: [...]
  licenses: [...]
result:
  observed: ...
  uncertainty: ...
  failure_kind: ...
decision:
  action: reject | retain_as_candidate | authorize_persistence | promote_to_witness
  warrant_id: ...
```

## Persistent Update Record

```yaml
update_id: upd-...
state_before: state-...
state_after: state-... | null
experiment_id: exp-...
proposed_delta: ...
evaluation_id: eval-...
warrant_id: warrant-... | null
authorization:
  granted: true | false
  scope: ...
  expires_or_epochs: ...
commit:
  occurred: true | false
  reason: ...
provenance: ...
```

Invariant:

```text
authorization.granted = false
⇒ commit.occurred = false
```

## Competition Submission Record

Every external submission should record:

```yaml
submission_id: sub-...
model_state_id: state-...
code_commit: ...
internal_validation:
  log_loss: ...
  calibration: ...
public_leaderboard:
  score: ... | unknown
  rank: ... | unknown
submitted_at: ...
submission_budget_index: ...
notes: ...
```

Public leaderboard feedback is an external observation, not automatic authorization for a model change.

## Promotion Rules

### Hypothesis → Witness

Requires all of:

```text
frozen discriminating experiment
valid execution
held-out result
predeclared or justified acceptance predicate
relevant alternatives addressed
scope stated
provenance preserved
result actually discriminates target proposition
```

### Component Witnesses → Composition Hypothesis

Allowed as motivation for composition testing.

### Component Witnesses → Composition Witness

Forbidden.

```text
Witness[A] ∧ Witness[B] ∧ ... ↛ CompositionWitness
```

### Leaderboard Result → CEA Witness

Forbidden without a separate discriminating CEA experiment.

## Negative Results

Negative results are first-class ledger objects.

Do not delete an experiment merely because:

```text
ΔU <= 0
hypothesis failed
implementation exposed a specification flaw
component interaction was antagonistic
```

Record failure locus using the shallowest applicable category:

```text
Observation
Inference
Mechanism
Representation
Interface
Implementation
Specification
```

Then follow:

```text
generate competing explanations
→ discriminate with independent evidence
→ minimal sufficient revision
→ preserve unaffected structure
→ retest
```
