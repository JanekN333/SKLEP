#!/usr/bin/env python3
"""Extract the key frames (distinct beats) from a short-form video.

Usage:
    python3 extract_frames.py VIDEO [--out DIR] [--threshold 0.27] [--min-gap 0.45]
                              [--max-gap 2.5] [--dedupe 6] [--cols 4]

Writes into DIR (default: ./frames_<video-name>):
    frame_01.png ... frame_NN.png   full-resolution stills, in reel order
    frames.json                      timing data (start, end, duration of each beat)
    contact_sheet.png                grid with "N  T.Ts" label above each frame

Needs ffmpeg/ffprobe on PATH and Pillow.
"""
import argparse
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def probe(video):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=width,height,r_frame_rate:format=duration",
               "-of", "json", video]).stdout
    d = json.loads(out)
    s = d["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return float(d["format"]["duration"]), int(s["width"]), int(s["height"]), float(num) / float(den)


def scene_times(video, threshold):
    """Timestamps where ffmpeg's scene score exceeds the threshold."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video, "-vf",
         f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
        capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", proc.stderr)]


def grab(video, t, path):
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video,
         "-frames:v", "1", path])
    if not os.path.exists(path):  # seek past the last decodable frame -> take the final frame instead
        run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.5", "-i", video,
             "-update", "1", "-q:v", "1", path])


def ahash(path, size=16):
    img = Image.open(path).convert("L").resize((size, size), Image.LANCZOS)
    px = list(img.tobytes())
    avg = sum(px) / len(px)
    return [p > avg for p in px]


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def font(size):
    for f in ("/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def contact_sheet(frames, out_path, cols, thumb_w=360):
    first = Image.open(frames[0]["file_abs"])
    thumb_h = int(thumb_w * first.height / first.width)
    bar, pad = 34, 8
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (thumb_h + bar + pad) + pad), "white")
    draw, fnt = ImageDraw.Draw(sheet), font(22)
    for i, fr in enumerate(frames):
        r, c = divmod(i, cols)
        x, y = pad + c * (thumb_w + pad), pad + r * (thumb_h + bar + pad)
        draw.text((x + 4, y + 5), f"{fr['index']}  {fr['time']:.1f}s", fill="black", font=fnt)
        sheet.paste(Image.open(fr["file_abs"]).convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS), (x, y + bar))
    sheet.save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out")
    ap.add_argument("--threshold", type=float, default=0.27, help="scene-change sensitivity (lower = more frames)")
    ap.add_argument("--min-gap", type=float, default=0.45, help="min seconds between two kept frames")
    ap.add_argument("--max-gap", type=float, default=2.5, help="add a frame if a beat is longer than this")
    ap.add_argument("--dedupe", type=int, default=12, help="max 16x16 hash distance treated as duplicate (0 = off)")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--count", type=int, default=20,
                    help="exact number of frames to output (default 20, user rule); 0 = natural count")
    a = ap.parse_args()

    video = os.path.abspath(a.video)
    name = os.path.splitext(os.path.basename(video))[0]
    out = os.path.abspath(a.out or f"frames_{re.sub(r'[^A-Za-z0-9_-]+', '_', name)}")
    os.makedirs(out, exist_ok=True)
    duration, w, h, fps = probe(video)
    last_t = max(0.0, duration - 1.5 / fps)

    # 1) candidate cut points: start + scene changes (sampled just after the cut so the frame is clean)
    cands = sorted(set([0.0] + [min(t + 0.12, last_t) for t in scene_times(video, a.threshold)]))
    times = []
    for t in cands:  # enforce min gap between cuts
        if not times or t - times[-1] >= a.min_gap:
            times.append(t)

    # 2) grab cut frames, drop near-identical neighbours (never the first)
    kept, prev = [], None
    for k, t in enumerate(times):
        p = os.path.join(out, f"_cand_{k:03d}.png")
        grab(video, t, p)
        hsh = ahash(p)
        if a.dedupe and prev is not None and hamming(hsh, prev) <= a.dedupe:
            os.remove(p)
            continue
        kept.append((t, p))
        prev = hsh

    # 3) coverage: split beats longer than max-gap, and always include the last frame
    tmp = []
    bounds = [t for t, _ in kept] + [duration]
    for i, (t, p) in enumerate(kept):
        tmp.append((t, p))
        span = bounds[i + 1] - t
        n = int(span // a.max_gap)
        for j in range(1, n + 1):
            ft = t + span * j / (n + 1)
            fp = os.path.join(out, f"_fill_{i:03d}_{j}.png")
            grab(video, ft, fp)
            tmp.append((ft, fp))
    if last_t - tmp[-1][0] >= a.min_gap:
        lp = os.path.join(out, "_last.png")
        grab(video, last_t, lp)
        tmp.append((last_t, lp))

    # 4) fixed frame count (user rule: 20 beats per reel): split the longest beat until we reach --count,
    #    or drop the frame most similar to its predecessor (never first/last) while above it
    if a.count:
        k = 0
        while len(tmp) < a.count:
            bounds = [t for t, _ in tmp] + [duration]
            i = max(range(len(tmp)), key=lambda j: bounds[j + 1] - tmp[j][0])
            mid = (tmp[i][0] + bounds[i + 1]) / 2
            fp = os.path.join(out, f"_split_{k:03d}.png")
            k += 1
            grab(video, mid, fp)
            tmp.insert(i + 1, (mid, fp))
        while len(tmp) > a.count:
            hs = [ahash(p) for _, p in tmp]
            i = min(range(1, len(tmp) - 1), key=lambda j: hamming(hs[j], hs[j - 1]))
            os.remove(tmp[i][1])
            del tmp[i]

    frames = []
    for i, (t, p) in enumerate(tmp, 1):
        final = os.path.join(out, f"frame_{i:02d}.png")
        os.replace(p, final)
        end = tmp[i][0] if i < len(tmp) else duration
        frames.append({"index": i, "file": os.path.basename(final), "file_abs": final,
                       "time": round(t, 2), "end": round(end, 2), "duration": round(end - t, 2)})

    contact_sheet(frames, os.path.join(out, "contact_sheet.png"), a.cols)
    meta = {"video": os.path.basename(video), "duration": round(duration, 2), "width": w, "height": h,
            "fps": round(fps, 3), "frame_count": len(frames),
            "frames": [{k: v for k, v in f.items() if k != "file_abs"} for f in frames]}
    with open(os.path.join(out, "frames.json"), "w") as fh:
        json.dump(meta, fh, indent=2)

    # coverage report for the agent
    gaps = [f for f in frames if f["duration"] > a.max_gap + 0.01]
    print(f"OUT={out}")
    print(f"video {duration:.1f}s {w}x{h} -> {len(frames)} frames")
    print(f"first frame at {frames[0]['time']}s, last at {frames[-1]['time']}s")
    print("longest beats:", ", ".join(f"#{f['index']} {f['duration']}s" for f in sorted(frames, key=lambda f: -f["duration"])[:3]))
    if gaps:
        print("WARNING long beats (consider --max-gap lower):", [g["index"] for g in gaps])


if __name__ == "__main__":
    sys.exit(main())
