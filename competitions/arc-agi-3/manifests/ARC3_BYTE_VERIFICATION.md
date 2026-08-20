# ARC-AGI-3 Kaggle bundle byte verification

Date: 2026-08-20

## Input

- Uploaded Kaggle archive: `arc-prize-2026-arc-agi-3.zip`
- ZIP SHA-256: `c72400a32db5e48da9014baf893b48016b300e9a6a77bd5d505de2b1ec61d645`
- Frozen mirror manifest SHA-256: `7c91a79a2b5c8ebedc2ab0b125fe133ff28a95c92be5be931ae31633b5f2c327`

## Non-semantic verification result

- Public game slugs discovered from archive paths: **25**
- `*.py` environment implementations: **25**
- `metadata.json` files: **25**
- Version tokens matching frozen mirror: **25/25**
- Implementation Git-blob hashes matching mirror: **0/25**
- Metadata Git-blob hashes matching mirror: **0/25**

Result: **the mirror preserved the same slug/version naming but is not byte-identical to the actual Kaggle bundle.** The mirror byte witness is therefore superseded for authoritative byte provenance. It remains preserved as a failed witness.

No `*.py` or `metadata.json` contents were parsed, printed, summarized, or semantically inspected during this verification. Only archive paths, byte lengths, SHA-256 hashes, and Git object hashes were computed.

## Sealed split

The sealed assignment remains unchanged because it was defined from game slugs only, not mirror file hashes.

- `SEALED_HOLDOUT`: cn04, dc22, lf52, lp85, m0r0, tn36, tr87
- Role counts: {"DEVELOPMENT": 18, "SEALED_HOLDOUT": 7}

## Authoritative replacement manifest

- `ARC3_PROV_MANIFEST_KAGGLE_V1.csv`
- SHA-256: `adcfc775844a5a817cd81d82eb16511c9f489f81dc838b3b5e8de06c8baface0`

This manifest is now the authoritative byte-level provenance record for the uploaded Kaggle bundle.

## Authority state

`MIRROR_BYTE_WITNESS = FALSIFIED`

`KAGGLE_BYTE_MANIFEST = VERIFIED_FROM_UPLOADED_ARCHIVE`

`SEALED_SPLIT = UNCHANGED`

`SEALED_MECHANICS_INSPECTED = NO`
