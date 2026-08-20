# StateStore — Issue #44 Conception

The sequential `StateStore` is the semantic transition machine beneath the concurrent wrapper.

## Contract

```text
not AllGuardsValid → Err and ΔC = 0
Ok → ΔC ≠ 0
```

The guard set includes branch, task, protocol, scope, all epoch clocks, revocation, and target liveness.

Current failure classes:

- `WrongBranch`
- `WrongTask`
- `WrongProtocol`
- `WrongScope`
- `StaleEpoch`
- `StaleCandidateEpoch`
- `StaleProtocolEpoch`
- `ProtocolRevoked`
- `CandidateAlreadyExcluded`

Guard precedence is a hard semantic policy.

## Concurrency Boundary

The production `ConcurrentStateStore` encloses the sequential store in one synchronization boundary. The intended linearization critical section is:

```text
lock → assess → validate → mutate → record → unlock
```

The concurrency theorem belongs to `verification/`; this file records only the state-machine contract that the theorem must preserve.
