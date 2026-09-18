#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

MEDIA_EXTENSIONS = {
    '.mp4', '.mov', '.mkv', '.webm', '.avi', '.m4v',
    '.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg',
    '.jpg', '.jpeg', '.png', '.webp'
}


def run_ffprobe(path: Path) -> dict:
    cmd = [
        'ffprobe', '-v', 'error', '-show_streams', '-show_format',
        '-of', 'json', str(path)
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=60)
    return json.loads(proc.stdout)


def rational_to_float(value):
    if not value or value in {'0/0', 'N/A'}:
        return None
    try:
        return round(float(Fraction(value)), 3)
    except Exception:
        return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def orientation(width, height):
    if not width or not height:
        return None
    if width == height:
        return 'square'
    return 'portrait' if height > width else 'landscape'


def safe_float(value):
    try:
        return round(float(value), 3)
    except (TypeError, ValueError):
        return None


def inspect_file(path: Path, root: Path, do_hash: bool) -> dict:
    probe = run_ffprobe(path)
    streams = probe.get('streams', [])
    fmt = probe.get('format', {})
    video = next((s for s in streams if s.get('codec_type') == 'video'), {})
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), {})
    width = video.get('width')
    height = video.get('height')
    duration = safe_float(fmt.get('duration')) or safe_float(video.get('duration')) or safe_float(audio.get('duration'))

    item = {
        'path': path.relative_to(root).as_posix(),
        'extension': path.suffix.lower(),
        'size_bytes': path.stat().st_size,
        'duration_seconds': duration,
        'video': {
            'codec': video.get('codec_name'),
            'width': width,
            'height': height,
            'orientation': orientation(width, height),
            'fps': rational_to_float(video.get('avg_frame_rate') or video.get('r_frame_rate')),
        } if video else None,
        'audio': {
            'codec': audio.get('codec_name'),
            'sample_rate': int(audio['sample_rate']) if audio.get('sample_rate', '').isdigit() else None,
            'channels': audio.get('channels'),
        } if audio else None,
    }
    if do_hash:
        item['sha256'] = sha256_file(path)
    return item


def main():
    parser = argparse.ArgumentParser(description='Inventory media files with ffprobe.')
    parser.add_argument('source', help='Source file or directory')
    parser.add_argument('--out', default='footage-index.json', help='Output JSON path')
    parser.add_argument('--hash', action='store_true', help='Compute SHA-256 for each file')
    args = parser.parse_args()

    if not shutil.which('ffprobe'):
        raise SystemExit('ffprobe was not found on PATH')

    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f'Source not found: {source}')

    if source.is_file():
        root = source.parent
        files = [source]
    else:
        root = source
        files = sorted(
            p for p in source.rglob('*')
            if p.is_file() and p.suffix.lower() in MEDIA_EXTENSIONS
        )

    out = Path(args.out).resolve()
    if out.exists() or out.is_symlink():
        raise SystemExit('Output already exists; choose a new version')
    if out == source or (source.is_dir() and out.is_relative_to(source)):
        raise SystemExit('Output must be outside source')
    if not files:
        raise SystemExit('No supported media files found')
    entries = []
    errors = []
    for path in files:
        try:
            entries.append(inspect_file(path, root, args.hash))
        except Exception as exc:
            errors.append({'path': path.relative_to(root).as_posix(), 'error': str(exc)})

    payload = {
        'version': 1,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_dir': str(root),
        'file_count': len(entries),
        'files': entries,
        'errors': errors,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf-8') as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    print(out)
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
