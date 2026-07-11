#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path


CANDIDATE_ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest() -> dict[str, str]:
    records: dict[str, str] = {}
    for line in CANDIDATE_ROOT.joinpath("skill-manifest.sha256").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        records[relative] = digest
    return records


def verify_skill(skill_root: Path) -> None:
    expected = {name.removeprefix("skill/"): digest for name, digest in manifest().items()}
    actual = {
        str(path.relative_to(skill_root)): sha256(path)
        for path in skill_root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(name for name in set(actual) & set(expected) if actual[name] != expected[name])
        raise RuntimeError(f"skill manifest mismatch; missing={missing}, extra={extra}, changed={changed}")


def require_file_match(actual: Path, expected: Path, label: str) -> None:
    if not actual.exists() or actual.read_bytes() != expected.read_bytes():
        raise RuntimeError(f"{label} does not match reviewed activation snapshot")


def atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(source.read_bytes())
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def default_workflow_root() -> Path:
    return CANDIDATE_ROOT.parents[2]
