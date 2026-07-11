#!/usr/bin/env python3
"""Deterministic event-ledger core for the noncanonical Orchestrator V0 pilot."""

from __future__ import annotations

import copy
import fcntl
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA_VERSION = 0
EXIT_INVALID_LOG = 4
EXIT_CAS_CONFLICT = 5
EXIT_LOCK_BUSY = 6
EXIT_STALE_COORDINATOR = 7


class LedgerError(Exception):
    exit_code = EXIT_INVALID_LOG
    marker = "INVALID_LOG"


class CasConflict(LedgerError):
    exit_code = EXIT_CAS_CONFLICT
    marker = "CAS_CONFLICT"


class LockBusy(LedgerError):
    exit_code = EXIT_LOCK_BUSY
    marker = "LOCK_BUSY"


class StaleCoordinator(LedgerError):
    exit_code = EXIT_STALE_COORDINATOR
    marker = "STALE_COORDINATOR"


PROGRAM_TRANSITIONS = {
    "draft": {"authority_locked", "paused", "blocked", "cancelled"},
    "authority_locked": {"draft", "graph_ready", "paused", "blocked", "cancelled"},
    "graph_ready": {"authority_locked", "active", "paused", "blocked", "cancelled"},
    "active": {"integrating", "awaiting_operator_gate", "done", "paused", "blocked", "cancelled"},
    "integrating": {"active", "awaiting_operator_gate", "done", "paused", "blocked", "cancelled"},
    "awaiting_operator_gate": {"active", "integrating", "done", "paused", "blocked", "cancelled"},
    "paused": {"draft", "authority_locked", "graph_ready", "active", "integrating", "awaiting_operator_gate", "blocked", "cancelled"},
    "blocked": {"draft", "authority_locked", "graph_ready", "active", "integrating", "awaiting_operator_gate", "paused", "cancelled"},
    "done": set(),
    "cancelled": set(),
}

TASK_TRANSITIONS = {
    "proposed": {"planning", "cancelled", "superseded"},
    "planning": {"review_ready", "waiting_dependency", "awaiting_approval", "paused", "failed", "cancelled", "superseded"},
    "review_ready": {"spec_review", "waiting_dependency", "awaiting_approval", "paused", "failed", "cancelled", "superseded"},
    "spec_review": {"planning", "ready", "awaiting_approval", "paused", "failed", "cancelled", "superseded"},
    "ready": {"assigned", "waiting_dependency", "awaiting_approval", "environment_blocked", "paused", "failed", "cancelled", "superseded"},
    "assigned": {"running", "awaiting_approval", "environment_blocked", "recovery", "paused", "failed", "cancelled", "superseded"},
    "running": {"verifying", "awaiting_approval", "environment_blocked", "recovery", "paused", "failed", "cancelled", "superseded"},
    "verifying": {"running", "inner_review", "awaiting_approval", "environment_blocked", "recovery", "paused", "failed", "cancelled", "superseded"},
    "inner_review": {"patching", "frozen", "awaiting_approval", "environment_blocked", "recovery", "paused", "failed", "cancelled", "superseded"},
    "patching": {"verifying", "awaiting_approval", "environment_blocked", "recovery", "paused", "failed", "cancelled", "superseded"},
    "frozen": {"verifying", "integrated", "paused", "failed", "cancelled", "superseded"},
    "integrated": {"verifying", "complete", "paused", "failed", "cancelled", "superseded"},
    "waiting_dependency": set(),
    "awaiting_approval": set(),
    "environment_blocked": set(),
    "paused": set(),
    "recovery": set(),
    "failed": {"recovery", "cancelled", "superseded"},
    "complete": set(),
    "cancelled": set(),
    "superseded": set(),
}

