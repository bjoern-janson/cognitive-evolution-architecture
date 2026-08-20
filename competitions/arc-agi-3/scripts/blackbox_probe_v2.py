from __future__ import annotations

import argparse
import hashlib
import json
import logging
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np

from arc_agi import Arcade, OperationMode
from arcengine import GameAction

DEV = {
    'ar25','bp35','cd82','ft09','g50t','ka59','ls20','r11l','re86',
    's5i5','sb26','sc25','sk48','sp80','su15','tu93','vc33','wa30'
}
SEALED = {'cn04','dc22','lf52','lp85','m0r0','tn36','tr87'}
SIMPLE_IDS = (1,2,3,4,5,7)
LATTICE = (0,16,32,47,63)

parser = argparse.ArgumentParser()
parser.add_argument('--environment-root', required=True, type=Path)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
ROOT = args.environment_root
OUT = args.output

assert ROOT.is_dir()
assert {p.name for p in ROOT.iterdir() if p.is_dir()} == DEV
assert not any((ROOT / s).exists() for s in SEALED)

logging.getLogger().setLevel(logging.ERROR)


def arr_of(frame) -> np.ndarray:
    arr = np.asarray(frame.frame)
    if arr.ndim == 3:
        arr = arr[-1]
    return np.asarray(arr)


def frame_sha(arr: np.ndarray) -> str:
    return hashlib.sha256(arr.tobytes()).hexdigest()


def bbox(mask: np.ndarray):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


def action_ids(frame) -> list[int]:
    return [int(x.value if hasattr(x, 'value') else x) for x in (frame.available_actions or [])]


def state_name(frame) -> str:
    return str(frame.state.name if hasattr(frame.state, 'name') else frame.state)


def frame_record(frame) -> dict[str, Any]:
    a = arr_of(frame)
    return {
        'frame_sha256': frame_sha(a),
        'shape': list(a.shape),
        'state': state_name(frame),
        'levels_completed': int(frame.levels_completed),
        'available_actions': action_ids(frame),
    }


def transition_record(initial_arr: np.ndarray, before, after) -> dict[str, Any]:
    a = arr_of(before)
    b = arr_of(after)
    same_shape = a.shape == b.shape
    if same_shape:
        diff = a != b
        changed = int(diff.sum())
        change_box = bbox(diff)
        equal_prior = bool(np.array_equal(a, b))
    else:
        changed = None
        change_box = None
        equal_prior = False
    equal_initial = bool(initial_arr.shape == b.shape and np.array_equal(initial_arr, b))
    return {
        'frame_sha256_after': frame_sha(b),
        'shape_after': list(b.shape),
        'state_after': state_name(after),
        'levels_completed_after': int(after.levels_completed),
        'available_actions_after': action_ids(after),
        'changed_cells_from_prior': changed,
        'change_bbox_xyxy': change_box,
        'equal_immediately_prior_frame': equal_prior,
        'equal_initial_frame': equal_initial,
    }


def nonmodal_component_centroids(arr: np.ndarray, cap: int = 12) -> list[dict[str, int]]:
    vals, counts = np.unique(arr, return_counts=True)
    bg = int(vals[np.argmax(counts)])
    mask = arr != bg
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    comps: list[tuple[int,int,int,int]] = []
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            q = deque([(y,x)])
            seen[y,x] = True
            pts = []
            while q:
                cy,cx = q.popleft()
                pts.append((cy,cx))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx = cy+dy,cx+dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny,nx] and not seen[ny,nx]:
                        seen[ny,nx] = True
                        q.append((ny,nx))
            cy = int(round(sum(p[0] for p in pts) / len(pts)))
            cx = int(round(sum(p[1] for p in pts) / len(pts)))
            comps.append((-len(pts), cy, cx, len(pts)))
    comps.sort(key=lambda t: (t[0], t[1], t[2]))
    return [{'x': int(cx), 'y': int(cy), 'component_size': int(size)} for _,cy,cx,size in comps[:cap]]


def click_points(initial_frame) -> list[dict[str, Any]]:
    arr = arr_of(initial_frame)
    h,w = arr.shape
    assert (h,w) == (64,64)
    pts: list[dict[str, Any]] = []
    for y in LATTICE:
        for x in LATTICE:
            pts.append({'x':x,'y':y,'rule':'lattice'})
    for c in nonmodal_component_centroids(arr, 12):
        pts.append({'x':c['x'],'y':c['y'],'rule':'nonmodal_component_centroid','component_size':c['component_size']})
    out=[]; seen=set()
    for p in pts:
        key=(p['x'],p['y'])
        if key in seen:
            continue
        seen.add(key); out.append(p)
    return out


