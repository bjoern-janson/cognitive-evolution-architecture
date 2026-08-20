# FCD/OCC C0 — Attack Ledger

## Current state

```text
NO ATTACK EXECUTED
NO COUNTERTRACE RECORDED
NO CONSTITUTION-LEVEL TERMINAL STATUS ASSIGNED
```

The exact C0 constitution anchor is recorded in [STATUS.md](STATUS.md). This ledger begins empty so that the candidate ancestor precedes every attack result.

## Prospective attack inventory

| ID | Attack class | Primary target | State |
| --- | --- | --- | --- |
| A1 | Phantom reopening | `C3`, `χ` | `NOT RUN` |
| A2 | Coverage laundering | `C4`, `C6`, `Disc` | `NOT RUN` |
| A3 | Reference / contract laundering | `C1`, `(P,h,B,Ω)` | `NOT RUN` |
| A4 | Authority laundering | `C2`, `C5`, `L^auth` | `NOT RUN` |
| A5 | Resource illusion | `C1`, `C4`, `B` | `NOT RUN` |
| A6 | Self-generated challenge | `C1`, `C3`, externality | `NOT RUN` |
| A7 | Valid counterexample | Any overconstraining clause | `NOT RUN` |
| A8 | False survivor | C0 as a whole | `NOT RUN` |

This inventory records prospective targets only. It contains no attack premise, countermodel, result, or interpretation.

## Result-entry template

Future attack records must be appended as immutable descendants and include:

```text
attack_id:
target_anchor:
target_clause:
reference_tuple:
premises:
countertrace:
filtration_before:
filtration_after:
route_structure_before:
route_structure_after:
coverage_before:
coverage_after:
authorized_losses:
trace_classification: # HEALTHY_CORRECTIVE | DEFECTIVE_SEALED | DISPUTED
clause_satisfaction: # C1..C6 each SATISFIED | VIOLATED | INVALID
corrective_property: # independently established property preserved or lost
first_violated_clause: # clause identifier, or NONE for a false survivor
minimal_evidence:
rival_explanations:
residual_uncertainty:
attack_outcome: # COUNTERMODEL_REJECTED | COUNTEREXAMPLE_ESTABLISHED | INVALID_UNDERCONSTITUTED
result_commit:
```

Per-attack outcomes:

```text
COUNTERMODEL REJECTED BY C0
COUNTEREXAMPLE ESTABLISHED
ATTACK INVALID / UNDERCONSTITUTED
```

Constitution-level terminal statuses, assignable only after completion of a separately frozen finite attack suite:

```text
SURVIVED CONSTITUTION ATTACK
FAILED CONSTITUTION
INVALID / UNDERCONSTITUTED
```

An outcome may not be written into the anchored ancestor. A future ledger update must identify the exact result commit and must not modify the C0 constitution files.
