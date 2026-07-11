#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from orchestrator_core import EXIT_INVALID_LOG, LedgerError, rebuild_views, view_status


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check-views", action="store_true")
    group.add_argument("--startup-recover", action="store_true")
    parser.add_argument("program_dir", type=Path)
    args = parser.parse_args()
    try:
        if args.check_views:
            marker = view_status(args.program_dir)
            print(marker)
            return 0 if marker == "CURRENT" else 3
        marker = rebuild_views(args.program_dir)
        print(marker)
        return 0
    except LedgerError as exc:
        print(f"INVALID_LOG: {exc}", file=sys.stderr)
        return EXIT_INVALID_LOG


if __name__ == "__main__":
    raise SystemExit(main())
