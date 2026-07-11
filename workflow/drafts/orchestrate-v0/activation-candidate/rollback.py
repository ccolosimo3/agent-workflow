#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

from candidate_common import CANDIDATE_ROOT, atomic_copy, default_workflow_root, require_file_match, verify_skill


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-root", type=Path, default=default_workflow_root())
    args = parser.parse_args()
    workflow = args.workflow_root.resolve()
    agents = workflow / "AGENTS.md"
    mode = workflow / "ORCHESTRATOR_MODE.md"
    target = workflow / "skills/orchestrate"
    quarantine = target.parent / f".orchestrate.rollback-{os.getpid()}"

    require_file_match(agents, CANDIDATE_ROOT / "AGENTS.after.md", "AGENTS.md")
    require_file_match(mode, CANDIDATE_ROOT / "ORCHESTRATOR_MODE.after.md", "ORCHESTRATOR_MODE.md")
    if not target.is_dir():
        raise SystemExit("active orchestrate skill is missing")
    verify_skill(target)
    os.replace(target, quarantine)
    try:
        atomic_copy(CANDIDATE_ROOT / "AGENTS.before.md", agents)
        atomic_copy(CANDIDATE_ROOT / "ORCHESTRATOR_MODE.before.md", mode)
    except Exception:
        os.replace(quarantine, target)
        atomic_copy(CANDIDATE_ROOT / "AGENTS.after.md", agents)
        atomic_copy(CANDIDATE_ROOT / "ORCHESTRATOR_MODE.after.md", mode)
        raise
    shutil.rmtree(quarantine)
    print("ROLLED_BACK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