def make_arcade():
    logger = logging.getLogger('arc3probe-v2')
    logger.handlers.clear(); logger.addHandler(logging.NullHandler()); logger.propagate=False
    return Arcade(operation_mode=OperationMode.OFFLINE, environments_dir=str(ROOT), logger=logger)


def step_action(env, frame, spec: dict[str, Any]):
    aid = int(spec['action_id'])
    if aid not in action_ids(frame):
        return None, {'planned_action': spec, 'not_available': True}
    if aid == 6:
        after = env.step(GameAction.ACTION6, {'x': int(spec['x']), 'y': int(spec['y'])})
    else:
        after = env.step(GameAction.from_id(aid))
    return after, {'planned_action': spec, 'not_available': False}


def run_sequence(arcade, game_id: str, specs: list[dict[str, Any]]) -> dict[str, Any]:
    env = arcade.make(game_id, seed=0)
    if env is None or env.observation_space is None:
        return {'error': 'make_failed'}
    initial = env.observation_space
    initial_arr = arr_of(initial).copy()
    rec = {
        'initial': frame_record(initial),
        'planned_sequence': specs,
        'steps': [],
    }
    current = initial
    for i,spec in enumerate(specs, start=1):
        before = current
        after, meta = step_action(env, before, spec)
        step_rec = {'step_index': i, **meta}
        if meta.get('not_available'):
            rec['steps'].append(step_rec)
            break
        if after is None:
            step_rec['error'] = 'step_failed'
            rec['steps'].append(step_rec)
            break
        step_rec.update(transition_record(initial_arr, before, after))
        rec['steps'].append(step_rec)
        current = after
        if state_name(after) in {'WIN','GAME_OVER'}:
            break
    return rec


arcade = make_arcade()
envs = {e.game_id.split('-',1)[0]: e for e in arcade.available_environments}
assert set(envs) == DEV

results: dict[str, Any] = {
    'schema': 'ARC3_DEV_BLACKBOX_PROBE_V2',
    'policy': {
        'source_inspection': False,
        'sealed_games_present_in_runtime': False,
        'seed': 0,
        'families': ['A_simple_repetition','B_ordered_simple_pair','C_action6_repeat','D_simple_then_action6','E_action6_then_simple'],
        'simple_action_ids': list(SIMPLE_IDS),
        'action6_lattice': list(LATTICE),
        'action6_component_centroid_cap': 12,
    },
    'games': {},
}

for slug in sorted(DEV):
    info = envs[slug]
    init_env = arcade.make(info.game_id, seed=0)
    assert init_env is not None and init_env.observation_space is not None
    init = init_env.observation_space
    avail = action_ids(init)
    simple = [a for a in SIMPLE_IDS if a in avail]
    pts = click_points(init) if 6 in avail else []

    game = {
        'game_id': info.game_id,
        'initial': frame_record(init),
        'simple_actions': simple,
        'action6_points': pts,
        'families': {},
    }

    famA=[]
    for a in simple:
        specs=[{'action_id':a} for _ in range(3)]
        famA.append(run_sequence(arcade, info.game_id, specs))
    game['families']['A_simple_repetition']=famA

    famB=[]
    for a in simple:
        for b in simple:
            famB.append(run_sequence(arcade, info.game_id, [{'action_id':a},{'action_id':b}]))
    game['families']['B_ordered_simple_pair']=famB

    famC=[]
    for p in pts:
        spec={'action_id':6,'x':p['x'],'y':p['y'],'point_rule':p['rule']}
        if 'component_size' in p:
            spec['component_size']=p['component_size']
        famC.append(run_sequence(arcade, info.game_id, [dict(spec),dict(spec)]))
    game['families']['C_action6_repeat']=famC

    famD=[]
    for a in simple:
        for p in pts:
            click={'action_id':6,'x':p['x'],'y':p['y'],'point_rule':p['rule']}
            if 'component_size' in p:
                click['component_size']=p['component_size']
            famD.append(run_sequence(arcade, info.game_id, [{'action_id':a},click]))
    game['families']['D_simple_then_action6']=famD

    famE=[]
    for p in pts:
        for a in simple:
            click={'action_id':6,'x':p['x'],'y':p['y'],'point_rule':p['rule']}
            if 'component_size' in p:
                click['component_size']=p['component_size']
            famE.append(run_sequence(arcade, info.game_id, [click,{'action_id':a}]))
    game['families']['E_action6_then_simple']=famE

    results['games'][slug]=game
    seqs=sum(len(v) for v in game['families'].values())
    print(slug, 'simple', simple, 'click_points', len(pts), 'sequences', seqs, flush=True)

OUT.write_text(json.dumps(results, indent=2, sort_keys=True), encoding='utf-8')
print('WROTE', OUT)
