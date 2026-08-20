# Memory — Conception

Memory is not merely retained content. The current conception is:

```text
memory = persistent state + provenance
```

A retained update should preserve enough lineage to answer:

- what was learned;
- why it was learned;
- under which conditions it is valid;
- what evidence could invalidate it;
- which future decisions it is allowed to influence.

Persistence alone does not establish correctness or authority. Issue #44 is the current substrate hypothesis for governing which validated changes may become durable canonical state.
