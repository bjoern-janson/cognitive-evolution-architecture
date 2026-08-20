# Evaluator — Issue #44 Conception

## Firewall

```text
Observation
→ Observation Model
→ Likelihood Vector
→ Triage
```

The distinctions are strict:

```text
Information ≠ Discrimination ≠ Exclusion ≠ Mutation
```

## Reference Partition

The finite reference evaluator distinguishes:

- `ProtocolFailure`
- `ExogenousDiscrepancy` for `[0,0,0]`
- `NonDiscriminating` when all positive likelihoods are equal
- `Discriminating` when all likelihoods are positive and at least two differ
- `ExclusionWarranted(θ_i)` when `L_i = 0`

Precedence is semantic policy rather than incidental branch order.

Critical prohibition:

```text
Discriminating ↛ ValidatedEvaluation
```

## Authority Bridge

The bridge is one-way:

```text
Observation → ValidatedEvaluation → ExclusionCapability
```

`ValidatedEvaluation` is authority-internal, non-`Clone`, non-`Copy`, and consumed when minting a capability.

```text
ExclusionCapability exists
→ ValidatedEvaluation previously existed
```

The reverse implication to mutation does not hold because authority may become stale before commit.
