# FCD/OCC C0 — Prospective Adversarial Attack Protocol

## Status

```text
PROTOCOL FROZEN BEFORE ATTACK EXECUTION
NO ATTACK RESULT RECORDED
NO CEA OR ARC3 AUTHORITY MOVEMENT
```

This protocol defines how the frozen C0 candidate may be attacked. It does not execute an attack, select an empirical benchmark, or repair the constitution.

## 1. Protected target

The target is the exact commit identified as the **C0 constitution anchor** in [STATUS.md](STATUS.md).

Attack work may add records and immutable descendants. It may not edit the anchored versions of:

- [CONSTITUTION.md](CONSTITUTION.md);
- [DEFINITIONS.md](DEFINITIONS.md);
- this protocol.

If a repair is proposed, it must be a separately named successor constitution with explicit ancestry and a localized change record.

## 2. Attack objective

The attack seeks the smallest valid construction that establishes one of the following:

1. a constitutional clause is internally inconsistent;
2. a clause is vacuous under an ordinary countermodel;
3. all clauses can be satisfied while irreversible corrective closure still occurs;
4. a healthy adaptive transition is rejected despite preserving future corrective distinguishability;
5. a load-bearing referent cannot be prospectively constituted;
6. a claimed localization cannot be distinguished from a relevant rival explanation.

The attack is not required to make C0 succeed. A valid failure is a successful scientific result.

## 3. Global validity gates

Before an attack instance may establish either `COUNTERMODEL REJECTED BY C0` or `COUNTEREXAMPLE ESTABLISHED`, it must establish:

- the exact C0 anchor;
- the frozen reference tuple `(P,h,B,Ω,S/E boundary)`;
- the candidate transition and state identities;
- the relevant challenge episodes and filtration memberships;
- the proposed `Disc` comparison;
- the warrant and authority provenance used by any claimed loss;
- the criterion distinguishing the attacked proposition from rival explanations.

If any load-bearing object is absent or circularly defined, the result is:

```text
ATTACK INVALID / UNDERCONSTITUTED
```

Global referent, provenance, and evaluator-validity failures take precedence over apparent clause satisfaction or violation.

## 4. Minimal countertrace

Every conclusive attack must preserve a minimal countertrace:

```text
K_0 --τ_1--> K_1 --τ_2--> ... --τ_n--> K_n
```

with:

```text
attack identifier
target clause
frozen reference tuple
system / environment boundary
initial and terminal open commitments
Q filtration and R^corr route structure before and after each relevant transition
Disc coverage before and after
claimed authorized losses and provenance
independently established trace classification: healthy/corrective, defective/sealed, or disputed
C1–C6 satisfaction vector
externally established corrective property preserved or lost
first violated or underconstituted clause, or `NONE` for a false survivor
minimal evidence establishing the result
relevant rival explanations
attack outcome
```

Minimality means that removing any retained transition or premise would prevent the trace from establishing the reported result. It does not claim globally unique minimality.

When a clause is violated, the first violated clause is reported. Later failures may be recorded as secondary observations but cannot replace the shallowest established failure.

A false survivor has a different witness form: every clause is apparently satisfied while a required future correction is nevertheless irreversibly unreachable or ineffective. Such a record must state `first_violated_clause: NONE`, record `C1–C6: SATISFIED`, and identify the independently established corrective distinction that the clauses failed to protect.

A sealed or otherwise defective trace that the constitution correctly rejects is not a counterexample to C0; it is evidence that the targeted clause blocked that attack. A healthy trace rejected by C0 is an overconstraint counterexample.

## 5. Rejected-countermodel record

An attack instance whose countermodel is rejected by C0 must record:

```text
attack premise
attempted countermodel or transition
why the reference tuple remained valid
which targeted clause rejected the trace
why that violation tracks the independently established defect
why any unaffected targeted clauses remained satisfied
which alternatives were actually excluded
which residual uncertainties remain
```

Failure to find a counterexample is not evidence that none exists.

## 6. Frozen attack classes

### A1 — Phantom reopening

Construct a commitment with a syntactic `χ` that cannot causally rescope, revise, retire, or leave the commitment consequentially unresolved.

Primary target: `C3`.

### A2 — Coverage laundering

Substitute a new route claimed to replace an old route while omitting at least one required correction-relevant distinction.

Primary targets: `C4`, `C6`, and `Disc`.

### A3 — Reference or contract laundering

