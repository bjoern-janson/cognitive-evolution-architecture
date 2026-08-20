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
