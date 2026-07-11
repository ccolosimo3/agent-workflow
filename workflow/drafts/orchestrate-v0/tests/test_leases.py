import tempfile
import unittest
from pathlib import Path

from common import append, event, init_program
from orchestrator_core import LedgerError


class LeaseTests(unittest.TestCase):
    def test_overlapping_writer_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            base = {"scope": "src", "mode": "write", "owner": "T1", "assignment_generation": 1}
            append(path, event("P1", "lease_acquired", payload={"lease_id": "L1", **base}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "lease_acquired", payload={"lease_id": "L2", **base}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "lease_acquired", payload={"lease_id": "L3", **base, "scope": "src/child.py"}))
            append(path, event("P1", "lease_released", payload={"lease_id": "L1"}))
            append(path, event("P1", "lease_acquired", payload={"lease_id": "L2", **base}))


if __name__ == "__main__":
    unittest.main()
