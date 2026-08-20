from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, median
from typing import Optional


@dataclass
class PredictionEvent:
    game_slug: str
    level: int
    step: int
    arm: str
    parent_nll: float
    emitted_nll: float
    z_change: int
    claim_id: Optional[str] = None
    scope_matched: bool = False


@dataclass
class MetricsLedger:
    predictions: list[PredictionEvent] = field(default_factory=list)
    unauthorized_promotions: int = 0
    total_promotions: int = 0
    false_refusals: int = 0
    capacity_refusals: int = 0
    eligible_promotion_events: int = 0
    action_count: int = 0
    localization_violations: int = 0

    def transition_nll(self) -> float:
        return mean([e.emitted_nll for e in self.predictions]) if self.predictions else float("nan")

    def unauthorized_rate(self) -> float:
        return self.unauthorized_promotions / max(1, self.total_promotions)

    def false_refusal_strict(self) -> float:
        return self.false_refusals / max(1, self.eligible_promotion_events)

    def false_refusal_including_capacity(self) -> float:
        return (self.false_refusals + self.capacity_refusals) / max(1, self.eligible_promotion_events)


def paired_persistence_summary(differences: list[float]) -> dict[str, float | int]:
    if not differences:
        return {"n": 0, "mean_nll_difference": float("nan"), "median_nll_difference": float("nan"), "fraction_improved": float("nan")}
    return {
        "n": len(differences),
        "mean_nll_difference": mean(differences),
        "median_nll_difference": median(differences),
        "fraction_improved": sum(d < 0 for d in differences) / len(differences),
    }
