import tempfile
import unittest
from pathlib import Path

from common import add_task, append, assign_task, confirm_policy, event, init_program
from orchestrator_core import LedgerError


class SafetyContractTests(unittest.TestCase):
    def test_schema_authority_and_freshness_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            confirm_policy(path)
            assign_task(path, "T1", "thread-1")
            with self.assertRaises(LedgerError):
                append(path, event("P1", "program_transition", prior_state="draft", next_state="authority_locked", actor="operator", payload={"authority_envelope": "claimed"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "task_transition", task_id="T1", prior_state="proposed", next_state="planning", actor="worker"))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "status_reported", payload={"message_kind": "informational", "unknown": True}))
            with self.assertRaises(LedgerError):
                append(path, {**event("P1", "status_reported"), "surprise": True})
            with self.assertRaises(LedgerError):
                append(path, event("P1", "assignment_started", task_id="T1", payload={"assignment_generation": 2, "assignment_id": "A2", "idempotency_key": "missing"}))
            append(path, event("P1", "approval_requested", payload={"approval_id": "expired", "action": "push", "effect": "external mutation", "exact_target": "origin", "expires_at": "2000-01-01T00:00:00Z"}))
            append(path, event("P1", "approval_granted", payload={"approval_id": "expired", "granting_message_pointer": "turn"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "approval_consumed", payload={"approval_id": "expired", "action": "push", "effect": "external mutation", "exact_target": "origin"}))
            lease = {"lease_id": "L1", "mode": "write", "scope": "src", "owner": "T1", "assignment_generation": 1, "heartbeat_at": "2026-01-01T00:00:00Z", "expires_at": "2099-01-01T00:00:00Z"}
            append(path, event("P1", "lease_acquired", task_id="T1", payload=lease))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "lease_acquired", task_id="T1", payload={**lease, "lease_id": "L2", "scope": "src/child.py"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "environment_attested", payload={"id": "E1", "task_id": "T1", "checkout": "/tmp/x", "base": "abc", "commands": [], "ready": False}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "environment_attested", payload={"id": "E2", "task_id": "T1", "checkout": "/does/not/exist", "base": "abc", "commands": [{"command": "smoke", "result": "passed", "exit_code": 0, "output_sha256": "abc"}], "ready": True, "dirty_state": "clean", "evidence": "fixture"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "candidate_recorded", payload={"id": "C1", "tip": "abc", "inner_review_id": "missing", "outer_review_id": "missing2", "state": "outer_approved"}))


if __name__ == "__main__":
    unittest.main()
