import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def synth_source(path, seconds=4):
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=480x854:r=30", "-f", "lavfi", "-i",
                    "sine=frequency=330:sample_rate=48000", "-af", "volume=-12dB", "-shortest", "-t", str(seconds),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-threads", "2", str(path)], check=True)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
class LoteRunTest(unittest.TestCase):
    def test_runs_a_lote_end_to_end_and_skips_existing_on_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source_root = tmp / "source"
            source_root.mkdir()
            synth_source(source_root / "clip.mp4")
            lote = tmp / "lote-teste"
            lote.mkdir()
            edp = {"project_id": "teste-c01", "source_files": [{"path": "source/clip.mp4", "immutable": True}],
                   "output": {"format": "9:16", "duration_seconds": 3.0, "filename": "teste.mp4"},
                   "concept": {"id": "c01", "summary": "x"}, "hook": {"id": "h01", "summary": "y"},
                   "execution": {"id": "e01", "summary": "z"},
                   "timeline": [{"order": 1, "source": "clip.mp4", "in": "00:00:00.000", "out": "00:00:01.500", "crop": "",
                                 "text_overlay": "Panela de barro racha?", "notes": ""},
                                {"order": 2, "source": "clip.mp4", "in": "00:00:02.000", "out": "00:00:03.500", "crop": "",
                                 "text_overlay": "12x R$ 39,90 + frete · Comenta EU QUERO", "notes": ""}],
                   "qc": {"technical": "pending", "creative": "pending", "truth_compliance": "pending"},
                   "human_approval": "required"}
            (lote / "teste-c01.edit-plan.yaml").write_text(yaml.safe_dump(edp, allow_unicode=True), encoding="utf-8")
            renders = tmp / "renders"
            manifest = {"id": "lote-teste", "product_line": "teste", "format": "9:16", "max_seconds": 10,
                        "renders_dir": str(renders), "pieces": [{"id": "c01", "edp": "teste-c01.edit-plan.yaml", "output": "teste__c01__v01"}]}
            (lote / "lote.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
            script = ROOT / "scripts" / "lote_run.py"
            first = subprocess.run([sys.executable, str(script), str(lote), "--source-root", str(source_root),
                                    "--report", str(lote / "r1.md")], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertTrue((renders / "teste__c01__v01.mp4").exists())
            self.assertTrue((renders / "teste__c01__v01-draft.mp4").exists())
            self.assertTrue((renders / "teste__c01__v01-draft.qc.json").exists())
            self.assertIn("| c01 |", (lote / "r1.md").read_text(encoding="utf-8"))
            self.assertIn("pass", first.stdout)
            second = subprocess.run([sys.executable, str(script), str(lote), "--source-root", str(source_root),
                                     "--report", str(lote / "r2.md")], capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertIn("existia", second.stdout)
            third = subprocess.run([sys.executable, str(script), str(lote), "--source-root", str(source_root),
                                    "--report", str(lote / "r2.md")], capture_output=True, text=True)
            self.assertNotEqual(third.returncode, 0)


if __name__ == "__main__":
    unittest.main()
