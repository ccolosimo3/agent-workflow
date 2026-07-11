import tempfile
import unittest
from pathlib import Path

from common import append, event, init_program
from orchestrator_core import LedgerError, load_events, replay


class ApprovalTests(unittest.TestCase):
    def test_approval_is_exact_and_consumable_once(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            request = {"approval_id": "A1", "action": "archive", "effect": "hide task", "exact_target": "task-1", "expires_at": "2099-01-01T00:00:00Z", "cap": 1}
            append(path, event("P1", "approval_requested", payload=request))
            append(path, event("P1", "approval_granted", payload={"approval_id": "A1", "granting_message_pointer": "turn-1"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "approval_consumed", payload={"approval_id": "A1", "action": "archive", "effect": "hide task", "exact_target": "task-2"}))
            append(path, event("P1", "approval_consumed", payload={"approval_id": "A1", "action": "archive", "effect": "hide task", "exact_target": "task-1"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "approval_consumed", payload={"approval_id": "A1", "action": "archive", "effect": "hide task", "exact_target": "task-1"}))
            self.assertEqual(replay(load_events(path))["approvals"]["A1"]["state"], "consumed")


if __name__ == "__main__":
    unittest.main()
