import json
import sys
import types
from pathlib import Path

import numpy as np

from cea_arc3.arms import ARMS
from cea_arc3.authority import AuthorityGate
from cea_arc3.core import MechanismCore
from cea_arc3.descriptors import describe_observation
from cea_arc3.firewall import DEVELOPMENT_GAMES
from cea_arc3.logger import EventLogger
from cea_arc3.provenance import proposal_snapshot_from_hypothesis, proposal_snapshot_hash
from cea_arc3.runner import DevelopmentRunner
from cea_arc3.state import CanonicalEntry, CanonicalMemory, ClaimRecord, GoalState, Hypothesis, LineageState, TransitionRecord
from cea_arc3.transition import STATE_DELTA_CLASSES, TransitionModel, action_mask


def test_v14_descriptor_uses_smallest_modal_color_on_tie():
    a = np.zeros((64, 64), dtype=np.uint8)
    a.flat[:2048] = 3
    d = describe_observation(a, [1])
    assert d.color_histogram[0] == 2048
    assert d.color_histogram[3] == 2048
    assert d.modal_color_id == 0
    assert d.non_modal_cells == 2048


def test_v14_goal_wallclock_is_explicitly_null_in_development():
    g = GoalState("NOT_FINISHED", 0, 2, 256, None)
    assert g.remaining_wallclock_budget is None


def test_v14_secondary_heads_are_prequential_unit_priors_and_base_only():
    m = TransitionModel()
    from cea_arc3.state import RawHistory
    h = RawHistory()
    mask = action_mask([1])
    ctx = m.base_context(1, None, h, mask)
    sec = m.predict_secondary(ctx)
    assert sec["changed_count_bucket"] == (1/7,) * 7
    assert sec["state_delta_class"] == (1/3,) * 3
    assert sec["level_delta_positive"] == 0.5
    assert sec["action_surface_changed"] == 0.5
    assert sec["exact_return_flag"] == 0.5
    vals = m.predicate_values(h, "x", mask)
    m.update(
        context=ctx,
        predicate_values=vals,
        z_change=1,
        bucket=3,
        state_delta="WIN",
        level_delta_positive=1,
        action_surface_changed=1,
        exact_return_flag=1,
    )
    sec2 = m.predict_secondary(ctx)
    assert sec2["changed_count_bucket"][3] > sec["changed_count_bucket"][3]
    assert sec2["state_delta_class"][STATE_DELTA_CLASSES.index("WIN")] > sec["state_delta_class"][1]
    assert sec2["level_delta_positive"] > 0.5
    assert all(not hasattr(cell, "state_delta") for cell in m.q.values())


def _eligible_hypothesis():
    h = Hypothesis(
        "h", (1, None, "START", "START", 2), "prev2_z", 1,
        ((1, None, "START", "START", 2), "prev2_z", 1),
        proposal_gain_nll=1.0,
        proposal_snapshot_counts=((2, 2, (0,0,0,0,0,0,0)), (1, 1, (0,0,0,0,0,0,0))),
        forward_support=5,
        forward_gain_nll=3.0,
        forward_event_gains=[0.6] * 5,
        sibling_support=4,
        evidence_ids=[f"e{i}" for i in range(5)],
        sibling_evidence_ids=[f"e{i}" for i in range(5, 9)],
    )
    h.proposal_snapshot_hash = proposal_snapshot_hash(proposal_snapshot_from_hypothesis(h))
    return h


def test_v14_capacity_refusal_is_eligible_but_not_authorized():
    from cea_arc3.state import EvidenceRecord
    h = _eligible_hypothesis()
    lineage = LineageState()
    lineage.add_claim(ClaimRecord(h.claim_id, None, h.proposal_snapshot_hash, (h.predicate_id, h.predicate_value), h.scope, h.status))
    for i in range(9):
        lineage.add_evidence(EvidenceRecord(f"e{i}", "ar25", 0, i, "f", "w", 1, None, (1,)))
    memory = CanonicalMemory()
    for i in range(64):
        memory.add(CanonicalEntry(f"x{i}", ("s",), 0.0, (), f"a{i}", 0, 0, 0))
    d = AuthorityGate().evaluate(h, lineage, memory, created_level=0, created_step=0, local_predictive_delta=0.2)
    assert d.eligible
    assert not d.authorize
    assert d.reason_code == "CAPACITY_REFUSAL"


