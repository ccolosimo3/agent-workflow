import tempfile
import unittest
import json
import subprocess
import sys
from pathlib import Path

from common import add_task, append, event, init_program
from common import ROOT
from orchestrator_core import LedgerError, handle_operator_message, load_events, render_status, replay, select_route


class StatusAndRoutingTests(unittest.TestCase):
    def test_pilot_executes_full_mechanism_lifecycle(self):
        scenario = ROOT / "pilot" / "scenario.json"
        runner = ROOT / "pilot" / "run_orchestrated.py"
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "out"
            result = subprocess.run([sys.executable, str(runner), "--scenario", str(scenario), "--output", str(output)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            state = replay(load_events(output))
            self.assertTrue(all(task["state"] == "complete" for task in state["tasks"].values()))
            self.assertEqual(state["leases"]["writer-1"]["state"], "released")
            self.assertEqual(state["review_records"]["R1"]["freshness"], "stale")
            self.assertEqual(state["integration_candidates"]["C1"]["state"], "awaiting_outer")
            self.assertEqual(state["approvals"]["outer-gate"]["state"], "requested")
            self.assertEqual(state["state"], "awaiting_operator_gate")
            broken = json.loads(scenario.read_text())
            broken["tasks"] = []
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(broken))
            rejected = subprocess.run([sys.executable, str(runner), "--scenario", str(bad), "--output", str(Path(td) / "bad-out")], text=True, capture_output=True)
            self.assertNotEqual(rejected.returncode, 0)

    def test_status_preserves_next_action(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            handle_operator_message(path, "informational", "status?", event("P1", "task_transition", task_id="T1", prior_state="proposed", next_state="planning"))
            self.assertIn("Next: plan", render_status(replay(load_events(path))))
            self.assertEqual(replay(load_events(path))["tasks"]["T1"]["state"], "planning")

    def test_reasoning_uses_lowest_adequate_route_and_xhigh_needs_trigger(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            init_program(path)
            add_task(path)
            policy = {
                "policy_revision": 1, "mode": "auto", "quality_bias": "balanced",
                "route_classes": {
                    "deep": {"model": "gpt-5.6-sol", "max_reasoning": "xhigh"},
                    "balanced": {"model": "gpt-5.6-terra", "max_reasoning": "xhigh"},
                    "fast": {"model": "gpt-5.6-luna", "max_reasoning": "high"},
                },
            }
            append(path, event("P1", "model_policy_confirmed", payload=policy))
            self.assertEqual(select_route(policy, "low"), {"route_class": "fast", "model_id": "gpt-5.6-luna", "reasoning_effort": "medium"})
            self.assertEqual(select_route(policy, "mechanical_multistep"), {"route_class": "fast", "model_id": "gpt-5.6-luna", "reasoning_effort": "high"})
            self.assertEqual(select_route(policy, "routine"), {"route_class": "balanced", "model_id": "gpt-5.6-terra", "reasoning_effort": "high"})
            self.assertEqual(select_route(policy, "moderate"), {"route_class": "balanced", "model_id": "gpt-5.6-terra", "reasoning_effort": "high"})
            base = {"model_policy_revision": 1, "route_class": "balanced", "model_id": "gpt-5.6-terra", "risk_class": "routine"}
            append(path, event("P1", "model_route_selected", task_id="T1", payload={**base, "reasoning_effort": "high"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "model_route_changed", task_id="T1", payload={**base, "reasoning_effort": "xhigh"}))
            append(path, event("P1", "model_route_changed", task_id="T1", payload={**base, "reasoning_effort": "xhigh", "exceptional_trigger": "repeated non-convergence"}))
            with self.assertRaises(LedgerError):
                append(path, event("P1", "model_route_changed", task_id="T1", payload={"model_policy_revision": 1, "route_class": "fast", "model_id": "gpt-5.6-luna", "reasoning_effort": "medium", "risk_class": "security"}))


if __name__ == "__main__":
    unittest.main()
