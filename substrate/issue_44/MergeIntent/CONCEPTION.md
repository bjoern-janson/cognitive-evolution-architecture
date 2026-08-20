# MergeIntent — Issue #44 Conception

This notebook area collects the semantic preconditions for a merge and the coordination authority that follows when they are satisfied.

## Warrant Algebra

Warrants carry local claims such as `Excludes(θ)` and `Supports(θ)`.

Absence of a claim is not contradiction.

```text
ConflictingClaim(W_A, W_B)
iff one warrant excludes θ while the other supports θ
```

Composition may not amplify authority:

```text
strength(W_A ⊗ W_B) ≤ min(strength(W_A), strength(W_B))
```

## Compatibility

```text
Context Compatibility ≠ Claim Compatibility
```

Diagnostic precedence is:

```text
context incompatibility ≺ claim conflict
```

A context mismatch must not be mislabeled as semantic contradiction.

## Evidence Adjudication

```text
Provenance
→ Dependence Adjudication
→ Pooling Verdict
```

Duplicate or derived evidence cannot create additional independent information. Unknown dependence does not authorize independent pooling.

## MergeCapability

`MergeCapability` is coordination authority, not empirical authority. It binds exact left/right roots, warrant certificate, evidence certificate, resulting root, and merge commitment.

```text
C_W.roots = C_E.roots = C_M.roots = (R_A, R_B)
```

Stale certificate replay must fail with root mismatch.
