# ARC-AGI-3 Implementation Preregistration v1.1

Status: **FROZEN BEFORE FIRST IMPLEMENTATION RESULT**.

This document supersedes `IMPLEMENTATION_PREREGISTRATION_V1.md` only through the explicit amendment below. Every v1 clause not named here remains unchanged and binding.

Reason for revision: `SF-001` in `SPECIFICATION_FAILURES.md`.

No comparative implementation result, development arm result, sealed-holdout result, or environment-source inspection occurred between the v1 freeze and this amendment.

---

# Amendment A — ordinary predictive state gains aggregate predicate contingencies

Replace v1 section 2.1 with the following complete section.

## 2.1 Shared ordinary predictive state

All arms may maintain the same conventional online transition-statistics state `Theta_t` within a level. `Theta_t` is not counted as C-specific memory and is identically available across arms.

`Theta_t` contains two classes of **aggregate counts only**.

### A. Base-context predictive counts

Beta-Bernoulli counts for `z_change` and Dirichlet counts for `changed_count_bucket`, indexed by:

`c_base = (current_action_token, ACTION6_coordinate_bin_or_null, previous_action_token_or_START, previous_z_change_or_START, available_action_mask)`.

ACTION6 coordinates are quantized into an 8x8 grid over the 64x64 frame; non-ACTION6 actions use `null`.

All count tables use unit symmetric priors.

### B. Predicate-contingency counts `Q_t`

For each observed event and each v1 section-5 allowed predicate that is defined for that event, maintain:

`Q_t[(base_context, predicate_id, predicate_value)] = (n_change_0, n_change_1, bucket_counts[7])`.

These are unordered aggregate statistics only.

`Q_t` is explicitly prohibited from storing:

- prior frame payloads;
- ordered event sequences;
- raw transition objects;
- unquantized historical ACTION6 coordinates;
- timestamps sufficient to reconstruct ordering;
- source-derived fields;
- semantic mechanic/goal/usefulness labels.

The only historical information available through `Q_t` is the contingency total for a frozen base context, frozen predicate, predicate value, primary outcome, and changed-count bucket.

Candidate generation may use `Q_t` to determine whether an allowed predicate divides accumulated evidence into non-empty subsets and to compute proposal-stage in-sample predictive reduction.

Evidence in `Q_t` that predates proposal creation remains **proposal evidence only** and may not satisfy any forward authorization predicate in `Gamma_X`.

Candidate-local forward-evaluation counts begin at zero at proposal creation and are maintained separately inside the provisional hypothesis object, together with provenance evidence ids as frozen in v1.

`Theta_t`, including `Q_t`, is reset at every level transition for all primary mechanism-isolation arms. The separate conventional-persistence control defined in v1 section 13 persists the same complete `Theta_t`, including `Q_t`, across levels.

---

# Amendment B — candidate-generation wording

In v1 section 5.1, interpret:

> evaluates each allowed extra predicate that is defined for the stored evidence

as exactly:

> queries `Q_t` for each allowed extra predicate defined in the frozen predicate language and creates a candidate only when the corresponding aggregate contingency table contains at least two non-empty predicate-value subsets under the triggered base context.

No raw event older than `H_raw` may be recovered or inspected to perform this operation.

Candidate ranking by in-sample binary log-loss reduction is computed from `Q_t` aggregate counts only.

---

# Amendment C — strong conventional-persistence control

Clarify v1 section 13 arm `B_PERSIST`:

`B_PERSIST` persists the complete ordinary predictive state `Theta_t = (base counts, Q_t)` across ARC levels within the same game. It still has no L candidate/correction state, no C canonical ledger, no AIEC allocator, and no X authority gate.

This preserves the intended contrast:

`structured corrective persistence` versus `generic conventional statistical persistence`.

---

# Unchanged constraints

The following remain exactly as frozen in v1:

- `H_raw = 2 completed transitions + current observation`;
- no historical full-frame transcript;
- exact `R_t`, `M_t`, `G_t`, `Lambda_t`, and `H_t` schemas except for the `Theta_t/Q_t` clarification above;
- primary target and prequential scoring;
- candidate predicate language;
- CLPR correction operator;
- level-boundary persistence semantics;
- AIEC rule and fixed-allocation controls;
- X authorization predicates and thresholds;
- metric definitions;
- 256-action development budget;
- arm matrix;
- deterministic evaluation and typed failure handling;
- sealed-holdout firewall;
- no development source inspection.

# Authority consequence

`SF-001` and this amendment authorize implementation of the missing aggregate contingency substrate only.

They do not authorize:

- widening raw history;
- adding semantic features;
- changing thresholds;
- altering candidate predicates;
- modifying budgets or arms;
- interpreting any implementation behavior as evidence before invariant verification and matched development execution.
