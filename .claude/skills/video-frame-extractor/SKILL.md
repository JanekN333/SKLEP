---
name: video-frame-extractor
description: Extract every distinct beat (key frame) from a short-form video — a competitor's TikTok, Instagram Reel, YouTube Short or a local .mp4 — as numbered full-res PNGs, a labelled contact sheet and frames.json timing data, then describe the reel's structure (hook, product reveal, demo, close-ups, CTA). Use when the user drops a reel and says "extract all the images/frames", "break down this reel", "get the start frames", or before running reel-replicate.
---

# Video frame extractor

Turns a short video into a clean, numbered set of the **distinct shots/poses ("beats")** so they can be
reviewed, picked by number and replicated (see the `reel-replicate` skill). Talk to the user in their language.

## 1. Get the video
- **Attached file** → use it directly.
- **Link (TikTok / Instagram / YouTube)** → `pip install -q "yt-dlp[default]"` then
  `yt-dlp -f "bv*+ba/b" --merge-output-format mp4 -o reel.mp4 "<url>"` (YouTube may also need `--js-runtimes node`).
  If the site asks for login / bot check, do **not** try to get around it: ask the user to download the reel
  themselves (e.g. snapinsta.to for Instagram, any TikTok downloader) and drop the .mp4 in the chat.
- Needs `ffmpeg` + Pillow (`pip install -q pillow` if missing).

## 2. Extract
Keep a task list ("Updated tasks…") so the user sees progress: get video → extract → verify coverage → report.

```bash
python3 <skill_dir>/scripts/extract_frames.py reel.mp4 --out frames_<name>
```
What the script does: ffmpeg scene detection → one frame just after every cut, min gap 0.45 s → drops
near-identical neighbours (perceptual hash) → splits any beat longer than 2.5 s so slow pose changes are kept →
always includes the first and the last frame. Outputs `frame_01.png…`, `frames.json`
(`index, time, end, duration` per frame) and `contact_sheet.png` (4 columns, white bar with `N  T.Ts` above each frame).

Tuning: too few frames → `--threshold 0.18 --max-gap 1.5`; too many → `--threshold 0.35 --dedupe 18`.

## 3. Verify coverage (always — look at the images yourself)
Open `contact_sheet.png` (and single frames when needed) and check:
- first (0.0 s) and last frame present;
- every distinct action of the reel got its own frame (e.g. the hook reaction, an object being dropped,
  the whip-pan, the product on the shelf/rack, each step of the demo, each close-up, the CTA);
- no shot is missing between two frames — if one is, re-run with lower `--threshold`/`--max-gap`, or grab it with
  `ffmpeg -ss <t> -i reel.mp4 -frames:v 1 frames_<name>/frame_XXb.png` and renumber.
Remove pure duplicates; keep near-duplicates only if the pose changes (say so).

## 4. Report (format the user expects)
Short, like:
> Coverage checks out — first (0.0s) and last (13.2s) frames present, the in-store rack shots (4–5) survived,
> and each cat-emerging beat got its own frame.
>
> All 15 distinct beats extracted. Structure: shocked hook in-store (1–3, incl. cup-drop), whip-pan to the product
> on the rack (4–5), "it's a cat carrier hoodie" demo (6–9), close-ups of the cat popping out (10–13),
> "Comment Hoodie" CTA (14–15). The `frames.json` timing data is saved too, so each shot's duration is ready
> if you want to animate replicas to match.
>
> A couple of pairs are near-duplicates by design (8/9, 14/15) — I kept them since the pose shifts slightly.
>
> Want me to run these through **reel-replicate** next — swap in your product, background, and avatar?
> If so, tell me which frame numbers to use (or skip) and what to swap in.

Then present the files: **Contact sheet (PNG)** first, then **Frame 01 … Frame NN (PNG)**, then `frames.json`
(in Claude.ai/desktop: save to the outputs folder so each shows as a downloadable file).
Also note any on-screen text overlay (hook text, CTA) — reel-replicate needs it.

## Notes
- The frame numbers you report are the IDs the user will use later ("do all frames except 4, 7, 8, 12, 15").
  Never renumber after reporting.
- Keep `frames.json`: reel-replicate uses `duration` to set clip lengths.
