from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "orchestrate" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from orchestrator_core import append_event, load_events, replay  # noqa: E402


def init_program(path: Path, program_id: str = "P1") -> dict:
    return append_event(path, {
        "event_type": "program_initialized",
        "program_id": program_id,
        "payload": {"title": "Pilot", "goal": "Prove orchestration", "next_action": "plan"},
    }, None, 1)


def add_task(path: Path, task_id: str = "T1") -> dict:
    events = load_events(path)
    return append_event(path, {
        "event_type": "task_added",
        "program_id": events[0]["program_id"],
        "task_id": task_id,
        "payload": {"title": task_id, "deliverable": "result", "next_action": "plan"},
    }, events[-1]["event_hash"], replay(events)["coordinator_generation"])


def append(path: Path, event: dict) -> dict:
    events = load_events(path)
    return append_event(path, event, events[-1]["event_hash"] if events else None, replay(events)["coordinator_generation"])


def run_script(name: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], text=True, capture_output=True, env=env)


def event(program_id: str, event_type: str, **kwargs) -> dict:
    return {"program_id": program_id, "event_type": event_type, "payload": kwargs.pop("payload", {}), **kwargs}
