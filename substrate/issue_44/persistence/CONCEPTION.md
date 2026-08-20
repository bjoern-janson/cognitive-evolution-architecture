# Persistence — Issue #44 Conception

Semantic commitment and physical durability are distinct states.

```text
SemanticCommitted
→ DurablyCommitted | PersistencePending | PersistenceFailed
```

Persistence failure does not roll back semantic authority.

## Retry Safety

```text
retry ↛ re-evaluation
retry ↛ new capability
```

A retry operates against the same immutable semantic commit, preventing storage timeout from becoming duplicate authority.

## Recovery

History conservation requires:

```text
Recover(L) = LongestValidCommittedPrefix(L)
```

Physical recovery and fuzzing of recovery behavior belong to the verification layer; this file records the semantic persistence contract.
