---
name: reel-replicate
description: Replicate a viral product reel beat-for-beat with the user's own avatar, product (or colour variant) and backgrounds — generates new start-frame images for every kept frame of the original (Higgsfield, Nano Banana Pro), lays everything out on a Miro board, then animates each shot (Seedance via Higgsfield) and stitches one finished vertical reel per background. Use after video-frame-extractor, or when the user says "replicate this reel", "swap it for my avatar/product/background", "do all the frames for background 1-5", "put them on my Miro board", "now generate all the videos".
---

# Reel replicate

Pipeline that turns the frames of a competitor reel into N new reels (one per background) featuring the
user's avatar and product. Talk to the user in their language. Keep a task list the whole time.

Requires the **Higgsfield** connector (custom connector URL `https://mcp.higgsfield.ai/mcp`) and, for the
board step, the **Miro** connector. ffmpeg for stitching. If a connector is missing, tell the user how to add it
(Settings → Connectors → Add custom connector → name + URL) and stop.

**Credits rule:** before every paid batch (images, re-rolls, videos) quote the cost (`get_cost: true` on one item ×
number of items) and wait for a yes. Never resubmit a job whose outcome is unknown — check its job ID first.

---

## Stage 0 — Inputs
Collect (ask only for what is missing):
1. **Original frames** — output of `video-frame-extractor` (`frame_NN.png`, `frames.json`, contact sheet).
   If the user only sent a video, run that skill first.
2. **Frames to skip** — e.g. "all frames except 4, 7, 8, 12, 15" (duplicates / unneeded).
3. **Avatar** image (person who replaces the original creator).
4. **Product / colour variant** image (what replaces the original product; pet/prop included if shown).
5. **Backgrounds** 1…N (rooms etc.). Each background = one set = one finished reel.
6. Optional: on-screen hook text / CTA to use, language of speech.

If the user has no avatar/backgrounds yet (or wants better ones than the competitor), run the
`reel-casting` skill first. If a `casting.json` exists, use its media_ids (avatar + extra angles,
backgrounds, store variants) directly and skip uploading those references.

Upload every reference to Higgsfield yourself: `media_upload` → PUT bytes with curl → `media_confirm`
(or `media_import_url` for web links). Keep a table `ref → media_id`.

## Stage 1 — Plan the sets
- Look at every kept frame and name its beat (e.g. 01 shocked hook, 02 cup drop, 03 whip pan, 05 product rack,
  06 cradling the pet, 09 zipping with pet's face in the hole, 10 peek close-up, 11 head out, 13 profile,
  14 seated petting). Keep the original frame numbers.