EXCEPTIONAL = {"waiting_dependency", "awaiting_approval", "environment_blocked", "paused", "recovery"}
TERMINAL_TASKS = {"complete", "cancelled", "superseded"}
EVENT_FIELDS = {"schema_version", "event_id", "event_type", "program_id", "coordinator_generation", "task_id", "assignment_generation", "actor", "actor_ref", "occurred_at", "prior_state", "next_state", "topology_revision", "payload", "invalidates", "prev_event_hash", "event_hash"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def event_hash(event: dict[str, Any]) -> str:
    body = {k: v for k, v in event.items() if k != "event_hash"}
    return hashlib.sha256(canonical_json(body)).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        dir_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


@contextmanager
def ledger_lock(program_dir: Path, nonblocking: bool = True) -> Iterator[None]:
    lock_path = program_dir / ".events.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        flags = fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0)
        try:
            fcntl.flock(handle.fileno(), flags)
        except BlockingIOError as exc:
            raise LockBusy("ledger writer is active") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_events(program_dir: Path) -> list[dict[str, Any]]:
    path = program_dir / "events.jsonl"
    if not path.exists():
        return []
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise LedgerError("events.jsonl has a truncated final line")
    events: list[dict[str, Any]] = []
    previous_hash: str | None = None
    for index, line in enumerate(raw.splitlines(), start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"invalid event JSON at line {index}: {exc}") from exc
        if event.get("schema_version") != SCHEMA_VERSION:
            raise LedgerError(f"unsupported schema at event {index}")
        if event.get("event_id") != index:
            raise LedgerError(f"event ID gap/duplicate at line {index}")
        if event.get("prev_event_hash") != previous_hash:
            raise LedgerError(f"hash predecessor mismatch at event {index}")
        calculated = event_hash(event)
        if event.get("event_hash") != calculated:
            raise LedgerError(f"event hash mismatch at event {index}")
        previous_hash = calculated
        events.append(event)
    return events


def initial_state(program_id: str = "") -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "program_id": program_id,
        "title": "",
        "state": None,
        "resume_state": None,
        "topology_revision": 1,
        "coordinator_generation": 1,
        "last_event_id": 0,
        "last_event_hash": None,
        "goal": "",
        "done_definition": [],
        "authority": {},
        "model_routing": {"policy_revision": 0},
        "repo": {},
        "tasks": {},
        "leases": {},
        "environment_attestations": {},
        "verification_records": {},
        "review_records": {},
        "integration_candidates": {},
        "decisions": {},
        "recoveries": {},
        "host_operations": {},
        "approvals": {},
        "next_action": "",
        "updated_at": None,
    }


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise LedgerError(message)


def _fields(payload: dict[str, Any], required: set[str], allowed: set[str]) -> None:
    _require(not (required - payload.keys()), f"missing fields: {sorted(required - payload.keys())}")
    _require(not (payload.keys() - allowed), f"unknown fields: {sorted(payload.keys() - allowed)}")


def _path_overlap(left: str, right: str) -> bool:
    a, b = Path(left), Path(right)
    return a == b or a in b.parents or b in a.parents


def select_route(policy: dict[str, Any], complexity: str, risk_class: str = "routine") -> dict[str, str]:
    """Choose the lowest adequate allowed route from operator-confirmed policy."""
    table = {"low": ("fast", "medium"), "mechanical_multistep": ("fast", "high"), "routine": ("balanced", "high"), "moderate": ("balanced", "high"), "high": ("deep", "high")}
    route_class, effort = table.get(complexity, table["high"])
    if risk_class in {"security", "auth", "data_loss", "migration", "provider", "certifying_review"} and route_class == "fast":
        route_class, effort = "balanced", "high"
    route = policy.get("route_classes", {}).get(route_class)
    _require(route is not None, "selected route unavailable")
    return {"route_class": route_class, "model_id": route["model"], "reasoning_effort": effort}


