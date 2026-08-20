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
