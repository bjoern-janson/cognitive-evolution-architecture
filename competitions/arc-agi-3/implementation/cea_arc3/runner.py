from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np

from .arms import ARMS, ArmConfig
from .core import MechanismCore
from .firewall import assert_development_slug, assert_isolated_root
from .logger import EventLogger
from .transition import frame_sha256, transition_record_from_arrays

ACTION_BUDGET = 256


def visible_array(frame: Any) -> np.ndarray:
    arr = np.asarray(frame.frame)
    if arr.ndim == 3:
        arr = arr[-1]
    arr = np.asarray(arr)
    if arr.shape != (64, 64):
        raise ValueError(f"expected 64x64 visible frame, got {arr.shape}")
    return arr


def available_action_ids(frame: Any) -> list[int]:
    return [int(x.value if hasattr(x, "value") else x) for x in (frame.available_actions or [])]


def state_name(frame: Any) -> str:
    s = frame.state
    return str(s.name if hasattr(s, "name") else s)


@dataclass
class RunResult:
    game_slug: str
    arm: str
    actions: int
    levels_completed: int
    terminal_state: str
    transition_nll: float
    total_promotions: int
    unauthorized_rate: float
    false_refusal_strict: float


class DevelopmentRunner:
    """Development-only ARC runner with a fail-closed 18-game corpus boundary."""

    def __init__(
        self,
        environment_root: Path,
        *,
        arcade_factory: Optional[Callable[[Path], Any]] = None,
        log_dir: Optional[Path] = None,
    ) -> None:
        self.environment_root = Path(environment_root)
        assert_isolated_root(self.environment_root)
        self.arcade_factory = arcade_factory
        self.log_dir = Path(log_dir) if log_dir else None

    def _arcade(self):
        if self.arcade_factory is not None:
            return self.arcade_factory(self.environment_root)
        from arc_agi import Arcade, OperationMode
        return Arcade(operation_mode=OperationMode.OFFLINE, environments_dir=str(self.environment_root))

    def run_game(self, game_slug: str, arm: str | ArmConfig, *, seed: int = 0, action_budget: int = ACTION_BUDGET) -> RunResult:
        assert_development_slug(game_slug)
        if action_budget != ACTION_BUDGET:
            raise ValueError(f"v1.x development action budget is frozen at {ACTION_BUDGET}")
        config = ARMS[arm] if isinstance(arm, str) else arm
        arcade = self._arcade()
        envs = {e.game_id.split("-", 1)[0]: e.game_id for e in arcade.available_environments}
        if set(envs) != set(self._expected_games()):
            raise RuntimeError("runtime environment membership drift")
        game_id = envs[game_slug]
        env = arcade.make(game_id, seed=seed)
        if env is None or env.observation_space is None:
            raise RuntimeError(f"failed to initialize development game {game_slug}")

        core = MechanismCore(config, game_slug)
        logger = EventLogger(self.log_dir / f"{game_slug}.{config.name}.jsonl") if self.log_dir else None
        current = env.observation_space
        actions = 0

        while actions < action_budget and state_name(current) not in {"WIN", "GAME_OVER"}:
            before_arr = visible_array(current)
            before_hash = frame_sha256(before_arr)
            avail = available_action_ids(current)
            aid, coord, policy_mode = core.choose_action(before_hash, avail)
            if aid == 0:
                break
            if aid not in avail:
                raise RuntimeError(f"policy selected unavailable action {aid}")
            pred = core.predict_action(
                action_token=aid,
                action_coordinate=coord,
                current_frame_hash=before_hash,
                available_actions=avail,
            )

            from arcengine import GameAction
            action = GameAction.from_id(aid)
            if aid == 6:
                if coord is None:
                    raise RuntimeError("ACTION6 requires coordinate")
                after = env.step(action, {"x": int(coord[0]), "y": int(coord[1])})
            else:
                after = env.step(action)
            if after is None:
                raise RuntimeError("environment step returned None")

            after_arr = visible_array(after)
            prior_hashes = [r.pre_frame_hash for r in core.history] + [r.post_frame_hash for r in core.history]
            record = transition_record_from_arrays(
                before=before_arr,
                after=after_arr,
                action_token=aid,
                action_coordinate=coord,
                state_before=state_name(current),
                state_after=state_name(after),
                level_before=int(current.levels_completed),
                level_after=int(after.levels_completed),
                available_actions_before=avail,
                available_actions_after=available_action_ids(after),
                prior_hashes=prior_hashes,
            )
            core.observe(prediction=pred, record=record, current_frame_hash_before=before_hash)
            core.metrics.action_count += 1
            actions += 1
            if logger:
                logger.append("transition", {
                    "game_slug": game_slug,
                    "arm": config.name,
                    "step": actions - 1,
                    "policy_mode": policy_mode,
                    "prediction": {
                        "p_change": pred.probability_change,
                        "parent_p_change": pred.parent_probability,
                        "claim_id": pred.claim_id,
                        "correction_source": pred.correction_source,
                    },
                    "transition": record,
                })
            current = after

        return RunResult(
            game_slug=game_slug,
            arm=config.name,
            actions=actions,
            levels_completed=int(current.levels_completed),
            terminal_state=state_name(current),
            transition_nll=core.metrics.transition_nll(),
            total_promotions=core.metrics.total_promotions,
            unauthorized_rate=core.metrics.unauthorized_rate(),
            false_refusal_strict=core.metrics.false_refusal_strict(),
        )

    @staticmethod
    def _expected_games():
        from .firewall import DEVELOPMENT_GAMES
        return DEVELOPMENT_GAMES
