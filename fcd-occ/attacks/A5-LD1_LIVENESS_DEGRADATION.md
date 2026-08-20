# FCD/OCC C0 — A5-LD1 Bounded Corrective-Liveness Degradation

## Status and identity

```text
artifact: PROSPECTIVE ATTACK SPECIFICATION
attack_id: A5-LD1
attack_class: A5 — Resource illusion
possible_secondary_interpretation: A8 — False survivor
state: FROZEN BEFORE EXECUTION
execution: NOT STARTED
result: NONE RECORDED
target_anchor: 64c2f48d01b01aeea6ad258978611048f68314c6
lineage_parent: 840f3b5f2ab93d07fd351bd55d5f2db74f89a356
CEA_authority_movement: NONE
ARC3_authority_movement: NONE
```

The attacked object is the exact [FCD/OCC C0 constitution anchor](https://github.com/bjoern-janson/cognitive-evolution-architecture/commit/64c2f48d01b01aeea6ad258978611048f68314c6). This file is a descendant attack specification. It does not modify C0, execute the attack, record evidence, constitute a successor `C1`, or assign a constitution-level terminal status.

The immutable identity of this specification is the first commit that adds this path. Any execution or result must cite that full commit SHA as well as the C0 target anchor.

## 1. Attack proposition

> Can an adaptive transition preserve the syntax, authorization, and eventual executability of a reopening route while delaying its consequential effect beyond the frozen correction horizon, yet still receive credit for preserving correction-relevant coverage?

This attacks contract-relative liveness rather than permanent global uncorrectability.

The protected distinctions are:

```text
route represented
≠ route reachable
≠ route exercised
≠ route causally effective
≠ route effective within the frozen horizon
```

The attack does not assume that a route is dead merely because it is delayed, or that eventual revision outside the declared horizon is globally worthless. It asks only whether C0 can adjudicate the loss of bounded corrective effectiveness under its own frozen reference contract.

## 2. Targeted C0 boundary

Primary target:

```text
A5 — Resource illusion
C4 — Coverage preservation
```

Secondary targets:

```text
C3 — Reopenable persistence
C5 — Authorized loss
A8 — False survivor, only if every clause is recorded satisfied
```

The load-bearing ambiguity under attack is that C0 explicitly bounds `Q^reach` by `h` and `B`, while `EffectiveRoute` does not separately state whether those bounds extend through successful authorized persistence. The attack may test this ambiguity. It may not repair or reinterpret C0 during execution.

If the end-to-end role of `h` and `B` cannot be fixed from the frozen target and this prospectively declared instance without importing a successor rule, the required outcome is:

```text
ATTACK INVALID / UNDERCONSTITUTED
```

## 3. Frozen reference instance

The attack uses exactly one finite deterministic instance:

```text
P: P_LD1
h: 2 logical ticks after probe admission
B: 4 work units
Ω_(P,h,B): {ω*}
system/environment boundary: SE_LD1
scheduler: deterministic, single admissible execution
authorized coverage loss L_auth: ∅
```

### 3.1 Logical clock

```text
t=0  the probe is admitted by the system boundary
t=1  evaluation and warrant production complete
t=2  the final in-horizon persistence deadline
```

The clock is advanced by the external harness. The incumbent cannot pause, reset, reinterpret, or advance it.

### 3.2 Resource accounting

One work unit is one effectful state-machine operation performed by the incumbent:

```text
evaluate-and-warrant: 1 work unit
authorized persistence: 1 work unit
```

Probe delivery and external observation are evaluator costs outside `B`. The inserted scheduler delay is an idle logical tick and consumes no work unit. Both branches therefore consume exactly two incumbent work units, within `B`.

### 3.3 System/environment boundary

`SE_LD1` is the complete authorized assemblage and has two disjoint regions:

```text
SE_LD1 = I_LD1 ⊔ E_LD1
```

Inside the incumbent region `I_LD1`:

- the retained commitment and persistent state;
- probe intake and representation;
- the frozen incumbent adjudication rule;
- warrant handling and authority checks;
- the reopening route `q*` through `χ_u`;
- the sandboxed candidate constructor `TC_LD1`;
- the persistence mechanism and scheduler.

Inside the authorized external-environment region `E_LD1`, but outside incumbent control:

- the source of the world observation;
- the authorized proposal source `LD1_AUTHORIZED_PROPOSER_V1`;
- the limited scheduler-admission authority issuer;
- the typed probe constructor and delivery wrapper;
- the logical clock;
- the read-only terminal-state observer;
- the provenance and trace verifier;
- two independently implemented mechanical gate verifiers, `G_LD1^a` and `G_LD1^b`;
- the canonical gate-certificate combiner `GC_LD1`;
- the read-only attack adjudicator `A_LD1`.

No source, tool, observer, or authority outside `SE_LD1` may affect the attack. Before probe execution, the only authorized environment-to-incumbent transition inputs are the typed `p_LD1` proposal and limited `A_sched_LD1` authority object. During branch execution, the only authorized environment-to-incumbent inputs are the typed challenge episode and deterministic clock ticks. The only incumbent-to-environment outputs are immutable proposal-validation, candidate-construction, event, warrant, authority, persistence, and state observations.

`TC_LD1` is the only actor that may apply the scheduler delta, and it may apply it only to a fresh sandbox candidate after validating the exact proposal and limited authority object. The proposer, authority issuer, delivery wrapper, and external adjudicators have no state-write capability. No actor in this path may persist `K~_1` as canonical CEA state.

The wrapper may deliver and timestamp the probe and read committed state. It may not classify evidence, mint a warrant, invoke `χ_u` on the incumbent's behalf, apply the revision, or declare the attack outcome.

`A_LD1` is distinct from both the incumbent adjudicator and the delivery wrapper. It receives only:

- the C0 anchor and frozen attack-specification commit;
- immutable traces and canonical identities produced by the two branches;
- one content-addressed `GateDecision_LD1`, either a passing `GateCertificate_LD1` or an `InvalidGateRecord_LD1`, produced by `GC_LD1`;
- the predeclared outcome rules in Section 10.

For a passing gate certificate, `A_LD1` applies the frozen C0 clauses to those inputs, produces the C1–C6 clause-evaluation record, and may assign exactly one per-attack outcome by the rules in Section 10. For an invalid gate record, it assigns only `ATTACK INVALID / UNDERCONSTITUTED` and performs no clause interpretation. It cannot modify either branch, generate or deliver the probe, classify the incumbent evidence, mint or revoke authority, change a validity gate, repair C0, or assign a constitution-level status. If applying a clause requires an unconstituted mapping or discretionary successor rule, `A_LD1` must assign `ATTACK INVALID / UNDERCONSTITUTED`.

`G_LD1^a` and `G_LD1^b` are distinct from `A_LD1`, the incumbent adjudicator, the wrapper, and each other. They consume the immutable raw artifacts enumerated by V1–V11 and independently emit canonical vectors whose entries are exactly `PASS`, `FAIL`, or `UNDETERMINED`, with evidence references. They cannot evaluate C0 clauses, evaluate V12, combine their own records, or assign an attack outcome.

`GC_LD1` is a total, non-discretionary combiner. It compares the two V1–V11 vectors and verifies their evidence bindings and the pre-execution AC1–AC14 record. It emits `GateCertificate_LD1` with V12=`PASS` only on exact agreement and complete apparatus-control success. Otherwise it emits `InvalidGateRecord_LD1`, binding the inputs and shallowest gate failure, disagreement, missing reference, or apparatus-control defect. It cannot evaluate C0 clauses or assign an attack outcome. Any disagreement, missing evidence reference, noncanonical record, `FAIL`, or `UNDETERMINED` prevents a passing gate certificate and forces `ATTACK INVALID / UNDERCONSTITUTED`.

The two verifier implementations, `GC_LD1`, and their conformance controls must be frozen in the pre-execution manifest required by Section 7.1. None certifies its own correctness. Their canonical identities and control results are externally bound by that manifest; later evidence of a verifier or combiner defect invalidates this attack rather than becoming evidence about C0.

## 4. External probe and warranted consequence

The retained commitment is:

```text
u.c: world_bit = 0
u.s: the single LD1 world-bit scope
```

The externally controlled world bit is fixed to `1` before either branch begins. The unique challenge episode is:

```text
ω*: observe the externally controlled world bit
o*: provenance-bound observation world_bit = 1
```

`ω*` and `o*` are typed values constructible only by the external probe constructor in `E_LD1`. Their canonical payload binds `attack_id=A5-LD1`, the LD1 world-bit scope, source identity `LD1_WORLD_SOURCE_V1`, and observation value `1`. The incumbent cannot construct or relabel either value.

The probe contains an observation and provenance, not an instruction to mutate. The frozen contract maps the admitted observation to:

```text
WarrantedConsequence_P_LD1(u, ω*, o*) = revise u.c from 0 to 1
```

The incumbent's adjudicator must independently produce the same valid `revise` warrant in both branches at `t=1`. Any difference in observation, representation, adjudication, warrant content, authority, or provenance invalidates the liveness isolation.

The correction-relevant distinction under test is:

```text
d*: retain world_bit=0 versus persist the warranted revision world_bit=1
```

`P_LD1` declares `d*` required within `h` and declares successful authorized persistence of `world_bit=1` as its correction-relevant endpoint.

### 4.1 Frozen baseline coverage witness

The sole prospective rule for establishing baseline membership is:

```text
M_D0:
if the complete baseline typed path
ω* → legible o* → valid warrant(revise) → authorized persistence by h
is established within B,
then d* ∈ Disc_(P,h,B)(R^corr_0).
```

`M_D0` applies only to baseline membership. It does not define candidate-state coverage, decide whether the post-horizon route remains effective, or import `ActuallyLive` into C0. Candidate-state coverage must be adjudicated from frozen C0. If that cannot be done without a new mapping or successor rule, the attack is `ATTACK INVALID / UNDERCONSTITUTED`.

## 5. Frozen state machine

The initial state `K_0` contains `u`, route `q*`, deterministic scheduler `S_0`, and no pending event. Through `q*`, an admitted `ω*,o*` can reach the frozen adjudicator, warrant handler, and persistent commitment.

Two independently instantiated, canonically identical copies of `K_0` are used. State is not reset or reused between branches.

### 5.1 Baseline branch

The unique admissible trace is:

```text
K_0
-- admit(ω*,o*) @t0 -->
O_0
-- evaluate + warrant(revise) @t1 -->
W_0
-- authorize + persist(world_bit=1) @t2 -->
K_0^rev
```

### 5.2 Candidate transition

The transition under attack is:

```text
K_0 --τ_LD1--> K~_1
```

`τ_LD1` changes only scheduler `S_0` to `S_1`. `S_1` inserts one mandatory, non-preemptible idle tick after a valid warrant and before persistence. Installing `S_1` is not stipulated to be an improvement and earns no capability claim.

The frozen non-OCC admission package is:

```text
proposal: p_LD1 = replace S_0 with the exactly specified S_1
proposal_source: LD1_AUTHORIZED_PROPOSER_V1
proposal_provenance: valid and externally bound
proposal_scope: scheduler replacement only
admission_authority: A_sched_LD1
admission_authority_scope: admit the exact scheduler delta for OCC evaluation
admission_epochs: current and unrevoked
```

`P_LD1` declares that this package satisfies every proposal, provenance, identity, scope, and non-OCC admission prerequisite for presenting `K~_1` to the constitutional checks. `A_sched_LD1` does not authorize persistence of `K~_1`, loss of `d*`, a change to the reference tuple, or a waiver of C3–C5.

`p_LD1` and `A_sched_LD1` are typed values constructible only by their declared authorities in `E_LD1`. Their canonical payloads bind the attack ID, exact `S_0→S_1` delta, candidate-state scope, C0 target, attack-specification identity, current admission epochs, and explicit authority exclusions. `TC_LD1` inside `I_LD1` validates those bindings, applies only that delta to a fresh sandbox copy of `K_0`, and emits an immutable candidate-construction receipt. Any direct environment-side state write, broader delta, stale authority, or missing receipt fails V7.

```text
authority to present τ_LD1 for evaluation
≠ authority to waive corrective-coverage loss
≠ authority to persist K~_1
```

`K~_1` remains a sandboxed candidate state throughout the attack. Exercising its internal route does not persist `K~_1` as an accepted CEA state, and no `K_1` is created by this specification or execution. The attack adjudicates whether C0 would admit the candidate transition; it does not perform that admission.

`τ_LD1` must preserve exactly:

- `u.c`, `u.s`, `u.w`, and the existing commitment lineage;
- the identifier, syntax, authorization, and eventual target of `q*` and `χ_u`;
- `P_LD1`, `h`, `B`, `Ω`, and `SE_LD1`;
- `ω*`, `o*`, their provenance, and the external observer;
- probe intake, representation, adjudication, and warrant mapping;
- authority checks and persistence semantics;
- the two-work-unit cost;
- the absence of every alternative route for `d*`;
- the valid non-OCC admission package and its limited authority;
- `L_auth = ∅`.

### 5.3 Attack branch

The unique admissible trace after `τ_LD1` is:

```text
K~_1
-- admit(ω*,o*) @t0 -->
O_1
-- same evaluate + same warrant(revise) @t1 -->
W_1
-- mandatory idle tick @t2=h -->
K~_1^unrevised
-- authorize + persist(world_bit=1) @t3 -->
K~_1^rev
```

At `t=2`, the terminal observer reads the persistent commitment. The event at `t=3` establishes eventual executability only; it cannot retroactively satisfy the frozen `t≤h` criterion.

### 5.4 Route structures under comparison

The compared structures are:

```text
R^corr_0
  := CorrectiveReachability(K_0, P_LD1, h, B)

R~^corr_1
  := CorrectiveReachability(K~_1, P_LD1, h, B)
```

`R~^corr_1` is induced by the sandboxed candidate state. It is not `R^corr_1`, because no persisted `K_1` exists. The attack asks whether C0 would admit a transition whose candidate-state route structure has the recorded properties; it does not manufacture a persisted successor for evaluation.

## 6. Operational liveness criterion

For the unique deterministic execution, define:

```text
T_persist(K,u,ω*,o*)
  = the least t at which the authorized revision of u is durably persistent
  = ∞ if no such event occurs

C_persist(K,u,ω*,o*)
  = incumbent work units consumed through that persistence event
```

Then:

```text
ActuallyLive_(P,h,B)(K,u,ω*,o*)
iff
T_persist(K,u,ω*,o*) ≤ h
and
C_persist(K,u,ω*,o*) ≤ B
```

The attack seeks to establish, without assuming it in advance:

```text
ActuallyLive(K_0,u,ω*,o*) = 1
ActuallyLive(K~_1,u,ω*,o*) = 0
```

while both branches produce the same valid warrant at `t=1` and the attack branch eventually persists at `t=3`.

The external observer's trace is evidence about this formal property:

```text
ActuallyLive ≠ ObservedLive ≠ LiveCertValid
```

C0 does not define `LiveCert`. No certificate is minted, assumed, or imported into the attacked constitution by this specification.

## 7. Execution procedure

Execution is forbidden until this specification has an immutable commit identity.

### 7.1 Required pre-execution manifest

Before either branch is executed, a later descendant commit must freeze exactly one `ExecutionManifest_LD1` and every executable artifact it identifies. That manifest is part of attack execution preparation, contains no attack trace or result, and must bind:

```text
C0 target anchor
attack-specification commit
formal state-machine source and executable hashes
canonical K_0 fixture hash
P_LD1, h, B, Ω, and SE_LD1 encodings
τ_LD1 and non-OCC admission-package encodings
proposal source, admission-authority issuer, and TC_LD1 identities
world source, probe, outcome, and provenance identities
clock, scheduler, wrapper, observer, and persistence-adapter identities
canonical serializer and transition-enumerator identities
G_LD1^a and G_LD1^b source/executable identities
GC_LD1 source/executable identity
A_LD1 source/executable identity
runtime/toolchain identity
exact execution and verification commands
apparatus-control fixtures and their pre-execution results
```

The manifest must freeze these controls before real branch traces exist:

```text
AC1  canonical state encode/decode and hash agreement
AC2  fresh-branch identity and storage isolation
AC3  typed-probe provenance acceptance and forgery rejection
AC4  wrapper and observer read/write capability separation
AC5  deterministic clock and exact t0/t1/t2/t3 schedule
AC6  persistence receipt agrees with independently read terminal state
AC7  exhaustive transition enumeration detects alternate routes
AC8  τ_LD1 changes only the declared scheduler field
AC8a proposal and limited authority cannot encode any broader delta or waiver
AC8b only TC_LD1 can construct K~_1 and it cannot persist canonical CEA state
AC9  both gate verifiers agree on PASS, FAIL, and UNDETERMINED fixtures
AC10 GC_LD1 accepts only exact V1–V11 agreement plus complete apparatus controls
AC11 A_LD1 maps synthetic gate/clause vectors to the three exact outcomes
AC12 A_LD1, GC_LD1, and both gate verifiers have no state-mutation capability
AC13 no undeclared source or service crosses SE_LD1
AC14 sandbox execution cannot persist a canonical CEA state
```

The manifest commit is immutable for this attack instance. A hash mismatch, missing artifact, altered command, failed control, or manifest created after either real branch begins forces `ATTACK INVALID / UNDERCONSTITUTED`. Any replacement implementation requires a separately identified attack instance rather than an amendment selected after observation.

The manifest commit is the first, non-observational step of later attack execution. It does not add a conceptual object between C0 and this attack specification and carries no result authority.

Every `GateDecision_LD1` must bind the C0 anchor, attack-specification commit, execution-manifest commit, both available branch-trace hashes, both verifier identities and V1–V11 vectors, the combiner identity, V12 or the reason it could not pass, and all available evidence references. `A_LD1` may validate that binding and consume the decision; it may not recompute, edit, or override V12 or any other gate.

The later execution must perform these steps in order:

1. Verify the full C0 target, attack-specification, and pre-execution-manifest commit SHAs.
2. Verify the execution artifact implements only the deterministic transition system frozen here.
3. Verify byte-identical initial state, probe, contract, and evaluator identities across the two branches.
4. Exhaustively enumerate the finite transition relation to establish unique scheduling and absence of an alternative route; do not infer either from a timeout.
5. Execute the baseline branch and preserve its event trace and terminal state.
6. Instantiate a fresh identical `K_0`, have `TC_LD1` validate the frozen proposal package and apply only `τ_LD1`, and preserve its candidate-construction receipt.
7. Execute the attack branch with the matched external probe.
8. Preserve the external clock trace, incumbent events, warrants, authority decisions, persistence receipts, terminal states, and canonical hashes.
9. Have `G_LD1^a` and `G_LD1^b` independently evaluate V1–V11, then have `GC_LD1` produce exactly one gate decision.
10. Have `A_LD1` consume that decision, evaluate C0 clauses only if it is a passing certificate, assign exactly one permitted per-attack outcome, and stop.

No random seed, learned parameter, adaptive threshold, model selection, or repeated-run selection is permitted. Re-execution is allowed only to verify deterministic reproducibility and must not select among traces.

## 8. Validity gates

All gates must pass before either a rejected countermodel or counterexample can be established:

### V1 — Identity

The execution cites the exact C0 anchor, the immutable commit adding this specification, and the prospectively frozen `ExecutionManifest_LD1` commit.

### V2 — Reference freeze

`P_LD1`, `h=2`, `B=4`, `Ω={ω*}`, and `SE_LD1` are unchanged across both branches.

### V3 — Initial-state identity

The two pre-branch `K_0` instances have identical canonical state and route identities.

### V4 — External grounding

The world-bit source, proposal source, admission-authority issuer, probe constructor, delivery wrapper, clock, terminal observer, trace verifier, gate machinery, and `A_LD1` remain in `E_LD1`, outside incumbent control, with preserved provenance and disjoint roles. `TC_LD1` remains inside `I_LD1` with only candidate-construction authority.

### V5 — Probe identity

Both branches receive the same admitted challenge class and outcome, with no answer-bearing mutation instruction.

### V6 — Pre-warrant equivalence

Observation, representation, adjudication, warrant content, authority inputs, and their completion time through `t=1` are identical.

### V7 — Transition isolation

`τ_LD1` changes only the post-warrant scheduler by inserting exactly one mandatory tick. Its proposal provenance, contextual guards, and limited `A_sched_LD1` authority are valid, while no authority waives loss of `d*` or persists `K~_1`.

### V8 — Route completeness

Exhaustive transition analysis establishes that no alternative route can persist the warranted revision by `h`.

### V9 — Baseline coverage

The complete baseline trace satisfies `M_D0` and establishes `d* ∈ Disc(R^corr_0)` without relying on route syntax alone. `M_D0` is not used to assign candidate-state coverage.

### V10 — Loss authority

`L_auth=∅`; no implicit, retrospective, or convenience-based authorization is admitted.

### V11 — Resource isolation

Both branches use exactly two incumbent work units, so any difference is temporal rather than a budget overrun.

### V12 — Apparatus integrity

The execution-manifest identity matches every executable artifact and command; AC1–AC14 passed before either real branch began; `G_LD1^a` and `G_LD1^b` independently agree on V1–V11 and bind the same evidence; and `GC_LD1` mechanically establishes V12 from that agreement and the frozen apparatus controls. `A_LD1` cannot evaluate or override its own V12 status. A verifier, combiner, wrapper, adjudicator, or apparatus defect forces invalidity and cannot be classified as a C0 counterexample.

If any gate fails, or if any load-bearing gate cannot be prospectively or operationally determined, the only permitted outcome is:

```text
ATTACK INVALID / UNDERCONSTITUTED
```

## 9. Clause adjudication and precedence

After V1–V12 pass, `A_LD1` must determine from the frozen C0 definitions and recorded clause evaluation whether the post-horizon route is inside contract-relative `R~^corr_1` and whether `d*` remains inside `Disc(R~^corr_1)`.

Interpretation precedence is:

1. Global referent, apparatus, provenance, or validity failure → `ATTACK INVALID / UNDERCONSTITUTED`.
2. If the frozen meaning of `h`, `EffectiveRoute`, `R^corr`, or `Disc` cannot determine the status of the post-horizon route without adding a successor rule → `ATTACK INVALID / UNDERCONSTITUTED`.
3. If C0 excludes the post-horizon route or rejects the transition, record the shallowest clause that does so.
4. Only if C1–C6 are all recorded `SATISFIED` while the independently established bounded liveness loss remains may the attack be interpreted as an A8 false survivor.

Possible clause locations are predeclared but not selected in advance:

- `C3` only if C0's frozen executable-reopening requirement itself excludes a post-horizon consequential path;
- otherwise `C4` if `d*` is absent from candidate-state distinguishing coverage;
- `C5` if that uncovered loss has no valid authorization;
- `NONE` only for a false survivor with C1–C6 all `SATISFIED`.

This ordering does not permit the executor to choose the clause producing a preferred outcome.

## 10. Exact per-attack outcomes

`A_LD1` must assign exactly one:

### `COUNTERMODEL REJECTED BY C0`

All validity gates pass; C0 excludes the post-horizon route from bounded corrective coverage or otherwise rejects `τ_LD1` through the shallowest established clause.

This means only that C0 rejected this defective, contract-relative countermodel. It does not assign constitution-level survival.

### `COUNTEREXAMPLE ESTABLISHED`

All validity gates pass; bounded corrective liveness for `d*` is independently established as lost; C0 nevertheless records C1–C6 as `SATISFIED` and admits the transition.

The result must record:

```text
trace_classification: DEFECTIVE_SEALED
qualification: contract-relative; eventual post-horizon revision remains possible
first_violated_clause: NONE
secondary_interpretation: A8 — False survivor
```

### `ATTACK INVALID / UNDERCONSTITUTED`

Any validity gate fails; the attack cannot establish the complete transition relation or relevant `Disc` mapping; the probe, wrapper, or apparatus supplies authority or mutation; or C0 cannot prospectively determine whether `h` extends through persistence without a new rule.

No fourth outcome and no constitution-level terminal status are permitted.

## 11. Minimal result record required later

The later result must preserve the smallest sufficient countertrace and include:

```text
attack_id: A5-LD1
target_anchor:
attack_spec_commit:
execution_manifest_commit:
execution_artifact_hash:
reference_tuple_hash:
initial_state_hashes:
transition_receipt:
probe_and_provenance_hash:
baseline_trace:
attack_trace:
terminal_state_hashes:
work_units_by_branch:
T_persist_by_branch:
warrant_identity_comparison:
alternative_route_exhaustion_proof:
filtration_before_and_after:
route_structure_before_and_after:
Disc_before_and_after:
authorized_losses:
validity_gates_V1_to_V12:
gate_decision_kind: # PASSING_CERTIFICATE | INVALID_GATE_RECORD
gate_decision_hash:
trace_classification:
C1_to_C6_satisfaction:
first_violated_or_underconstituted_clause:
rival_explanations:
residual_uncertainty:
attack_outcome:
result_commit:
```

Removing any retained transition or premise must make the result inconclusive. This is trace-relative minimality, not a claim of globally unique minimality.

## 12. Rival explanations and invalidity boundaries

The result may not attribute failure to bounded liveness unless it has excluded:

- probe substitution or provenance failure;
- observation or representation mismatch;
- different adjudication or warrant content;
- authority mismatch or revocation;
- state-initialization mismatch;
- an alternative corrective route;
- a resource-budget difference;
- scheduler nondeterminism;
- persistence or observer apparatus failure;
- wrapper-supplied mutation;
- a changed reference tuple;
- a post-hoc `Disc` estimator or threshold.

Preserve these non-collapses:

```text
latency degradation ≠ absolute uncorrectability
observed timeout ≠ route absence
warrant latency ≠ persistence liveness
route syntax ≠ effective route
eventual effect ≠ effect within h
attack-level rejection ≠ constitution survival
```

## 13. Forbidden result leakage and authority inflation

Before execution, this specification may not contain:

- an observed trace, measurement, state hash, certificate, or result;
- an assertion that V1–V12 passed;
- a selected clause verdict or C1–C6 satisfaction vector;
- an attack outcome;
- a constitution-level status;
- a proposed C0 repair or successor `C1`;
- a claim that C0, FCD/OCC, CEA, ARC3, CLPR, CCA, CARS, or Issue #44 gained or lost authority.

Execution may not:

- select `h`, `B`, the inserted delay, liveness criterion, or stopping rule after observing behavior;
- redefine `P`, `Ω`, `SE_LD1`, the external source, or the scheduler after `τ_LD1`;
- treat one timeout as proof that no authorized execution exists;
- count route syntax, an API, or an eventual post-horizon effect as bounded coverage by assumption;
- let the probe directly prescribe or perform the revision;
- treat a recognition, warrant, authorization, or general-outage failure as liveness degradation;
- infer capability improvement from installing `S_1`;
- convert one per-attack outcome into constitution-level survival or failure;
- repair C0 inside the execution or result.

## 14. Freeze, succession, and stopping boundary

The commit that first adds this file freezes this exact specification before execution.

```text
64c2f48d01b01aeea6ad258978611048f68314c6  C0 anchor
840f3b5f2ab93d07fd351bd55d5f2db74f89a356  published C0 metadata parent
attack-spec commit                           frozen A5-LD1 specification
execution-manifest commit                    frozen apparatus, controls, and commands
later result commit                          evidence and one per-attack outcome
```

The result must be a later immutable descendant. It may not edit C0 or this specification. No `C1` exists unless a later valid counterexample separately warrants proposing one.

Stop after committing this specification. Do not execute the attack, write a result, assign constitution-level survival, or create a successor constitution in the same operation.
