# ARC-AGI-3 Experiment 2 Protocol

Freeze date: 2026-08-20

## Objective

Test whether CEA's governance of representation, correction, adaptive exploration, and persistence provides measurable benefit in novel interactive environments under matched model, compute, and action budgets.

The scientific object is not merely competitive score. The experiment must separate a competitive agent from a CEA scientific instrument that records hypothesis survival, localized correction, information-acquisition cost, memory reuse, cross-level transfer, false generalization, rule scope, and unauthorized persistence.

## Architecture mapping

- `L` / CLPR: localized, corrigible representation of environment distinctions.
- `C` / Cognitive Core: observe -> predict -> act -> consequence -> evaluate -> correct -> remember.
- `A` / AIEC: allocate scarce actions between information acquisition and exploitation.
- `X` / authority substrate: prevent weak/local evidence from becoming over-scoped persistent rules.

This mapping is a specification target, not an empirical result.

## Strong nulls

- `H0_L`: localized corrigible representation adds no benefit.
- `H0_C`: validated persistent correction adds no benefit.
- `H0_A`: adaptive exploration allocation adds no benefit over a matched fixed exploration policy.
- `H0_X`: warrant-gated persistence adds no benefit over unrestricted memory.
- `H0_Cmp`: `L+C+A+X` has no interaction advantage under matched model, compute, and action budgets.

## Public-game firewall

Public corpus size: 25.

Development slugs:

`ar25 bp35 cd82 ft09 g50t ka59 ls20 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tu93 vc33 wa30`

Sealed holdout slugs:

`cn04 dc22 lf52 lp85 m0r0 tn36 tr87`

For a sealed game, before the first frozen learner evaluation:

- no source inspection;
- no metadata inspection;
- no manual play;
- no replay or walkthrough inspection;
- no game-specific solver research;
- no tuning from its behavior;
- no local-runtime discovery over a root containing it.

Non-semantic path/hash verification is allowed.

## Development-root rule

Do not initialize the ARC local engine against the original 25-game directory. Construct an isolated root containing only the 18 development environments and point local execution there.

`prepare_dev_env.py` is the canonical preparation step on this branch.

## Provenance rule

Every consequential experiment should be traceable to:

`commit SHA + CEA configuration + corpus manifest + factor configuration + run metadata + notebook build + Kaggle version/result`

A generated Kaggle notebook must embed or copy all runtime source required for offline competition execution. It must not depend on network access at hidden-test time.

## Promotion firewall

A high ARC score does not by itself establish CEA advantage, mechanism necessity, interface invention, or composition witness.

Component and composition claims require matched ablations and evidence with discrimination scope at least as strong as the claimed authority.

## Current authorization

Authorized now:

1. Inspect/play/analyze only the 18 development environments.
2. Instrument pressure surfaces before committing to a full ARC-specific `L+C+A+X` implementation.
3. Build strong matched baselines and ablations.
4. Freeze a first learner before opening the seven sealed public games.

Not authorized now:

- inspecting sealed-game mechanics;
- calling public-development performance private-test evidence;
- promoting semantic overlap with prior-art agents to novelty;
- promoting conceptual fit to CEA evidence;
- submitting the untouched Stochastic Goose template merely to test Kaggle plumbing.
