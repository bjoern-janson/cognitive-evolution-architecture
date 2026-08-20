from cea_arc3.authority import AuthorityGate
from cea_arc3.provenance import proposal_snapshot_hash, proposal_snapshot_from_hypothesis
from cea_arc3.state import CanonicalMemory, ClaimRecord, EvidenceRecord, Hypothesis, LineageState


def lineage_for(h, n):
    l=LineageState()
    l.add_claim(ClaimRecord(h.claim_id,None,h.proposal_snapshot_hash,(h.predicate_id,h.predicate_value),h.scope,h.status))
    for i in range(n):
        eid=f'e{i}'
        l.add_evidence(EvidenceRecord(eid,'ar25',0,i,'f','w',1,None,(1,)))
    return l


def hyp(**kwargs):
    h=Hypothesis('h',('c',),'prev_z',1,('c','prev_z',1),proposal_gain_nll=1.0,proposal_snapshot_counts=((2,2,(0,0,0,0,0,0,0)),(1,1,(0,0,0,0,0,0,0))),**kwargs)
    h.proposal_snapshot_hash=proposal_snapshot_hash(proposal_snapshot_from_hypothesis(h))
    return h


def test_x_refuses_insufficient_forward_evidence():
    h=hyp(forward_support=3,forward_gain_nll=3.0,forward_event_gains=[1,1,1],sibling_support=4,evidence_ids=['e0','e1','e2'],sibling_evidence_ids=['e3','e4','e5','e6'])
    d=AuthorityGate().evaluate(h,lineage_for(h,7),CanonicalMemory(),created_level=0,created_step=0,local_predictive_delta=1.0)
    assert not d.authorize
    assert d.reason_code == 'INSUFFICIENT_FORWARD_SUPPORT'


def test_x_authorizes_only_when_all_predicates_hold():
    h=hyp(forward_support=5,forward_gain_nll=3.0,forward_event_gains=[.5,.5,.5,.5,.5],sibling_support=4,evidence_ids=['e0','e1','e2','e3','e4'],sibling_evidence_ids=['e5','e6','e7','e8'])
    l=lineage_for(h,9)
    mem=CanonicalMemory(); gate=AuthorityGate()
    d=gate.promote(hypothesis=h,lineage=l,memory=mem,created_level=0,created_step=5,local_predictive_delta=.8)
    assert d.authorize
    assert 'h' in mem.entries


def test_x_rejects_tampered_proposal_hash():
    h=hyp(forward_support=5,forward_gain_nll=3.0,forward_event_gains=[.5]*5,sibling_support=4,evidence_ids=['e0','e1','e2','e3','e4'],sibling_evidence_ids=['e5','e6','e7','e8'])
    l=lineage_for(h,9)
    h.proposal_snapshot_hash='bad'
    d=AuthorityGate().evaluate(h,l,CanonicalMemory(),created_level=0,created_step=5,local_predictive_delta=.8)
    assert not d.authorize
    assert d.reason_code=='INCOMPLETE_LINEAGE'
import numpy as np

from cea_arc3.arms import ARMS
from cea_arc3.core import MechanismCore
from cea_arc3.transition import transition_record_from_arrays


def make_transition(z, action=1, level_before=0, level_after=0):
    a=np.zeros((64,64),dtype=np.uint8); b=a.copy()
    if z: b[0,0]=1
    return transition_record_from_arrays(
        before=a,after=b,action_token=action,action_coordinate=None,
        state_before='NOT_FINISHED',state_after='NOT_FINISHED',
        level_before=level_before,level_after=level_after,
        available_actions_before=[1,2],available_actions_after=[1,2],
    )


def test_prediction_is_scored_before_update():
    c=MechanismCore(ARMS['B'],'ar25')
    pred=c.predict_action(action_token=1,action_coordinate=None,current_frame_hash='x',available_actions=[1,2])
    assert pred.parent_probability==.5
    c.observe(prediction=pred,record=make_transition(1),current_frame_hash_before='x')
    pred2=c.predict_action(action_token=1,action_coordinate=None,current_frame_hash='x',available_actions=[1,2])
    # base context now includes previous action/outcome and is fresh, so its prior is still 0.5.
    assert pred2.parent_probability==.5
    assert len(c.metrics.predictions)==1


def test_level_transition_clears_raw_history():
    c=MechanismCore(ARMS['B'],'ar25')
    pred=c.predict_action(action_token=1,action_coordinate=None,current_frame_hash='x',available_actions=[1,2])
    c.observe(prediction=pred,record=make_transition(1,level_before=0,level_after=1),current_frame_hash_before='x')
    assert len(c.history)==0
    assert c.level==1
