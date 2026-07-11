import tempfile
import unittest
from pathlib import Path

from common import add_task, append, event, init_program
from orchestrator_core import LedgerError, load_events, replay


class TransitionTests(unittest.TestCase):
    def test_task_happy_path_and_illegal_skip(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            with self.assertRaises(LedgerError):
                append(path, event("P1", "task_transition", task_id="T1", prior_state="proposed", next_state="complete"))
            for prior, nxt in [("proposed", "planning"), ("planning", "review_ready"), ("review_ready", "spec_review"), ("spec_review", "ready")]:
                append(path, event("P1", "task_transition", task_id="T1", prior_state=prior, next_state=nxt))
            self.assertEqual(replay(load_events(path))["tasks"]["T1"]["state"], "ready")


if __name__ == "__main__":
    unittest.main()
