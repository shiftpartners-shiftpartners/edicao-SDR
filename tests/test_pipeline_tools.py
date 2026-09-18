import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from edp_to_render_plan import convert, parse_timestamp  # noqa: E402
from diversity_check import audit  # noqa: E402
from handoff_pack import build  # noqa: E402

LEDGER = json.loads((ROOT / "templates" / "creative-ledger.example.jsonl").read_text(encoding="utf-8"))


class EdpConversionTest(unittest.TestCase):
    def test_timestamps(self):
        self.assertEqual(parse_timestamp("00:00:02.500"), 2.5)
        self.assertEqual(parse_timestamp("01:05"), 65.0)
        self.assertEqual(parse_timestamp(3), 3.0)
        for bad in ("abc", -1, True, "1:2:3:4", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_timestamp(bad)

    def test_template_converts_and_unsupported_is_reported(self):
        import yaml
        edp = yaml.safe_load((ROOT / "templates" / "edit-plan.example.yaml").read_text(encoding="utf-8"))
        plan, unsupported = convert(edp)
        self.assertEqual(plan, {"version": 1, "format": "9:16", "clips": [{"source": "exemplo.mp4", "in": 0.0, "out": 2.5}]})
        self.assertEqual(unsupported, [])
        edp["timeline"][0]["text_overlay"] = "PROMO"
        _, unsupported = convert(edp)
        self.assertEqual(unsupported[0]["field"], "text_overlay")

    def test_rejects_escaping_source_and_bad_interval(self):
        edp = {"output": {"format": "9:16"}, "timeline": [{"order": 1, "source": "../x.mp4", "in": 0, "out": 1}]}
        with self.assertRaises(ValueError):
            convert(edp)
        edp["timeline"][0].update({"source": "x.mp4", "in": 2, "out": 1})
        with self.assertRaises(ValueError):
            convert(edp)

    def test_cli_refuses_unsupported_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            edp = Path(tmp) / "edp.yaml"
            edp.write_text('output: {format: "4:5"}\ntimeline:\n  - {order: 1, source: a.mp4, in: 0, out: 1, crop: "center"}\n', encoding="utf-8")
            out = Path(tmp) / "plan.json"
            cmd = [sys.executable, str(ROOT / "scripts" / "edp_to_render_plan.py"), str(edp), "--out", str(out)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            self.assertFalse(out.exists())
            result = subprocess.run(cmd + ["--unsupported", "report"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("crop", result.stderr)
            self.assertEqual(json.loads(out.read_text())["format"], "4:5")


class DiversityTest(unittest.TestCase):
    def test_template_ledger_is_consistent(self):
        coverage, findings = audit([LEDGER])
        self.assertEqual(coverage[LEDGER["product_line"]]["variants"], 1)
        self.assertEqual(findings, [])

    def test_cosmetic_twin_is_flagged(self):
        twin = dict(LEDGER, creative_id="kitcozinha-c01-h01-e01-9x16-v02", version=2, notes="só mudou a cor")
        _, findings = audit([LEDGER, twin])
        self.assertTrue(any(f["severity"] == "fail" for f in findings))

    def test_single_concept_warns_but_hook_change_passes(self):
        other = dict(LEDGER, creative_id="kitcozinha-c01-h02-e01-9x16-v01", hook={"id": "h02", "summary": "Pergunta seca"})
        _, findings = audit([LEDGER, other])
        self.assertEqual([f["severity"] for f in findings], ["warn"])

    def test_cli_exit_codes(self):
        script = ROOT / "scripts" / "diversity_check.py"
        ok = subprocess.run([sys.executable, str(script), str(ROOT / "templates" / "creative-ledger.example.jsonl")], capture_output=True)
        self.assertEqual(ok.returncode, 0)
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as handle:
            handle.write(json.dumps(LEDGER) + "\n" + json.dumps(dict(LEDGER, creative_id="kitcozinha-c01-h01-e01-9x16-v02")) + "\n")
        result = subprocess.run([sys.executable, str(script), handle.name], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(subprocess.run([sys.executable, str(script), handle.name, "--report-only"], capture_output=True).returncode, 0)


class HandoffTest(unittest.TestCase):
    def test_refuses_unapproved_unless_draft(self):
        with self.assertRaises(ValueError):
            build(LEDGER, "conversas", "Operador", "2026-09-18")
        text = build(LEDGER, "conversas", "", "2026-09-18", draft=True)
        self.assertIn("NÃO APROVADO", text)
        self.assertIn(LEDGER["creative_id"], text)

    def test_approved_includes_qc(self):
        record = dict(LEDGER, human_approval="approved", status="approved")
        qc = {"technical_verdict": "pass", "sha256": "abc", "duration_seconds": 15, "checks": [{"status": "pass", "name": "x", "detail": "y"}]}
        text = build(record, "conversas", "Operador", "2026-09-18", qc)
        self.assertIn("HANDOFF PARA MÍDIA", text)
        self.assertIn("Operador", text)
        self.assertIn("pass: x", text)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
class QcRenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        base = Path(cls.temp.name)
        common = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-threads", "2", "-t", "2"]
        cls.good = base / "good.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30", "-f", "lavfi",
                        "-i", "sine=frequency=440:sample_rate=48000", "-af", "volume=-12dB", "-shortest"] + common + [str(cls.good)], check=True)
        cls.black = base / "black.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=30", "-f", "lavfi",
                        "-i", "anullsrc=r=48000:cl=stereo", "-shortest"] + common + [str(cls.black)], check=True)
        cls.script = ROOT / "scripts" / "qc_render.py"

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_qc(self, *extra):
        return subprocess.run([sys.executable, str(self.script)] + list(extra), capture_output=True, text=True)

    def test_good_render_passes(self):
        out = Path(self.temp.name) / "qc.json"
        result = self.run_qc(str(self.good), "--format", "9:16", "--max-seconds", "3", "--out", str(out))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(out.read_text())
        self.assertEqual(report["technical_verdict"], "pass")
        self.assertEqual(report["human_approval"], "required")
        self.assertNotEqual(self.run_qc(str(self.good), "--out", str(out)).returncode, 0)

    def test_black_silent_render_fails(self):
        result = self.run_qc(str(self.black), "--format", "9:16")
        self.assertEqual(result.returncode, 1)
        names = {c["name"] for c in json.loads(result.stdout)["checks"] if c["status"] == "fail"}
        self.assertIn("no_black_opening", names)
        self.assertIn("audio_not_silent", names)

    def test_wrong_geometry_fails(self):
        result = self.run_qc(str(self.good), "--format", "1:1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("geometry", result.stdout)


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
class ContactSheetOnRenderTest(unittest.TestCase):
    """Regression: sheets of concatenated renders must contain the opening frames."""

    def test_first_tile_comes_from_the_opening(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from render_plan import render
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "source"
            root.mkdir()
            white, black = root / "white.mp4", root / "black.mp4"
            for path, color in ((white, "white"), (black, "black")):
                subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", f"color=c={color}:s=320x240:r=30",
                                "-t", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-threads", "2", str(path)], check=True)
            plan = {"version": 1, "format": "1:1", "clips": [
                {"source": "white.mp4", "in": 0, "out": 1.5}, {"source": "black.mp4", "in": 0, "out": 1.5}]}
            output = base / "concat.mp4"
            render(plan, root, output, execute=True)
            sheet = base / "sheet.png"
            script = ROOT / "scripts" / "contact_sheet.py"
            subprocess.run([sys.executable, str(script), str(output), "--out", str(sheet), "--frames", "4", "--columns", "4", "--width", "64"],
                           check=True, capture_output=True)
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(sheet), "-vf", "crop=32:32:8:8", "-f", "rawvideo",
                                  "-pix_fmt", "gray", "-"], check=True, capture_output=True).stdout
            self.assertGreater(sum(raw) / len(raw), 200, "first tile should come from the white opening clip")
            raw_last = subprocess.run(["ffmpeg", "-v", "error", "-i", str(sheet), "-vf", "crop=32:32:iw-40:8", "-f", "rawvideo",
                                       "-pix_fmt", "gray", "-"], check=True, capture_output=True).stdout
            self.assertLess(sum(raw_last) / len(raw_last), 60, "last tile should come from the black closing clip")
