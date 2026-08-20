from pathlib import Path
import pytest
from cea_arc3.logger import EventLogger


def test_logger_rejects_frame_payload(tmp_path: Path):
    log=EventLogger(tmp_path/'x.jsonl')
    with pytest.raises(ValueError):
        log.append('bad', {'frame': [[0]]})


def test_logger_allows_hash_summary(tmp_path: Path):
    p=tmp_path/'x.jsonl'; log=EventLogger(p)
    log.append('ok', {'frame_sha256':'abc','changed_cells':2})
    assert p.read_text().count('\n')==1
