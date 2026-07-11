#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "orchestrate" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from orchestrator_core import append_event, handle_operator_message, load_events, replay, render_status, select_route  # noqa: E402


def append(output: Path, item: dict) -> dict:
    events = load_events(output)
    return append_event(output, item, events[-1]["event_hash"] if events else None, replay(events)["coordinator_generation"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.scenario.read_bytes()
    scenario = json.loads(raw)
    args.output.mkdir(parents=True, exist_ok=True)
    required = {"informational_status", "environment_repair", "stale_review", "controlled_reviewer_replacement", "model_escalation", "outer_gate"}
    expected_tasks = {"research": ("balanced", "environment_blocked"), "review": ("deep", "stale_tip")}
    actual_tasks = {t.get("task_id"): (t.get("class"), t.get("failure")) for t in scenario.get("tasks", [])}
    mechanisms = {"authority_lock", "dispatch", "writer_lease", "environment_attestation", "verification", "review_invalidation", "assignment_fence", "route_escalation", "replacement_dispatch", "candidate_certification", "operator_gate"}
    authority = scenario.get("authority") == {"mode": "read_only_offline", "writers": 1, "operator_gates": ["outer_gate"]}
    routing = scenario.get("routing") == {"research": {"class": "balanced", "reasoning": "high"}, "review": {"class": "deep", "reasoning": "high", "escalated_reasoning": "xhigh"}}
    if set(scenario.get("injections", [])) != required or actual_tasks != expected_tasks or scenario.get("expected_operator_gates") != ["outer_gate"] or set(scenario.get("expected_mechanisms", [])) != mechanisms or not authority or not routing:
        raise SystemExit("scenario injections do not match V0 oracle")
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "program_initialized", "payload": {"title": "Pilot", "goal": "Execute immutable scenario", "next_action": "continue safe work"}})
    for task in scenario["tasks"]:
        task_contract = {"owned_paths": ["pilot-output"], "verification_commands": ["offline-smoke"]} if task["task_id"] == "research" else {"owned_paths": ["review-output"], "verification_commands": []}
        append(args.output, {"program_id": scenario["scenario_id"], "event_type": "task_added", "task_id": task["task_id"], "payload": {"title": task["task_id"], "failure": task["failure"], **task_contract}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "program_transition", "prior_state": "draft", "next_state": "authority_locked", "payload": {"authority_envelope": "operator-confirmed read-only offline pilot"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "program_transition", "prior_state": "authority_locked", "next_state": "graph_ready", "payload": {}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "program_transition", "prior_state": "graph_ready", "next_state": "active", "payload": {"next_action": "dispatch"}})
    policy = {"policy_revision": 1, "mode": "auto", "route_classes": {"fast": {"model": "luna", "max_reasoning": "high"}, "balanced": {"model": "terra", "max_reasoning": "xhigh"}, "deep": {"model": "sol", "max_reasoning": "xhigh"}}}
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "model_policy_confirmed", "payload": policy})
    for task in scenario["tasks"]:
        route = select_route(policy, "moderate" if task["class"] == "balanced" else "high")
        route_payload = {"model_policy_revision": 1, **route, "risk_class": "routine", "routing_rationale": "scenario complexity"}
        append(args.output, {"program_id": scenario["scenario_id"], "event_type": "model_route_selected", "task_id": task["task_id"], "payload": route_payload})
        append(args.output, {"program_id": scenario["scenario_id"], "event_type": "dispatch_intent_recorded", "task_id": task["task_id"], "payload": {"assignment_generation": 1, "idempotency_key": f"pilot:{task['task_id']}:1"}})
        handle = {"thread_id": f"desktop-{task['task_id']}-1", "state": "active"}
        append(args.output, {"program_id": scenario["scenario_id"], "event_type": "assignment_started", "task_id": task["task_id"], "payload": {"assignment_generation": 1, "assignment_id": f"{task['task_id']}-1", "idempotency_key": f"pilot:{task['task_id']}:1", "task_handle": handle, "model_policy_revision": 1, "model_route": route}})
        for prior, nxt in (("proposed", "planning"), ("planning", "review_ready"), ("review_ready", "spec_review"), ("spec_review", "ready"), ("ready", "assigned"), ("assigned", "running")):
            append(args.output, {"program_id": scenario["scenario_id"], "event_type": "task_transition", "task_id": task["task_id"], "prior_state": prior, "next_state": nxt, "payload": {}})
    handle_operator_message(args.output, "informational", "status?", {"program_id": scenario["scenario_id"], "event_type": "task_transition", "task_id": "review", "prior_state": "running", "next_state": "verifying", "payload": {"next_action": "review"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "task_transition", "task_id": "research", "prior_state": "running", "next_state": "environment_blocked", "payload": {"resume_state": "running", "reason": "missing readiness"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "environment_attested", "task_id": "research", "payload": {"id": "environment-repair", "task_id": "research", "checkout": str(args.output.resolve()), "base": "pilot-base", "tip": "final", "assignment_generation": 1, "topology_revision": 1, "commands": [{"command": "offline-smoke", "result": "passed", "exit_code": 0, "output_sha256": hashlib.sha256(b"offline-smoke:passed").hexdigest()}], "ready": True, "dirty_state": "clean", "evidence": "isolated temporary directory"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "task_transition", "task_id": "research", "prior_state": "environment_blocked", "next_state": "running", "payload": {}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "task_transition", "task_id": "review", "prior_state": "verifying", "next_state": "inner_review", "payload": {}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "review_recorded", "task_id": "research", "payload": {"review_id": "R1", "review_unit": "pilot", "review_role": "inner", "reviewer_task_id": "desktop-review-1", "reviewer_assignment_task_id": "review", "assignment_generation": 1, "verdict": "APPROVED", "tip": "old"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "assignment_fenced", "task_id": "review", "payload": {"assignment_generation": 1, "reason": "stale reviewer tip"}})
    escalated = {"route_class": "deep", "model_id": "sol", "reasoning_effort": "xhigh"}
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "model_route_changed", "task_id": "review", "payload": {"model_policy_revision": 1, **escalated, "risk_class": "certifying_review", "exceptional_trigger": "stale adversarial review"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "dispatch_intent_recorded", "task_id": "review", "payload": {"assignment_generation": 2, "idempotency_key": "pilot:review:2"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "assignment_started", "task_id": "review", "payload": {"assignment_generation": 2, "assignment_id": "review-2", "idempotency_key": "pilot:review:2", "task_handle": {"thread_id": "desktop-review-2", "state": "active"}, "model_policy_revision": 1, "model_route": escalated}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "lease_acquired", "task_id": "research", "payload": {"lease_id": "writer-1", "mode": "write", "scope": "pilot-output", "owner": "research", "assignment_generation": 1, "heartbeat_at": "2026-01-01T00:00:00Z", "expires_at": "2099-01-01T00:00:00Z"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "verification_recorded", "task_id": "research", "payload": {"id": "V1", "command": "offline-smoke", "result": "passed", "tip": "final", "assignment_generation": 1, "environment_attestation_id": "environment-repair", "topology_revision": 1}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "lease_released", "task_id": "research", "payload": {"lease_id": "writer-1"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "review_recorded", "task_id": "research", "payload": {"review_id": "R2", "review_unit": "integrated_candidate", "review_role": "inner", "reviewer_task_id": "desktop-review-2", "reviewer_assignment_task_id": "review", "assignment_generation": 2, "verdict": "APPROVED", "tip": "final"}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "candidate_recorded", "payload": {"id": "C1", "tip": "final", "inner_review_id": "R2", "state": "awaiting_outer", "verification_ids": ["V1"]}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "approval_requested", "payload": {"approval_id": "outer-gate", "action": "activate", "effect": "promote draft", "exact_target": "orchestrator-v0", "expires_at": "2099-01-01T00:00:00Z"}})
    for task, start in (("research", "running"), ("review", "inner_review")):
        sequence = [("running", "verifying"), ("verifying", "inner_review"), ("inner_review", "frozen"), ("frozen", "integrated"), ("integrated", "complete")] if start == "running" else [("inner_review", "frozen"), ("frozen", "integrated"), ("integrated", "complete")]
        for prior, nxt in sequence:
            append(args.output, {"program_id": scenario["scenario_id"], "event_type": "task_transition", "task_id": task, "prior_state": prior, "next_state": nxt, "payload": {}})
    append(args.output, {"program_id": scenario["scenario_id"], "event_type": "program_transition", "prior_state": "active", "next_state": "awaiting_operator_gate", "payload": {"next_action": "outer gate"}})
    state = replay(load_events(args.output))
    trace = [{"event_id": e["event_id"], "event": e["event_type"], "payload": e["payload"]} for e in load_events(args.output)]
    continued = state["tasks"]["review"]["state"] == "complete"
    repaired = state["tasks"]["research"]["state"] == "complete" and state["environment_attestations"].get("environment-repair", {}).get("freshness") == "fresh"
    stale = state["review_records"].get("R1", {}).get("freshness") == "stale"
    expected_gates = len(scenario["expected_operator_gates"])
    metrics = {
        "scenario_sha256": hashlib.sha256(raw).hexdigest(),
        "avoidable_pause": 0 if continued else 1,
        "operator_repair": 0 if repaired else 1,
        "operator_request_expected": expected_gates,
        "operator_request_avoidable": 0 if state["next_action"] == "outer gate" else 1,
        "false_green": 0 if stale else 1,
        "authority_violations": 0 if state["state"] == "awaiting_operator_gate" and state["next_action"] == "outer gate" and state["tasks"]["review"].get("fenced_generation") == 1 else 1,
    }
    args.output.joinpath("trace.jsonl").write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in trace))
    args.output.joinpath("metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    args.output.joinpath("final-status.md").write_text(render_status(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
