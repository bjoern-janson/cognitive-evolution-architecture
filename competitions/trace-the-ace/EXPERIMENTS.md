# Experimental Program

## 0. Validation Firewall

The default validation unit is `session_id`, not `response_id`.

```text
train_session_ids ∩ validation_session_ids = ∅
```

Recommended initial protocol:

- fixed grouped train/development/held-out partition;
- grouped cross-validation for model selection where compute permits;
- frozen seeds and split identifiers;
- separate calibration analysis;
- no public-leaderboard score used as a substitute for internal held-out evaluation.

If objective/topic stratification is added, it must preserve session grouping.

## 1. Baseline Ladder

Establish competitive reference points before CEA interventions.

```text
B0 — global prevalence / calibrated constant
B1 — transparent transcript statistics + lexical baseline
B2 — strong transcript representation + conventional predictive head
B3 — strongest rule-compliant pretrained/fine-tuned baseline feasible under license and runtime constraints
```

Every later CEA intervention compares against the strongest relevant baseline under matched data and compute budgets.

## 2. Cognitive Core Experiment

Question:

> Does persistent, provenance-preserving correction improve future development outcomes relative to equivalent reset/non-persistent development?

Compare matched regimes:

```text
RESET      — each development episode starts from the same accepted baseline
PERSISTENT — accepted corrections become K_{t+1}
```

Measure:

- grouped held-out log loss;
- calibration;
- retention of previous gains;
- regression on previously valid scopes;
- correction cost/time;
- future correction-capacity proxy `F_B`.

A repeated correction loop that merely memorizes errors without producing retained held-out gains is not a Cognitive Core witness.

## 3. CLPR Experiment

Candidate representation factors may include, provisionally:

```text
concept / objective alignment
student demonstrated understanding
misconception / error pattern
uncertainty / hesitation
repair trajectory
student participation
scaffolding / prompting
explanation / worked-example behavior
key interaction moments
```

These are candidate factors, not assumed natural factors of tutoring.

For factor `k`:

```text
z' = z + Δz_k
```

Test whether the downstream prediction change is:

```text
localized
predictable
useful for correction
low-collateral
```

Suggested metrics:

- perturbation-to-outcome predictability;
- target-factor sensitivity;
- off-target/collateral sensitivity;
- counterfactual consistency;
- correction gain per unit latent change;
- held-out log-loss change after localized correction.

Strong negative:

```text
localized latent intervention
↛ localized predictable downstream change
```

If ordinary representations match or beat CLPR on these measures under matched budgets, CLPR is not promoted as necessary.

## 4. AIEC Experiment

Use AIEC to allocate a fixed development budget between:

```text
Explore — generate new feature/model/representation hypotheses
Exploit — refine/promote already promising hypotheses
```

Compare:

```text
adaptive marginal-return switching
fixed exploration
fixed exploitation
fixed alternating schedule
random switching
retrospective oracle allocation (analysis-only upper bound)
```

Primary claim:

```text
adaptive allocation > fixed/random schedules
```

on held-out development streams under matched compute.

Track:

```text
M_E = ΔU / ΔC_E
M_X = ΔU / ΔC_X
```

and whether allocation changes when marginal returns cross.

Strong negative:

```text
adaptive Explore/Exploit
not >
matched simpler allocation policies
```

## 5. Authority / Issue #44 Experiment

Authority is a transition-integrity layer, not primarily a leaderboard feature.

For any persistent CEA regime, test adversarial transitions including:

```text
mutation without warrant
mutation after stale evaluation
wrong task / scope / branch
stale epoch / candidate epoch / protocol epoch
revoked protocol
already-excluded target
replayed / duplicated evidence
invalid composition promotion
```

Primary integrity metric:

```text
UnauthorizedMutationSuccessRate = 0
```

within the modeled guard suite.

Also measure false refusal separately so zero overreach is not purchased by making all useful mutation impossible.

## 6. Component / Composition Matrix

Treat CLPR (`L`), persistent Core (`C`), and AIEC (`A`) as experimentally switchable factors.

Authority/provenance enforcement is mandatory for persistent CEA arms rather than treated as a performance toggle.

Run the factorial regimes where feasible:

| Regime | L | C | A |
| --- | --- | --- | --- |
| 000 | — | — | — |
| 100 | ✓ | — | — |
| 010 | — | ✓ | — |
| 001 | — | — | ✓ |
| 110 | ✓ | ✓ | — |
| 101 | ✓ | — | ✓ |
| 011 | — | ✓ | ✓ |
| 111 | ✓ | ✓ | ✓ |

For any higher-is-better utility `U` (for competition performance use `U=-logloss`), estimate the three-way interaction:

```text
τ_LCA =
  U111
- U110 - U101 - U011
+ U100 + U010 + U001
- U000
```

Interpretation:

```text
τ_LCA > 0 with held-out uncertainty excluding 0
```

is evidence for a positive three-way interaction under the tested regime.

It is not evidence of universal synergy or open-endedness.

Also report pairwise interactions and the raw component effects so one dominant component cannot hide behind the aggregate score.

## 7. Longitudinal Experiment

Construct a pre-registered sequence of development environments from training data without using competition test labels.

Possible environment boundaries include grouped session shards, topic/objective clusters, or controlled distribution shifts. The partition rule must be frozen before adaptive development begins.

At each epoch:

```text
K_t
→ observe development evidence
→ propose corrections
→ authorize accepted correction
→ K_{t+1}
→ evaluate on untouched future environment
```

Measure:

- `U_pred(K_t)` over future environments;
- `F_B(K_t)` future correction capacity;
- retention/regression curves;
- correction cost;
- authority violations;
- saturation behavior.

The strongest horizon-scoped CEA result would be:

```text
validated persistent corrections
→ improved future predictive performance
+ improved budgeted future correction capacity
```

across held-out environment transitions.

Even sustained positive improvement across the tested horizon does not prove open-ended improvement. The correct claim remains horizon-scoped.

## 8. Falsification Discipline

A component loses authority when its predicted advantage fails under the experiment designed to discriminate it.

```text
CLPR failure  → no localization/predictability advantage
Core failure  → persistence does not improve future correction or causes unacceptable regression
AIEC failure  → adaptive allocation does not beat matched simpler schedules
Authority failure → unauthorized mutation succeeds or useful authorized mutation is structurally impossible
Composition failure → full stack has no interaction advantage beyond component/additive effects
```

Negative results are retained in `RESULTS.md` and may force evidence-pulled revision of CEA.
