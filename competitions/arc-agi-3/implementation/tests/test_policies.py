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
