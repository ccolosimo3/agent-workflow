#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--orchestrated", type=Path, required=True)
    args = parser.parse_args()
    baseline = json.loads(args.baseline.joinpath("metrics.json").read_text())
    orchestrated = json.loads(args.orchestrated.joinpath("metrics.json").read_text())
    checks = {
        "same_scenario": baseline["scenario_sha256"] == orchestrated["scenario_sha256"],
        "zero_orchestrated_pauses": orchestrated["avoidable_pause"] == 0,
        "fewer_pauses": orchestrated["avoidable_pause"] < baseline["avoidable_pause"],
        "no_more_repair": orchestrated["operator_repair"] <= baseline["operator_repair"],
        "no_avoidable_requests": orchestrated["operator_request_avoidable"] == 0,
        "no_false_green": orchestrated["false_green"] == 0,
        "no_authority_violations": orchestrated["authority_violations"] == 0,
    }
    print(json.dumps(checks, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
