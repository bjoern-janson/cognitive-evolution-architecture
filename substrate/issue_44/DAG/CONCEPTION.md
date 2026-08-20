# DAG — Issue #44 Conception

## Canonical Parent Identity

Parents are canonically ordered so merge identity is commutative with respect to input ordering:

```text
CanonPair(A, B) = CanonPair(B, A)
Encode(M(A, B)) = Encode(M(B, A))
```

## Construction Funnel

```text
MergeCapability → MerkleDagNodeBody
```

A warrant certificate plus evidence certificate is insufficient by itself to construct a node body.

## Identity Conservation

```text
N.id = H(CanonicalEncode(N.body))
```

Node identity is deterministic and content-derived.

## Lineage Availability

Cryptographic validity and lineage availability are distinct. Nodes may be:

- `VALID_NODE`
- `VALID_NODE_CHAIN_INCOMPLETE`
- `INVALID_NODE`

Missing ancestors do not automatically imply node corruption.
