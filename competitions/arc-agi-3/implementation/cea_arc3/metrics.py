from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, median
from typing import Any, Optional


@dataclass
class PredictionEvent:
    game_slug: str
    level: int
    step: int
    arm: str
    parent_nll: float
    emitted_nll: float
    z_change: int
    bucket_nll: float
    state_delta_nll: float
    level_delta_nll: float
    action_surface_nll: float
    exact_return_nll: float
    claim_id: Optional[str] = None
    correction_source: Optional[str] = None
    scope_matched: bool = False


@dataclass
class MetricsLedger:
    predictions: list[PredictionEvent] = field(default_factory=list)
    unauthorized_promotions: int = 0
    total_promotions: int = 0
    ungated_promotions: int = 0
    false_refusals: int = 0
    capacity_refusals: int = 0
    eligible_promotion_events: int = 0
    action_count: int = 0
    localization_violations: int = 0
    policy_counts: dict[str, int] = field(default_factory=dict)
    aliasing_trigger_keys: set[tuple[Any, ...]] = field(default_factory=set)
    forward_supported_claims: set[str] = field(default_factory=set)
    admitted_claims: set[str] = field(default_factory=set)
    canonical_applications: int = 0
    provisional_applications: int = 0

    def transition_nll(self) -> float:
        return mean([e.emitted_nll for e in self.predictions]) if self.predictions else float("nan")

    def parent_transition_nll(self) -> float:
        return mean([e.parent_nll for e in self.predictions]) if self.predictions else float("nan")

    def secondary_nll(self) -> dict[str, float]:
        if not self.predictions:
            return {
                "changed_count_bucket": float("nan"),
                "state_delta_class": float("nan"),
                "level_delta_positive": float("nan"),
                "action_surface_changed": float("nan"),
                "exact_return_flag": float("nan"),
            }
        return {
            "changed_count_bucket": mean(e.bucket_nll for e in self.predictions),
            "state_delta_class": mean(e.state_delta_nll for e in self.predictions),
            "level_delta_positive": mean(e.level_delta_nll for e in self.predictions),
            "action_surface_changed": mean(e.action_surface_nll for e in self.predictions),
            "exact_return_flag": mean(e.exact_return_nll for e in self.predictions),
        }

    def per_level_primary_nll(self) -> dict[int, float]:
        out: dict[int, float] = {}
        for level in sorted({e.level for e in self.predictions}):
            vals = [e.emitted_nll for e in self.predictions if e.level == level]
            out[level] = mean(vals)
        return out

    def record_policy(self, mode: str) -> None:
        self.policy_counts[str(mode)] = self.policy_counts.get(str(mode), 0) + 1

    def unauthorized_rate(self) -> float:
        return self.unauthorized_promotions / max(1, self.total_promotions)

    def false_refusal_strict(self) -> float:
        return self.false_refusals / max(1, self.eligible_promotion_events)

    def false_refusal_including_capacity(self) -> float:
        return (self.false_refusals + self.capacity_refusals) / max(1, self.eligible_promotion_events)

    def localization_yield(self) -> float:
        numerator = len(self.forward_supported_claims)
        return numerator / max(1, len(self.aliasing_trigger_keys))


def paired_persistence_summary(differences: list[float]) -> dict[str, float | int]:
    if not differences:
        return {
            "n": 0,
            "mean_nll_difference": float("nan"),
            "median_nll_difference": float("nan"),
            "fraction_improved": float("nan"),
        }
    return {
        "n": len(differences),
        "mean_nll_difference": mean(differences),
        "median_nll_difference": median(differences),
        "fraction_improved": sum(d < 0 for d in differences) / len(differences),
    }
