from __future__ import annotations

import hashlib
import json
import logging
from collections import deque
from pathlib import Path
from typing import Any
import argparse

import numpy as np

from arc_agi import Arcade, OperationMode
from arcengine import GameAction

_parser = argparse.ArgumentParser()
_parser.add_argument('--environment-root', required=True, type=Path)
_parser.add_argument('--output', required=True, type=Path)
_args = _parser.parse_args()
ROOT = _args.environment_root
OUT = _args.output
DEV = {
    'ar25','bp35','cd82','ft09','g50t','ka59','ls20','r11l','re86',
    's5i5','sb26','sc25','sk48','sp80','su15','tu93','vc33','wa30'
}
SEALED = {'cn04','dc22','lf52','lp85','m0r0','tn36','tr87'}

assert ROOT.is_dir()
assert {p.name for p in ROOT.iterdir() if p.is_dir()} == DEV
assert not any((ROOT / s).exists() for s in SEALED)

logging.getLogger().setLevel(logging.ERROR)


def arr_of(frame) -> np.ndarray:
    arr = np.asarray(frame.frame)
    if arr.ndim == 3:
        arr = arr[-1]
    return np.asarray(arr)


def sha(arr: np.ndarray) -> str:
    return hashlib.sha256(arr.tobytes()).hexdigest()


def bbox(mask: np.ndarray):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


def largest_component_centroid(arr: np.ndarray, bg: int) -> tuple[int, int] | None:
    mask = arr != bg
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    best = []
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            q = deque([(y, x)])
            seen[y, x] = True
            comp = []
            while q:
                cy, cx = q.popleft()
                comp.append((cy, cx))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if len(comp) > len(best):
                best = comp
    if not best:
        return None
    ys = [p[0] for p in best]
    xs = [p[1] for p in best]
    return (int(round(sum(xs) / len(xs))), int(round(sum(ys) / len(ys))))


def frame_summary(frame) -> dict[str, Any]:
    arr = arr_of(frame)
    vals, counts = np.unique(arr, return_counts=True)
    palette = {str(int(v)): int(c) for v, c in zip(vals, counts)}
    bg = int(vals[np.argmax(counts)])
    return {
        'state': str(frame.state.name if hasattr(frame.state, 'name') else frame.state),
        'levels_completed': int(frame.levels_completed),
        'win_levels': int(frame.win_levels),
        'available_actions': [int(x.value if hasattr(x, 'value') else x) for x in (frame.available_actions or [])],
        'shape': list(arr.shape),
        'sha256': sha(arr),
        'palette_counts': palette,
        'modal_color': bg,
        'nonmodal_cells': int((arr != bg).sum()),
    }


def action_effect(before, after) -> dict[str, Any]:
    a = arr_of(before)
    b = arr_of(after)
    same_shape = a.shape == b.shape
    if same_shape:
        diff = a != b
        changed = int(diff.sum())
        dbbox = bbox(diff)
    else:
        changed = None
        dbbox = None
    return {
        'after_state': str(after.state.name if hasattr(after.state, 'name') else after.state),
        'levels_completed_before': int(before.levels_completed),
        'levels_completed_after': int(after.levels_completed),
        'level_delta': int(after.levels_completed) - int(before.levels_completed),
        'available_actions_after': [int(x.value if hasattr(x, 'value') else x) for x in (after.available_actions or [])],
        'same_shape': bool(same_shape),
        'changed_cells': changed,
        'change_bbox_xyxy': dbbox,
        'frame_sha256_after': sha(b),
        'palette_counts_after': {str(int(v)): int(c) for v, c in zip(*np.unique(b, return_counts=True))},
    }


def make_arcade():
    logger = logging.getLogger('arc3probe')
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
    return Arcade(operation_mode=OperationMode.OFFLINE, environments_dir=str(ROOT), logger=logger)


arcade = make_arcade()
envs = {e.game_id.split('-', 1)[0]: e for e in arcade.available_environments}
assert set(envs) == DEV

results = {
    'schema': 'ARC3_DEV_BLACKBOX_PROBE_V1',
    'policy': {
        'source_inspection': False,
        'sealed_games_present_in_runtime': False,
        'seed': 0,
        'probe_scope': 'initial observation + reset repeatability + one-step fresh-reset interventions',
        'action6_points': 'center and centroid of largest visible non-modal connected component when distinct',
    },
    'games': {},
}

for slug in sorted(DEV):
    info = envs[slug]
    g = {
        'game_id': info.game_id,
        'title': info.title,
        'tags': info.tags,
        'baseline_actions': info.baseline_actions,
    }

    env = arcade.make(info.game_id, seed=0)
    if env is None or env.observation_space is None:
        g['error'] = 'make_failed'
        results['games'][slug] = g
        continue
    init = env.observation_space
    g['initial'] = frame_summary(init)

    reset2 = env.reset()
    if reset2 is None:
        g['reset_repeatability'] = {'error': 'reset_failed'}
    else:
        a = arr_of(init)
        b = arr_of(reset2)
        g['reset_repeatability'] = {
            'same_frame': bool(a.shape == b.shape and np.array_equal(a, b)),
            'same_available_actions': g['initial']['available_actions'] == [int(x.value if hasattr(x, 'value') else x) for x in (reset2.available_actions or [])],
            'second_sha256': sha(b),
        }

    probes = []
    avail = g['initial']['available_actions']
    for aid in [1, 2, 3, 4, 5, 7]:
        if aid not in avail:
            continue
        e = arcade.make(info.game_id, seed=0)
        before = e.observation_space
        after = e.step(GameAction.from_id(aid))
        rec = {'action_id': aid, 'data': {}}
        if after is None:
            rec['error'] = 'step_failed'
        else:
            rec.update(action_effect(before, after))
        probes.append(rec)

    if 6 in avail:
        a0 = arr_of(init)
        h, w = a0.shape
        vals, counts = np.unique(a0, return_counts=True)
        bg = int(vals[np.argmax(counts)])
        points = [('center', (w // 2, h // 2))]
        comp = largest_component_centroid(a0, bg)
        if comp is not None and comp != points[0][1]:
            points.append(('largest_nonmodal_component_centroid', comp))
        seen = set()
        for label, (x, y) in points:
            if (x, y) in seen:
                continue
            seen.add((x, y))
            e = arcade.make(info.game_id, seed=0)
            before = e.observation_space
            after = e.step(GameAction.ACTION6, {'x': int(x), 'y': int(y)})
            rec = {'action_id': 6, 'data': {'x': int(x), 'y': int(y)}, 'point_rule': label}
            if after is None:
                rec['error'] = 'step_failed'
            else:
                rec.update(action_effect(before, after))
            probes.append(rec)

    g['one_step_probes'] = probes
    results['games'][slug] = g
    print(slug, 'actions', avail, 'probes', len(probes))

OUT.write_text(json.dumps(results, indent=2, sort_keys=True), encoding='utf-8')
print('WROTE', OUT)
