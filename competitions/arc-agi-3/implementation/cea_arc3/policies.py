from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from .state import RawHistory
from .transition import TransitionModel, action_mask

ENTROPY_THRESHOLD_NATS = 0.55

def action6_schedule() -> tuple[tuple[int,int], ...]:
    centers = tuple(4 + 8*i for i in range(8))
    return tuple((x,y) for y in centers for x in centers)

def candidate_actions(available_actions: Iterable[int]) -> tuple[tuple[int,Optional[tuple[int,int]]], ...]:
    out=[]
    for aid in sorted(int(a) for a in available_actions):
        if aid == 0: continue
        if aid == 6: out.extend((6,xy) for xy in action6_schedule())
        else: out.append((aid,None))
    return tuple(out)

@dataclass
class AIECPolicy:
    model: TransitionModel
    exec_index: int = 0
    def choose(self, *, history: RawHistory, current_frame_hash: str, available_actions: Iterable[int]) -> tuple[int,Optional[tuple[int,int]],str]:
        available=tuple(sorted(int(a) for a in available_actions if int(a)!=0))
        if not available: return 0,None,"RESET"
        mask=action_mask(available); candidates=candidate_actions(available); entropies=[]
        for aid,coord in candidates:
            ctx=self.model.base_context(aid,coord,history,mask); p,_=self.model.predict(ctx); entropies.append((self.model.entropy(p),aid,coord))
        mean_entropy=sum(x[0] for x in entropies)/len(entropies)
        if mean_entropy > ENTROPY_THRESHOLD_NATS:
            best=sorted(entropies,key=lambda t:(-t[0],t[1],t[2] or (-1,-1)))[0]; return best[1],best[2],"P_INFO"
        choice=candidates[self.exec_index%len(candidates)]; self.exec_index+=1; return choice[0],choice[1],"P_EXEC"

@dataclass
class FixedAllocationPolicy:
    info_percent: int
    model: TransitionModel
    step_index: int = 0
    exec_index: int = 0
    def __post_init__(self) -> None:
        if self.info_percent not in (0,25,50,75,100): raise ValueError("info_percent must be one of 0,25,50,75,100")
    def _use_info(self) -> bool:
        i=self.step_index
        if self.info_percent==0:return False
        if self.info_percent==100:return True
        if self.info_percent==50:return i%2==1
        if self.info_percent==25:return i%4==3
        return i%4!=3
    def choose(self, *, history: RawHistory, current_frame_hash: str, available_actions: Iterable[int]):
        available=tuple(sorted(int(a) for a in available_actions if int(a)!=0))
        if not available:return 0,None,"RESET"
        mask=action_mask(available); candidates=candidate_actions(available); use_info=self._use_info(); self.step_index+=1
        if use_info:
            scored=[]
            for aid,coord in candidates:
                ctx=self.model.base_context(aid,coord,history,mask); p,_=self.model.predict(ctx); scored.append((self.model.entropy(p),aid,coord))
            best=sorted(scored,key=lambda t:(-t[0],t[1],t[2] or (-1,-1)))[0]; return best[1],best[2],"P_INFO"
        choice=candidates[self.exec_index%len(candidates)]; self.exec_index+=1; return choice[0],choice[1],"P_EXEC"
