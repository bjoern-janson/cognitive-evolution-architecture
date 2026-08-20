from pathlib import Path
import pytest
from cea_arc3.firewall import DEVELOPMENT_GAMES, SealedHoldoutAccessError
from cea_arc3.runner import DevelopmentRunner


def isolated_root(tmp_path: Path):
    for slug in DEVELOPMENT_GAMES:
        (tmp_path/slug).mkdir()
    return tmp_path


def test_runner_rejects_sealed_before_arcade_factory_called(tmp_path: Path):
    root=isolated_root(tmp_path); called=[]
    def factory(_):
        called.append(True)
        raise AssertionError('must not be called')
    r=DevelopmentRunner(root,arcade_factory=factory)
    with pytest.raises(SealedHoldoutAccessError):
        r.run_game('cn04','B')
    assert called==[]


def test_budget_cannot_be_silently_changed(tmp_path: Path):
    root=isolated_root(tmp_path)
    r=DevelopmentRunner(root,arcade_factory=lambda _: None)
    with pytest.raises(ValueError):
        r.run_game('ar25','B',action_budget=255)
