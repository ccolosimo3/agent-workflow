import json
import tempfile
import unittest
from pathlib import Path

from common import append, event, init_program
from orchestrator_core import LedgerError, load_events


class EventLogTests(unittest.TestCase):
    def test_hash_chain_detects_tamper_and_truncation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            append(path, event("P1", "status_reported", payload={"message_kind": "informational", "next_action": "continue"}))
            rows = path.joinpath("events.jsonl").read_text().splitlines()
            broken = json.loads(rows[1])
            broken["payload"]["next"] = "tampered"
            rows[1] = json.dumps(broken, separators=(",", ":"), sort_keys=True)
            path.joinpath("events.jsonl").write_text("\n".join(rows) + "\n")
            with self.assertRaises(LedgerError):
                load_events(path)
            path.joinpath("events.jsonl").write_text(rows[0])
            with self.assertRaises(LedgerError):
                load_events(path)


if __name__ == "__main__":
    unittest.main()
