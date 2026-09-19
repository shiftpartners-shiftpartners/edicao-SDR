#!/usr/bin/env python3
"""Automated technical QC for a rendered MP4. Human creative/truth QC remains mandatory."""
import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from media_probe import run_ffprobe, sha256_file

FORMATS = {"9:16": (1080, 1920), "4:5": (1080, 1350), "1:1": (1080, 1080), "16:9": (1920, 1080)}
TEMPLATES_FILE = Path(__file__).resolve().parents[1] / "templates" / "osdr-formats.json"


def load_template(name):
    data = json.loads(TEMPLATES_FILE.read_text(encoding="utf-8"))
    if name not in data["templates"]:
        raise ValueError(f"unknown template: {name}; known: {sorted(data['templates'])}")
    return data["templates"][name]


def ffmpeg_stderr(args):
    proc = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + args, capture_output=True, text=True, timeout=600)
    return proc.returncode, proc.stderr


def check(name, ok, detail, severity="fail"):
    return {"name": name, "status": "pass" if ok else severity, "detail": detail}


def technical_qc(path, fmt=None, min_seconds=None, max_seconds=None, allow_silent=False):
    checks = []
    info = run_ffprobe(path)
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(info.get("format", {}).get("duration") or 0)
    checks.append(check("video_stream", video is not None, "video stream present" if video else "no video stream"))
    if video is None:
        return checks, duration
    checks.append(check("codec_h264", video.get("codec_name") == "h264", f"codec={video.get('codec_name')}"))
    pix = video.get("pix_fmt")
    checks.append(check("pix_fmt_yuv420p", pix in (None, "yuv420p"), f"pix_fmt={pix}", "warn" if pix is None else "fail"))
    width, height = video.get("width"), video.get("height")
    if fmt:
        expected = FORMATS[fmt]
        checks.append(check("geometry", (width, height) == expected, f"{width}x{height} expected {expected[0]}x{expected[1]}"))
    else:
        checks.append(check("geometry", bool(width and height), f"{width}x{height}"))
    fps_raw = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/0"
    try:
        num, den = fps_raw.split("/")
        fps = float(num) / float(den) if float(den) else 0
    except ValueError:
        fps = 0
    checks.append(check("fps_30", 29.5 <= fps <= 30.5, f"fps={fps:.3f}", "warn"))
    if min_seconds is not None:
        checks.append(check("duration_min", duration >= min_seconds - 0.05, f"{duration:.2f}s >= {min_seconds}s"))
    if max_seconds is not None:
        checks.append(check("duration_max", duration <= max_seconds + 0.05, f"{duration:.2f}s <= {max_seconds}s"))
    if audio is None:
        checks.append(check("audio_stream", allow_silent, "no audio stream", "warn" if allow_silent else "fail"))
    else:
        checks.append(check("audio_aac", audio.get("codec_name") == "aac", f"codec={audio.get('codec_name')}"))
    code, err = ffmpeg_stderr(["-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"])
    checks.append(check("full_decode", code == 0, err.strip()[-300:] or "decoded without errors"))
    code, err = ffmpeg_stderr(["-v", "info", "-i", str(path), "-an", "-vf", "blackdetect=d=0.1:pix_th=0.10", "-f", "null", "-"])
    black_start = re.search(r"black_start:\s*([0-9.]+)", err)
    opens_black = bool(black_start) and float(black_start.group(1)) < 0.05
    checks.append(check("no_black_opening", not opens_black, "opening frames are black" if opens_black else "opening is not black"))
    if audio is not None:
        code, err = ffmpeg_stderr(["-v", "info", "-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"])
        mean = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", err)
        peak = re.search(r"max_volume:\s*(-?[0-9.]+) dB", err)
        mean_db = float(mean.group(1)) if mean else -math.inf
        peak_db = float(peak.group(1)) if peak else -math.inf
        checks.append(check("audio_not_silent", mean_db > -50, f"mean_volume={mean_db:.1f} dB", "warn" if allow_silent else "fail"))
        checks.append(check("audio_not_clipping", peak_db < -0.3, f"max_volume={peak_db:.1f} dB", "warn"))
    return checks, duration


def main():
    parser = argparse.ArgumentParser(description="Technical QC of a rendered MP4 (does not approve creative or truth).")
    parser.add_argument("render", type=Path)
    parser.add_argument("--format", choices=sorted(FORMATS))
    parser.add_argument("--min-seconds", type=float)
    parser.add_argument("--max-seconds", type=float)
    parser.add_argument("--allow-silent", action="store_true")
    parser.add_argument("--template", help="OSDR editorial template from templates/osdr-formats.json (sets format and duration window)")
    parser.add_argument("--out", type=Path, help="write JSON report (must not exist)")
    args = parser.parse_args()
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            parser.exit(2, f"missing dependency: {binary}\n")
    if not args.render.is_file():
        parser.exit(1, "render not found\n")
    if args.out and (args.out.exists() or args.out.is_symlink()):
        parser.exit(1, "report already exists; choose a new version\n")
    template = None
    if args.template:
        try:
            template = load_template(args.template)
        except (OSError, ValueError, KeyError) as exc:
            parser.exit(2, f"{exc}\n")
        args.format = args.format or template["format"]
        args.min_seconds = args.min_seconds if args.min_seconds is not None else template["min_seconds"]
        args.max_seconds = args.max_seconds if args.max_seconds is not None else template["max_seconds"]
    try:
        checks, duration = technical_qc(args.render, args.format, args.min_seconds, args.max_seconds, args.allow_silent)
    except (subprocess.SubprocessError, ValueError, KeyError, OSError) as exc:
        parser.exit(1, f"qc failed to run: {exc}\n")
    failed = [c for c in checks if c["status"] == "fail"]
    report = {"render": args.render.name, "sha256": sha256_file(args.render), "duration_seconds": round(duration, 3),
              "technical_verdict": "fail" if failed else "pass", "checks": checks,
              "template": args.template, "creative_qc": "pending_human", "truth_qc": "pending_human", "human_approval": "required"}
    if template:
        report["house_style_reminders"] = [
            f"gancho: comida, produto ou movimento nos primeiros {template['hook_window_seconds']}s (conferir no contact sheet)",
            "legenda dinâmica obrigatória" if template["caption_required"] else "legenda opcional neste template",
            "som de produto em pelo menos um momento; fechamento sem 'siga, curta, compartilhe'",
        ]
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as handle:
            handle.write(text)
    print(text)
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
