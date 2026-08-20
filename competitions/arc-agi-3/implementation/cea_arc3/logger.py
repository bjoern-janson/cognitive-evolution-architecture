from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Mapping


class EventLogger:
    """Append-only JSONL logger for typed summaries; historical frame payloads forbidden."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, kind: str, payload: Any) -> None:
        normalized = self._normalize(payload)
        self._reject_frame_payload(normalized)
        record = {"kind": str(kind), "payload": normalized}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

    @classmethod
    def _normalize(cls, value: Any) -> Any:
        if is_dataclass(value):
            return cls._normalize(asdict(value))
        if isinstance(value, Mapping):
            return {str(k): cls._normalize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set, frozenset)):
            return [cls._normalize(v) for v in value]
        if hasattr(value, "value") and value.__class__.__module__ == "enum":
            return value.value
        # CanonicalStatus and other Enum subclasses are handled by json only if str;
        # convert generic Enums without importing enum here.
        if hasattr(value, "value") and hasattr(value, "name"):
            return cls._normalize(value.value)
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    @classmethod
    def _reject_frame_payload(cls, payload: Any) -> None:
        if isinstance(payload, dict):
            for k, v in payload.items():
                if str(k).lower() in {"frame", "frames", "raw_frame", "frame_payload", "current_frame"}:
                    raise ValueError("historical frame payload logging is forbidden")
                cls._reject_frame_payload(v)
        elif isinstance(payload, (list, tuple)):
            for v in payload:
                cls._reject_frame_payload(v)
