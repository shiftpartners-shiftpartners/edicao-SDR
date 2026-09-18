#!/usr/bin/env python3
"""Evenly sampled contact sheet with accurate per-frame seeks.

Frames are extracted one by one at exact timestamps (accurate seek) and tiled
afterwards. This avoids the missing/shifted tiles that the fps+tile filter
chain produced on concatenated renders with B-frames.
"""
import argparse
import math
import shutil
import subprocess
import tempfile
from pathlib import Path


def duration_seconds(path: Path) -> float:
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=60)
    return float(proc.stdout.strip())


def sample_times(duration: float, frames: int):
    """Midpoints of `frames` equal windows, so the last sample never hits EOF."""
    step = duration / frames
    return [round(step * (i + 0.5), 3) for i in range(frames)]


def extract_frame(source: Path, seconds: float, width: int, target: Path):
    cmd = [
        'ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
        '-ss', f'{seconds:.3f}', '-i', str(source), '-frames:v', '1', '-an',
        '-vf', f'scale={width}:-2:force_original_aspect_ratio=decrease', '-update', '1', str(target)
    ]
    subprocess.run(cmd, check=True, timeout=120)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f'no frame decoded at {seconds:.3f}s')


def build_sheet(source: Path, out: Path, frames: int, columns: int, width: int):
    duration = duration_seconds(source)
    if not math.isfinite(duration) or duration <= 0:
        raise RuntimeError('Could not determine a positive video duration')
    rows = math.ceil(frames / columns)
    with tempfile.TemporaryDirectory(prefix='contact-sheet-') as temp:
        temp = Path(temp)
        for index, seconds in enumerate(sample_times(duration, frames)):
            extract_frame(source, seconds, width, temp / f'{index:03d}.png')
        cmd = [
            'ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-n',
            '-framerate', '1', '-i', str(temp / '%03d.png'),
            '-vf', f'tile={columns}x{rows}:nb_frames={frames}:padding=4:margin=4',
            '-frames:v', '1', '-update', '1', str(out)
        ]
        subprocess.run(cmd, check=True, timeout=120)
    return duration


def main():
    parser = argparse.ArgumentParser(description='Create an evenly sampled contact sheet with FFmpeg.')
    parser.add_argument('input', help='Input video')
    parser.add_argument('--out', default='contact-sheet.png', help='Output PNG')
    parser.add_argument('--frames', type=int, default=12, help='Number of sampled frames')
    parser.add_argument('--columns', type=int, default=4, help='Tile columns')
    parser.add_argument('--width', type=int, default=320, help='Width of each tile')
    args = parser.parse_args()

    for binary in ('ffmpeg', 'ffprobe'):
        if not shutil.which(binary):
            raise SystemExit(f'{binary} was not found on PATH')

    source = Path(args.input).resolve()
    if not source.exists() or not source.is_file():
        raise SystemExit(f'Input video not found: {source}')
    if args.frames < 1 or args.columns < 1 or args.width < 64:
        raise SystemExit('frames and columns must be >= 1; width must be >= 64')

    out = Path(args.out)
    if out.resolve() == source or out.exists() or out.is_symlink():
        raise SystemExit('Output exists or equals source; choose a new path')
    if out.suffix.lower() != '.png':
        raise SystemExit('Output must be PNG')
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        build_sheet(source, out, args.frames, args.columns, args.width)
    except (subprocess.SubprocessError, RuntimeError, OSError) as exc:
        raise SystemExit(f'contact sheet failed: {exc}')
    print(out)


if __name__ == '__main__':
    main()
