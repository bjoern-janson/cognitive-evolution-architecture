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
