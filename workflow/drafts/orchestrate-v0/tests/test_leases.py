import tempfile
import unittest
from pathlib import Path

from common import add_task, append, assign_task, confirm_policy, event, init_program
from orchestrator_core import LedgerError


class LeaseTests(unittest.TestCase):
    def test_overlapping_writer_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            confirm_policy(path)
            assign_task(path, "T1", "thread-1")
            base = {"scope": "src", "mode": "write", "owner": "T1", "assignment_generation": 1, "heartbeat_at": "2026-01-01T00:00:00Z", "expires_at": "2099-01-01T00:00:00Z"}
            append(path, event("P1", "lease_acquired", task_id="T1", payload={"lease_id": "L1", **base}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "lease_acquired", task_id="T1", payload={"lease_id": "L2", **base}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "lease_acquired", task_id="T1", payload={"lease_id": "L3", **base, "scope": "src/child.py"}))
            append(path, event("P1", "lease_released", payload={"lease_id": "L1"}))
            append(path, event("P1", "lease_acquired", task_id="T1", payload={"lease_id": "L2", **base}))
            append(path, event("P1", "lease_heartbeat", task_id="T1", payload={"lease_id": "L2", "assignment_generation": 1, "heartbeat_at": "2026-07-01T00:00:00Z", "expires_at": "2099-01-01T00:00:00Z"}))

    def test_fenced_assignment_cannot_reacquire_writer_lease(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            confirm_policy(path)
            assign_task(path, "T1", "thread-1")
            append(path, event("P1", "assignment_fenced", task_id="T1", payload={"assignment_generation": 1, "reason": "replacement"}))
            lease = {"lease_id": "L1", "scope": "src", "mode": "write", "owner": "T1", "assignment_generation": 1, "heartbeat_at": "2026-01-01T00:00:00Z", "expires_at": "2099-01-01T00:00:00Z"}
            with self.assertRaises(LedgerError):
                append(path, event("P1", "lease_acquired", task_id="T1", payload=lease))


if __name__ == "__main__":
    unittest.main()
