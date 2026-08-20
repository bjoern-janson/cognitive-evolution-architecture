# Operationalization

## 1. Mutable Cognitive State

Instantiate the development-time Cognitive Core as an inspectable state:

```text
K_t = (R_t, M_t, G_t, Λ_t)
```

where:

- `R_t` — current predictive/representational state;
- `M_t` — persistent learned memory and accepted corrections;
- `G_t` — current objective and constraints;
- `Λ_t` — provenance and transition history.

For Trace the Ace, the primary objective is held-out probabilistic prediction of the follow-up outcome, subject to competition compliance and CEA authority constraints.

## 2. Typed Development Update

Every proposed development update is represented as:

```text
u_t = (
  state_before,
  hypothesis,
  intervention,
  observation,
  evaluation,
  proposed_delta,
  warrant,
  provenance,
  authorization,
  state_after
)
```

No update may be silently incorporated outside this object.

Minimum recorded fields:

```text
update_id
parent_state_id
hypothesis_id
intervention_type
code_commit
train_data_hash
validation_split_id
random_seed
compute_budget
metrics_before
metrics_after
collateral_metrics
warrant_id
decision
result_scope
```

## 3. What Counts as Improvement

Do not use the phrase "got better" as a measurement.

Let the primary competition utility be:

```text
U_pred(K) = - GroupHeldOutLogLoss(K)
```

Additional CEA dimensions are measured separately:

```text
P = predictive performance / calibration
L = persistence of accepted improvement
C = future correction capacity
D = collateral degradation
S = authority integrity
```

A candidate correction should therefore be evaluated as a vector, not collapsed prematurely into one scalar:

```text
I(u) = (ΔP, ΔL, ΔC, -ΔD, ΔS)
```

Acceptance predicates must state which dimensions they authorize.

## 4. Future Correction Capacity

The true reachable refinement set is not directly observable. Do not pretend it is.

Use a budgeted empirical proxy.

Let `G(K,B)` be the set of candidate corrections generated from state `K` under a fixed development budget `B`. Define:

```text
F_B(K) = E[ max_{u in G(K,B)} ΔU_future(u) ]
```

where `ΔU_future` is evaluated on a held-out development environment not used to construct the candidate.

Then:

```text
ΔF_B = F_B(K_{t+1}) - F_B(K_t)
```

is an operational proxy for whether an accepted correction made useful future corrections easier to discover.

Complementary measures:

- correction success rate under fixed budget;
- compute/time to recover from an injected or natural failure;
- number of distinct accepted correction classes found under fixed budget;
- best held-out gain reached within `h` development steps;
- regression rate on previously valid scopes.

These are horizon- and budget-specific. They do not establish open-endedness.

## 5. Research Objects Become Executable

Use typed epistemic states:

```text
SourceClaim
VerifiedPhenomenon
Hypothesis
Experiment
Witness
CompositionHypothesis
CompositionExperiment
CompositionWitness
```

Promotion is predicate-gated.

Examples:

```text
Hypothesis ↛ Witness
PositiveDevResult ↛ Witness
ComponentWitness[] ↛ CompositionWitness
LeaderboardScore ↛ CEAWitness
```

A `Witness` requires a frozen discriminating experiment, held-out result, explicit scope, preserved provenance, and a result that distinguishes the target proposition from relevant alternatives.

## 6. Authorization Gates Mutation

Persistent state transition:

```text
CandidateCorrection
→ EvidenceCheck
→ WarrantCheck
→ Authorization
→ Commit
```

The implementation target is structural:

```text
unauthorized path to persistent state = unavailable
```

Within the modeled threat surface, measure:

```text
P(unauthorized mutation succeeds)
```

The target is zero across the specified adversarial/guard test suite.

This is not a claim that the system is globally safe.

## 7. Development vs Evaluation

Maintain at least three distinct evaluation surfaces:

```text
exploratory development
frozen internal held-out evaluation
external competition evaluation
```

They may not share authority.

Public leaderboard feedback is especially vulnerable to iterative overfitting. Submission attempts must therefore be ledgered and should not replace the frozen internal validation protocol.
