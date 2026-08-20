# ARC-AGI-3 Experiment 2 — Development Corpus Inventory

Status: **metadata-only development exposure**

This inventory was derived from the uploaded Kaggle competition bundle after the 18/7 development/holdout split was frozen. Only `metadata.json` files for the 18 `DEVELOPMENT` games were read. No `SEALED_HOLDOUT` source or metadata was opened.

## Boundary

- Development games: 18
- Sealed holdout games: 7
- Development levels represented by metadata: 134
- Levels per development game: 6–9
- Human-baseline action counts observed in development metadata: 6–442

## Development games

| game | version | levels | interaction tag |
|---|---|---:|---|
| ar25 | 0c556536 | 8 | keyboard_click |
| bp35 | 0a0ad940 | 9 | keyboard_click |
| cd82 | fb555c5d | 6 | keyboard_click |
| ft09 | 0d8bbf25 | 6 | untagged |
| g50t | 5849a774 | 7 | keyboard |
| ka59 | 38d34dbb | 7 | keyboard_click |
| ls20 | 9607627b | 7 | keyboard |
| r11l | 495a7899 | 6 | click |
| re86 | 8af5384d | 8 | keyboard_click |
| s5i5 | 18d95033 | 8 | click |
| sb26 | 7fbdac44 | 8 | keyboard_click |
| sc25 | 635fd71a | 6 | keyboard_click |
| sk48 | d8078629 | 8 | keyboard_click |
| sp80 | 589a99af | 6 | keyboard_click |
| su15 | 1944f8ab | 9 | click |
| tu93 | 0768757b | 9 | keyboard_click |
| vc33 | 5430563c | 7 | click |
| wa30 | ee6fef47 | 9 | keyboard |

Interaction-tag distribution:

- `keyboard_click`: 10
- `keyboard`: 3
- `click`: 4
- untagged: 1

## Epistemic status

This inventory establishes only corpus shape and metadata-visible interaction classes. It does **not** establish mechanics, goals, transition rules, representation requirements, CEA component necessity, or any empirical advantage.

The next authorized exposure is **interface-first black-box probing** of the 18 development games. Game implementation source remains unnecessary at this stage and should not be inspected unless a later engineering/debugging requirement justifies it.
