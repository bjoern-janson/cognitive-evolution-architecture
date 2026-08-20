# ARC-AGI-3 Implementation Preregistration v1.3

Status: **FROZEN BEFORE FIRST ARC ENVIRONMENT EXECUTION OR COMPARATIVE IMPLEMENTATION RESULT**.

This document supersedes implementation preregistration v1.2 only through the explicit provenance amendment below. All v1, v1.1, and v1.2 clauses not named here remain unchanged and binding.

Reason for revision: `SF-003` in `SPECIFICATION_FAILURES.md`.

At freeze time, the latest pure unit/invariant suite passed 20/20 tests. No ARC development environment had been executed by the implementation and no comparative arm result had been observed.

---

# Amendment F — two-tier hypothesis provenance

The lineage model is split between proposal-stage aggregate provenance and forward authorization provenance.

## F.1 Proposal-stage provenance

Candidate generation continues to use only the non-reconstructive aggregate contingency substrate `Q_t` authorized by v1.1.

For every proposed hypothesis, construct a canonical proposal snapshot containing exactly:

- `base_context`;
- `predicate_id`;
- `predicate_value`;
- parent observed counts `(n_change_0, n_change_1, bucket_counts[7])` with unit priors removed;
- local observed counts `(n_change_0, n_change_1, bucket_counts[7])` with unit priors removed;
- `proposal_gain_nll`.

Canonicalization uses deterministic JSON with sorted keys and compact separators. Tuples are represented as JSON arrays. The proposal snapshot hash is:

`proposal_snapshot_hash = SHA256(canonical_json_utf8)`.

The provisional hypothesis stores:

- `proposal_snapshot_hash`;
- `proposal_snapshot_counts` sufficient to reproduce the canonical snapshot numerically.

It does **not** store historical creation event IDs that have left `H_raw`.

`Q_t` remains aggregate-only and gains no event index, timestamp sequence, or reconstructive identifier list.

## F.2 Forward authorization provenance

Strictly forward events observed after proposal creation continue to receive individual immutable `evidence_id` values exactly as frozen previously.

Every forward event that contributes to:

- in-scope support;
- forward NLL gain; or
- sibling support required by `Gamma_X`

must be represented in the lineage ledger by its individual `evidence_id`.

The hypothesis stores the individual IDs for its in-scope forward support. The authorization decision records the complete set of forward evidence IDs considered for the frozen predicates.

## F.3 X lineage completeness

The v1 X predicate `lineage completeness` is satisfied iff:

1. `proposal_snapshot_hash` is present and recomputes exactly from the hypothesis's stored proposal snapshot fields;
2. every forward evidence id declared by the hypothesis exists in `Lambda_t.evidence`;
3. the authorization decision records the proposal snapshot hash and the forward evidence ids it considered.

Proposal-stage aggregate evidence is not converted into individual evidence IDs after the fact.

## F.4 Claim lineage schema clarification

A claim lineage record therefore contains:

`(claim_id, parent_claim_or_null, proposal_snapshot_hash, predicate, scope, current_status)`.

Forward evidence remains linked through the hypothesis and authorization decision records.

This replaces only the v1 requirement that a newly proposed claim contain exact historical `creation_evidence_ids` once those events are no longer present in the bounded raw window.

---

# Unchanged constraints

All other v1/v1.1/v1.2 clauses remain binding, including:

- `H_raw = 2` completed transitions plus current observation;
- aggregate-only `Q_t` history;
- no historical full-frame transcript;
- frozen candidate predicate language;
- strictly forward X authorization evidence;
- non-compositional correction arbitration;
- X thresholds;
- budgets and arms;
- sealed-holdout firewall;
- no development source inspection.

# Authority consequence

v1.3 authorizes only a provenance representation compatible with non-reconstructive aggregate proposal evidence.

It does not authorize widening history, weakening lineage, adding semantic fields, changing thresholds, or interpreting pure implementation checks as empirical CEA evidence.
