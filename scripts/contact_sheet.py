#!/usr/bin/env python3
import argparse
import math
import shutil
import subprocess
from pathlib import Path


def duration_seconds(path: Path) -> float:
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=60)
    return float(proc.stdout.strip())


def main():
    parser = argparse.ArgumentParser(description='Create an evenly sampled contact sheet with FFmpeg.')
    parser.add_argument('input', help='Input video')
    parser.add_argument('--out', default='contact-sheet.png', help='Output PNG')
    parser.add_argument('--frames', type=int, default=12, help='Approximate number of sampled frames')
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

    duration = duration_seconds(source)
    if not math.isfinite(duration) or duration <= 0:
        raise SystemExit('Could not determine a positive video duration')

    rows = math.ceil(args.frames / args.columns)
    sample_fps = args.frames / duration
    vf = (
        f'fps={sample_fps:.8f},'
        f'scale={args.width}:-2:force_original_aspect_ratio=decrease,'
        f'tile={args.columns}x{rows}:nb_frames={args.frames}:padding=4:margin=4'
    )

    out = Path(args.out)
    if out.resolve() == source or out.exists() or out.is_symlink():
        raise SystemExit('Output exists or equals source; choose a new path')
    if out.suffix.lower() != '.png':
        raise SystemExit('Output must be PNG')
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(source),
        '-vf', vf, '-frames:v', '1', str(out)
    ]
    subprocess.run(cmd, check=True, timeout=120)
    print(out)


if __name__ == '__main__':
    main()