Allow the incumbent or transition to shrink or reinterpret `Ω`, `P`, `h`, `B`, or the system/environment boundary so that destroyed challenge routes disappear from evaluation.

Primary target: `C1`.

### A4 — Authority laundering

Construct `L_t^auth` from convenience, incumbent preference, post-hoc success, resource pressure, or an authority object that cannot warrant the claimed loss.

Primary targets: `C2`, `C5`.

### A5 — Resource illusion

Claim a corrective route exists even though it cannot be realized within the frozen horizon, resource budget, or authorized environment boundary.

Primary targets: `C1`, `C4`.

### A6 — Self-generated challenge

Let the incumbent control the commitment, challenge generation, evaluation, and consequence such that no independently grounded route remains.

Primary targets: `C1`, `C3`.

### A7 — Valid counterexample

Construct a genuinely healthy adaptive transition that violates a constitutional clause while preserving all correction-relevant distinguishability required by the frozen reference contract.

Primary target: overconstraint of any clause.

### A8 — False survivor

Construct a transition satisfying all six clauses while nevertheless making a required future correction irreversibly unreachable or causally ineffective.

Primary target: underdetermination of C0 as a whole.

## 7. Negative controls on attack interpretation

An attack may not infer constitution failure merely from:

- a missing implementation;
- a failed model run;
- an unavailable tool outside the frozen authorized environment;
- ordinary resource differences between systems;
- a challenge that supplies the answer or authority by instruction;
- a wrapper action falsely attributed to the system;
- a route whose relevance to the declared corrective distinction is unestablished;
- a surface cue or task-family shortcut;
- a post-hoc lookup policy fitted to a finite realized trajectory.

These may establish invalidity, apparatus failure, or a narrower rival. They do not automatically refute the constitution.

## 8. Per-attack outcomes and constitution-level terminal statuses

Each executed attack instance records exactly one outcome:

```text
COUNTERMODEL REJECTED BY C0
COUNTEREXAMPLE ESTABLISHED
ATTACK INVALID / UNDERCONSTITUTED
```

- `COUNTERMODEL REJECTED BY C0` means a defective or sealed trace was rejected by the targeted clause.
- `COUNTEREXAMPLE ESTABLISHED` means a healthy trace was wrongly rejected, a false survivor passed all clauses, or a valid proof established inconsistency or vacuity.
- `ATTACK INVALID / UNDERCONSTITUTED` means the instance lacked a load-bearing referent or discriminating criterion.

This protocol freezes attack classes, not a finite executable suite. A separately frozen attack plan must enumerate the concrete instances, models, and stopping rules before any constitution-level terminal status can be assigned.

After every instance in that separately frozen suite reaches a valid outcome, exactly one constitution-level terminal status is permitted:

```text
SURVIVED CONSTITUTION ATTACK
FAILED CONSTITUTION
INVALID / UNDERCONSTITUTED
```

### Survival

Every instance in the prospectively frozen suite was validly completed and no counterexample was established against the exact anchor.

```text
survival ≠ truth
survival ≠ necessity
survival ≠ implementation validity
survival ≠ assay validity
survival ≠ CEA promotion
```

### Failure

At least one valid minimal countertrace establishes inconsistency, vacuity, overconstraint, or false survival. A defective trace correctly rejected for violating a protected clause does not establish constitution failure.

### Invalidity / underconstitution

At least one load-bearing suite instance lacks a prospectively fixed referent, comparison, evaluator warrant, or discriminating criterion, preventing the suite from supporting either survival or failure. Apparent positive and negative outcomes remain uninterpretable.

## 9. No-repair rule

```text
failure of C0 ≠ permission to edit C0
```

An attack instance stops after recording its countertrace and attack outcome. A constitution-level result stops after recording its terminal status. Either may recommend the smallest implicated boundary for a successor, but neither may create, adopt, or test that successor inside the same result.

Any successor must state:

- its exact C0 ancestor;
- the countertrace that motivated reopening;
- the smallest changed clause or definition;
- the authority gained and not gained;
- the attacks that must be rerun.

## 10. Execution ceiling

This protocol authorizes no attack execution by itself. A separately frozen attack plan must identify the models, formal system, benchmark, evaluator, resource budget, metrics, and stopping conditions used for an actual attack.

No implementation, CEA revision, ARC3 protocol change, benchmark claim, or empirical interpretation is authorized here.
