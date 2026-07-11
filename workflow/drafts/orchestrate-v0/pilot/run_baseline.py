#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.scenario.read_bytes()
    scenario = json.loads(raw)
    args.output.mkdir(parents=True, exist_ok=True)
    trace = [
        {"event": "started"},
        {"event": "informational_status"},
        {"event": "yielded_with_safe_next_action"},
        {"event": "operator_continue"},
        {"event": "operator_environment_repair"},
        {"event": "outer_gate"},
    ]
    metrics = {
        "scenario_sha256": hashlib.sha256(raw).hexdigest(),
        "avoidable_pause": 1,
        "operator_repair": 2,
        "operator_request_expected": len(scenario["expected_operator_gates"]),
        "operator_request_avoidable": 1,
        "false_green": 0,
        "authority_violations": 0,
    }
    args.output.joinpath("trace.jsonl").write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in trace))
    args.output.joinpath("metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    args.output.joinpath("final-status.md").write_text("Outcome/phase: awaiting_operator_gate\nNext: outer gate\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
