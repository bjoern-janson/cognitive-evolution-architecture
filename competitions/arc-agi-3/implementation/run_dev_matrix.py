from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from cea_arc3.firewall import DEVELOPMENT_GAMES
from cea_arc3.runner import DevelopmentRunner

ARM_ORDER = (
    "B",
    "B_PERSIST",
    "B+L",
    "B+C",
    "B+A",
    "B+X",
    "B+L+C",
    "B+L+A",
    "B+C+A",
    "B+L+C+A",
    "B+L+C+A+X",
    "A_fixed_0",
    "A_fixed_25",
    "A_fixed_50",
    "A_fixed_75",
    "A_fixed_100",
)
SEED = 0
EXPECTED_RUNS = len(DEVELOPMENT_GAMES) * len(ARM_ORDER)


def _jsonable(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        if isinstance(v, (dict, list, tuple)):
            out[k] = json.dumps(v, sort_keys=True, separators=(",", ":"))
        else:
            out[k] = v
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Run frozen ARC3 Exp2 development matrix")
    ap.add_argument("--environment-root", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--implementation-commit", required=True)
    args = ap.parse_args()

    out = args.output_dir
    if out.exists() and any(out.iterdir()):
        raise RuntimeError(f"output directory must be absent or empty; refusing resume/tuning: {out}")
    out.mkdir(parents=True, exist_ok=True)
    logs = out / "logs"
    logs.mkdir()

    manifest = {
        "status": "RUNNING",
        "implementation_commit": args.implementation_commit,
        "seed": SEED,
        "games": sorted(DEVELOPMENT_GAMES),
        "arms": list(ARM_ORDER),
        "expected_runs": EXPECTED_RUNS,
        "action_budget_per_game_arm": 256,
        "sealed_games_exposed": 0,
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    runner = DevelopmentRunner(args.environment_root, log_dir=logs)
    rows: list[dict] = []
    partial = out / "results.partial.jsonl"

    for game in sorted(DEVELOPMENT_GAMES):
        for arm in ARM_ORDER:
            result = runner.run_game(game, arm, seed=SEED)
            row = asdict(result)
            rows.append(row)
            with partial.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
            print(f"{len(rows):03d}/{EXPECTED_RUNS} {game} {arm} actions={result.actions} levels={result.levels_completed} state={result.terminal_state}", flush=True)

    if len(rows) != EXPECTED_RUNS:
        raise RuntimeError(f"incomplete matrix: {len(rows)} != {EXPECTED_RUNS}")

    (out / "results.json").write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    csv_rows = [_jsonable(r) for r in rows]
    with (out / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)

    manifest["status"] = "COMPLETE"
    manifest["completed_runs"] = len(rows)
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"COMPLETE {len(rows)}/{EXPECTED_RUNS}", flush=True)


if __name__ == "__main__":
    main()
