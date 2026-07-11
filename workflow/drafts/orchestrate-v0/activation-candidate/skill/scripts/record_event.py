#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from orchestrator_core import LedgerError, append_event


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("program_dir", type=Path)
    parser.add_argument("--event-file", type=Path)
    parser.add_argument("--event-json")
    parser.add_argument("--expected-prev-event-hash", default="")
    parser.add_argument("--coordinator-generation", type=int, required=True)
    parser.add_argument("--wait-for-lock", action="store_true")
    args = parser.parse_args()
    if bool(args.event_file) == bool(args.event_json):
        parser.error("provide exactly one of --event-file or --event-json")
    event = json.loads(args.event_file.read_text() if args.event_file else args.event_json)
    expected = args.expected_prev_event_hash or None
    try:
        result = append_event(args.program_dir, event, expected, args.coordinator_generation, not args.wait_for_lock)
    except LedgerError as exc:
        print(f"{exc.marker}: {exc}", file=sys.stderr)
        return exc.exit_code
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
