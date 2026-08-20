# Authority — Issue #44 Conception

## Conservation Law

```text
Compose(A, B) ⪯ meet(A, B)
```

Composition cannot exceed the authority warranted by either input.

## Opaque Context

Authority-bearing execution binds opaque identifiers such as `TaskId`, `ProtocolId`, `ScopeHash`, `BranchId`, and `CapabilityId`.

```text
identifier ≠ capability
```

Knowing an identifier never grants standalone permission.

## Temporal Context

The substrate distinguishes three strictly monotonic clocks:

```text
(E, E_C, E_P)
Epoch, CandidateEpoch, ProtocolEpoch
```

Callers cannot manufacture or artificially advance them.

## Affine ExclusionCapability

An `ExclusionCapability` binds the excluded hypothesis to branch, task, protocol, scope, all three epochs, and capability identity.

Required semantic properties include private construction, non-`Clone`, non-`Copy`, restricted minting, single consumption, and exact contextual binding.

```text
capability existence ≠ capability validity at commit
```

## Authority at Commit

```text
MutationOccurred
iff CapabilityValidAtCommit and TargetLive
```

A stale capability never becomes fresh again. Spatial and temporal validity remain orthogonal.

```text
Capability_A ⊬ ΔS_B
Capability_e ⊬ ΔS_(e+1)
```
