#!/usr/bin/env python3
"""Upscale a low-resolution source clip 2x with the Real-ESRGAN x2plus weights (pure torch).

Why pure torch: the `basicsr`/`realesrgan` packages do not build against current torch on
every machine, so the RRDBNet architecture is reproduced here (same layer names as
xinntao/Real-ESRGAN, BSD-3-Clause) and only the weights file is needed:
RealESRGAN_x2plus.pth from the Real-ESRGAN release v0.2.1 (weights have their own terms).

Requirements: torch, PyAV, numpy, Pillow, ffmpeg on PATH. CPU is enough (about 1 to 3 s per
480p frame). Never overwrites: the output must not exist. The original stays untouched; the
result is a sibling `<name>.esrgan2x.mp4` (or `<name>.esrgan2x.<start>-<end>.mp4` for a range)
to be referenced by the EDP like any other source.

Usage:
  python tools/upscale_realesrgan.py media/source/clip.mp4 --weights RealESRGAN_x2plus.pth
  python tools/upscale_realesrgan.py media/source/clip.mp4 --weights W.pth --start 4 --duration 3
"""
import argparse
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def build_model(torch):
    import torch.nn as nn
    import torch.nn.functional as F

    class ResidualDenseBlock(nn.Module):
        def __init__(self, num_feat=64, num_grow_ch=32):
            super().__init__()
            self.conv1 = nn.Conv2d(num_feat, num_grow_ch, 3, 1, 1)
            self.conv2 = nn.Conv2d(num_feat + num_grow_ch, num_grow_ch, 3, 1, 1)
            self.conv3 = nn.Conv2d(num_feat + 2 * num_grow_ch, num_grow_ch, 3, 1, 1)
            self.conv4 = nn.Conv2d(num_feat + 3 * num_grow_ch, num_grow_ch, 3, 1, 1)
            self.conv5 = nn.Conv2d(num_feat + 4 * num_grow_ch, num_feat, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

        def forward(self, x):
            x1 = self.lrelu(self.conv1(x))
            x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
            x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
            x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
            x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
            return x5 * 0.2 + x

    class RRDB(nn.Module):
        def __init__(self, num_feat, num_grow_ch=32):
            super().__init__()
            self.rdb1 = ResidualDenseBlock(num_feat, num_grow_ch)
            self.rdb2 = ResidualDenseBlock(num_feat, num_grow_ch)
            self.rdb3 = ResidualDenseBlock(num_feat, num_grow_ch)

        def forward(self, x):
            out = self.rdb3(self.rdb2(self.rdb1(x)))
            return out * 0.2 + x

    class RRDBNet(nn.Module):
        def __init__(self, num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32):
            super().__init__()
            self.conv_first = nn.Conv2d(num_in_ch * 4, num_feat, 3, 1, 1)  # scale 2: pixel-unshuffle input
            self.body = nn.Sequential(*[RRDB(num_feat, num_grow_ch) for _ in range(num_block)])
            self.conv_body = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
            self.conv_up1 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
            self.conv_up2 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
            self.conv_hr = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
            self.conv_last = nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

        def forward(self, x):
            feat = F.pixel_unshuffle(x, 2)
            feat = self.conv_first(feat)
            feat = feat + self.conv_body(self.body(feat))
            feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode="nearest")))
            feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode="nearest")))
            return self.conv_last(self.lrelu(self.conv_hr(feat)))

    return RRDBNet()


def main():
    parser = argparse.ArgumentParser(description="Real-ESRGAN x2 upscale of one clip (pure torch, CPU ok).")
    parser.add_argument("source", type=Path)
    parser.add_argument("--weights", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--start", type=float, default=0.0, help="seconds; skip frames before this time")
    parser.add_argument("--duration", type=float, default=0.0, help="seconds; 0 = until the end")
    parser.add_argument("--max-frames", type=int, default=0, help="debug: stop after N frames")
    parser.add_argument("--threads", type=int, default=0, help="torch CPU threads (0 = default)")
    args = parser.parse_args()
    suffix = ".esrgan2x" + (f".{args.start:g}-{args.start + args.duration:g}" if args.duration else "") + ".mp4"
    out = args.out or args.source.with_name(args.source.stem + suffix)
    if out.exists():
        sys.exit(f"recusado: {out} já existe")
    if not args.weights.exists():
        sys.exit(f"pesos não encontrados: {args.weights}")
    try:
        import av
        import numpy as np
        import torch
        from PIL import Image
    except ImportError as exc:
        sys.exit(f"dependência ausente ({exc}); instale torch, av, numpy, pillow")
    if args.threads:
        torch.set_num_threads(args.threads)
    model = build_model(torch)
    state = torch.load(str(args.weights), map_location="cpu")
    state = state.get("params_ema", state.get("params", state))
    model.load_state_dict(state, strict=True)
    model.eval()
    container = av.open(str(args.source))
    stream = container.streams.video[0]
    fps = float(stream.average_rate or 30)
    started = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        frames_dir = Path(tmp)
        count = 0
        for frame in container.decode(stream):
            t = float(frame.pts * stream.time_base) if frame.pts is not None else count / fps
            if t < args.start:
                continue
            if args.duration and t >= args.start + args.duration:
                break
            img = frame.to_ndarray(format="rgb24").astype(np.float32) / 255.0
            tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)
            with torch.no_grad():
                output = model(tensor).clamp_(0, 1)
            arr = (output.squeeze(0).permute(1, 2, 0).numpy() * 255.0).round().astype(np.uint8)
            Image.fromarray(arr).save(frames_dir / f"{count:06d}.png")
            count += 1
            if count % 25 == 0:
                print(f"  {count} quadros, {(time.time() - started) / count:.2f} s/quadro", flush=True)
            if args.max_frames and count >= args.max_frames:
                break
        if not count:
            sys.exit("nenhum quadro na faixa pedida")
        cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n", "-framerate", f"{fps:.3f}",
               "-i", str(frames_dir / "%06d.png"), "-ss", f"{args.start:.3f}", "-i", str(args.source),
               "-map", "0:v:0", "-map", "1:a:0?", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)]
        subprocess.run(cmd, check=True)
    print(f"{out} ({count} quadros, {fps:.2f} fps, {(time.time() - started) / 60:.1f} min)")


if __name__ == "__main__":
    main()