from cea_arc3.corrections import apply_delta, clipped_delta, select_provisional
from cea_arc3.state import Hypothesis


def test_delta_roundtrips_local_probability_without_clipping():
    p_parent=.4; p_local=.7
    d=clipped_delta(p_parent,p_local)
    assert abs(apply_delta(p_parent,d)-p_local) < 1e-9


def test_provisional_arbitration_uses_forward_gain_then_claim_id():
    ctx=('c',); vals={'prev_z':1}
    a=Hypothesis('H2',ctx,'prev_z',1,(ctx,'prev_z',1),proposal_gain_nll=9,forward_support=1,forward_gain_nll=1)
    b=Hypothesis('H1',ctx,'prev_z',1,(ctx,'prev_z',1),proposal_gain_nll=1,forward_support=1,forward_gain_nll=2)
    assert select_provisional([a,b],ctx,vals).claim_id=='H1'
import numpy as np
from cea_arc3.descriptors import describe_observation


def test_descriptor_is_nonsemantic_and_exact_histogram():
    a=np.zeros((64,64),dtype=np.uint8); a[0,0]=3
    d=describe_observation(a,[1,6])
    assert len(d.color_histogram)==16
    assert d.color_histogram[0]==4095
    assert d.color_histogram[3]==1
    assert d.non_modal_color==0
    assert d.non_modal_cells==1
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
from cea_arc3.hypotheses import HypothesisManager
from cea_arc3.state import RawHistory, TransitionRecord
from cea_arc3.transition import TransitionModel, action_mask


def make_record(action,z):
    return TransitionRecord(
        action_token=action, action_coordinate=None,
        pre_frame_hash='a', post_frame_hash='b' if z else 'a', z_change=z,
        changed_cell_count=z, changed_count_bucket=z,
        state_before='NOT_FINISHED', state_after='NOT_FINISHED',
        level_before=0, level_after=0,
        available_action_mask_before=6, available_action_mask_after=6,
        exact_return_flag=0,
    )


def test_trigger_requires_four_and_both_classes():
    m=TransitionModel(); h=RawHistory(); mask=action_mask([1,2]); ctx=m.base_context(1,None,h,mask)
    hm=HypothesisManager()
    for z in [0,0,0]:
        m.update(context=ctx,predicate_values=m.predicate_values(h,'a',mask),z_change=z,bucket=z)
    assert not hm.trigger_met(m.base[ctx])
    m.update(context=ctx,predicate_values=m.predicate_values(h,'a',mask),z_change=1,bucket=1)
    assert hm.trigger_met(m.base[ctx])


def test_proposal_uses_q_and_is_bounded():
    m=TransitionModel(); hm=HypothesisManager(); mask=action_mask([1,2])
    # Same base context but predicate prev2_action splits outcomes.
    for prev2_action,z in [(1,0),(1,0),(2,1),(2,1)]:
        h=RawHistory([make_record(prev2_action,0), make_record(9,0)])
        ctx=m.base_context(1,None,h,mask)
        vals=m.predicate_values(h,'same',mask)
        m.update(context=ctx,predicate_values=vals,z_change=z,bucket=z)
    # base differs because prev action is constant 9, so one triggered context exists.
    ctx=m.base_context(1,None,RawHistory([make_record(1,0),make_record(9,0)]),mask)
    props=hm.propose_from_q(m,ctx)
    assert props
    assert len(hm.live) <= 32
    assert any(p.predicate_id == 'prev2_action' for p in props)
from pathlib import Path
import pytest
from cea_arc3.logger import EventLogger


def test_logger_rejects_frame_payload(tmp_path: Path):
    log=EventLogger(tmp_path/'x.jsonl')
    with pytest.raises(ValueError):
        log.append('bad', {'frame': [[0]]})


def test_logger_allows_hash_summary(tmp_path: Path):
    p=tmp_path/'x.jsonl'; log=EventLogger(p)
    log.append('ok', {'frame_sha256':'abc','changed_cells':2})
    assert p.read_text().count('\n')==1
from cea_arc3.arms import ARMS
from cea_arc3.core import MechanismCore
from cea_arc3.state import CanonicalEntry


def test_b_persist_keeps_theta_but_not_canonical_memory():
    c=MechanismCore(ARMS['B_PERSIST'],'ar25')
    c.model.base[('x',)].binary.one += 2
    c.memory.add(CanonicalEntry('h',('s',),.2,(), 'a',0,0,0))
    c.on_level_transition(1)
    assert c.model.base[('x',)].binary.one > 1
    assert not c.memory.entries


