#!/usr/bin/env python3
"""Stitch generated clips into one vertical reel.

Usage:
    python3 stitch_reel.py OUT.mp4 clip1.mp4[:SECONDS] clip2.mp4[:SECONDS] ... [--size 720x1280] [--fps 30]

`:SECONDS` trims a clip to its first N seconds (e.g. a 4 s Seedance clip used as a 2 s b-roll -> zip.mp4:2).
Every clip is scaled/cropped to the same size and fps; clips without audio get silence, so native
Seedance audio is kept where it exists.
"""
import argparse
import json
import subprocess
import sys


def has_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                          "stream=index", "-of", "json", path], capture_output=True, text=True).stdout
    return bool(json.loads(out or "{}").get("streams"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--size", default="720x1280")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    w, h = a.size.split("x")

    inputs, filters, labels = [], [], []
    for i, spec in enumerate(a.clips):
        path, trim = spec, ""
        if ":" in spec:
            path, trim = spec.rsplit(":", 1)
            try:
                float(trim)
            except ValueError:
                path, trim = spec, ""
        inputs += (["-t", trim] if trim else []) + ["-i", path]
        filters.append(f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
                       f"fps={a.fps},setsar=1,format=yuv420p[v{i}]")
        if has_audio(path):
            filters.append(f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo[a{i}]")
        else:
            dur = trim or subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
            filters.append(f"anullsrc=r=44100:cl=stereo,atrim=0:{dur}[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    filters.append("".join(labels) + f"concat=n={len(a.clips)}:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters),
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    print("OK", a.out)


if __name__ == "__main__":
    sys.exit(main())
