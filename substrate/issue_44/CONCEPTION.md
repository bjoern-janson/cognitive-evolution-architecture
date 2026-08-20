# Issue #44 Authority Substrate — Conception Index

## Status

- Semantic specification: **frozen**
- Implementation: active
- Verification: active

Governing rule:

```text
Specification ≠ Implementation ≠ Verification Result
```

Core directive:

> Never weaken the specification merely to make implementation tests pass.

## Core Architectural Law

> **No lower layer may manufacture authority or information absent upstream.**

The substrate is decomposed here into notebook areas matching the current semantic and verification specification:

- `authority/` — affine capabilities, authority-at-commit, spatial/temporal binding;
- `evaluator/` — observation/likelihood/triage firewall and ValidatedEvaluation bridge;
- `StateStore/` — sequential transition semantics and guard precedence;
- `MergeIntent/` — warrant/evidence compatibility, certificates, MergeCapability coordination;
- `DAG/` — canonical parent identity, node construction, root binding;
- `codec/` — canonical encoding/decoding and granular representation errors;
- `persistence/` — semantic vs durable commit, recovery, retry safety;
- `verification/` — Loom linearizability, Proptest state machine, invariants, shrinking, triage.

## End-to-End Authority Chain

```text
Observation
→ ValidatedEvaluation
→ ExclusionCapability
→ MutationReceipt
→ WarrantCert + EvidenceCert
→ MergeCapability
→ MerkleDagNodeBody
→ CanonicalBytes
```

No transition in this chain may create authority or information not warranted by its predecessor.
