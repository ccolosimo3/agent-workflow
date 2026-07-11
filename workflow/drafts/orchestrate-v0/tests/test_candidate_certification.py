import hashlib
import tempfile
import unittest
from pathlib import Path

from common import add_task, append, assign_task, confirm_policy, event, init_program
from orchestrator_core import LedgerError, load_events, replay


class CandidateCertificationTests(unittest.TestCase):
    def _setup(self, path: Path) -> None:
        init_program(path)
        for task_id in ("work", "inner-reviewer", "outer-reviewer"):
            add_task(path, task_id)
        confirm_policy(path)
        assign_task(path, "work", "work-thread")
        assign_task(path, "inner-reviewer", "inner-thread")
        assign_task(path, "outer-reviewer", "outer-thread")
        append(path, event("P1", "environment_attested", task_id="work", payload={
            "id": "E1",
            "task_id": "work",
            "checkout": str(path.resolve()),
            "base": "base",
            "tip": "base",
            "assignment_generation": 1,
            "topology_revision": 1,
            "commands": [{"command": "smoke", "result": "passed", "exit_code": 0, "output_sha256": hashlib.sha256(b"passed").hexdigest()}],
            "ready": True,
            "dirty_state": "clean",
            "evidence": "temporary checkout",
        }))
        for verification_id, tip in (("V-good", "final"), ("V-wrong-tip", "old")):
            append(path, event("P1", "verification_recorded", task_id="work", payload={
                "id": verification_id,
                "command": "smoke",
                "result": "passed",
                "tip": tip,
                "assignment_generation": 1,
                "environment_attestation_id": "E1",
                "topology_revision": 1,
            }))
        append(path, event("P1", "review_recorded", task_id="work", payload={
            "review_id": "R-inner",
            "review_unit": "integrated_candidate",
            "review_role": "inner",
            "reviewer_task_id": "inner-thread",
            "reviewer_assignment_task_id": "inner-reviewer",
            "assignment_generation": 1,
            "verdict": "APPROVED",
            "tip": "final",
        }))
        append(path, event("P1", "review_recorded", task_id="work", payload={
            "review_id": "R-outer",
            "review_unit": "integrated_candidate",
            "review_role": "outer",
            "reviewer_task_id": "outer-thread",
            "reviewer_assignment_task_id": "outer-reviewer",
            "assignment_generation": 1,
            "verdict": "APPROVED",
            "tip": "final",
        }))

    def test_candidate_requires_current_exact_tip_verification_and_independent_reviews(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            self._setup(path)
            with self.assertRaises(LedgerError):
                append(path, event("P1", "candidate_recorded", payload={"id": "missing", "tip": "final", "inner_review_id": "R-inner", "state": "awaiting_outer", "verification_ids": ["missing"]}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "candidate_recorded", payload={"id": "wrong-tip", "tip": "final", "inner_review_id": "R-inner", "state": "awaiting_outer", "verification_ids": ["V-wrong-tip"]}))
            append(path, event("P1", "candidate_recorded", payload={"id": "approved", "tip": "final", "inner_review_id": "R-inner", "outer_review_id": "R-outer", "state": "outer_approved", "verification_ids": ["V-good"]}))
            self.assertEqual(replay(load_events(path))["integration_candidates"]["approved"]["state"], "outer_approved")

    def test_topology_change_invalidates_environment_verification_review_and_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            self._setup(path)
            append(path, event("P1", "candidate_recorded", payload={"id": "C1", "tip": "final", "inner_review_id": "R-inner", "state": "awaiting_outer", "verification_ids": ["V-good"]}))
            append(path, {**event("P1", "status_reported", payload={"outcome": "topology changed"}), "topology_revision": 2})
            state = replay(load_events(path))
            self.assertEqual(state["environment_attestations"]["E1"]["freshness"], "stale")
            self.assertEqual(state["verification_records"]["V-good"]["freshness"], "stale")
            self.assertEqual(state["review_records"]["R-inner"]["freshness"], "stale")
            self.assertEqual(state["integration_candidates"]["C1"]["state"], "stale")
            with self.assertRaises(LedgerError):
                append(path, event("P1", "candidate_recorded", payload={"id": "C2", "tip": "final", "inner_review_id": "R-inner", "state": "awaiting_outer", "verification_ids": ["V-good"]}))


if __name__ == "__main__":
    unittest.main()
