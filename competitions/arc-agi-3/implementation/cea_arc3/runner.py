from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np

from .arms import ARMS, ArmConfig
from .core import MechanismCore
from .descriptors import describe_observation
from .firewall import assert_development_slug, assert_isolated_root
from .logger import EventLogger
from .state import GoalState, RepresentationalState
from .transition import action_mask, frame_sha256, transition_record_from_arrays

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
    seed: int
    actions: int
    levels_completed: int
    terminal_state: str
    transition_nll: float
    parent_transition_nll: float
    secondary_nll: dict[str, float]
    per_level_primary_nll: dict[int, float]
    aliasing_triggers: int
    admitted_claims: int
    forward_supported_claims: int
    provisional_applications: int
    canonical_applications: int
    total_promotions: int
    ungated_promotions: int
    eligible_promotion_events: int
    unauthorized_rate: float
    false_refusal_strict: float
    false_refusal_including_capacity: float
    capacity_refusals: int
    localization_violations: int
    policy_counts: dict[str, int]


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
        logger = EventLogger(self.log_dir / f"{game_slug}.{config.name}.seed{seed}.jsonl") if self.log_dir else None
        current = env.observation_space
        actions = 0

        if logger:
            logger.append("run_start", {
                "game_slug": game_slug,
                "arm": config.name,
                "seed": int(seed),
                "action_budget": int(action_budget),
                "environment_membership_count": len(envs),
            })

        while actions < action_budget and state_name(current) not in {"WIN", "GAME_OVER"}:
            before_arr = visible_array(current)
            before_hash = frame_sha256(before_arr)
            avail = available_action_ids(current)
            descriptor = describe_observation(before_arr, avail)
            goal = GoalState(
                environment_state=state_name(current),
                levels_completed=int(current.levels_completed),
                live_action_mask=action_mask(avail),
                remaining_action_budget=int(action_budget - actions),
                remaining_wallclock_budget=None,
            )
            # Materialize the frozen R/G state. The current frame exists only for
            # the live decision and is never serialized as historical evidence.
            _r_state = RepresentationalState(
                current_frame=before_arr,
                descriptor=descriptor,
                raw_window=core.history,
                distinctions=dict(core.hypotheses.live) if config.L else {},
            )

            aid, coord, policy_mode = core.choose_action(before_hash, avail)
            core.metrics.record_policy(policy_mode)
            if aid == 0:
                if logger:
                    logger.append("no_action_available", {
                        "game_slug": game_slug,
                        "arm": config.name,
                        "seed": int(seed),
                        "step": actions,
                        "goal": asdict(goal),
                        "descriptor": asdict(descriptor),
                    })
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

            audit_events = core.observe(prediction=pred, record=record, current_frame_hash_before=before_hash)
            core.metrics.action_count += 1
            actions += 1

            if logger:
                score = core.metrics.predictions[-1]
                logger.append("transition", {
                    "game_slug": game_slug,
                    "arm": config.name,
                    "seed": int(seed),
                    "step": actions - 1,
                    "action_legal": True,
                    "policy_mode": policy_mode,
                    "action_token": aid,
                    "action_coordinate": coord,
                    "descriptor": asdict(descriptor),
                    "goal": asdict(goal),
                    "prediction": {
                        "p_change": pred.probability_change,
                        "parent_p_change": pred.parent_probability,
                        "secondary": pred.secondary_probabilities,
                        "claim_id": pred.claim_id,
                        "correction_source": pred.correction_source,
                    },
                    "score": asdict(score),
                    "transition": record,
                })
                for kind, payload in audit_events:
                    logger.append(kind, payload)
            current = after

        result = RunResult(
            game_slug=game_slug,
            arm=config.name,
            seed=int(seed),
            actions=actions,
            levels_completed=int(current.levels_completed),
            terminal_state=state_name(current),
            transition_nll=core.metrics.transition_nll(),
            parent_transition_nll=core.metrics.parent_transition_nll(),
            secondary_nll=core.metrics.secondary_nll(),
            per_level_primary_nll=core.metrics.per_level_primary_nll(),
            aliasing_triggers=len(core.metrics.aliasing_trigger_keys),
            admitted_claims=len(core.metrics.admitted_claims),
            forward_supported_claims=len(core.metrics.forward_supported_claims),
            provisional_applications=core.metrics.provisional_applications,
            canonical_applications=core.metrics.canonical_applications,
            total_promotions=core.metrics.total_promotions,
            ungated_promotions=core.metrics.ungated_promotions,
            eligible_promotion_events=core.metrics.eligible_promotion_events,
            unauthorized_rate=core.metrics.unauthorized_rate(),
            false_refusal_strict=core.metrics.false_refusal_strict(),
            false_refusal_including_capacity=core.metrics.false_refusal_including_capacity(),
            capacity_refusals=core.metrics.capacity_refusals,
            localization_violations=core.metrics.localization_violations,
            policy_counts=dict(core.metrics.policy_counts),
        )

        if logger:
            # End snapshots make durable Lambda_t completeness directly auditable.
            logger.append("lineage_snapshot", {
                "evidence": {k: asdict(v) for k, v in sorted(core.lineage.evidence.items())},
                "claims": {k: asdict(v) for k, v in sorted(core.lineage.claims.items())},
                "decisions": {k: asdict(v) for k, v in sorted(core.lineage.decisions.items())},
            })
            logger.append("canonical_snapshot", {
                "entries": {k: asdict(v) for k, v in sorted(core.memory.entries.items())}
            })
            logger.append("run_summary", asdict(result))
        return result

    @staticmethod
    def _expected_games():
        from .firewall import DEVELOPMENT_GAMES
        return DEVELOPMENT_GAMES
