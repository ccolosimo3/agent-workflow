import tempfile
import unittest
from pathlib import Path

from common import add_task, append, assign_task, confirm_policy, event, init_program
from orchestrator_core import LedgerError, load_events, replay


class ReviewFreshnessTests(unittest.TestCase):
    def test_review_invalidation_is_durable(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            add_task(path, "reviewer")
            confirm_policy(path)
            assign_task(path, "T1", "worker-thread")
            assign_task(path, "reviewer", "reviewer-thread")
            append(path, event("P1", "review_recorded", task_id="T1", payload={"review_id": "R1", "review_unit": "task", "review_role": "inner", "reviewer_task_id": "reviewer-thread", "reviewer_assignment_task_id": "reviewer", "assignment_generation": 1, "tip": "abc", "verdict": "APPROVED"}))
            append(path, event("P1", "review_invalidated", payload={"review_id": "R1", "reason": "tip changed"}))
            self.assertEqual(replay(load_events(path))["review_records"]["R1"]["freshness"], "stale")

    def test_self_review_and_duplicate_outer_identity_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            add_task(path, "reviewer")
            confirm_policy(path)
            assign_task(path, "T1", "worker-thread")
            assign_task(path, "reviewer", "reviewer-thread")
            with self.assertRaises(LedgerError):
                append(path, event("P1", "review_recorded", task_id="T1", payload={"review_id": "self", "review_unit": "task", "review_role": "inner", "reviewer_task_id": "worker-thread", "reviewer_assignment_task_id": "T1", "assignment_generation": 1, "tip": "abc", "verdict": "APPROVED"}))
            append(path, event("P1", "review_recorded", task_id="T1", payload={"review_id": "inner", "review_unit": "integrated_candidate", "review_role": "inner", "reviewer_task_id": "reviewer-thread", "reviewer_assignment_task_id": "reviewer", "assignment_generation": 1, "tip": "abc", "verdict": "APPROVED"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "candidate_recorded", payload={"id": "C1", "tip": "abc", "inner_review_id": "inner", "outer_review_id": "inner", "state": "outer_approved", "verification_ids": ["missing"]}))


if __name__ == "__main__":
    unittest.main()