def _transition(container: dict[str, Any], prior: str, nxt: str, table: dict[str, set[str]], label: str) -> None:
    _require(container.get("state") == prior, f"{label} prior state mismatch")
    _require(nxt in table.get(prior, set()), f"illegal {label} transition {prior}->{nxt}")
    container["state"] = nxt


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> None:
    _require(not (event.keys() - EVENT_FIELDS), f"unknown event fields: {sorted(event.keys() - EVENT_FIELDS)}")
    etype = event["event_type"]
    payload = event.get("payload", {})
    task_id = event.get("task_id")

    if etype == "program_initialized":
        _fields(payload, {"title", "goal"}, {"title", "goal", "done_definition", "authority", "repo", "next_action"})
        _require(event["actor"] in {"coordinator", "operator"}, "invalid program initializer")
        _require(state["state"] is None, "program already initialized")
        state.update({
            "program_id": event["program_id"],
            "title": payload["title"],
            "state": "draft",
            "goal": payload["goal"],
            "done_definition": payload.get("done_definition", []),
            "authority": payload.get("authority", {}),
            "repo": payload.get("repo", {}),
            "next_action": payload.get("next_action", "lock authority"),
        })
    elif etype == "program_transition":
        _fields(payload, set(), {"resume_state", "next_action", "authority_envelope", "reason"})
        _require(event["actor"] == "coordinator", "program transition requires coordinator")
        if event["next_state"] == "authority_locked":
            _require(bool(payload.get("authority_envelope")), "authority lock requires confirmed operator envelope")
        prior, nxt = event["prior_state"], event["next_state"]
        _transition(state, prior, nxt, PROGRAM_TRANSITIONS, "program")
        if nxt in {"paused", "blocked"}:
            state["resume_state"] = payload.get("resume_state", prior)
        elif prior in {"paused", "blocked"}:
            _require(nxt == state.get("resume_state"), "program resume target mismatch")
            state["resume_state"] = None
        state["next_action"] = payload.get("next_action", state.get("next_action", ""))
    elif etype == "task_added":
        _fields(payload, {"title"}, {"title", "deliverable", "next_action", "failure", "dependencies", "risk_class"})
        _require(task_id and task_id not in state["tasks"], "duplicate/missing task")
        task = copy.deepcopy(payload)
        task.update({"task_id": task_id, "state": "proposed", "assignment_generation": 0, "model_policy_revision": 0})
        state["tasks"][task_id] = task
    elif etype == "task_transition":
        _fields(payload, set(), {"resume_state", "next_action", "reason"})
        _require(event["actor"] == "coordinator", "task transition requires coordinator")
        _require(task_id in state["tasks"], "unknown task")
        task = state["tasks"][task_id]
        prior, nxt = event["prior_state"], event["next_state"]
        if prior in EXCEPTIONAL:
            _require(nxt == task.get("resume_state"), "exceptional task resume target mismatch")
        else:
            _require(nxt in TASK_TRANSITIONS.get(prior, set()), f"illegal task transition {prior}->{nxt}")
        _require(task.get("state") == prior, "task prior state mismatch")
        task["state"] = nxt
        if nxt in EXCEPTIONAL:
            resume = payload.get("resume_state", prior)
            _require(resume not in EXCEPTIONAL and resume != "failed", "invalid exceptional resume state")
            task["resume_state"] = resume
        elif prior in EXCEPTIONAL:
            task["resume_state"] = None
        task["next_action"] = payload.get("next_action", task.get("next_action", ""))
    elif etype == "assignment_started":
        _fields(payload, {"assignment_generation", "assignment_id", "idempotency_key", "task_handle", "model_policy_revision", "model_route"}, {"assignment_generation", "assignment_id", "idempotency_key", "task_handle", "model_policy_revision", "model_route"})
        _require(task_id in state["tasks"], "unknown task")
        task = state["tasks"][task_id]
        generation = int(payload["assignment_generation"])
        _require(generation == int(task.get("assignment_generation", 0)) + 1, "assignment generation must increment")
        intent = task.get("dispatch_intent")
        _require(intent is not None, "assignment requires a durable dispatch intent")
        _require(intent["assignment_generation"] == generation, "dispatch intent generation mismatch")
        _require(intent["idempotency_key"] == payload.get("idempotency_key"), "dispatch idempotency key mismatch")
        _require(intent.get("state") == "pending", "dispatch intent is not pending")
        _require(state["model_routing"].get("policy_revision", 0) > 0, "assignment requires confirmed model policy")
        expected_route = task.get("pending_model_route") or task.get("model_route")
        _require(expected_route is not None, "assignment requires selected model route")
        _require(payload.get("model_policy_revision") == state["model_routing"]["policy_revision"], "assignment model policy is stale")
        _require(payload.get("model_route") == {k: expected_route[k] for k in ("route_class", "model_id", "reasoning_effort")}, "assignment route mismatch")
        task["assignment_generation"] = generation
        task["assignment_id"] = payload["assignment_id"]
        task["task_handle"] = copy.deepcopy(payload.get("task_handle"))
        task["model_policy_revision"] = payload.get("model_policy_revision", state["model_routing"].get("policy_revision", 0))
        task["model_route"] = copy.deepcopy(payload.get("model_route"))
        task.pop("pending_model_route", None)
        intent["state"] = "reconciled"
        intent["task_handle"] = copy.deepcopy(payload.get("task_handle"))
        for review in state["review_records"].values():
            if review.get("task_id") == task_id and review.get("freshness") == "fresh":
                review["freshness"] = "stale"
                review["invalidation_reason"] = "assignment generation advanced"
    elif etype == "dispatch_intent_recorded":
        _fields(payload, {"assignment_generation", "idempotency_key"}, {"assignment_generation", "idempotency_key", "kickoff_hash"})
        _require(task_id in state["tasks"], "unknown task")
        task = state["tasks"][task_id]
        generation = int(payload["assignment_generation"])
        _require(generation == int(task.get("assignment_generation", 0)) + 1, "dispatch intent generation must be next")
        prior = task.get("dispatch_intent")
        _require(prior is None or prior.get("state") == "reconciled", "unreconciled dispatch intent already exists")
        key = payload.get("idempotency_key")
        _require(bool(key), "dispatch intent requires idempotency key")
        for existing in state["tasks"].values():
            existing_intent = existing.get("dispatch_intent")
            _require(not existing_intent or existing_intent.get("idempotency_key") != key, "duplicate dispatch idempotency key")
        task["dispatch_intent"] = copy.deepcopy(payload)
        task["dispatch_intent"]["state"] = "pending"
    elif etype == "assignment_fenced":
        _fields(payload, {"assignment_generation", "reason"}, {"assignment_generation", "reason"})
        _require(task_id in state["tasks"], "unknown task")
        task = state["tasks"][task_id]
        _require(payload["assignment_generation"] == task.get("assignment_generation"), "fenced assignment is not current")
        task["fenced_generation"] = payload["assignment_generation"]
    elif etype == "assignment_continued":
        _fields(payload, {"assignment_generation", "assignment_id", "task_handle"}, {"assignment_generation", "assignment_id", "task_handle", "model_policy_revision", "model_route"})
        _require(task_id in state["tasks"], "unknown task")
        task = state["tasks"][task_id]
        generation = int(payload["assignment_generation"])
        _require(generation == int(task.get("assignment_generation", 0)) + 1, "assignment generation must increment")
        _require(payload.get("task_handle") == task.get("task_handle"), "continued assignment must reuse task handle")
        _require(payload.get("model_policy_revision") == state["model_routing"].get("policy_revision"), "continued assignment model policy is stale")
        proposed_route = payload.get("model_route")
        _require(proposed_route is not None, "continued assignment requires explicit route")
        pending = task.get("pending_model_route")
        if pending is not None:
            _require(task.get("fenced_generation") == task.get("assignment_generation"), "continued route override requires fenced assignment")
            _require(proposed_route == {k: pending[k] for k in ("route_class", "model_id", "reasoning_effort")}, "continued route does not match pending route")
        else:
            _require(proposed_route == task.get("model_route"), "continued route requires validated pending override")
        task["assignment_generation"] = generation
        task["assignment_id"] = payload["assignment_id"]
        task["model_policy_revision"] = payload.get("model_policy_revision", state["model_routing"].get("policy_revision", 0))
        task["model_route"] = copy.deepcopy(proposed_route)
        task.pop("pending_model_route", None)
        for review in state["review_records"].values():
            if review.get("task_id") == task_id and review.get("freshness") == "fresh":
                review["freshness"] = "stale"
                review["invalidation_reason"] = "assignment generation advanced"
    elif etype == "model_policy_confirmed":
        _fields(payload, {"policy_revision", "mode", "route_classes"}, {"policy_revision", "mode", "route_classes", "quality_bias", "pins", "capabilities", "fallback"})
        revision = int(payload["policy_revision"])
        _require(revision == int(state["model_routing"].get("policy_revision", 0)) + 1, "model policy revision must increment")
        state["model_routing"] = copy.deepcopy(payload)
    elif etype in {"model_route_selected", "model_route_changed", "model_route_unavailable"}:
        _require(task_id in state["tasks"], "unknown task")
        if etype == "model_route_unavailable":
            _fields(payload, {"model_policy_revision", "reason"}, {"model_policy_revision", "reason", "attempted_route"})
        else:
            _fields(payload, {"model_policy_revision", "route_class", "model_id", "reasoning_effort"}, {"model_policy_revision", "route_class", "model_id", "reasoning_effort", "risk_class", "routing_rationale", "exceptional_trigger"})
            task = state["tasks"][task_id]
            _require(payload["model_policy_revision"] == state["model_routing"]["policy_revision"], "stale model policy")
            route_class = payload["route_class"]
            route = state["model_routing"].get("route_classes", {}).get(route_class)
            _require(route is not None, "route class is not allowed")
            _require(payload["model_id"] == route["model"], "model does not match route class")
            efforts = ["low", "medium", "high", "xhigh"]
            _require(payload["reasoning_effort"] in efforts, "unsupported reasoning effort")
            _require(efforts.index(payload["reasoning_effort"]) <= efforts.index(route["max_reasoning"]), "reasoning exceeds route ceiling")
            prohibited_fast = payload.get("risk_class") in {"security", "auth", "data_loss", "migration", "provider", "certifying_review"}
            _require(not (route_class == "fast" and prohibited_fast), "fast route prohibited for risk/review surface")
            if payload["reasoning_effort"] == "xhigh":
                _require(bool(payload.get("exceptional_trigger")), "xhigh requires exceptional trigger")
            if etype == "model_route_changed" and task.get("assignment_generation", 0) > 0:
                _require(task.get("fenced_generation") == task["assignment_generation"], "active route change requires fenced assignment")
                task["pending_model_route"] = copy.deepcopy(payload)
            else:
                task["model_route"] = copy.deepcopy(payload)
            task["model_policy_revision"] = payload["model_policy_revision"]
    elif etype == "approval_requested":
        _fields(payload, {"approval_id", "action", "effect", "exact_target", "expires_at"}, {"approval_id", "action", "effect", "exact_target", "expires_at", "cap", "amount", "reason"})
        aid = payload["approval_id"]
        _require(aid not in state["approvals"], "duplicate approval")
        state["approvals"][aid] = {**copy.deepcopy(payload), "state": "requested", "consumed_amount": 0}
    elif etype == "approval_granted":
        _fields(payload, {"approval_id", "granting_message_pointer"}, {"approval_id", "granting_message_pointer"})
        approval = state["approvals"].get(payload["approval_id"])
        _require(approval and approval["state"] == "requested", "approval not requestable")
        approval.update({"state": "granted", "granted_at": event["occurred_at"], "granting_message_pointer": payload["granting_message_pointer"]})
    elif etype == "approval_consumed":
        _fields(payload, {"approval_id", "action", "effect", "exact_target"}, {"approval_id", "action", "effect", "exact_target", "amount"})
        approval = state["approvals"].get(payload["approval_id"])
        _require(approval and approval["state"] == "granted", "approval is not consumable")
        _require(payload.get("exact_target") == approval.get("exact_target"), "approval target drift")
        _require(payload.get("action") == approval.get("action"), "approval action drift")
        _require(payload.get("effect") == approval.get("effect"), "approval effect drift")
        _require(datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00")) <= datetime.fromisoformat(approval["expires_at"].replace("Z", "+00:00")), "approval expired")
        amount = payload.get("amount", 1)
        cap = approval.get("cap", 1)
        _require(approval["consumed_amount"] + amount <= cap, "approval cap exceeded")
        approval["consumed_amount"] += amount
        if approval["consumed_amount"] == cap:
            approval["state"] = "consumed"
    elif etype == "lease_acquired":
        _fields(payload, {"lease_id", "mode", "scope", "owner", "assignment_generation"}, {"lease_id", "mode", "scope", "owner", "assignment_generation", "expires_at"})
        lid = payload["lease_id"]
        _require(lid not in state["leases"], "duplicate lease")
        if payload.get("mode") == "write":
            for lease in state["leases"].values():
                _require(not (lease.get("state") == "active" and lease.get("mode") == "write" and _path_overlap(lease.get("scope"), payload.get("scope"))), "overlapping writer lease")
        state["leases"][lid] = {**copy.deepcopy(payload), "state": "active"}
    elif etype in {"lease_released", "lease_revoked", "lease_expired"}:
        _fields(payload, {"lease_id"}, {"lease_id", "reason"})
        lease = state["leases"].get(payload["lease_id"])
        _require(lease and lease["state"] == "active", "lease is not active")
        lease["state"] = etype.split("_")[1]
    elif etype == "review_recorded":
        _fields(payload, {"review_id", "review_unit", "reviewer_task_id", "assignment_generation", "verdict", "tip"}, {"review_id", "review_unit", "reviewer_task_id", "assignment_generation", "verdict", "tip", "base", "resolves", "finding"})
        _require(payload["assignment_generation"] > 0, "review requires active assignment generation")
        _require(task_id in state["tasks"], "review requires scoped task")
        _require(payload["assignment_generation"] == state["tasks"][task_id]["assignment_generation"], "review assignment generation is stale")
        _require(payload["verdict"] in {"APPROVED", "ACTIONABLE"}, "invalid review verdict")
        rid = payload["review_id"]
        _require(rid not in state["review_records"], "duplicate review")
        state["review_records"][rid] = {**copy.deepcopy(payload), "task_id": task_id, "freshness": "fresh"}
    elif etype == "review_invalidated":
        _fields(payload, {"review_id", "reason"}, {"review_id", "reason"})
        review = state["review_records"].get(payload["review_id"])
        _require(review is not None, "unknown review")
        review["freshness"] = "stale"
        review["invalidation_reason"] = payload["reason"]
    elif etype == "coordinator_replaced":
        _fields(payload, {"coordinator_generation", "reason"}, {"coordinator_generation", "reason", "prior_coordinator"})
        _require(event["actor"] == "operator", "coordinator replacement requires operator")
        generation = int(payload["coordinator_generation"])
        _require(generation == int(state["coordinator_generation"]) + 1, "coordinator generation must increment")
        state["coordinator_generation"] = generation
    elif etype == "status_reported":
        _require(event["actor"] in {"coordinator", "operator"}, "invalid status actor")
        _fields(payload, set(), {"message_kind", "operator_message", "continued", "next_action", "outcome", "completed", "blocked_decision", "safety_spend"})
        _require(payload.get("message_kind") or payload.get("outcome"), "status requires message kind or outcome")
        state["last_status"] = copy.deepcopy(payload)
    elif etype == "host_operation_recorded":
        if "arguments" in payload:
            _fields(payload, {"operation_id", "operation", "task_id", "thread_id", "arguments", "result", "linked_event_id"}, {"operation_id", "operation", "task_id", "thread_id", "arguments", "result", "linked_event_id", "assignment_generation"})
        else:
            _fields(payload, {"operation_id", "operation", "task_id", "thread_id", "result"}, {"operation_id", "operation", "task_id", "thread_id", "result", "assignment_generation"})
        _require(payload["operation_id"] not in state["host_operations"], "duplicate host operation")
        _require(payload["task_id"] in state["tasks"], "host operation task is unknown")
        state["host_operations"][payload["operation_id"]] = copy.deepcopy(payload)
        archived_result = payload["result"] == "archived" or (isinstance(payload["result"], dict) and payload["result"].get("archived") is True)
        if payload["operation"] == "set_thread_archived" and archived_result:
            task = state["tasks"][payload["task_id"]]
            _require(task.get("task_handle", {}).get("thread_id") == payload["thread_id"], "archived handle is not current")
            task["task_handle"]["state"] = "archived"
    elif etype == "environment_attested":
        _fields(payload, {"id", "task_id", "checkout", "base", "commands", "ready"}, {"id", "task_id", "checkout", "base", "commands", "ready", "evidence", "dirty_state"})
        _require(payload["task_id"] in state["tasks"], "environment attestation task is unknown")
        _require(payload["ready"] is True and bool(payload["commands"]), "environment attestation is not ready")
        _require(all(isinstance(item, dict) and item.get("command") and item.get("result") == "passed" and item.get("exit_code") == 0 and item.get("output_sha256") for item in payload["commands"]), "environment commands lack passed result evidence")
        _require(Path(payload["checkout"]).is_absolute() and Path(payload["checkout"]).is_dir() and bool(payload["base"]), "environment checkout/base evidence is invalid")
        _require(payload.get("dirty_state") in {"clean", "known"} and bool(payload.get("evidence")), "environment clean-state evidence is missing")
        state["environment_attestations"][payload["id"]] = copy.deepcopy(payload)
    elif etype == "candidate_recorded":
        _fields(payload, {"id", "tip", "inner_review_id", "state"}, {"id", "tip", "inner_review_id", "outer_review_id", "state", "child_tips", "merge_order", "verification_ids"})
        review_keys = ("inner_review_id",) if payload["state"] == "awaiting_outer" else ("inner_review_id", "outer_review_id")
        _require(payload["state"] in {"awaiting_outer", "outer_approved"}, "invalid candidate state")
        if payload["state"] == "awaiting_outer":
            _require(not payload.get("outer_review_id"), "awaiting_outer candidate cannot claim outer review")
        for key in review_keys:
            review = state["review_records"].get(payload[key])
            _require(review and review["verdict"] == "APPROVED" and review["freshness"] == "fresh" and review["tip"] == payload["tip"], f"candidate {key} is not fresh approved exact-tip evidence")
        state["integration_candidates"][payload["id"]] = copy.deepcopy(payload)
    elif etype in {"verification_recorded", "decision_recorded", "recovery_recorded"}:
        required = {"verification_recorded": {"id", "command", "result", "tip"}, "decision_recorded": {"id", "decision"}, "recovery_recorded": {"id", "kind"}}[etype]
        _require(not (required - payload.keys()), f"missing fields: {sorted(required - payload.keys())}")
        collection = {
            "environment_attested": "environment_attestations",
            "verification_recorded": "verification_records",
            "decision_recorded": "decisions",
            "recovery_recorded": "recoveries",
        }[etype]
        key = payload.get("id") or payload.get(f"{collection[:-1]}_id") or str(event["event_id"])
        state[collection][key] = copy.deepcopy(payload)
    else:
        raise LedgerError(f"unknown event type: {etype}")

    state["last_event_id"] = event["event_id"]
    state["last_event_hash"] = event["event_hash"]
    state["updated_at"] = event["occurred_at"]


def replay(events: list[dict[str, Any]]) -> dict[str, Any]:
    program_id = events[0]["program_id"] if events else ""
    state = initial_state(program_id)
    for event in events:
        if event.get("coordinator_generation") != state["coordinator_generation"]:
            if event["event_type"] != "coordinator_replaced":
                raise LedgerError(f"stale coordinator generation at event {event['event_id']}")
        apply_event(state, event)
    return state


def handle_operator_message(program_dir: Path, message_kind: str, text: str, continue_event: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Record a message and, when informational, execute the supplied safe next operation."""
    events = load_events(program_dir)
    state = replay(events)
    first = append_event(program_dir, {"program_id": state["program_id"], "event_type": "status_reported", "payload": {"message_kind": message_kind, "operator_message": text, "continued": message_kind == "informational", "next_action": state["next_action"]}}, events[-1]["event_hash"], state["coordinator_generation"])
    if message_kind != "informational" or continue_event is None:
        return [first]
    events = load_events(program_dir)
    second = append_event(program_dir, continue_event, events[-1]["event_hash"], state["coordinator_generation"])
    return [first, second]


def render_status(state: dict[str, Any]) -> str:
    tasks = list(state["tasks"].values())
    completed = [t["task_id"] for t in tasks if t["state"] in TERMINAL_TASKS]
    active = [f"{t['task_id']}:{t['state']}" for t in tasks if t["state"] not in TERMINAL_TASKS]
    blocked = [f"{t['task_id']}:{t['state']}" for t in tasks if t["state"] in {"awaiting_approval", "environment_blocked", "failed"}]
    return (
        f"Outcome/phase: {state.get('state') or 'uninitialized'}\n"
        f"Completed: {', '.join(completed) or 'none'}\n"
        f"In flight: {', '.join(active) or 'none'}\n"
        f"Blocked/decision: {', '.join(blocked) or 'none'}\n"
        "Safety/spend: see approvals and authority ledger\n"
        f"Next: {state.get('next_action') or 'none'}\n"
        "Estimate: unknown unless recorded by coordinator\n"
    )


def write_views(program_dir: Path, state: dict[str, Any], crash_point: str | None = None) -> None:
    program_view = {k: v for k, v in state.items() if k != "approvals"}
    atomic_write(program_dir / "program.json", json.dumps(program_view, indent=2, sort_keys=True).encode() + b"\n")
    if crash_point == "after_program_view":
        raise RuntimeError("injected crash after_program_view")
    approvals_view = {
        "schema_version": SCHEMA_VERSION,
        "last_event_id": state["last_event_id"],
        "last_event_hash": state["last_event_hash"],
        "approvals": state["approvals"],
    }
    atomic_write(program_dir / "approvals.json", json.dumps(approvals_view, indent=2, sort_keys=True).encode() + b"\n")
    if crash_point == "after_approvals_view":
        raise RuntimeError("injected crash after_approvals_view")
    atomic_write(program_dir / "status.md", render_status(state).encode())


def append_event(
    program_dir: Path,
    event: dict[str, Any],
    expected_prev_hash: str | None,
    coordinator_generation: int,
    nonblocking: bool = True,
) -> dict[str, Any]:
    with ledger_lock(program_dir, nonblocking=nonblocking):
        events = load_events(program_dir)
        state = replay(events)
        current_hash = events[-1]["event_hash"] if events else None
        if current_hash != expected_prev_hash:
            raise CasConflict(f"expected {expected_prev_hash}, found {current_hash}")
        if coordinator_generation != state["coordinator_generation"]:
            raise StaleCoordinator(f"expected generation {state['coordinator_generation']}")
        new_event = copy.deepcopy(event)
        new_event.update({
            "schema_version": SCHEMA_VERSION,
            "event_id": len(events) + 1,
            "prev_event_hash": current_hash,
            "coordinator_generation": coordinator_generation,
            "occurred_at": new_event.get("occurred_at") or utc_now(),
            "topology_revision": new_event.get("topology_revision", state.get("topology_revision", 1)),
            "invalidates": new_event.get("invalidates", []),
            "assignment_generation": new_event.get("assignment_generation"),
            "task_id": new_event.get("task_id"),
            "prior_state": new_event.get("prior_state"),
            "next_state": new_event.get("next_state"),
            "actor": new_event.get("actor", "coordinator"),
            "actor_ref": new_event.get("actor_ref", "coordinator"),
            "payload": new_event.get("payload", {}),
        })
        new_event["event_hash"] = event_hash(new_event)
        candidate_events = events + [new_event]
        candidate_state = replay(candidate_events)
        crash_point = os.environ.get("ORCH_CRASH_POINT")
        if crash_point == "before_log_replace":
            raise RuntimeError("injected crash before_log_replace")
        log_bytes = b"".join(canonical_json(item) + b"\n" for item in candidate_events)
        atomic_write(program_dir / "events.jsonl", log_bytes)
        if crash_point == "after_log_replace":
            raise RuntimeError("injected crash after_log_replace")
        write_views(program_dir, candidate_state, crash_point)
        return new_event


def view_status(program_dir: Path) -> str:
    events = load_events(program_dir)
    state = replay(events)
    expected = (state["last_event_id"], state["last_event_hash"])
    for name in ("program.json", "approvals.json"):
        path = program_dir / name
        if not path.exists():
            return "STALE_VIEW"
        try:
            view = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return "STALE_VIEW"
        if (view.get("last_event_id"), view.get("last_event_hash")) != expected:
            return "STALE_VIEW"
    if not (program_dir / "status.md").exists():
        return "STALE_VIEW"
    return "CURRENT"


def rebuild_views(program_dir: Path) -> str:
    events = load_events(program_dir)
    state = replay(events)
    status = view_status(program_dir)
    if status == "CURRENT":
        return "CURRENT"
    write_views(program_dir, state)
    return "REBUILT"
