from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

class EventLogger:
    """Append-only JSONL logger. Callers must pass typed summaries, never frame payloads."""
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def append(self, kind: str, payload: Any) -> None:
        if is_dataclass(payload):
            payload = asdict(payload)
        self._reject_frame_payload(payload)
        record = {"kind": str(kind), "payload": payload}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True, separators=(",", ":"), default=str) + "\n")
    @classmethod
    def _reject_frame_payload(cls, payload: Any) -> None:
        if isinstance(payload, dict):
            for k, v in payload.items():
                if str(k).lower() in {"frame", "frames", "raw_frame", "frame_payload"}:
                    raise ValueError("historical frame payload logging is forbidden")
                cls._reject_frame_payload(v)
        elif isinstance(payload, (list, tuple)):
            for v in payload:
                cls._reject_frame_payload(v)
