#!/usr/bin/env python3
"""Bounded local rough-cut renderer. No arbitrary filters, URLs or shell."""
import argparse
import json
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from media_probe import run_ffprobe, sha256_file

FORMATS = {"9:16": (1080, 1920), "4:5": (1080, 1350),
           "1:1": (1080, 1080), "16:9": (1920, 1080)}
EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_plan(plan, root):
    if not isinstance(plan, dict) or set(plan) != {"version", "format", "clips"}:
        raise ValueError("plan requires only version, format and clips")
    if type(plan["version"]) is not int or plan["version"] != 1 or plan["format"] not in FORMATS:
        raise ValueError("unsupported version or format")
    clips = plan["clips"]
    if not isinstance(clips, list) or not 1 <= len(clips) <= 30:
        raise ValueError("expected 1..30 clips")
    total = 0
    resolved = []
    for clip in clips:
        if not isinstance(clip, dict) or set(clip) != {"source", "in", "out"}:
            raise ValueError("clips require only source, in and out")
        if not isinstance(clip["source"], str):
            raise ValueError("source must be a relative filename")
        path = (root / clip["source"]).resolve()
        if Path(clip["source"]).is_absolute() or not path.is_relative_to(root):
            raise ValueError("source escapes root")
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            raise ValueError("source must be a supported local video")
        start, end = clip["in"], clip["out"]
        if not finite(start) or not finite(end) or not 0 <= start < end:
            raise ValueError("invalid clip interval")
        info = run_ffprobe(path)
        videos = [s for s in info["streams"] if s["codec_type"] == "video"]
        if not videos:
            raise ValueError("source has no video")
        duration = float(videos[0].get("duration", info["format"].get("duration", 0)))
        if not math.isfinite(duration) or end > duration + 0.01:
            raise ValueError("clip exceeds source duration")
        total += end - start
        resolved.append((path, start, end, any(s["codec_type"] == "audio" for s in info["streams"])))
    if total > 180:
        raise ValueError("rough-cut budget is 180 seconds")
    return resolved, total


def run(command):
    subprocess.run(command, check=True, capture_output=True, text=True, timeout=600)


def render(plan, root, output, execute=False):
    root, output = root.resolve(), output.absolute()
    if not root.is_dir():
        raise ValueError("source root is missing")
    if output.resolve().is_relative_to(root) or output.suffix.lower() != ".mp4":
        raise ValueError("output must be an MP4 outside source root")
    report_path = Path(str(output) + ".json")
    if output.exists() or output.is_symlink() or report_path.exists() or report_path.is_symlink():
        raise ValueError("output/report already exists; choose a new version")
    clips, duration = validate_plan(plan, root)
    width, height = FORMATS[plan["format"]]
    report = {"plan": plan, "duration_seconds": duration,
              "sources": [{"source": str(p.relative_to(root)), "sha256": sha256_file(p)} for p, _, _, _ in clips],
              "human_approval": "required", "mode": "render" if execute else "dry-run"}
    if not execute:
        return report
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sdr-render-", dir=output.parent) as temp:
        temp = Path(temp)
        segments = []
        for i, (source, start, end, audio) in enumerate(clips):
            target = temp / f"segment-{i}.mp4"
            cmd = ["ffmpeg", "-nostdin", "-v", "error", "-n",
                   "-protocol_whitelist", "file,pipe", "-ss", str(start), "-i", str(source)]
            if not audio:
                cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            cmd += ["-t", str(end-start), "-map", "0:v:0", "-map", "0:a:0" if audio else "1:a:0",
                    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
                    "-af", "apad", "-c:v", "libx264", "-threads", "2", "-preset", "veryfast",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000",
                    "-ac", "2", "-map_metadata", "-1", str(target)]
            run(cmd)
            segments.append(target)
        concat = temp / "segments.txt"
        concat.write_text("".join(f"file '{p.name}'\n" for p in segments), encoding="utf-8")
        candidate = temp / "candidate.mp4"
        run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "concat", "-safe", "1",
             "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(candidate)])
        info = run_ffprobe(candidate)
        actual = float(info["format"]["duration"])
        video = next(s for s in info["streams"] if s["codec_type"] == "video")
        if abs(actual-duration) > 0.15 + len(clips)/30 or (video["width"], video["height"]) != (width, height):
            raise ValueError("render duration or geometry failed QC")
        run(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(candidate), "-f", "null", "-"])
        report.update({"output_sha256": sha256_file(candidate), "actual_duration_seconds": actual,
                       "technical_checks": ["full_decode", "duration", "geometry"],
                       "ffmpeg_version": subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True).stdout.splitlines()[0]})
        # Hard-link promotion is atomic and refuses to replace an existing path.
        # Temporary directory is on the output filesystem.
        report_file = temp / "report.json"
        report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        os.link(report_file, report_path)
        os.link(candidate, output)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            parser.exit(2, f"missing dependency: {binary}\n")
    try:
        report = render(json.loads(args.plan.read_text(encoding="utf-8")), args.source_root, args.out, args.execute)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    except (ValueError, TypeError, KeyError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"render failed: {exc}\n")


if __name__ == "__main__":
    main()
