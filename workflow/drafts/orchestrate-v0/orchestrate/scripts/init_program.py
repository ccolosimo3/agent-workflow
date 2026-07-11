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
    parser.add_argument("--program-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--next-action", default="lock authority")
    args = parser.parse_args()
    args.program_dir.mkdir(parents=True, exist_ok=True)
    event = {
        "event_type": "program_initialized",
        "program_id": args.program_id,
        "payload": {"title": args.title, "goal": args.goal, "next_action": args.next_action},
    }
    try:
        result = append_event(args.program_dir, event, None, 1)
    except LedgerError as exc:
        print(f"{exc.marker}: {exc}", file=sys.stderr)
        return exc.exit_code
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
