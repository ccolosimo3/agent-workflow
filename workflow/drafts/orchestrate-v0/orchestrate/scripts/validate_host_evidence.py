#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_core import load_events, replay


REQUIRED = {"operation", "arguments", "result", "timestamp", "ledger_event_id"}
ALLOWED = REQUIRED | {"task_id", "route_attestation"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--program", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()
    event_list = load_events(args.program)
    events = {event["event_id"]: event for event in event_list}
    seen: set[int] = set()
    seen_operations: set[tuple[str, str]] = set()
    counts: dict[str, int] = {}
    for number, line in enumerate(args.evidence.read_text().splitlines(), start=1):
        item = json.loads(line)
        missing = REQUIRED - set(item)
        if missing:
            raise SystemExit(f"line {number}: missing {sorted(missing)}")
        if set(item) - ALLOWED:
            raise SystemExit(f"line {number}: unknown fields {sorted(set(item) - ALLOWED)}")
        event_id = int(item["ledger_event_id"])
        if event_id not in events:
            raise SystemExit(f"line {number}: unknown ledger event {event_id}")
        event = events[event_id]
        if event["event_type"] != "host_operation_recorded":
            raise SystemExit(f"line {number}: evidence must link host_operation_recorded")
        recorded = event["payload"]
        if recorded.get("operation") != item["operation"] or recorded.get("arguments") != item["arguments"] or recorded.get("result") != item["result"]:
            raise SystemExit(f"line {number}: exact host operation mismatch")
        linked = events.get(recorded.get("linked_event_id"))
        if linked is None:
            raise SystemExit(f"line {number}: missing linked lifecycle event")
        counts[item["operation"]] = counts.get(item["operation"], 0) + 1
        thread_key = item.get("arguments", {}).get("thread_id") or item.get("result", {}).get("thread_id", "")
        operation_key = (item["operation"], str(thread_key), str(item.get("arguments", {}).get("assignment_generation", "")))
        if operation_key in seen_operations and item["operation"] != "read_thread":
            raise SystemExit(f"line {number}: duplicate host operation {operation_key}")
        seen_operations.add(operation_key)
        if event_id in seen:
            raise SystemExit(f"line {number}: ledger event {event_id} reused")
        seen.add(event_id)
        if item["operation"] == "create_thread":
            if not item.get("task_id") or item.get("route_attestation") not in {"dispatch_accepted", "runtime_reported"}:
                raise SystemExit(f"line {number}: incomplete task creation evidence")
            if linked["event_type"] != "assignment_started" or linked.get("task_id") != item["task_id"]:
                raise SystemExit(f"line {number}: create is not linked to assignment_started")
            handle = linked["payload"].get("task_handle", {})
            if handle.get("thread_id") != item["result"].get("thread_id"):
                raise SystemExit(f"line {number}: create thread mismatch")
            expected = linked["payload"].get("model_route", {})
            if item["arguments"].get("model") != expected.get("model_id") or item["arguments"].get("thinking") != expected.get("reasoning_effort"):
                raise SystemExit(f"line {number}: create route mismatch")
        elif item["operation"] == "send_message_to_thread":
            if linked["event_type"] != "assignment_continued" or linked["payload"].get("task_handle", {}).get("thread_id") != item["arguments"].get("thread_id"):
                raise SystemExit(f"line {number}: continuation mismatch")
            route = linked["payload"].get("model_route", {})
            if item["arguments"].get("model") != route.get("model_id") or item["arguments"].get("thinking") != route.get("reasoning_effort") or item["arguments"].get("assignment_generation") != linked["payload"].get("assignment_generation") or item["result"] != {"accepted": True, "same_thread": True}:
                raise SystemExit(f"line {number}: continuation arguments/result mismatch")
        elif item["operation"] == "read_thread":
            thread_id = item["arguments"].get("thread_id")
            matches = False
            if linked["event_type"] == "assignment_started":
                matches = linked["payload"].get("task_handle", {}).get("thread_id") == thread_id
            elif linked["event_type"] == "review_recorded":
                matches = linked["payload"].get("reviewer_task_id") == thread_id and item["result"].get("verdict") == linked["payload"].get("verdict")
            elif linked["event_type"] == "host_operation_recorded":
                matches = linked["payload"].get("operation") == "read_thread" and linked["payload"].get("thread_id") == thread_id
            if not matches or item["result"].get("status") != "completed" or not item["result"].get("marker"):
                raise SystemExit(f"line {number}: read reconciliation mismatch")
        elif item["operation"] == "set_thread_archived":
            if linked["event_type"] != "host_operation_recorded" or linked["payload"].get("operation") != "set_thread_archived" or linked["payload"].get("thread_id") != item["arguments"].get("thread_id"):
                raise SystemExit(f"line {number}: archival mismatch")
            if item["result"].get("archived") is not True:
                raise SystemExit(f"line {number}: archive result mismatch")
        else:
            raise SystemExit(f"line {number}: unsupported operation {item['operation']}")
    state = replay(event_list)
    for task in state["tasks"].values():
        if task.get("task_handle") and task["task_handle"].get("state") != "archived":
            raise SystemExit(f"task {task['task_id']}: handle lifecycle is not archived")
        if task.get("state") not in {"complete", "cancelled", "superseded"}:
            raise SystemExit(f"task {task['task_id']}: lifecycle is not reconciled")
    expected_counts = {"create_thread": len(state["tasks"]), "read_thread": 4, "send_message_to_thread": 2, "set_thread_archived": len(state["tasks"])}
    if counts != expected_counts:
        raise SystemExit(f"incomplete host operation set: {counts}, expected {expected_counts}")
    print(f"VALID_HOST_EVIDENCE: {len(seen)} linked events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
