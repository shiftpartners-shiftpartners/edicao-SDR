#!/usr/bin/env python3
"""Segment speech into short caption blocks (OSDR standard: 3-5 words per block).

Input: a transcript JSON from scripts/transcribe_local.py (word timestamps) or a
plain text file. Output: JSON blocks and, when timestamps exist, an SRT file to
import in the editor (CapCut, Kdenlive, Premiere). The renderer v1 does not
burn captions; this tool prepares them for human finishing and review.
"""
import argparse
import json
import re
from pathlib import Path

BREAK_AFTER = re.compile(r"[.!?…]$")
SOFT_BREAK_AFTER = re.compile(r"[,;:]$")
FORBIDDEN = {"—": "travessão proibido no padrão OSDR", "–": "meia-risca; usar vírgula ou ponto"}


def segment_words(words, min_words=3, max_words=5):
    """words: list of dicts {word, start?, end?}. Returns list of blocks."""
    blocks, current = [], []

    def flush():
        if current:
            blocks.append({"text": " ".join(w["word"].strip() for w in current),
                           "start": current[0].get("start"), "end": current[-1].get("end"),
                           "words": len(current)})
            current.clear()

    for word in words:
        token = word["word"].strip()
        if not token:
            continue
        current.append(word)
        if BREAK_AFTER.search(token) and len(current) >= min(2, min_words):
            flush()
        elif len(current) >= max_words:
            flush()
        elif SOFT_BREAK_AFTER.search(token) and len(current) >= min_words:
            flush()
    flush()
    # merge a trailing orphan (1 word) into the previous block when possible
    if len(blocks) >= 2 and blocks[-1]["words"] == 1 and blocks[-2]["words"] < max_words:
        last = blocks.pop()
        blocks[-1]["text"] += " " + last["text"]
        blocks[-1]["end"] = last["end"] if last["end"] is not None else blocks[-1]["end"]
        blocks[-1]["words"] += 1
    return blocks


def lint(blocks):
    issues = []
    for i, block in enumerate(blocks, 1):
        for char, why in FORBIDDEN.items():
            if char in block["text"]:
                issues.append({"block": i, "issue": why})
        if block["words"] > 5:
            issues.append({"block": i, "issue": "mais de 5 palavras"})
        if block["start"] is not None and block["end"] is not None and block["end"] - block["start"] > 3.5:
            issues.append({"block": i, "issue": "bloco fica mais de 3,5s na tela; revisar sincronia"})
    return issues


def srt_time(seconds):
    millis = int(round(seconds * 1000))
    h, rem = divmod(millis, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def to_srt(blocks):
    lines = []
    for i, block in enumerate(blocks, 1):
        if block["start"] is None or block["end"] is None:
            raise ValueError("SRT requires timestamps on every block")
        lines += [str(i), f"{srt_time(block['start'])} --> {srt_time(block['end'])}", block["text"], ""]
    return "\n".join(lines)


def words_from_input(path):
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        words = []
        for segment in data.get("segments", []):
            if segment.get("words"):
                words.extend({"word": w["word"], "start": w.get("start"), "end": w.get("end")} for w in segment["words"])
            else:
                words.extend({"word": w, "start": None, "end": None} for w in segment.get("text", "").split())
        return words
    return [{"word": w, "start": None, "end": None} for w in path.read_text(encoding="utf-8").split()]


def main():
    parser = argparse.ArgumentParser(description="Segment speech into 3-5 word caption blocks (OSDR standard).")
    parser.add_argument("source", type=Path, help="transcript JSON (with words) or plain .txt")
    parser.add_argument("--out", type=Path, required=True, help="JSON blocks output (must not exist)")
    parser.add_argument("--srt", type=Path, help="optional SRT output (requires timestamps)")
    parser.add_argument("--max-words", type=int, default=5)
    args = parser.parse_args()
    for target in (args.out, args.srt):
        if target and (target.exists() or target.is_symlink()):
            parser.exit(1, f"output already exists: {target}\n")
    try:
        blocks = segment_words(words_from_input(args.source), max_words=args.max_words)
        issues = lint(blocks)
        payload = {"source": args.source.name, "blocks": blocks, "issues": issues, "review_required": True}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        if args.srt:
            args.srt.parent.mkdir(parents=True, exist_ok=True)
            with args.srt.open("x", encoding="utf-8") as handle:
                handle.write(to_srt(blocks))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(1, f"caption segmentation failed: {exc}\n")
    print(json.dumps({"blocks": len(blocks), "issues": issues}, ensure_ascii=False))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
