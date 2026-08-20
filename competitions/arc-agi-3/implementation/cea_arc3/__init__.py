"""ARC3 CEA mechanism-isolation implementation substrate."""

from .state import (
    CanonicalEntry,
    EvidenceRecord,
    GoalState,
    Hypothesis,
    LineageState,
    RawHistory,
    RepresentationalState,
    TransitionRecord,
)
from .transition import TransitionModel, transition_record_from_arrays
from .hypotheses import HypothesisManager
from .authority import AuthorityGate, AuthorizationDecision
from .policies import AIECPolicy, FixedAllocationPolicy, action6_schedule

__all__ = [
    "CanonicalEntry",
    "EvidenceRecord",
    "GoalState",
    "Hypothesis",
    "LineageState",
    "RawHistory",
    "RepresentationalState",
    "TransitionRecord",
    "TransitionModel",
    "transition_record_from_arrays",
    "HypothesisManager",
    "AuthorityGate",
    "AuthorizationDecision",
    "AIECPolicy",
    "FixedAllocationPolicy",
    "action6_schedule",
]
