from __future__ import annotations

import hashlib
import json
from typing import Any

from .transition import AggregateCell

def observed_counts(cell: AggregateCell) -> tuple[int,int,tuple[int,...]]:
    return (cell.binary.zero-1, cell.binary.one-1, tuple(c-1 for c in cell.buckets.counts))

def proposal_snapshot(*, base_context: tuple[Any,...], predicate_id: str, predicate_value: Any, parent_cell: AggregateCell, local_cell: AggregateCell, proposal_gain_nll: float) -> dict[str,Any]:
    p0,p1,pb=observed_counts(parent_cell); l0,l1,lb=observed_counts(local_cell)
    return {"base_context":list(base_context),"predicate_id":predicate_id,"predicate_value":predicate_value,"parent_counts":[p0,p1,list(pb)],"local_counts":[l0,l1,list(lb)],"proposal_gain_nll":float(proposal_gain_nll)}

def canonical_json(snapshot: dict[str,Any]) -> str:
    return json.dumps(snapshot,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def proposal_snapshot_hash(snapshot: dict[str,Any]) -> str:
    return hashlib.sha256(canonical_json(snapshot).encode("utf-8")).hexdigest()

def proposal_snapshot_from_hypothesis(h) -> dict[str,Any]:
    parent,local=h.proposal_snapshot_counts; p0,p1,pb=parent; l0,l1,lb=local
    return {"base_context":list(h.parent_context),"predicate_id":h.predicate_id,"predicate_value":h.predicate_value,"parent_counts":[p0,p1,list(pb)],"local_counts":[l0,l1,list(lb)],"proposal_gain_nll":float(h.proposal_gain_nll)}
