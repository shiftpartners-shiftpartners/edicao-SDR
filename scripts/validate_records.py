#!/usr/bin/env python3
"""Strict JSON Schema validation plus bounded operational invariants."""
import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

def reject_constant(value):
    raise ValueError(f"non-finite JSON number: {value}")

def strict_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("non-finite JSON number")
    return number

def load_records(path):
    text = path.read_text(encoding="utf-8")
    rows = [(n, json.loads(raw, parse_constant=reject_constant, parse_float=strict_float))
            for n, raw in enumerate(text.splitlines(), 1) if raw.strip()] if path.suffix == ".jsonl" else [
                (1, json.loads(text, parse_constant=reject_constant, parse_float=strict_float))]
    if not rows:
        raise ValueError("empty record file")
    return rows

def operational_errors(record):
    errors = []
    if record.get("status") in {"approved", "observing", "decided"} and record.get("human_approval") != "approved":
        errors.append("active creative requires human approval")
    if "window_start" in record and "window_end" in record:
        try:
            start = datetime.fromisoformat(record["window_start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(record["window_end"].replace("Z", "+00:00"))
            if start.tzinfo is None or end.tzinfo is None or end <= start:
                errors.append("window_end must follow window_start; timezone offsets required")
            zone = ZoneInfo(record["timezone"])
            for point in (start, end):
                if point.utcoffset() != point.astimezone(zone).utcoffset():
                    errors.append("timestamp offset disagrees with timezone")
        except (ValueError, TypeError, KeyError):
            errors.append("invalid date or IANA timezone")
    if record.get("decision") in {"scale", "iterate", "pause"}:
        metrics = record.get("metrics", {})
        if not record.get("objective") or not metrics.get("impressions") or metrics.get("spend") is None:
            errors.append("decision requires objective, spend and positive impressions")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        print("Install requirements.txt: full validation is mandatory", file=sys.stderr)
        return 2
    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        rows = load_records(args.records)
        seen = set()
        failures = 0
        for line, record in rows:
            errors = [error.message for error in validator.iter_errors(record)]
            if not errors:
                errors.extend(operational_errors(record))
                key = record.get("observation_id", record.get("creative_id"))
                if key in seen:
                    errors.append(f"duplicate identity: {key}")
                seen.add(key)
            for error in errors:
                print(f"line {line}: {error}", file=sys.stderr)
            failures += bool(errors)
        print(f"records: {len(rows)}, invalid: {failures}")
        return 1 if failures else 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
