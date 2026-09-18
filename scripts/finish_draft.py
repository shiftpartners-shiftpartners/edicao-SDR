#!/usr/bin/env python3
"""Draft finishing for review: burn caption blocks from the EDP and mix a voice-over.

This is the "rascunho de acabamento": it makes a cut watchable (captions in place,
voice-over over the product sound, loudness normalised) so a human can judge the
piece on a phone. It does not replace the final finishing in the editor (music bed,
brand font, logo) and it never overwrites: the output must not exist.

Captions come from `text_overlay` of each EDP clip (one block per clip). A block
with " · " is split into two lines. Blocks containing a dash are refused (OSDR
caption standard). Timing is derived from the clip durations in the EDP, so the
render must have been produced from the same EDP.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import yaml

FORBIDDEN = {"—": "travessão proibido no padrão de legenda", "–": "meia-risca; usar vírgula ou ponto"}

STYLE_TEXT = "Legenda,{font},74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,3,2,90,90,{margin},1"
STYLE_CTA = "CTA,{font},66,&H0000E5FF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,3,2,70,70,{margin},1"
LOUDNORM = "loudnorm=I=-14:TP=-1.5:LRA=11"


def parse_ts(value):
    hours, minutes, seconds = str(value).split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int(seconds % 3600 // 60)
    return f"{hours}:{minutes:02d}:{seconds % 60:05.2f}"


def caption_events(edp):
    """Return (start, end, style, text) for every EDP clip with text_overlay."""
    events, cursor = [], 0.0
    for clip in sorted(edp["timeline"], key=lambda c: c["order"]):
        duration = parse_ts(clip["out"]) - parse_ts(clip["in"])
        text = (clip.get("text_overlay") or "").strip()
        if text:
            for char, why in FORBIDDEN.items():
                if char in text:
                    raise ValueError(f"legenda do trecho {clip['order']}: {why}")
            style = "CTA" if ("R$" in text or "Comenta" in text) else "Legenda"
            events.append((cursor, cursor + duration, style, text.replace(" · ", "\\N")))
        cursor += duration
    return events, cursor


def build_ass(events, width=1080, height=1920, font="DejaVu Sans", margin=470):
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {width}", f"PlayResY: {height}", "WrapStyle: 0", "",
             "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
             "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
             "MarginR, MarginV, Encoding",
             "Style: " + STYLE_TEXT.format(font=font, margin=margin),
             "Style: " + STYLE_CTA.format(font=font, margin=margin),
             "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for start, end, style, text in events:
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}")
    return "\n".join(lines) + "\n"


def ffmpeg_command(render, out, ass_path, total, vo=None, vo_delay_ms=300, bed_gain=0.35, loudnorm=True, fontsdir=None):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n", "-i", str(render)]
    audio_chain = f"[0:a]volume={bed_gain}[bed]" if vo else "[0:a]anull[mix]"
    if vo:
        cmd += ["-i", str(vo)]
        audio_chain += (f";[1:a]adelay={vo_delay_ms}|{vo_delay_ms},volume=1.0[vo];"
                        "[bed][vo]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix]")
    audio_chain += f";[mix]{LOUDNORM}[a]" if loudnorm else ";[mix]anull[a]"
    sub = f"subtitles={ass_path}" + (f":fontsdir={fontsdir}" if fontsdir else "")
    video_chain = f"[0:v]{sub}[v]" if ass_path else "[0:v]null[v]"
    cmd += ["-filter_complex", f"{audio_chain};{video_chain}", "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
            "-t", f"{total:.3f}", str(out)]
    return cmd


def main():
    parser = argparse.ArgumentParser(description="Burn EDP captions and mix a voice-over into a rendered cut (draft only).")
    parser.add_argument("edp", type=Path)
    parser.add_argument("render", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="output MP4 (must not exist)")
    parser.add_argument("--vo", type=Path, help="voice-over audio file (mp3/wav)")
    parser.add_argument("--vo-delay-ms", type=int, default=300)
    parser.add_argument("--bed-gain", type=float, default=0.35, help="product-sound level under the voice-over")
    parser.add_argument("--no-loudnorm", action="store_true", help="skip EBU R128 normalisation to -14 LUFS")
    parser.add_argument("--no-captions", action="store_true")
    parser.add_argument("--font", default="DejaVu Sans")
    parser.add_argument("--fontsdir")
    parser.add_argument("--dry-run", action="store_true", help="write the .ass and print the command only")
    args = parser.parse_args()
    if args.out.exists():
        sys.exit(f"recusado: {args.out} já existe (nunca sobrescrever)")
    if args.vo and not args.vo.exists():
        sys.exit(f"locução não encontrada: {args.vo}")
    edp = yaml.safe_load(args.edp.read_text(encoding="utf-8"))
    try:
        events, total = caption_events(edp)
    except ValueError as exc:
        sys.exit(f"recusado: {exc}")
    ass_path = None
    if not args.no_captions and events:
        ass_path = args.out.with_suffix(".ass")
        if ass_path.exists():
            sys.exit(f"recusado: {ass_path} já existe")
        ass_path.write_text(build_ass(events, font=args.font), encoding="utf-8")
    cmd = ffmpeg_command(args.render, args.out, ass_path, total, vo=args.vo, vo_delay_ms=args.vo_delay_ms,
                         bed_gain=args.bed_gain, loudnorm=not args.no_loudnorm, fontsdir=args.fontsdir)
    if args.dry_run:
        print(" ".join(cmd))
        return
    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    print(f"{args.out} ({args.out.stat().st_size} bytes); legendas: {ass_path.name if ass_path else 'nenhuma'}; "
          f"blocos: {len(events)}; duração: {total:.2f}s")


if __name__ == "__main__":
    main()
