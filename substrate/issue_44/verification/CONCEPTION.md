# Verification — Issue #44 Conception

## Verification Ladder

```text
trybuild
→ E1–E5 Evaluator
→ StateStore Guards
→ 2-Thread Loom
→ 3-Thread Event-Traced Loom
→ State-Machine Proptest
→ Dependency-Aware Shrinker
```

The previous ad-hoc `Mutex<StateStore>` test wrapper was insufficient because it proved only that an externally imposed mutex serialized test calls. The production primitive must itself be linearizable.

## Production Primitive

`ConcurrentStateStore` owns synchronization internally, with conditional compilation selecting `loom::sync::Mutex` under Loom and `std::sync::Mutex` otherwise.

The linearization boundary is entirely inside the component critical section:

```text
lock → assess → validate → mutate → record → unlock
```

## Three-Way Administrative Linearizability

The core model examines:

```text
exclude || advance_epoch || revoke_protocol
```

There are six serial orders. Administrative revocation has higher denial precedence than temporal staleness:

```text
ProtocolRevoked ≻ StaleEpoch
```

Expected oracle outcomes:

| Serial order | Outcome |
| --- | --- |
| E, A, R | EXCLUDED |
| E, R, A | EXCLUDED |
| A, E, R | STALE_EPOCH |
| A, R, E | PROTOCOL_REVOKED |
| R, E, A | PROTOCOL_REVOKED |
| R, A, E | PROTOCOL_REVOKED |

## Event Trace

The event recorder is observational only:

```text
Event Recorder ↛ Kernel State
```

It records begin/check/commit/reject events and administrative linearization events without becoming synchronization or authority.

## Anti-Frankenstein Invariant

Across all schedules:

```text
(ProtocolRevoked or StaleEpoch) → ΔC = 0
Error and ΔC ≠ 0 → impossible
```

## State-Machine Model

The Proptest reference model contains no infrastructure logic. It computes pure transitions with `step` and mutates only through `apply`.

## Continuous Invariants

The current audit suite checks:

1. unauthorized mutation prevention;
2. branch isolation;
3. root/certificate binding;
4. evidence non-amplification;
5. belief/structure separation;
6. valid-prefix recovery;
7. lineage reconstruction.

## Dependency-Aware Shrinking

A minimized failing trace must preserve the transitive prerequisites of the failure witness:

```text
Keep(c) → Keep(Deps*(c))
|Q'| < |Q|
FailureKind(Q') = FailureKind(Q)
```

## Failure Triage

Every reproducible failure is classified as exactly one of:

1. **IMPLEMENTATION BUG** — the SUT violated a frozen requirement or diverged from a valid model transition;
2. **MODEL / ORACLE BUG** — the reference model computed the wrong transition or precedence;
3. **SPECIFICATION BUG** — the frozen invariant itself is over-constrained, incomplete, or contradictory.

The specification is never weakened merely to make an implementation test pass.
