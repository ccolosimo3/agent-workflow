#!/usr/bin/env python3
"""Audit and safely externalize terminal plan folders to a Git repository."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Iterable


TERMINAL_STATUSES = {"implemented", "closed", "deferred"}
MAX_FILE_BYTES = 50 * 1024 * 1024
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    "credentials",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
}
SENSITIVE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(rb"\bghp_[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    re.compile(rb"\bsk-proj-[A-Za-z0-9_-]{20,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
)


class ArchiveError(RuntimeError):
    pass


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ArchiveError(f"command failed ({' '.join(command)}): {detail}")
    return result.stdout.strip()


def validate_component(value: str, label: str) -> str:
    if not SAFE_COMPONENT.fullmatch(value):
        raise ArchiveError(f"unsafe {label}: {value!r}")
    return value


def parse_frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip("'\"")
    return values if closed else {}


def parse_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs):
            path = current_path / name
            if path.is_symlink():
                yield path
        for name in sorted(files):
            yield current_path / name


def scan_tree(root: Path) -> tuple[list[str], int, int]:
    blockers: list[str] = []
    total_bytes = 0
    file_count = 0
    if root.is_symlink():
        blockers.append("work-item root is a symlink")
    for path in iter_files(root):
        relative = path.relative_to(root).as_posix()
        if "\t" in relative or "\n" in relative:
            blockers.append(f"unsupported path characters: {relative!r}")
            continue
        if path.is_symlink():
            blockers.append(f"symlink: {relative}")
            continue
        if not path.is_file():
            blockers.append(f"unsupported filesystem entry: {relative}")
            continue
        file_count += 1
        size = path.stat().st_size
        total_bytes += size
        name = path.name.lower()
        if name in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES:
            blockers.append(f"sensitive filename: {relative}")
        if size > MAX_FILE_BYTES:
            blockers.append(f"file exceeds 50 MiB: {relative} ({size} bytes)")
            continue
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                if any(pattern.search(chunk) for pattern in SECRET_PATTERNS):
                    blockers.append(f"likely credential content: {relative}")
                    break
    return sorted(set(blockers)), file_count, total_bytes


def item_record(item_dir: Path, cutoff: dt.date) -> dict[str, object]:
    metadata = parse_frontmatter(item_dir / "README.md")
    status = metadata.get("status", "").split("—", 1)[0].strip().lower()
    landed = parse_date(metadata.get("landed"))
    updated = parse_date(metadata.get("updated"))
    age_date = landed or updated
    age_source = "landed" if landed else "updated" if updated else None
    reasons: list[str] = []
    if status not in TERMINAL_STATUSES:
        reasons.append("status is not terminal")
    if age_date is None:
        reasons.append("missing valid landed/updated date")
    elif age_date > cutoff:
        reasons.append(f"{age_source} date is newer than cutoff")
    blockers, file_count, total_bytes = scan_tree(item_dir)
    reasons.extend(blockers)
    return {
        "item": item_dir.name,
        "status": status or None,
        "age_date": age_date.isoformat() if age_date else None,
        "age_source": age_source,
        "eligible": not reasons,
        "reasons": reasons,
        "files": file_count,
        "bytes": total_bytes,
    }


def audit(plans_root: Path, project: str, older_than_days: int) -> dict[str, object]:
    validate_component(project, "project slug")
    archive_root = plans_root.resolve() / "archive"
    if not archive_root.is_dir():
        raise ArchiveError(f"archive directory not found: {archive_root}")
    cutoff = dt.date.today() - dt.timedelta(days=older_than_days)
    records = []
    for child in sorted(archive_root.iterdir(), key=lambda path: path.name):
        if child.is_dir() and not child.name.startswith("."):
            validate_component(child.name, "work-item name")
            records.append(item_record(child, cutoff))
    return {
        "project": project,
        "plans_root": str(plans_root.resolve()),
        "archive_root": str(archive_root),
        "cutoff": cutoff.isoformat(),
        "older_than_days": older_than_days,
        "eligible": [record for record in records if record["eligible"]],
        "held": [record for record in records if not record["eligible"]],
    }


def file_manifest(root: Path) -> list[tuple[str, int, str]]:
    entries: list[tuple[str, int, str]] = []
    for path in iter_files(root):
        if path.is_symlink() or not path.is_file():
            raise ArchiveError(f"cannot manifest unsafe path: {path}")
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        entries.append((path.relative_to(root).as_posix(), path.stat().st_size, digest.hexdigest()))
    return sorted(entries)


def compare_trees(source: Path, destination: Path) -> None:
    source_manifest = file_manifest(source)
    destination_manifest = file_manifest(destination)
    if source_manifest != destination_manifest:
        raise ArchiveError(
            f"archive verification mismatch: {source.name} differs from {destination}"
        )


def write_batch_manifest(
    path: Path,
    archive_root: Path,
    destinations: list[Path],
) -> None:
    rows = ["sha256\tbytes\tpath"]
    for destination in destinations:
        for relative, size, digest in file_manifest(destination):
            archived_path = (destination.relative_to(archive_root) / relative).as_posix()
            rows.append(f"{digest}\t{size}\t{archived_path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def remote_default_branch(clone: Path) -> str:
    branch = run(["git", "branch", "--show-current"], cwd=clone)
    if not branch:
        raise ArchiveError("archive clone has no checked-out default branch")
    return branch


def sync(
    plans_root: Path,
    project: str,
    remote: str,
    items: list[str],
    older_than_days: int,
    prune: bool,
) -> dict[str, object]:
    validate_component(project, "project slug")
    if not items:
        raise ArchiveError("sync requires at least one --item")
    if len(set(items)) != len(items):
        raise ArchiveError("duplicate --item values")

    archive_root = plans_root.resolve() / "archive"
    cutoff = dt.date.today() - dt.timedelta(days=older_than_days)
    sources: list[Path] = []
    for item in items:
        validate_component(item, "work-item name")
        source = archive_root / item
        if not source.is_dir():
            raise ArchiveError(f"work item not found: {source}")
        record = item_record(source, cutoff)
        if not record["eligible"]:
            raise ArchiveError(f"work item is not eligible: {item}: {record['reasons']}")
        sources.append(source)

    with tempfile.TemporaryDirectory(prefix="plan-cleanup-") as temp:
        temp_root = Path(temp)
        clone = temp_root / "archive"
        run(["git", "clone", "--quiet", remote, str(clone)])
        branch = remote_default_branch(clone)
        destinations: list[Path] = []
        copied_destinations: list[Path] = []
        for source in sources:
            destination = clone / "projects" / project / source.name
            if destination.exists():
                compare_trees(source, destination)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, destination, copy_function=shutil.copy2)
                compare_trees(source, destination)
                copied_destinations.append(destination)
            destinations.append(destination)

        manifest_relative: str | None = None
        if copied_destinations:
            stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            manifest = clone / "manifests" / f"{stamp}-{project}.tsv"
            if manifest.exists():
                raise ArchiveError(f"manifest collision: {manifest.name}")
            write_batch_manifest(manifest, clone, copied_destinations)
            manifest_relative = manifest.relative_to(clone).as_posix()
            run(["git", "add", "--", "projects", "manifests"], cwd=clone)
            run(
                [
                    "git",
                    "-c",
                    "user.name=Plan Archive",
                    "-c",
                    "user.email=plan-archive@local.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    f"Archive {project}: {', '.join(items)}",
                ],
                cwd=clone,
            )
            run(["git", "push", "--quiet", "origin", f"HEAD:{branch}"], cwd=clone)

        commit = run(["git", "rev-parse", "HEAD"], cwd=clone)
        remote_commit_output = run(["git", "ls-remote", remote, f"refs/heads/{branch}"])
        remote_commit = remote_commit_output.split()[0] if remote_commit_output else ""
        if remote_commit != commit:
            raise ArchiveError(
                f"remote verification failed: expected {commit}, found {remote_commit or 'nothing'}"
            )

        verify_clone = temp_root / "verify"
        run(
            [
                "git",
                "clone",
                "--quiet",
                "--branch",
                branch,
                "--single-branch",
                remote,
                str(verify_clone),
            ]
        )
        verified_commit = run(["git", "rev-parse", "HEAD"], cwd=verify_clone)
        if verified_commit != commit:
            raise ArchiveError(
                f"fresh clone is stale: expected {commit}, found {verified_commit}"
            )
        for source in sources:
            compare_trees(source, verify_clone / "projects" / project / source.name)

        pruned: list[str] = []
        if prune:
            for source in sources:
                shutil.rmtree(source)
                pruned.append(source.name)

        return {
            "remote": remote,
            "branch": branch,
            "commit": commit,
            "project": project,
            "items": items,
            "new_items": [path.name for path in copied_destinations],
            "manifest": manifest_relative,
            "verified_with_fresh_clone": True,
            "pruned": pruned,
        }


def format_audit(result: dict[str, object]) -> str:
    lines = [
        f"Project: {result['project']}",
        f"Archive: {result['archive_root']}",
        f"Cutoff: {result['cutoff']} ({result['older_than_days']} days)",
        "Eligible:",
    ]
    eligible = result["eligible"]
    if eligible:
        for record in eligible:
            lines.append(
                f"  - {record['item']} ({record['status']}, {record['files']} files, {record['bytes']} bytes)"
            )
    else:
        lines.append("  - none")
    lines.append("Held:")
    held = result["held"]
    if held:
        for record in held:
            lines.append(f"  - {record['item']}: {'; '.join(record['reasons'])}")
    else:
        lines.append("  - none")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="read-only candidate audit")
    audit_parser.add_argument("--plans-root", required=True, type=Path)
    audit_parser.add_argument("--project", required=True)
    audit_parser.add_argument("--older-than-days", type=int, default=30)
    audit_parser.add_argument("--json", action="store_true")

    sync_parser = subparsers.add_parser("sync", help="archive an exact approved batch")
    sync_parser.add_argument("--plans-root", required=True, type=Path)
    sync_parser.add_argument("--project", required=True)
    sync_parser.add_argument("--remote", required=True)
    sync_parser.add_argument("--item", action="append", required=True)
    sync_parser.add_argument("--older-than-days", type=int, default=30)
    sync_parser.add_argument("--prune", action="store_true")
    sync_parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.older_than_days < 0:
        print("error: --older-than-days must be non-negative", file=sys.stderr)
        return 2
    try:
        if args.command == "audit":
            result = audit(args.plans_root, args.project, args.older_than_days)
            print(json.dumps(result, indent=2) if args.json else format_audit(result))
        else:
            result = sync(
                args.plans_root,
                args.project,
                args.remote,
                args.item,
                args.older_than_days,
                args.prune,
            )
            print(json.dumps(result, indent=2) if args.json else json.dumps(result))
    except (ArchiveError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
