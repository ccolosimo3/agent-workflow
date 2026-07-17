#!/usr/bin/env python3

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("plan_archive.py")


def command(args: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def write_item(plans: Path, name: str, status: str = "implemented", days_old: int = 60) -> Path:
    item = plans / "archive" / name
    item.mkdir(parents=True)
    date = (dt.date.today() - dt.timedelta(days=days_old)).isoformat()
    (item / "README.md").write_text(
        f"---\ntitle: {name}\nstatus: {status}\nupdated: {date}\nlanded: {date}\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    (item / "notes.md").write_text("durable plan notes\n", encoding="utf-8")
    return item


def seed_remote(root: Path) -> Path:
    remote = root / "archive.git"
    command(["git", "init", "--bare", "--initial-branch=main", str(remote)])
    seed = root / "seed"
    command(["git", "clone", str(remote), str(seed)])
    (seed / "README.md").write_text("# Plan archive\n", encoding="utf-8")
    command(["git", "add", "README.md"], cwd=seed)
    command(
        [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-m",
            "Initialize archive",
        ],
        cwd=seed,
    )
    command(["git", "push", "origin", "main"], cwd=seed)
    return remote


class PlanArchiveTests(unittest.TestCase):
    def test_audit_separates_eligible_and_held_items(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            plans = Path(temp) / "plans"
            write_item(plans, "done-item")
            write_item(plans, "active-item", status="promoted")
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "audit",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--json",
                ]
            )
            payload = json.loads(result.stdout)
            self.assertEqual(["done-item"], [item["item"] for item in payload["eligible"]])
            self.assertEqual(["active-item"], [item["item"] for item in payload["held"]])

    def test_audit_holds_likely_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            plans = Path(temp) / "plans"
            item = write_item(plans, "unsafe-item")
            (item / ".env").write_text("TOKEN=secret\n", encoding="utf-8")
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "audit",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--json",
                ]
            )
            payload = json.loads(result.stdout)
            self.assertEqual([], payload["eligible"])
            self.assertIn("sensitive filename: .env", payload["held"][0]["reasons"])

    def test_audit_holds_symlinked_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            plans = Path(temp) / "plans"
            item = write_item(plans, "linked-item")
            outside = Path(temp) / "outside.md"
            outside.write_text("must not be followed\n", encoding="utf-8")
            (item / "linked.md").symlink_to(outside)
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "audit",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--json",
                ]
            )
            payload = json.loads(result.stdout)
            self.assertEqual([], payload["eligible"])
            self.assertIn("symlink: linked.md", payload["held"][0]["reasons"])

    def test_sync_pushes_and_fresh_clone_verifies_without_pruning(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plans = root / "plans"
            item = write_item(plans, "done-item")
            remote = seed_remote(root)
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "sync",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--remote",
                    str(remote),
                    "--item",
                    "done-item",
                    "--json",
                ]
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["verified_with_fresh_clone"])
            self.assertEqual([], payload["pruned"])
            self.assertTrue(item.exists())
            verify = root / "manual-verify"
            command(["git", "clone", "--quiet", str(remote), str(verify)])
            self.assertEqual(
                "durable plan notes\n",
                (verify / "projects" / "example" / "done-item" / "notes.md").read_text(),
            )
            self.assertEqual(1, len(list((verify / "manifests").glob("*.tsv"))))

    def test_sync_prunes_only_after_verified_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plans = root / "plans"
            item = write_item(plans, "done-item")
            remote = seed_remote(root)
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "sync",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--remote",
                    str(remote),
                    "--item",
                    "done-item",
                    "--prune",
                    "--json",
                ]
            )
            payload = json.loads(result.stdout)
            self.assertEqual(["done-item"], payload["pruned"])
            self.assertFalse(item.exists())

    def test_remote_conflict_fails_and_preserves_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plans = root / "plans"
            item = write_item(plans, "done-item")
            remote = seed_remote(root)
            first = command(["git", "clone", str(remote), str(root / "conflict")])
            self.assertEqual(0, first.returncode)
            conflict = root / "conflict"
            destination = conflict / "projects" / "example" / "done-item"
            destination.mkdir(parents=True)
            (destination / "README.md").write_text("different bytes\n", encoding="utf-8")
            command(["git", "add", "."], cwd=conflict)
            command(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-m",
                    "Create conflict",
                ],
                cwd=conflict,
            )
            command(["git", "push", "origin", "main"], cwd=conflict)
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "sync",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--remote",
                    str(remote),
                    "--item",
                    "done-item",
                    "--prune",
                ],
                check=False,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("archive verification mismatch", result.stderr)
            self.assertTrue(item.exists())

    def test_rejected_push_preserves_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plans = root / "plans"
            item = write_item(plans, "done-item")
            remote = seed_remote(root)
            hook = remote / "hooks" / "pre-receive"
            hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
            hook.chmod(0o755)
            result = command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "sync",
                    "--plans-root",
                    str(plans),
                    "--project",
                    "example",
                    "--remote",
                    str(remote),
                    "--item",
                    "done-item",
                    "--prune",
                ],
                check=False,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("git push", result.stderr)
            self.assertTrue(item.exists())


if __name__ == "__main__":
    unittest.main()
