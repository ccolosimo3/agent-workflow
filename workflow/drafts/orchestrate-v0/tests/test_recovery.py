import json
import tempfile
import unittest
from pathlib import Path

from common import add_task, append, event, init_program, run_script
from orchestrator_core import LedgerError


class RecoveryTests(unittest.TestCase):
    def test_dispatch_requires_durable_unique_intent(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            policy = {"policy_revision": 1, "mode": "auto", "route_classes": {"balanced": {"model": "terra", "max_reasoning": "xhigh"}}}
            append(path, event("P1", "model_policy_confirmed", payload=policy))
            route = {"model_policy_revision": 1, "route_class": "balanced", "model_id": "terra", "reasoning_effort": "high", "risk_class": "routine"}
            append(path, event("P1", "model_route_selected", task_id="T1", payload=route))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "assignment_started", task_id="T1", payload={"assignment_generation": 1, "assignment_id": "A1", "idempotency_key": "K1"}))
            append(path, event("P1", "dispatch_intent_recorded", task_id="T1", payload={"assignment_generation": 1, "idempotency_key": "K1"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "dispatch_intent_recorded", task_id="T1", payload={"assignment_generation": 1, "idempotency_key": "K2"}))
            append(path, event("P1", "assignment_started", task_id="T1", payload={"assignment_generation": 1, "assignment_id": "A1", "idempotency_key": "K1", "task_handle": "thread-1", "model_policy_revision": 1, "model_route": {"route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"}}))
            append(path, event("P1", "review_recorded", task_id="T1", payload={"review_id": "R1", "review_unit": "task", "reviewer_task_id": "thread-1", "assignment_generation": 1, "verdict": "APPROVED", "tip": "one"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "assignment_continued", task_id="T1", payload={"assignment_generation": 2, "assignment_id": "stale-policy", "task_handle": "thread-1", "model_policy_revision": 999, "model_route": {"route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"}}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "assignment_continued", task_id="T1", payload={"assignment_generation": 2, "assignment_id": "unsupported-route", "task_handle": "thread-1", "model_policy_revision": 1, "model_route": {"route_class": "deep", "model_id": "unsupported", "reasoning_effort": "xhigh"}}))
            append(path, event("P1", "assignment_fenced", task_id="T1", payload={"assignment_generation": 1, "reason": "route escalation"}))
            append(path, event("P1", "model_route_changed", task_id="T1", payload={"model_policy_revision": 1, "route_class": "balanced", "model_id": "terra", "reasoning_effort": "xhigh", "exceptional_trigger": "adversarial proof"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "assignment_continued", task_id="T1", payload={"assignment_generation": 2, "assignment_id": "old-route", "task_handle": "thread-1", "model_policy_revision": 1, "model_route": {"route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"}}))
            append(path, event("P1", "assignment_continued", task_id="T1", payload={"assignment_generation": 2, "assignment_id": "A2", "task_handle": "thread-1", "model_policy_revision": 1, "model_route": {"route_class": "balanced", "model_id": "terra", "reasoning_effort": "xhigh"}}))
            self.assertEqual(__import__("orchestrator_core").replay(__import__("orchestrator_core").load_events(path))["review_records"]["R1"]["freshness"], "stale")

    def test_detect_and_rebuild_stale_views(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            view = json.loads(path.joinpath("program.json").read_text())
            view["last_event_id"] = 0
            path.joinpath("program.json").write_text(json.dumps(view))
            detected = run_script("validate_program.py", "--check-views", str(path))
            self.assertEqual((detected.returncode, detected.stdout.strip()), (3, "STALE_VIEW"))
            rebuilt = run_script("validate_program.py", "--startup-recover", str(path))
            self.assertEqual((rebuilt.returncode, rebuilt.stdout.strip()), (0, "REBUILT"))
            current = run_script("validate_program.py", "--check-views", str(path))
            self.assertEqual((current.returncode, current.stdout.strip()), (0, "CURRENT"))


if __name__ == "__main__":
    unittest.main()
