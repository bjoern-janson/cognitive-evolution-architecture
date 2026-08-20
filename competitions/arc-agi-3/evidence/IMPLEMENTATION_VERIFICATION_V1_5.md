# ARC-AGI-3 Implementation Verification v1.5

Status: **REPOSITORY_IMPLEMENTATION_VERIFIED_v1.5**.

This is an artifact-identity and execution-conformance verification result. It is not an ARC behavioral result, component witness, composition witness, benchmark result, or evidence of intelligent behavior.

## Operative specification

The operative execution specification is:

`V1 + V1.1 + V1.2 + V1.3 + V1.4 + V1.5`.

Specification failures `SF-001` through `SF-010` remain preserved in the specification-failure lineage.

## Frozen implementation snapshot

Execution implementation commit:

`dc60b57c3d066d3e1f09e34af422061952da60fb`

This commit contains the completed v1.5 lifecycle-lineage repair and the v1.4/v1.5 conformance tests. Subsequent verification-record commits are documentation descendants only; `dc60b57...` remains the frozen execution artifact.

## Verification surface

The v1.5 execution-verification surface contains **32 Python files**:

- 16 modules under `implementation/cea_arc3/`;
- `implementation/run_dev_matrix.py`;
- `implementation/test_implementation.py`;
- 14 modules under `implementation/tests/`.

The previous v1.3 verification surface contained 29 files and was verified 29/29 at commit `219d80a...`.

A repository comparison from `219d80a...` to `dc60b57...` shows that, within the execution-verification surface:

- 19 previously verified files are unchanged;
- 10 previously verified files are modified;
- 3 files are new.

Therefore the 19 unchanged files inherit their exact previously verified Git blobs. The 13 modified/new files were independently compared against the locally verified v1.5 bytes using Git's canonical blob hash.

Result:

- inherited unchanged exact blobs: **19/19**;
- modified/new exact blob matches: **13/13**;
- total execution-verification surface: **32/32 exact**;
- mismatches: **0**.

## Frozen 32-file Git-blob manifest

```text
4f4fa480769bc8fec96f0ff96cbd18cf716625d6  cea_arc3/__init__.py
d299aefbb90fcab3f872917d6ce4467fcf8b88b8  cea_arc3/arms.py
6a9b9c6ddbe4bc050db04ae5543260b53afd6bd0  cea_arc3/authority.py
225d62543a531e51802f7d0666a91be375e48a7f  cea_arc3/core.py
864ed7c978bdd8e63ff7a11a2481d533e0208ab2  cea_arc3/corrections.py
f2a80f16628ecd74a9c9a611ebf1da16bb65671f  cea_arc3/descriptors.py
b723d592a8bfb8053ff598d80a75e77bc30af83b  cea_arc3/firewall.py
31c92c0e52549b6be9035ee374492c4f31f1d872  cea_arc3/hypotheses.py
10b64010c031136ca33d5f6b09a9349db572fcdc  cea_arc3/logger.py
dddfc56c85aecccc2aa8127ea6418ebe7034d0f9  cea_arc3/metrics.py
ded09a1d16bbb648bb43bd25e106231451a15b84  cea_arc3/policies.py
bc9d147816d6730b8d49571e2819859f9d715adf  cea_arc3/provenance.py
22fbafc52690b48fe17e08d9f319e2da3ac092ea  cea_arc3/reducer.py
5948da78c646d23d9f70df0cac7a5adabe72880d  cea_arc3/runner.py
a5b42b0fcfaa91826e79ce746b008e2d8b013aaf  cea_arc3/state.py
86e5c7b302c22a41eee3511132a0fe7676bd558b  cea_arc3/transition.py
8308539b59afa1a22fc7a0290c6a685d16119b3a  run_dev_matrix.py
1f2b76726f90d8d878a743d90d3a2927f23ff93d  test_implementation.py
cc922b61cce01c5b94e4e3666245472edc243a03  tests/test_authority.py
d51bef47b9186e4e2c13015fa0c9147d5a048cea  tests/test_core.py
99b252589f3ebc8cbb3df9c602eb2317b4ce0034  tests/test_corrections.py
610a4090d4986e7ab3859f030416e8b4d0031fa4  tests/test_descriptors.py
4334c01cc2cc5a4a6bb425c569a5650c6b979f8e  tests/test_firewall.py
5352749f429e59dae2afbe78e67e090f54c46002  tests/test_hypotheses.py
55aab0380782b8f8384794ffd360e049350be118  tests/test_logger.py
b655d1e07fdfc041a9c5b4114f952a7eee3ab246  tests/test_persistence.py
450f2a337273cf51d34b9abfb5929e8528f209ff  tests/test_policies.py
6dcd8b10405be9aad974ade4ceb2dc53d73705ab  tests/test_provenance.py
e9a2310f34061918806bc52af03ea467bb150877  tests/test_runner.py
6b3f8a553b70217bda3f81dd886d3fad2385101a  tests/test_state.py
bc53c3f6250d5850abd00aeb9c37406af5dea16f  tests/test_transition.py
eb10676f8114f65ea7f4bfb04c48c53f00b8e31e  tests/test_v14_conformance.py
```

## Fresh byte-equivalent materialization

As in the earlier verification, the execution container is not treated as having completed a network Git checkout. Instead, only the byte-verified files were copied into a fresh empty verification directory after equality was established.

From that fresh 32-file materialization, with Python bytecode writing disabled:

`PYTHONDONTWRITEBYTECODE=1 python -m pytest -q`

Result:

`67 passed in 0.23s`

No ARC environment was instantiated by this verification.

## Supplementary non-tuning control

Before repository transfer was finalized, the repaired implementation was compared with v1.3 on a deterministic 100-step synthetic interaction trace for all 16 frozen arms. Actions, ACTION6 coordinates, primary predictions, selected correction claims/sources, canonical-memory membership, and promotion counts were identical for 16/16 arms.

This is bounded evidence against opportunistic behavioral mutation on that synthetic surface. It is not universal behavioral equivalence.

## Environment-exposure state

During v1.5 repair and repository verification:

- ARC development execution: **NO**;
- ARC environment instantiation by the implementation: **NO**;
- comparative ARC outcome observed: **NO**;
- sealed-holdout exposure: **0**;
- environment source inspection: **0**.

## Authority consequence

The execution-readiness gate is conjunctive:

`Spec Frozen AND Reachable Byte Identity AND Fresh-Materialization Conformance`.

For v1.5:

- `Spec Frozen = YES`;
- `Reachable Byte Identity = 32/32 EXACT`;
- `Fresh-Materialization Conformance = 67/67 PASS`.

Therefore:

`REPOSITORY_IMPLEMENTATION_VERIFIED_v1.5 = EARNED`

and:

`EXECUTION_READY_v1.5 = EARNED`.

This licenses only the preregistered development-only execution. It licenses no CEA component or composition claim.

## Next authorized operation

Execute the frozen v1.5 artifact on the 18 DEVELOPMENT games only, under the frozen 16-arm matrix and 256 non-RESET action budget per arm/game pair.

The seven SEALED_HOLDOUT games remain excluded.
