import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from caption_segments import lint, segment_words, to_srt  # noqa: E402
from qc_render import load_template  # noqa: E402


class CaptionTest(unittest.TestCase):
    def test_blocks_respect_3_to_5_words_and_punctuation(self):
        text = "Sabe por que esse arroz não queima? A panela de barro segura o calor, sem pressão."
        blocks = segment_words([{"word": w} for w in text.split()])
        self.assertTrue(all(2 <= b["words"] <= 5 for b in blocks), blocks)
        self.assertEqual(blocks[0]["text"], "Sabe por que esse arroz")
        self.assertTrue(any(b["text"].endswith("queima?") for b in blocks))

    def test_lint_flags_dash_and_long_blocks(self):
        blocks = [{"text": "panela — barro", "start": 0, "end": 5, "words": 3}]
        issues = lint(blocks)
        self.assertTrue(any("travessão" in i["issue"] for i in issues))
        self.assertTrue(any("3,5s" in i["issue"] for i in issues))

    def test_srt_and_cli(self):
        words = [{"word": w, "start": i * 0.4, "end": i * 0.4 + 0.35} for i, w in enumerate("feijão em quarenta minutos sem panela de pressão".split())]
        srt = to_srt(segment_words(words))
        self.assertIn("00:00:00,000 -->", srt)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "t.json"
            src.write_text(json.dumps({"segments": [{"text": "", "words": words}]}), encoding="utf-8")
            out, srt_path = Path(tmp) / "c.json", Path(tmp) / "c.srt"
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "caption_segments.py"), str(src), "--out", str(out), "--srt", str(srt_path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(srt_path.exists())
            self.assertNotEqual(subprocess.run([sys.executable, str(ROOT / "scripts" / "caption_segments.py"), str(src), "--out", str(out)], capture_output=True).returncode, 0)


class TemplateTest(unittest.TestCase):
    def test_templates_are_well_formed(self):
        data = json.loads((ROOT / "templates" / "osdr-formats.json").read_text(encoding="utf-8"))
        for name, t in data["templates"].items():
            self.assertLess(t["min_seconds"], t["max_seconds"], name)
            self.assertIn(t["format"], {"9:16", "4:5", "1:1", "16:9"}, name)
        self.assertEqual(load_template("meta-ad")["format"], "9:16")
        with self.assertRaises(ValueError):
            load_template("nope")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_qc_with_template_duration_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            clip = Path(tmp) / "ad.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30", "-f", "lavfi", "-i",
                            "sine=frequency=440:sample_rate=48000", "-af", "volume=-12dB", "-shortest", "-t", "2",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-threads", "2", str(clip)], check=True)
            script = ROOT / "scripts" / "qc_render.py"
            short = subprocess.run([sys.executable, str(script), str(clip), "--template", "meta-ad"], capture_output=True, text=True)
            self.assertEqual(short.returncode, 1)
            self.assertIn("duration_min", short.stdout)
            story = subprocess.run([sys.executable, str(script), str(clip), "--template", "story"], capture_output=True, text=True)
            self.assertEqual(story.returncode, 0, story.stdout + story.stderr)
            self.assertIn("house_style_reminders", story.stdout)


if __name__ == "__main__":
    unittest.main()
