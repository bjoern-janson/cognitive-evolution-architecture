# Codec — Issue #44 Conception

Canonical representation is independent of semantic interpretation.

## Laws

```text
Decode(Encode(N)) = N
Encode(Decode(b)) = b   for canonical b
```

If bytes are syntactically parseable but violate canonical representation rules:

```text
b ∉ B_canonical → Decode(b) = Err(NonCanonical)
```

Current granular error classes:

- `Truncated`
- `InvalidLength`
- `InvalidEnumTag`
- `TrailingBytes`
- `NonCanonical`
- `StructuralMismatch`

Codec logic must not manufacture or redefine semantic authority rules.
