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
