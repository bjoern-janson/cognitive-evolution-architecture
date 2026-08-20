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
