from pathlib import Path
import pytest

from cea_arc3.firewall import DEVELOPMENT_GAMES, SEALED_HOLDOUT, SealedHoldoutAccessError, assert_development_slug, assert_isolated_root


def test_sealed_slug_fails_closed():
    for slug in SEALED_HOLDOUT:
        with pytest.raises(SealedHoldoutAccessError):
            assert_development_slug(slug)


def test_all_development_slugs_allowed():
    for slug in DEVELOPMENT_GAMES:
        assert_development_slug(slug)


def test_root_with_sealed_dir_is_rejected(tmp_path: Path):
    for slug in DEVELOPMENT_GAMES:
        (tmp_path/slug).mkdir()
    (tmp_path/'cn04').mkdir()
    with pytest.raises(RuntimeError):
        assert_isolated_root(tmp_path)