def test_v14_x_refusal_is_durably_added_to_lineage():
    c = MechanismCore(ARMS["B+L+C+A+X"], "ar25")
    h = Hypothesis(
        "h", (1, None, "START", "START", 2), "prev2_z", 1,
        ((1, None, "START", "START", 2), "prev2_z", 1),
        proposal_gain_nll=0.1,
        proposal_snapshot_counts=((1, 1, (0,0,0,0,0,0,0)), (1, 0, (0,0,0,0,0,0,0))),
    )
    h.proposal_snapshot_hash = proposal_snapshot_hash(proposal_snapshot_from_hypothesis(h))
    c.hypotheses.live[h.claim_id] = h
    c.lineage.add_claim(ClaimRecord(h.claim_id, None, h.proposal_snapshot_hash, (h.predicate_id, h.predicate_value), h.scope, h.status))
    audit = c._maybe_promote_all()
    assert len(c.lineage.decisions) == 1
    rec = next(iter(c.lineage.decisions.values()))
    assert rec.decision == "REFUSED"
    assert rec.reason_code == "INSUFFICIENT_FORWARD_SUPPORT"
    assert any(kind == "authorization_decision" for kind, _ in audit)


def test_v14_logger_recursively_serializes_typed_dataclasses(tmp_path: Path):
    p = tmp_path / "events.jsonl"
    log = EventLogger(p)
    rec = TransitionRecord(1, None, "a", "b", 1, 1, 1, "NOT_FINISHED", "NOT_FINISHED", 0, 0, 2, 2, 0)
    log.append("transition", {"transition": rec})
    row = json.loads(p.read_text())
    assert row["payload"]["transition"]["action_token"] == 1
    assert row["payload"]["transition"]["post_frame_hash"] == "b"


class _State:
    def __init__(self, name): self.name = name


class _Frame:
    def __init__(self, arr, state="NOT_FINISHED", levels=0):
        self.frame = arr
        self.available_actions = [1]
        self.state = _State(state)
        self.levels_completed = levels


class _Env:
    def __init__(self):
        self.observation_space = _Frame(np.zeros((64,64), dtype=np.uint8))
    def step(self, action, data=None):
        arr = np.zeros((64,64), dtype=np.uint8); arr[0,0] = 1
        return _Frame(arr, state="WIN", levels=1)


class _EnvMeta:
    def __init__(self, slug): self.game_id = f"{slug}-v1"


class _Arcade:
    def __init__(self): self.available_environments = [_EnvMeta(s) for s in sorted(DEVELOPMENT_GAMES)]
    def make(self, game_id, seed=0): return _Env()


def test_v14_runner_emits_complete_minimal_trace_without_real_arc(tmp_path: Path, monkeypatch):
    root = tmp_path / "envs"; root.mkdir()
    for slug in DEVELOPMENT_GAMES: (root / slug).mkdir()
    fake_arcengine = types.SimpleNamespace(GameAction=types.SimpleNamespace(from_id=lambda aid: aid))
    monkeypatch.setitem(sys.modules, "arcengine", fake_arcengine)
    logs = tmp_path / "logs"
    r = DevelopmentRunner(root, arcade_factory=lambda _: _Arcade(), log_dir=logs)
    result = r.run_game("ar25", "B")
    assert result.actions == 1
    assert result.levels_completed == 1
    events = [json.loads(x) for x in next(logs.glob("*.jsonl")).read_text().splitlines()]
    kinds = [e["kind"] for e in events]
    for required in ("run_start", "transition", "prediction_score", "evidence", "level_transition", "lineage_snapshot", "canonical_snapshot", "run_summary"):
        assert required in kinds
    transition = next(e["payload"] for e in events if e["kind"] == "transition")
    assert transition["action_legal"] is True
    assert transition["goal"]["remaining_wallclock_budget"] is None
    assert "modal_color_id" in transition["descriptor"]
    assert set(transition["prediction"]["secondary"]) == {
        "changed_count_bucket", "state_delta_class", "level_delta_positive", "action_surface_changed", "exact_return_flag"
    }


def test_v14_reducer_checks_lineage_completeness_on_runner_trace(tmp_path: Path, monkeypatch):
    from cea_arc3.reducer import reduce_run
    root = tmp_path / "envs"; root.mkdir()
    for slug in DEVELOPMENT_GAMES: (root / slug).mkdir()
    fake_arcengine = types.SimpleNamespace(GameAction=types.SimpleNamespace(from_id=lambda aid: aid))
    monkeypatch.setitem(sys.modules, "arcengine", fake_arcengine)
    logs = tmp_path / "logs"
    DevelopmentRunner(root, arcade_factory=lambda _: _Arcade(), log_dir=logs).run_game("ar25", "B")
    reduced = reduce_run(next(logs.glob("*.jsonl")))
    assert reduced["logged_transitions"] == 1
    assert reduced["logged_evidence"] == 1
    assert reduced["collateral_violations_reduced"] == 0


