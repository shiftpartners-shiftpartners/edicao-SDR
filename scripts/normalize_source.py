#!/usr/bin/env python3
"""Make a WhatsApp/phone clip decodable by the FFmpeg filter graph without touching the original.

Some phone exports carry an invalid colour-range flag in the H.264 stream; FFmpeg then
refuses every filter ("Invalid color range"). This tool checks a clip by decoding one
frame through a scale filter and, when that fails (or with --force), writes a sibling
`<name>.rangefix.mp4` produced by a metadata-only remux (no re-encode, pixels untouched).
The original file is never modified or deleted.
"""
import argparse
import subprocess
import sys
from pathlib import Path

BSF = "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"


def decodes_through_filters(path):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(path), "-frames:v", "1",
           "-vf", "scale=64:-2", "-f", "null", "-"]
    return subprocess.run(cmd, capture_output=True, text=True).returncode == 0


def fixed_name(path):
    return path.with_name(path.stem + ".rangefix" + path.suffix)


def remux_fixed(path, target):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n", "-i", str(path), "-c", "copy",
           "-bsf:v", BSF, "-map_metadata", "-1", str(target)]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Check phone clips for the invalid-colour-range problem and write a fixed sibling.")
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--force", action="store_true", help="write the fixed sibling even when the clip decodes")
    parser.add_argument("--check", action="store_true", help="only report; never write")
    args = parser.parse_args()
    problems = 0
    for src in args.sources:
        if not src.exists() or src.suffix.lower() not in {".mp4", ".mov", ".m4v"}:
            print(f"ignorado: {src}")
            continue
        ok = decodes_through_filters(src)
        target = fixed_name(src)
        if ok and not args.force:
            print(f"ok: {src.name} decodifica normalmente")
            continue
        problems += 1
        if args.check:
            print(f"PROBLEMA: {src.name} não passa pelo filtro; rode sem --check para gerar {target.name}")
            continue
        if target.exists():
            print(f"existe: {target.name} (não sobrescrevo)")
            continue
        remux_fixed(src, target)
        state = "ok" if decodes_through_filters(target) else "AINDA FALHA"
        print(f"gerado: {target.name} ({target.stat().st_size} bytes) decodificação após correção: {state}")
    sys.exit(1 if (args.check and problems) else 0)


if __name__ == "__main__":
    main()
