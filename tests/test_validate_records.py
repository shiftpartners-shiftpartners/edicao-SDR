import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_records.py"


class ValidateRecordsTest(unittest.TestCase):
    def run_validation(self, record, schema_name):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", encoding="utf-8", delete=False) as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            temp_path = Path(handle.name)
        try:
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(temp_path), "--schema", str(ROOT / "schemas" / schema_name)],
                text=True, capture_output=True
            )
        finally:
            temp_path.unlink(missing_ok=True)

    def test_examples_are_valid(self):
        pairs = [
            ("creative-ledger.example.jsonl", "creative-variant.schema.json"),
            ("performance-observations.example.jsonl", "performance-observation.schema.json"),
        ]
        for record_name, schema_name in pairs:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(ROOT / "templates" / record_name), "--schema", str(ROOT / "schemas" / schema_name)],
                text=True, capture_output=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_creative_identity_fails(self):
        result = self.run_validation({"status": "draft"}, "creative-variant.schema.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("creative_id", result.stderr)

    def test_absence_is_not_silently_replaced_by_zero(self):
        row = json.loads((ROOT / "templates" / "performance-observations.example.jsonl").read_text(encoding="utf-8"))
        self.assertIsNone(row["metrics"]["purchases"])

    def test_invalid_observations_rejected(self):
        base = json.loads((ROOT / "templates" / "performance-observations.example.jsonl").read_text())
        for change in [{"window_end": "2026-01-01T00:00:00-03:00"},
                       {"window_start": "not-a-date"}, {"timezone": "Invalid/Zone"},
                       {"decided_by_human": False}, {"decision": "scale"},
                       {"metrics": {"spend": -1}}, {"metrics": {"purchases": True}}]:
            with self.subTest(change=change):
                row = dict(base, **change)
                self.assertNotEqual(self.run_validation(row, "performance-observation.schema.json").returncode, 0)

    def test_active_creative_requires_approval(self):
        row = json.loads((ROOT / "templates" / "creative-ledger.example.jsonl").read_text())
        row["status"] = "approved"
        self.assertEqual(self.run_validation(row, "creative-variant.schema.json").returncode, 1)

    def test_nonfinite_fails(self):
        row = json.loads((ROOT / "templates" / "performance-observations.example.jsonl").read_text())
        row["metrics"]["spend"] = float("nan")
        self.assertEqual(self.run_validation(row, "performance-observation.schema.json").returncode, 2)


if __name__ == "__main__":
    unittest.main()
