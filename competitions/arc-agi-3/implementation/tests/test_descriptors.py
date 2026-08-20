import numpy as np
from cea_arc3.descriptors import describe_observation


def test_descriptor_is_nonsemantic_and_exact_histogram():
    a=np.zeros((64,64),dtype=np.uint8); a[0,0]=3
    d=describe_observation(a,[1,6])
    assert len(d.color_histogram)==16
    assert d.color_histogram[0]==4095
    assert d.color_histogram[3]==1
    assert d.modal_color_id==0
    assert d.non_modal_cells==1