- Split beats into **store/hook beats** (the original retail location) and **room beats** (user's backgrounds).
- Retail hook beats: the user's backgrounds are usually rooms, so give each set its own believable store
  variant unless the user sent store photos — e.g. set 1 = original clothing store, 2 = superstore,
  3 = department store, 4 = boutique, 5 = pet-supply / category store. The product display in the store must be
  the user's product.
- Numbering: `set × 100 + frame` → 101, 102 … 205 … 514. Title format `S3-09 zip + dog in hole`.
- If a reference frame shows a beat the original only implies (e.g. pet climbing into the pouch, an extreme
  close-up), you may add it as `(new)` — say so.
- Tell the user: number of sets × beats = total images, model, cost estimate → wait for OK.

## Stage 2 — Generate start frames
Model: `nano_banana_pro` (or best image-edit model from `models_explore` if unavailable), `aspect_ratio: "9:16"`.
Per image pass as medias: the **original frame** (composition/pose/camera reference), the **avatar**, the
**product**, and the **background** (room beats) — check the model's media roles with `models_explore`.
Use `generate_image_batch` (≤12 per call, all sets in parallel), then `jobs_wait`, then ONE
`show_generation_by_ids` with all job IDs (≤60 per call).

Prompt skeleton (fill per beat — see `references/prompts.md`):
> Recreate the reference frame exactly — same camera angle, framing, lens, pose, hand positions, expression and
> action — but: the person is the woman from the avatar reference (identical face, hair, skin tone); she wears /
> holds the product from the product reference (identical colour, fabric, details, logo; true real-world size);
> the setting is [background reference / store variant]. Vertical 9:16 smartphone photo, natural light,
> realistic skin texture, no text, no watermark, correct finger count.

**Self-QA before showing** (open the results and look): same face as avatar in every set (spot-check at least
one hook + one room shot per set), product colour/details faithful, pet/prop present where the original has it
(e.g. pet's face *in* the hole, not an empty pouch), camera angle matches the original frame, no extra fingers,
no warped text. Re-roll failures yourself (one at a time, tell the user which and why) — if the miss is
systematic, fix the prompt for all sets.

Report like:
> All 60 frames are in the gallery above, no failures. Each set now has 12 beats, numbered by the last two
> digits: 01 shocked hook, 02 cup drop, 03 whip pan, 05 product rack — all in-store — then in the room: 06 …, 14 ….
> What I locked down this round: … Set guide: 100s = clothing store + city-view bedroom, 200s = superstore +
> mountain bedroom, …
> Go through the gallery — if any single frame is off, give me its number and I'll re-roll just that one.
> When you're happy, tell me which set(s) to animate and I'll match each clip's motion and duration to the original.

## Stage 3 — Miro board (always)
Board name: **AI Video Dropshipping** (find it with `board_search_boards`; create if missing; one project =
one new area/frame on it). Layout (see `references/miro-layout.md`):
- Row 0: the original reel's frames with their numbers + timing.
- One row per set (row label 1…N), beats left → right in reel order, each image titled `S{set}-{beat} {name}`.
- Under the rows: two columns **Hook 0-4sec** and **brolls 4-16 sec**, the hook prompt (from
  `references/prompts.md`, filled in) and one sticky per b-roll clip with action + length
  ("First B-roll Clip: … actual clip is 3–4sec").
Upload images via `image_get_upload_url`/`image_create` (or URL). Give the user the board link and say:
"remove frames you don't want, tweak the b-roll descriptions, then tell me to generate the videos".
Offer to rewrite their b-roll descriptions into stronger motion prompts.

## Stage 4 — Animate
Trigger: user says they've selected frames / "generate all the videos" (often with a screenshot of the board
and the original reel re-uploaded). Read the board (`canvas_read_as_svg` / `board_preview_read`) to get what
survived, the hook prompt and every b-roll note. Re-watch the original reel (frames.json durations) to match
pacing. Decide clip split per reel yourself:
- **Hook** = one continuous 4 s shot: start frame = shocked frame (01), end frame = product-rack frame (05),
  prompt = the hook template (gasp line → point → whip-pan with motion blur → payoff on the product display →
  hand grabs one). Native audio ON (gasp + store ambience only, no music/SFX).
- **B-rolls** = one clip per note, start frame = the matching kept frame, duration from the note
  (generate the model's minimum length and trim, e.g. 4 s → 2 s).
Model: **`seedance_2_5`** (user's choice; check durations/resolutions with `models_explore`). Draft 720p, 9:16,
audio on. Quote total cost first. Submit all sets with `generate_video_batch` (≤12 per call), `jobs_wait`,
one `show_generation_by_ids`.
- If a submission comes back with a **preset recommendation instead of a job**, decline it and resubmit the
  same direct request (say "N submissions got intercepted by a preset recommendation — declining and resubmitting").
- If a clip gets a **false content flag** (common with pets/kids), reword neutrally and regenerate that one.
- Frame-check at least the hook of set 1 (extract a few frames with ffmpeg): whip-pan lands on the rack,
  hand grabs the product, face stays the avatar.

## Stage 5 — Stitch & deliver
Download clips (`curl -L -o`), then per set:
```bash
python3 <skill_dir>/scripts/stitch_reel.py reel_set1.mp4 s1_hook.mp4 s1_b1.mp4:4 s1_b2.mp4:2 s1_b3.mp4:4 s1_b4.mp4:3
```
Deliver N stitched reels (~16–17 s, 720×1280) + individual clips, and a summary:
> All done — 25 clips generated with Seedance and delivered as 5 stitched reels (one per set, ~17s each, 720p 9:16
> with native audio). How each reel is built: hook = …; then the four b-rolls follow your notes: … (trimmed to 2s) …
> One hiccup handled: … If any single clip needs a re-roll (e.g. "set 3, zip clip") — just say so. I can also drop
> the reels or the individual clips onto your Miro board.
Optional: upscale/finalise chosen reels at 1080p (ask, costs credits); voice-over with ElevenLabs if asked.
Final edit (text overlay, music, transitions) is usually done by the user in CapCut — offer the hook text/CTA.
