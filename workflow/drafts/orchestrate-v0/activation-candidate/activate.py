#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from candidate_common import CANDIDATE_ROOT, atomic_copy, default_workflow_root, require_file_match, verify_skill


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-root", type=Path, default=default_workflow_root())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    workflow = args.workflow_root.resolve()
    agents = workflow / "AGENTS.md"
    mode = workflow / "ORCHESTRATOR_MODE.md"
    target = workflow / "skills/orchestrate"
    source = CANDIDATE_ROOT / "skill"

    verify_skill(source)
    require_file_match(agents, CANDIDATE_ROOT / "AGENTS.before.md", "AGENTS.md")
    require_file_match(mode, CANDIDATE_ROOT / "ORCHESTRATOR_MODE.before.md", "ORCHESTRATOR_MODE.md")
    if target.exists():
        raise SystemExit("active orchestrate skill already exists")
    if args.dry_run:
        print("ACTIVATION_READY")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.parent / f".orchestrate.activation-{os.getpid()}"
    if temporary.exists():
        raise SystemExit(f"temporary activation target already exists: {temporary}")
    shutil.copytree(source, temporary)
    verify_skill(temporary)
    installed = False
    try:
        atomic_copy(CANDIDATE_ROOT / "AGENTS.after.md", agents)
        atomic_copy(CANDIDATE_ROOT / "ORCHESTRATOR_MODE.after.md", mode)
        os.replace(temporary, target)
        installed = True
        smoke = subprocess.run([
            sys.executable,
            str(CANDIDATE_ROOT / "post_install_smoke.py"),
            "--skill", str(target),
            "--agents", str(agents),
            "--mode", str(mode),
        ], text=True, capture_output=True)
        if smoke.returncode != 0:
            raise RuntimeError(smoke.stderr or smoke.stdout)
    except Exception:
        atomic_copy(CANDIDATE_ROOT / "AGENTS.before.md", agents)
        atomic_copy(CANDIDATE_ROOT / "ORCHESTRATOR_MODE.before.md", mode)
        if installed and target.exists():
            shutil.rmtree(target)
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    print("ACTIVATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
