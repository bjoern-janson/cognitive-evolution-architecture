# ARC-AGI-3 — CEA Experiment 2

ARC-AGI-3 is the second proving ground for the Cognitive Evolution Architecture (CEA). It is an interactive environment benchmark rather than a static prediction task, so the implementation is intentionally fresh while the frozen CEA conception and epistemic laws remain unchanged.

## Current epistemic state

- `CEA_CONCEPTION`: frozen before ARC-AGI-3.
- `ARC3_CONCEPTUAL_FIT`: high; this is not evidence of CEA advantage.
- `ARC3_PUBLIC_CORPUS`: 25 games, verified from the uploaded Kaggle competition archive.
- `DEVELOPMENT`: 18 public games.
- `SEALED_HOLDOUT`: 7 public games.
- `SEALED_MECHANICS_INSPECTED`: no.
- `ARC3_CEA_IMPLEMENTATION`: not yet earned.
- `CEA_WITNESS`: not earned.
- `OFFICIAL_ARC3_SUBMISSIONS_SPENT`: 0 at this freeze.

The next authorized step is to expose and study only the 18 development games and let observed pressure constrain the first ARC-specific realization of `L + C + A + X`.

## Frozen public split

### Development — 18

`ar25`, `bp35`, `cd82`, `ft09`, `g50t`, `ka59`, `ls20`, `r11l`, `re86`, `s5i5`, `sb26`, `sc25`, `sk48`, `sp80`, `su15`, `tu93`, `vc33`, `wa30`

### Sealed holdout — 7

`cn04`, `dc22`, `lf52`, `lp85`, `m0r0`, `tn36`, `tr87`

The assignment is slug-stable and was frozen before inspecting environment-file mechanics. Some public games had already been contaminated by secondary-source/replay exposure during benchmark research; those were forced into development rather than permitted into holdout.

## Provenance

Authoritative uploaded Kaggle archive SHA-256:

`c72400a32db5e48da9014baf893b48016b300e9a6a77bd5d505de2b1ec61d645`

Authoritative Kaggle byte manifest:

`manifests/ARC3_PROV_MANIFEST_KAGGLE_V1.csv`

Manifest SHA-256:

`adcfc775844a5a817cd81d82eb16511c9f489f81dc838b3b5e8de06c8baface0`

The earlier public-mirror byte witness was falsified: all 25 version-directory tokens matched while 0/25 implementation blobs and 0/25 metadata blobs matched the Kaggle bytes. The failed witness is preserved in `manifests/ARC3_BYTE_VERIFICATION.md` rather than silently overwritten.

## Development firewall

Any ARC local-runtime initialization must point at a development-only environment root containing the 18 allowed games. Do not point the toolkit at the original 25-game `environment_files/` root during development because toolkit discovery may recursively inspect metadata.

Use:

```bash
python competitions/arc-agi-3/scripts/prepare_dev_env.py \
  /path/to/environment_files \
  /path/to/arc3_development_envs
```

The script verifies the 25-slug corpus and copies only the 18 development directories into the target root. The seven sealed directories are never traversed by the copy operation.

## Deployment boundary

GitHub is the development/provenance source of truth. Kaggle is the execution boundary.

```text
Git source
  -> tests / development experiments
  -> generated submission notebook
  -> Kaggle Save & Run All
  -> competition rerun on hidden games
  -> submission.parquet
  -> RHAE / leaderboard result
```

The Kaggle notebook is a deployment artifact, not the canonical source. Hidden evaluation must not depend on fetching GitHub because competition reruns are offline.

## Governing distinction

`same architecture != same implementation`

Trace the Ace operationalized CEA for static outcome prediction. ARC-AGI-3 must earn its own representation, correction, exploration, and authority mechanisms from interactive evidence.
