#!/usr/bin/env python3
"""Create an isolated ARC-AGI-3 development-only environment root.

This script validates only top-level game directory names before copying.
It traverses/copies content only for DEVELOPMENT games and never traverses
SEALED_HOLDOUT directories.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPLIT_PATH = HERE.parent / "manifests" / "ARC3_SEALED_SPLIT.json"


def _slug(game_id: str) -> str:
    return game_id.split("-", 1)[0]


def load_split() -> tuple[set[str], set[str]]:
    data = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    development = {_slug(x) for x in data["development"]}
    sealed = {_slug(x) for x in data["sealed_holdout"]}

    assert len(development) == 18
    assert len(sealed) == 7
    assert development.isdisjoint(sealed)
    assert len(development | sealed) == 25
    return development, sealed


def prepare(source_root: Path, target_root: Path) -> None:
    development, sealed = load_split()
    expected = development | sealed

    if not source_root.is_dir():
        raise FileNotFoundError(f"Environment root not found: {source_root}")

    # Names only: do not recursively inspect any source game here.
    live = {p.name for p in source_root.iterdir() if p.is_dir()}
    if live != expected:
        missing = sorted(expected - live)
        unexpected = sorted(live - expected)
        raise RuntimeError(
            "ARC3 public corpus drift detected. "
            f"missing={missing}, unexpected={unexpected}"
        )

    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True, exist_ok=True)

    for game_slug in sorted(development):
        source = source_root / game_slug
        target = target_root / game_slug
        shutil.copytree(source, target)

    exposed = {p.name for p in target_root.iterdir() if p.is_dir()}
    if exposed != development:
        raise AssertionError("Development-root contents differ from frozen split")
    if exposed & sealed:
        raise AssertionError("Sealed holdout leaked into development root")

    print("Development-only environment root created.")
    print(f"path: {target_root}")
    print(f"games exposed: {len(exposed)}")
    print(f"sealed games exposed: {len(exposed & sealed)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    parser.add_argument("target_root", type=Path)
    args = parser.parse_args()
    prepare(args.source_root, args.target_root)


if __name__ == "__main__":
    main()
