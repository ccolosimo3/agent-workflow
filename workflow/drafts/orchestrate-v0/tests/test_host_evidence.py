import json
import tempfile
import unittest
from pathlib import Path

from common import ROOT, run_script


class HostEvidenceTests(unittest.TestCase):
    def test_exact_and_complete_host_reconciliation(self):
        program = ROOT / "pilot" / "artifacts" / "host-run-2026-07-10"
        source = program / "host-evidence.jsonl"
        valid = run_script("validate_host_evidence.py", "--program", str(program), "--evidence", str(source))
        self.assertEqual(valid.returncode, 0, valid.stderr)
        rows = [json.loads(line) for line in source.read_text().splitlines()]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "evidence.jsonl"
            path.write_text(json.dumps(rows[0]) + "\n")
            incomplete = run_script("validate_host_evidence.py", "--program", str(program), "--evidence", str(path))
            self.assertNotEqual(incomplete.returncode, 0)
            mutated = [dict(row) for row in rows]
            mutated[4] = {**mutated[4], "result": {"accepted": False, "same_thread": True}}
            path.write_text("".join(json.dumps(row) + "\n" for row in mutated))
            wrong_result = run_script("validate_host_evidence.py", "--program", str(program), "--evidence", str(path))
            self.assertNotEqual(wrong_result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
