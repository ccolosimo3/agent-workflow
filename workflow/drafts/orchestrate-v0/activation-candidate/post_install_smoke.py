#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from candidate_common import verify_skill


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, type=Path)
    parser.add_argument("--agents", required=True, type=Path)
    parser.add_argument("--mode", required=True, type=Path)
    args = parser.parse_args()

    verify_skill(args.skill)
    skill_text = args.skill.joinpath("SKILL.md").read_text()
    metadata = args.skill.joinpath("agents/openai.yaml").read_text()
    if not skill_text.startswith("---\nname: orchestrate\n") or "$orchestrate" not in metadata:
        raise SystemExit("skill discovery metadata is invalid")
    if "**E) Orchestrate an end-to-end program**" not in args.agents.read_text():
        raise SystemExit("Startup Routing E is missing")
    if "status: active-v0" not in args.mode.read_text():
        raise SystemExit("Orchestrator Mode is not active-v0")

    scripts = args.skill / "scripts"
    with tempfile.TemporaryDirectory(prefix="orchestrate-activation-smoke-") as directory:
        program = Path(directory) / "program"
        initialized = subprocess.run([
            sys.executable,
            str(scripts / "init_program.py"),
            str(program),
            "--program-id", "ACTIVATION-SMOKE",
            "--title", "Activation smoke",
            "--goal", "Prove explicit-path installed skill execution",
        ], text=True, capture_output=True)
        if initialized.returncode != 0:
            raise SystemExit(initialized.stderr or initialized.stdout)
        validated = subprocess.run([
            sys.executable,
            str(scripts / "validate_program.py"),
            "--check-views",
            str(program),
        ], text=True, capture_output=True)
        if (validated.returncode, validated.stdout.strip()) != (0, "CURRENT"):
            raise SystemExit(validated.stderr or validated.stdout)
    print("ACTIVATION_SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