def test_c_persists_canonical_but_resets_theta():
    c=MechanismCore(ARMS['B+L+C'],'ar25')
    c.model.base[('x',)].binary.one += 2
    c.memory.add(CanonicalEntry('h',('s',),.2,(), 'a',0,0,0))
    c.on_level_transition(1)
    assert ('x',) not in c.model.base
    assert 'h' in c.memory.entries
    assert len(c.history)==0
from cea_arc3.policies import AIECPolicy, FixedAllocationPolicy, action6_schedule
from cea_arc3.state import RawHistory
from cea_arc3.transition import TransitionModel


def test_action6_schedule_is_8x8_row_major():
    pts=action6_schedule()
    assert len(pts)==64
    assert pts[0]==(4,4)
    assert pts[-1]==(60,60)


def test_aiec_prior_entropy_selects_info():
    p=AIECPolicy(TransitionModel())
    aid,coord,mode=p.choose(history=RawHistory(),current_frame_hash='x',available_actions=[1,2])
    assert mode=='P_INFO'
    assert aid==1


def test_fixed_25_schedule():
    p=FixedAllocationPolicy(25,TransitionModel())
    modes=[p.choose(history=RawHistory(),current_frame_hash='x',available_actions=[1])[2] for _ in range(8)]
    assert modes==['P_EXEC','P_EXEC','P_EXEC','P_INFO']*2
from cea_arc3.provenance import canonical_json, proposal_snapshot, proposal_snapshot_hash
from cea_arc3.transition import AggregateCell


def test_proposal_snapshot_hash_is_deterministic_and_count_only():
    parent=AggregateCell(); local=AggregateCell()
    parent.binary.zero += 2; parent.binary.one += 2
    local.binary.zero += 2
    snap=proposal_snapshot(base_context=(1,None,'START','START',6), predicate_id='prev_z', predicate_value=0, parent_cell=parent, local_cell=local, proposal_gain_nll=1.25)
    h1=proposal_snapshot_hash(snap); h2=proposal_snapshot_hash(dict(reversed(list(snap.items()))))
    assert h1==h2
    text=canonical_json(snap)
    assert 'frame' not in text.lower()
    assert 'evidence_id' not in text
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
import numpy as np
import pytest

from cea_arc3.state import H_RAW, RawHistory
from cea_arc3.transition import transition_record_from_arrays


def rec(i):
    a = np.zeros((64,64), dtype=np.uint8)
    b = a.copy(); b[0, i] = 1
    return transition_record_from_arrays(
        before=a, after=b, action_token=1, action_coordinate=None,
        state_before='NOT_FINISHED', state_after='NOT_FINISHED',
        level_before=0, level_after=0,
        available_actions_before=[1,2], available_actions_after=[1,2],
    )


def test_raw_history_is_hard_bounded_to_two():
    h = RawHistory()
    h.append(rec(0)); h.append(rec(1)); h.append(rec(2))
    assert len(h) == H_RAW == 2
    assert [r.changed_cell_count for r in h] == [1,1]
    assert h.as_tuple()[0].post_frame_hash == rec(1).post_frame_hash


def test_level_clear_is_explicit():
    h = RawHistory([rec(0), rec(1)])
    h.clear()
    assert len(h) == 0
import numpy as np

from cea_arc3.state import RawHistory
from cea_arc3.transition import TransitionModel, action_mask, changed_bucket, transition_record_from_arrays


def test_changed_bucket_boundaries():
    cases = [(0,0),(1,1),(2,2),(4,2),(5,3),(16,3),(17,4),(64,4),(65,5),(256,5),(257,6)]
    for n,b in cases:
        assert changed_bucket(n) == b


def test_prequential_prediction_is_prior_before_update():
    m = TransitionModel(); h = RawHistory(); mask = action_mask([1])
    ctx = m.base_context(1, None, h, mask)
    p,_ = m.predict(ctx)
    assert p == 0.5
    m.update(context=ctx, predicate_values=m.predicate_values(h, 'x', mask), z_change=1, bucket=1)
    p2,_ = m.predict(ctx)
    assert p2 > p


def test_q_is_aggregate_not_event_storage():
    m = TransitionModel(); h = RawHistory(); mask = action_mask([1,2])
    ctx = m.base_context(1,None,h,mask)
    vals = m.predicate_values(h,'abc',mask)
    m.update(context=ctx,predicate_values=vals,z_change=0,bucket=0)
    assert m.q
    assert all(hasattr(cell, 'binary') for cell in m.q.values())
    assert not any(hasattr(cell, 'events') for cell in m.q.values())
