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
