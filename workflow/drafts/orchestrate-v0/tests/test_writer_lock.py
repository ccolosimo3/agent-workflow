import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from common import SCRIPTS, init_program
from orchestrator_core import append_event, load_events, replay


class WriterLockTests(unittest.TestCase):
    def test_same_predecessor_never_loses_event(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            first = init_program(path)
            base = [sys.executable, str(SCRIPTS / "record_event.py"), str(path),
                    "--coordinator-generation", "1", "--expected-prev-event-hash", first["event_hash"]]
            commands = []
            for value in ("a", "b"):
                item = {"program_id": "P1", "event_type": "status_reported", "payload": {"message_kind": "informational", "operator_message": value}}
                commands.append(base + ["--event-json", json.dumps(item)])
            processes = [subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in commands]
            results = [proc.communicate() + (proc.returncode,) for proc in processes]
            self.assertEqual(sum(1 for _, _, code in results if code == 0), 1)
            self.assertTrue(all(code in {0, 5, 6} for _, _, code in results))
            self.assertEqual(len(load_events(path)), 2)
            loser = next(i for i, (_, _, code) in enumerate(results) if code != 0)
            events = load_events(path)
            append_event(path, {"program_id": "P1", "event_type": "status_reported", "payload": {"message_kind": "informational", "operator_message": ("a", "b")[loser]}}, events[-1]["event_hash"], replay(events)["coordinator_generation"], nonblocking=False)
            self.assertEqual(len(load_events(path)), 3)


if __name__ == "__main__":
    unittest.main()