def _write_persistence_log(path: Path, *, arm: str, source: str | None, p_change: float, parent: float, outcome: int, claim: str | None = None):
    events = [
        {"kind":"run_start","payload":{"game_slug":"ar25","arm":arm,"seed":0,"action_budget":256,"environment_membership_count":18}},
    ]
    if claim:
        events.append({"kind":"canonical_entry","payload":{"claim_id":claim,"scope_predicate":[],"local_predictive_delta":0.2,"evidence_ids":[],"authorization_id":"a","created_level":0,"created_step":1,"last_verified_level":0,"status":"AUTHORIZED"}})
    events.append({"kind":"transition","payload":{
        "game_slug":"ar25","arm":arm,"seed":0,"step":10,"action_token":1,"action_coordinate":None,
        "prediction":{"p_change":p_change,"parent_p_change":parent,"claim_id":claim,"correction_source":source},
        "score":{"level":1,"emitted_nll":TransitionModel.binary_nll(p_change,outcome)},
        "transition":{"z_change":outcome,"changed_count_bucket":1 if outcome else 0,"state_after":"NOT_FINISHED","level_before":1,"level_after":1,"available_action_mask_before":2,"available_action_mask_after":2,"exact_return_flag":0}
    }})
    events.append({"kind":"run_summary","payload":{"game_slug":"ar25","arm":arm,"seed":0}})
    path.write_text("\n".join(json.dumps(x) for x in events)+"\n")


def test_v14_persistence_pairing_uses_exact_key_and_transient_parent(tmp_path: Path):
    from cea_arc3.reducer import persistence_metric
    _write_persistence_log(tmp_path/"p.jsonl", arm="B+L+C", source="CANONICAL", p_change=0.8, parent=0.5, outcome=1, claim="h")
    _write_persistence_log(tmp_path/"t.jsonl", arm="B+L", source=None, p_change=0.5, parent=0.5, outcome=1, claim=None)
    out = persistence_metric(tmp_path)
    assert out["n"] == 1
    expected = TransitionModel.binary_nll(0.8,1) - TransitionModel.binary_nll(0.5,1)
    assert abs(out["mean_nll_difference"] - expected) < 1e-12
    assert out["non_evaluable_pairs"] == 0


def test_v15_level_boundary_marks_live_provisional_lineage_expired():
    c = MechanismCore(ARMS["B+L"], "ar25")
    h = Hypothesis(
        "h-expire", (1, None, "START", "START", 2), "prev2_z", 1,
        ((1, None, "START", "START", 2), "prev2_z", 1),
        proposal_gain_nll=0.1,
        proposal_snapshot_counts=((1, 1, (0,0,0,0,0,0,0)), (1, 0, (0,0,0,0,0,0,0))),
    )
    h.proposal_snapshot_hash = proposal_snapshot_hash(proposal_snapshot_from_hypothesis(h))
    c.hypotheses.live[h.claim_id] = h
    c.lineage.add_claim(ClaimRecord(h.claim_id, None, h.proposal_snapshot_hash, (h.predicate_id, h.predicate_value), h.scope, h.status))
    c.on_level_transition(1)
    assert h.claim_id not in c.hypotheses.live
    assert c.lineage.claims[h.claim_id].current_status == "EXPIRED"


def test_v15_evicted_claim_lineage_can_be_marked_evicted_without_control_effect():
    c = MechanismCore(ARMS["B+L"], "ar25")
    h = Hypothesis(
        "h-evict", (1, None, "START", "START", 2), "prev2_z", 1,
        ((1, None, "START", "START", 2), "prev2_z", 1),
        proposal_gain_nll=0.1,
        proposal_snapshot_counts=((1, 1, (0,0,0,0,0,0,0)), (1, 0, (0,0,0,0,0,0,0))),
    )
    h.proposal_snapshot_hash = proposal_snapshot_hash(proposal_snapshot_from_hypothesis(h))
    c.hypotheses.live[h.claim_id] = h
    c.lineage.add_claim(ClaimRecord(h.claim_id, None, h.proposal_snapshot_hash, (h.predicate_id, h.predicate_value), h.scope, h.status))
    # Exercise the frozen lineage mutation directly: this field is audit-only.
    c.lineage.update_claim_status(h.claim_id, "EVICTED")
    assert c.lineage.claims[h.claim_id].current_status == "EVICTED"
    assert c.hypotheses.live[h.claim_id].status == "PROVISIONAL"
