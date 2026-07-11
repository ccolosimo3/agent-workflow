from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script: str, workflow: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / script), "--workflow-root", str(workflow), *extra],
        text=True,
        capture_output=True,
    )


class ActivationTests(unittest.TestCase):
    def test_dry_run_activate_smoke_and_rollback(self):
        with tempfile.TemporaryDirectory(prefix="orchestrate-activation-test-") as directory:
            workflow = Path(directory) / "workflow"
            workflow.mkdir()
            shutil.copy2(ROOT / "AGENTS.before.md", workflow / "AGENTS.md")
            shutil.copy2(ROOT / "ORCHESTRATOR_MODE.before.md", workflow / "ORCHESTRATOR_MODE.md")
            workflow.joinpath("skills").mkdir()

            dry_run = run("activate.py", workflow, "--dry-run")
            self.assertEqual((dry_run.returncode, dry_run.stdout.strip()), (0, "ACTIVATION_READY"), dry_run.stderr)
            self.assertFalse(workflow.joinpath("skills/orchestrate").exists())

            activated = run("activate.py", workflow)
            self.assertEqual((activated.returncode, activated.stdout.strip()), (0, "ACTIVATED"), activated.stderr)
            self.assertEqual(workflow.joinpath("AGENTS.md").read_bytes(), ROOT.joinpath("AGENTS.after.md").read_bytes())
            self.assertEqual(workflow.joinpath("ORCHESTRATOR_MODE.md").read_bytes(), ROOT.joinpath("ORCHESTRATOR_MODE.after.md").read_bytes())

            smoke = subprocess.run([
                sys.executable,
                str(ROOT / "post_install_smoke.py"),
                "--skill", str(workflow / "skills/orchestrate"),
                "--agents", str(workflow / "AGENTS.md"),
                "--mode", str(workflow / "ORCHESTRATOR_MODE.md"),
            ], text=True, capture_output=True)
            self.assertEqual((smoke.returncode, smoke.stdout.strip()), (0, "ACTIVATION_SMOKE_OK"), smoke.stderr)

            skill_file = workflow / "skills/orchestrate/SKILL.md"
            original = skill_file.read_bytes()
            skill_file.write_text("tampered\n")
            protected = run("rollback.py", workflow)
            self.assertNotEqual(protected.returncode, 0)
            self.assertTrue(skill_file.exists())
            skill_file.write_bytes(original)

            rolled_back = run("rollback.py", workflow)
            self.assertEqual((rolled_back.returncode, rolled_back.stdout.strip()), (0, "ROLLED_BACK"), rolled_back.stderr)
            self.assertFalse(workflow.joinpath("skills/orchestrate").exists())
            self.assertEqual(workflow.joinpath("AGENTS.md").read_bytes(), ROOT.joinpath("AGENTS.before.md").read_bytes())
            self.assertEqual(workflow.joinpath("ORCHESTRATOR_MODE.md").read_bytes(), ROOT.joinpath("ORCHESTRATOR_MODE.before.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
