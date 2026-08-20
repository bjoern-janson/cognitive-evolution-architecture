from __future__ import annotations

from typing import Iterable

import numpy as np

from .state import ObservationDescriptor
from .transition import action_mask, frame_sha256


def describe_observation(frame: np.ndarray, available_actions: Iterable[int]) -> ObservationDescriptor:
    arr = np.asarray(frame)
    if arr.shape != (64, 64):
        raise ValueError(f"expected 64x64 visible frame, got {arr.shape}")
    vals, counts = np.unique(arr, return_counts=True)
    if any(int(v) < 0 or int(v) > 15 for v in vals):
        raise ValueError("visible color value outside 0..15")
    hist = [0] * 16
    for v, c in zip(vals, counts):
        hist[int(v)] = int(c)
    modal = int(vals[int(np.argmax(counts))])
    non_modal = int(arr.size - hist[modal])
    return ObservationDescriptor(frame_sha256=frame_sha256(arr), color_histogram=tuple(hist), non_modal_color=modal, non_modal_cells=non_modal, available_action_mask=action_mask(available_actions))
