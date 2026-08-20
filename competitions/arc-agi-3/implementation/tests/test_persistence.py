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
