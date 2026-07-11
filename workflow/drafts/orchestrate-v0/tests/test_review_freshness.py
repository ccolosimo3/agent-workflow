import tempfile
import unittest
from pathlib import Path

from common import add_task, append, event, init_program
from orchestrator_core import load_events, replay


class ReviewFreshnessTests(unittest.TestCase):
    def test_review_invalidation_is_durable(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            append(path, event("P1", "model_policy_confirmed", payload={"policy_revision": 1, "mode": "auto", "route_classes": {"balanced": {"model": "terra", "max_reasoning": "xhigh"}}}))
            route = {"model_policy_revision": 1, "route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"}
            append(path, event("P1", "model_route_selected", task_id="T1", payload=route))
            append(path, event("P1", "dispatch_intent_recorded", task_id="T1", payload={"assignment_generation": 1, "idempotency_key": "K1"}))
            append(path, event("P1", "assignment_started", task_id="T1", payload={"assignment_generation": 1, "assignment_id": "A1", "idempotency_key": "K1", "task_handle": {"thread_id": "thread-1"}, "model_policy_revision": 1, "model_route": {"route_class": "balanced", "model_id": "terra", "reasoning_effort": "high"}}))
            append(path, event("P1", "review_recorded", task_id="T1", payload={"review_id": "R1", "review_unit": "task", "reviewer_task_id": "thread-1", "assignment_generation": 1, "tip": "abc", "verdict": "APPROVED"}))
            append(path, event("P1", "review_invalidated", payload={"review_id": "R1", "reason": "tip changed"}))
            self.assertEqual(replay(load_events(path))["review_records"]["R1"]["freshness"], "stale")


if __name__ == "__main__":
    unittest.main()
