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
        "payload": {"title": task_id, "deliverable": "result", "next_action": "plan", "owned_paths": ["src"], "verification_commands": ["smoke"]},
    }, events[-1]["event_hash"], replay(events)["coordinator_generation"])


def confirm_policy(path: Path) -> dict:
    return append(path, event("P1", "model_policy_confirmed", payload={
        "policy_revision": 1,
        "mode": "auto",
        "route_classes": {"balanced": {"model": "terra", "max_reasoning": "xhigh"}},
    }))


def assign_task(path: Path, task_id: str, thread_id: str) -> dict:
    route = {"model_policy_revision": 1, "route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"}
    append(path, event("P1", "model_route_selected", task_id=task_id, payload=route))
    append(path, event("P1", "dispatch_intent_recorded", task_id=task_id, payload={"assignment_generation": 1, "idempotency_key": f"K-{task_id}"}))
    return append(path, event("P1", "assignment_started", task_id=task_id, payload={
        "assignment_generation": 1,
        "assignment_id": f"A-{task_id}",
        "idempotency_key": f"K-{task_id}",
        "task_handle": {"thread_id": thread_id},
        "model_policy_revision": 1,
        "model_route": {"route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"},
    }))


def append(path: Path, event: dict) -> dict:
    events = load_events(path)
    return append_event(path, event, events[-1]["event_hash"] if events else None, replay(events)["coordinator_generation"])


def run_script(name: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], text=True, capture_output=True, env=env)


def event(program_id: str, event_type: str, **kwargs) -> dict:
    return {"program_id": program_id, "event_type": event_type, "payload": kwargs.pop("payload", {}), **kwargs}
