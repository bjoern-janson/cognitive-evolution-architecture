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
