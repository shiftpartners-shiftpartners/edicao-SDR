import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from finish_draft import build_ass, caption_events, ffmpeg_command  # noqa: E402
from normalize_source import fixed_name  # noqa: E402

EDP = {"timeline": [
    {"order": 1, "in": "00:00:00.000", "out": "00:00:01.500", "text_overlay": "Panela de barro racha?"},
    {"order": 2, "in": "00:00:02.000", "out": "00:00:03.000", "text_overlay": ""},
    {"order": 3, "in": "00:00:00.000", "out": "00:00:01.000", "text_overlay": "12x R$ 39,90 + frete · Comenta EU QUERO"},
]}


def synth_clip(path, seconds=3.5):
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30", "-f", "lavfi", "-i",
                    "sine=frequency=440:sample_rate=48000", "-af", "volume=-12dB", "-shortest", "-t", str(seconds),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-threads", "2", str(path)], check=True)


class CaptionEventsTest(unittest.TestCase):
    def test_events_follow_clip_order_and_split_cta(self):
        events, total = caption_events(EDP)
        self.assertAlmostEqual(total, 3.5)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0][:3], (0.0, 1.5, "Legenda"))
        self.assertEqual(events[1][2], "CTA")
        self.assertIn("\\N", events[1][3])
        self.assertAlmostEqual(events[1][0], 2.5)

    def test_dash_is_refused(self):
        bad = {"timeline": [{"order": 1, "in": "00:00:00.000", "out": "00:00:01.000", "text_overlay": "barro — fogo"}]}
        with self.assertRaises(ValueError):
            caption_events(bad)

    def test_ass_and_command_shape(self):
        events, total = caption_events(EDP)
        ass = build_ass(events)
        self.assertIn("PlayResY: 1920", ass)
        self.assertEqual(ass.count("Dialogue:"), 2)
        cmd = ffmpeg_command(Path("r.mp4"), Path("o.mp4"), Path("o.ass"), total, vo=Path("v.mp3"))
        joined = " ".join(cmd)
        self.assertIn("amix=inputs=2", joined)
        self.assertIn("loudnorm", joined)
        self.assertIn("subtitles=o.ass", joined)
        self.assertIn("-t 3.500", joined)
        self.assertNotIn("amix", " ".join(ffmpeg_command(Path("r.mp4"), Path("o.mp4"), None, total)))


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
class FinishDraftCliTest(unittest.TestCase):
    def test_burns_captions_mixes_vo_and_refuses_overwrite(self):
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            render, vo, edp, out = tmp / "cut.mp4", tmp / "vo.wav", tmp / "plan.yaml", tmp / "draft.mp4"
            synth_clip(render)
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000", "-t", "2",
                            str(vo)], check=True)
            edp.write_text(yaml.safe_dump(EDP), encoding="utf-8")
            script = ROOT / "scripts" / "finish_draft.py"
            result = subprocess.run([sys.executable, str(script), str(edp), str(render), "--out", str(out), "--vo", str(vo)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())
            self.assertTrue(out.with_suffix(".ass").exists())
            probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                                   capture_output=True, text=True).stdout.strip()
            self.assertAlmostEqual(float(probe), 3.5, delta=0.3)
            again = subprocess.run([sys.executable, str(script), str(edp), str(render), "--out", str(out)], capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertIn("recusado", again.stderr)


@unittest.skipUnless(shutil.which("ffmpeg"), "FFmpeg required")
class NormalizeSourceTest(unittest.TestCase):
    def test_healthy_clip_is_left_alone_and_force_writes_sibling(self):
        with tempfile.TemporaryDirectory() as tmp:
            clip = Path(tmp) / "phone.mp4"
            synth_clip(clip, seconds=1)
            script = ROOT / "scripts" / "normalize_source.py"
            check = subprocess.run([sys.executable, str(script), str(clip), "--check"], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertIn("ok:", check.stdout)
            self.assertFalse(fixed_name(clip).exists())
            forced = subprocess.run([sys.executable, str(script), str(clip), "--force"], capture_output=True, text=True)
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertTrue(fixed_name(clip).exists())
            self.assertIn("decodificação após correção: ok", forced.stdout)
            self.assertEqual(fixed_name(clip).name, "phone.rangefix.mp4")


if __name__ == "__main__":
    unittest.main()
