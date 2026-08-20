# State — Conception

The cognitive core's working state is provisionally represented as:

```text
K_t = (R_t, M_t, G_t, Λ_t)
```

The state layer is responsible for preserving distinctions that may alter future prediction, evaluation, or action. It must not collapse current representation, learned memory, goals/constraints, and provenance into one undifferentiated object.

## Current principle

```text
future-relevant distinctions must remain distinguishable
```

The exact state schema is intentionally unfrozen. Changes to representation geometry belong to the CLPR research track; changes to commit authority belong to the Issue #44 substrate.
