#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from orchestrator_core import load_events, render_status, replay


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("program_dir", type=Path)
    args = parser.parse_args()
    print(render_status(replay(load_events(args.program_dir))), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
