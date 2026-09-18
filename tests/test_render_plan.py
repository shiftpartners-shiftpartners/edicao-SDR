import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from render_plan import render, validate_plan
from media_probe import sha256_file, run_ffprobe


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
class RenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.base = Path(cls.temp.name)
        cls.root = cls.base / "source"
        cls.root.mkdir()
        cls.source = cls.root / "test video.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                        "testsrc2=s=320x240:r=30", "-t", "3", "-c:v", "libx264",
                        "-threads", "2", str(cls.source)], check=True)
        cls.plan = {"version": 1, "format": "9:16", "clips": [
            {"source": cls.source.name, "in": 0, "out": 0.5},
            {"source": cls.source.name, "in": 1, "out": 1.5}]}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_real_render_silent_source_and_immutable_source(self):
        before = sha256_file(self.source)
        output = self.base / "result.mp4"
        result = render(self.plan, self.root, output, execute=True)
        self.assertEqual(before, sha256_file(self.source))
        self.assertEqual(result["human_approval"], "required")
        self.assertEqual(sha256_file(output), result["output_sha256"])
        self.assertTrue(Path(str(output) + ".json").exists())
        self.assertTrue(any(s["codec_type"] == "audio" for s in run_ffprobe(output)["streams"]))
        with self.assertRaises(ValueError):
            render(self.plan, self.root, output, execute=True)

    def test_dry_run_no_output(self):
        output = self.base / "dry.mp4"
        self.assertEqual(render(self.plan, self.root, output)["mode"], "dry-run")
        self.assertFalse(output.exists())

    def test_escape_root(self):
        plan = copy.deepcopy(self.plan)
        plan["clips"][0]["source"] = "../outside.mp4"
        with self.assertRaises(ValueError):
            validate_plan(plan, self.root)

    def test_symlink_escape(self):
        link = self.root / "escape.mp4"
        link.symlink_to(self.base / "outside.mp4")
        plan = copy.deepcopy(self.plan)
        plan["clips"][0]["source"] = link.name
        with self.assertRaises(ValueError):
            validate_plan(plan, self.root)

    def test_unknown_operation_fails(self):
        plan = dict(self.plan, subtitles="do-not-silently-ignore.srt")
        with self.assertRaises(ValueError):
            validate_plan(plan, self.root)

    def test_invalid_timestamps(self):
        for start, end in [(2, 1), (0, 99), (-1, 1), (0, float("nan")), (True, 2)]:
            with self.subTest(start=start, end=end):
                plan = copy.deepcopy(self.plan)
                plan["clips"][0].update({"in": start, "out": end})
                with self.assertRaises(ValueError):
                    validate_plan(plan, self.root)

    def test_output_in_source_rejected(self):
        with self.assertRaises(ValueError):
            render(self.plan, self.root, self.root / "new.mp4")

    def test_contact_sheet_protects_existing(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "contact_sheet.py"
        output = self.base / "sheet.png"
        command = [sys.executable, str(script), str(self.source), "--out", str(output)]
        subprocess.run(command, check=True, capture_output=True)
        before = sha256_file(output)
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(before, sha256_file(output))

    def test_probe_corrupt_input_fails(self):
        corrupt = self.base / "broken.mp4"
        corrupt.write_bytes(b"not a video")
        script = Path(__file__).resolve().parents[1] / "scripts" / "media_probe.py"
        result = subprocess.run([sys.executable, str(script), str(corrupt),
                                 "--out", str(self.base / "errors.json")], capture_output=True)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
