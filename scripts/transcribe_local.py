#!/usr/bin/env python3
"""Optional faster-whisper adapter. Models must already exist locally."""
import argparse
import json
from pathlib import Path
from media_probe import sha256_file


def transcribe(source, model_path, model_factory, language="pt"):
    model = model_factory(str(model_path), device="cpu", compute_type="int8", local_files_only=True)
    segments, info = model.transcribe(str(source), language=language, word_timestamps=True, vad_filter=True)
    return {"source": source.name, "source_sha256": sha256_file(source),
            "language": info.language, "review_required": True,
            "segments": [{"start": s.start, "end": s.end, "text": s.text,
                          "words": [{"start": w.start, "end": w.end, "word": w.word}
                                    for w in (s.words or [])]} for s in segments]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not args.source.is_file() or not args.model_dir.is_dir():
        parser.error("source and local model directory must exist; no automatic download")
    if args.out.exists() or args.out.is_symlink() or args.out.resolve() == args.source.resolve():
        parser.error("output already exists or equals source")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        parser.error("optional dependency missing: faster-whisper")
    result = transcribe(args.source, args.model_dir, WhisperModel)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
