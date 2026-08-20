from __future__ import annotations

from pathlib import Path

DEVELOPMENT_GAMES = frozenset({"ar25","bp35","cd82","ft09","g50t","ka59","ls20","r11l","re86","s5i5","sb26","sc25","sk48","sp80","su15","tu93","vc33","wa30"})
SEALED_HOLDOUT = frozenset({"cn04","dc22","lf52","lp85","m0r0","tn36","tr87"})

class SealedHoldoutAccessError(RuntimeError):
    pass

def assert_development_slug(slug: str) -> None:
    if slug in SEALED_HOLDOUT:
        raise SealedHoldoutAccessError(f"ACCESS DENIED: {slug} is SEALED_HOLDOUT")
    if slug not in DEVELOPMENT_GAMES:
        raise ValueError(f"unknown ARC3 development game: {slug}")

def development_game_path(root: Path, slug: str) -> Path:
    assert_development_slug(slug)
    path = Path(root) / slug
    if not path.is_dir():
        raise FileNotFoundError(path)
    return path

def assert_isolated_root(root: Path) -> None:
    root = Path(root)
    exposed = {p.name for p in root.iterdir() if p.is_dir()}
    if exposed != DEVELOPMENT_GAMES:
        raise RuntimeError(f"development root mismatch: missing={sorted(DEVELOPMENT_GAMES-exposed)} unexpected={sorted(exposed-DEVELOPMENT_GAMES)}")
    leaked = exposed & SEALED_HOLDOUT
    if leaked:
        raise SealedHoldoutAccessError(f"sealed games exposed: {sorted(leaked)}")
