#!/usr/bin/env python3
"""Convert an editorial Edit Decision Plan (YAML) into the executable render plan JSON v1.

The YAML EDP is a human document. The JSON plan is the bounded contract that
scripts/render_plan.py executes. This converter only carries what the renderer
supports (ordered clips with in/out) and refuses to silently drop crop, text
overlays or other finishing instructions unless --unsupported=report is given,
in which case they are listed for a human editor instead of being executed.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependency documented in requirements.txt
    yaml = None

FORMATS = {"9:16", "4:5", "1:1", "16:9"}
TIMESTAMP = re.compile(r"^(?:(\d{1,2}):)?(\d{1,2}):(\d{1,2})(?:[.,](\d{1,3}))?$")
UNSUPPORTED_FIELDS = ("crop", "text_overlay", "transition", "audio", "music", "speed", "overlay")


def parse_timestamp(value):
    """Accept seconds (number) or HH:MM:SS.mmm / MM:SS.mmm strings."""
    if isinstance(value, bool):
        raise ValueError(f"invalid timestamp: {value!r}")
    if isinstance(value, (int, float)):
        if value < 0:
            raise ValueError(f"negative timestamp: {value}")
        return float(value)
    if not isinstance(value, str):
        raise ValueError(f"invalid timestamp: {value!r}")
    match = TIMESTAMP.match(value.strip())
    if not match:
        raise ValueError(f"invalid timestamp: {value!r}")
    hours, minutes, seconds, millis = match.groups()
    total = int(hours or 0) * 3600 + int(minutes) * 60 + int(seconds)
    if millis:
        total += int(millis.ljust(3, "0")) / 1000
    return float(total)


def convert(edp):
    if not isinstance(edp, dict):
        raise ValueError("EDP must be a mapping")
    output = edp.get("output") or {}
    fmt = output.get("format")
    if fmt not in FORMATS:
        raise ValueError(f"output.format must be one of {sorted(FORMATS)}")
    timeline = edp.get("timeline")
    if not isinstance(timeline, list) or not timeline:
        raise ValueError("timeline must be a non-empty list")
    known_sources = {Path(s.get("path", "")).name for s in edp.get("source_files", []) if isinstance(s, dict)}
    clips = []
    unsupported = []
    for entry in sorted(timeline, key=lambda e: e.get("order", 0) if isinstance(e, dict) else 0):
        if not isinstance(entry, dict):
            raise ValueError("timeline entries must be mappings")
        source = entry.get("source")
        if not isinstance(source, str) or not source or Path(source).name != source:
            raise ValueError("timeline.source must be a bare filename inside the source root")
        if known_sources and source not in known_sources:
            raise ValueError(f"timeline source not declared in source_files: {source}")
        start = parse_timestamp(entry.get("in"))
        end = parse_timestamp(entry.get("out"))
        if end <= start:
            raise ValueError(f"clip out must be after in: {source} {start}-{end}")
        for field in UNSUPPORTED_FIELDS:
            value = entry.get(field)
            if value not in (None, "", [], {}):
                unsupported.append({"order": entry.get("order"), "field": field, "value": value})
        clips.append({"source": source, "in": start, "out": end})
    plan = {"version": 1, "format": fmt, "clips": clips}
    return plan, unsupported


def main():
    parser = argparse.ArgumentParser(description="Convert YAML EDP into render plan JSON v1.")
    parser.add_argument("edp", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--unsupported", choices=["reject", "report"], default="reject",
                        help="reject: fail if the EDP asks for crop/text/transitions; report: list them for manual finishing")
    args = parser.parse_args()
    if yaml is None:
        parser.exit(2, "missing dependency: PyYAML (see requirements.txt)\n")
    if args.out.exists() or args.out.is_symlink():
        parser.exit(1, "output already exists; choose a new version\n")
    try:
        edp = yaml.safe_load(args.edp.read_text(encoding="utf-8"))
        plan, unsupported = convert(edp)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        parser.exit(1, f"conversion failed: {exc}\n")
    if unsupported and args.unsupported == "reject":
        for item in unsupported:
            print(f"unsupported in render v1: order={item['order']} {item['field']}={item['value']!r}", file=sys.stderr)
        parser.exit(1, "EDP asks for finishing the renderer cannot execute; use --unsupported=report or a human editor\n")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2, ensure_ascii=False)
    print(args.out)
    if unsupported:
        print("manual finishing required (not rendered):", file=sys.stderr)
        for item in unsupported:
            print(f"  order={item['order']} {item['field']}={item['value']!r}", file=sys.stderr)


if __name__ == "__main__":
    main()
