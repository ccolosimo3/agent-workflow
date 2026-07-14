from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


HOOK = Path(__file__).resolve().parents[1] / "worktree_tripwire.py"


class WorktreeTripwireTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.base = Path(self.tempdir.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / "dist").mkdir()

    def run_hook(self, command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        payload = {"tool_input": {"command": command}, "cwd": str(cwd or self.repo)}
        return subprocess.run(
            ["python3", str(HOOK)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env={**os.environ, "TRIPWIRE_TEST_OUTSIDE": str(self.base / "outside")},
            check=False,
        )

    def assert_allowed(self, command: str, cwd: Path | None = None) -> None:
        result = self.run_hook(command, cwd)
        self.assertEqual(0, result.returncode, result.stderr)

    def assert_blocked(self, command: str, cwd: Path | None = None) -> None:
        result = self.run_hook(command, cwd)
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("Blocked", result.stderr)

    def test_allows_ordinary_commands_and_outside_reads(self) -> None:
        self.assert_allowed("pnpm test")
        self.assert_allowed("cat /etc/hosts")
        self.assert_allowed("echo 'rm -rf /'")
        self.assert_allowed("command -v rm")

    def test_allows_destructive_targets_inside_worktree(self) -> None:
        self.assert_allowed("rm -rf ./dist")
        self.assert_allowed("find ./dist -type f -delete")
        self.assert_allowed("rm -rf ./dist/*")

    def test_blocks_absolute_parent_and_root_targets(self) -> None:
        self.assert_blocked("rm -rf /Users/example")
        self.assert_blocked("rm -rf /")
        self.assert_blocked("rm -rf ..")
        self.assert_blocked("rm -rf /Volumes/example")

    def test_blocks_home_and_environment_targets(self) -> None:
        self.assert_blocked('rm -rf "$HOME"')
        self.assert_blocked('rm -rf "$TRIPWIRE_TEST_OUTSIDE"')
        self.assert_blocked('rm -rf "$UNKNOWN_TRIPWIRE_PATH"')
        self.assert_blocked('rm -rf "$(printf /tmp/example)"')

    def test_compound_command_cannot_smuggle_a_worktree_mention(self) -> None:
        self.assert_blocked(f"rm -rf /Users/example && echo {self.repo}")

    def test_directory_changes_are_applied_before_target_resolution(self) -> None:
        self.assert_blocked("cd .. && rm -rf ./outside")
        self.assert_allowed("cd ./dist && rm -rf ./generated")
        self.assert_blocked("cd - && rm -rf ./unknown")

    def test_nested_shell_and_wrappers_are_inspected(self) -> None:
        self.assert_blocked("bash -c 'rm -rf ..'")
        self.assert_blocked("bash -lc 'rm -rf ..'")
        self.assert_blocked("env TARGET=.. sh -c 'rm -rf $TARGET'")
        self.assert_allowed("env TARGET=./dist sh -c 'rm -rf $TARGET'")
        self.assert_blocked("printf '%s\\0' .. | xargs -0 rm -rf")
        self.assert_blocked("time rm -rf ..")
        self.assert_blocked("exec rm -rf ..")
        self.assert_blocked("command -p rm -rf ..")
        self.assert_blocked("printf '%s\\0' x | xargs -0 sh -c 'rm -rf ..'")

    def test_blocks_privileged_and_system_destructive_commands(self) -> None:
        self.assert_blocked("sudo true")
        self.assert_blocked("/sbin/diskutil eraseDisk APFS Empty /dev/disk9")
        self.assert_blocked("mkfs.ext4 /dev/disk9")

    def test_find_and_rsync_use_the_mutated_boundary(self) -> None:
        self.assert_blocked("find .. -type f -delete")
        self.assert_blocked("find .. -exec rm {} +")
        self.assert_blocked("find . -exec sh -c 'rm -rf /' +")
        self.assert_allowed("rsync --delete ../source/ ./dist/")
        self.assert_allowed("rsync --dry-run --delete ./dist/ ../destination/")
        self.assert_blocked("rsync --delete ./dist/ ../destination/")
        self.assert_blocked("rsync --delete ./dist/ host:/destination/")

    def test_mv_treats_source_and_destination_as_mutated(self) -> None:
        self.assert_blocked("mv ../source ./dist/")
        self.assert_blocked("mv ./dist --target-directory=../destination")

    def test_symlink_escape_is_blocked(self) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        (self.repo / "escape").symlink_to(outside, target_is_directory=True)
        self.assert_blocked("rm -rf ./escape/child")

    def test_destructive_command_outside_git_fails_closed(self) -> None:
        outside = self.base / "not-a-repo"
        outside.mkdir()
        self.assert_blocked("rm -rf ./dist", outside)
        self.assert_allowed("echo ok", outside)

    def test_malformed_destructive_command_fails_closed(self) -> None:
        self.assert_blocked("rm -rf 'unterminated")

    def test_invalid_payload_fails_closed(self) -> None:
        result = subprocess.run(
            ["python3", str(HOOK)],
            input="{}",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("invalid PreToolUse payload", result.stderr)


if __name__ == "__main__":
    unittest.main()
