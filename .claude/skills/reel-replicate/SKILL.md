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

If the avatar or backgrounds are missing, do NOT start casting on your own — ask first:
"I don't have an avatar/backgrounds yet — will you send your own, or should I run reel-casting
(pick a better avatar and backgrounds than the competitor's)?" Run `reel-casting` only if the user chooses it.
If the user asks for better ones than the competitor, that counts as choosing casting. If a `casting.json` exists, use its media_ids (avatar + extra angles,
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
Model: **`seedance_2_5`** (user's choice; check durations/resolutions with `models_explore`). 9:16, audio on.
Medias: `start_image` (and `end_image` for the hook) with a job_id of the approved frame; leave `mode` out —
Higgsfield switches to `omni_reference` itself when images are attached. Durations 4–30 s.
**Cheap test first:** one set at `480p` (≈12 kr / 4 s, ≈15 kr / 5 s; 720p ≈28 kr / 4 s), then remake the
winner at 720p/1080p (or use `draft: true` and finalise the draft at 1080p). Quote total cost first.
Measured prices (Plus plan): 4 s = 12 / 28 / 64 kr, 5 s = 15 / 35 / 80 kr for 480p / 720p / 1080p.
`upscale_video` (provider `topaz`, 1080p, 9:16) has no cost preflight but cost **3 kr for a 5 s clip** (balance
diff) — sharper edges, smoother skin, it cannot recover detail lost at 480p and outputs 24 fps. Never publish
plain ffmpeg-scaled 480p; export the final reel at 1080x1920 (`--size 1080x1920`).
Submit all sets with `generate_video_batch` (≤12 per call), `jobs_wait` (clips take ~5–8 min), one
`show_generation_by_ids`. While clips render, prepare the voice-over (below).
- If a submission comes back with a **preset recommendation instead of a job**, decline it and resubmit the
  same direct request (say "N submissions got intercepted by a preset recommendation — declining and resubmitting").
- If a clip gets a **false content flag** (common with pets/kids), reword neutrally and regenerate that one.
- Frame-check at least the hook of set 1 (extract a few frames with ffmpeg): whip-pan lands on the rack,
  hand grabs the product, face stays the avatar.

## Stage 5 — Stitch & deliver
Download clips (`curl -L -o`), contact-sheet each one (`ffmpeg -vf fps=2.4,scale=200:-1,tile=6x2`) and check
motion, product print and that nothing animates that must not (printed faces, logos). Then per set:
```bash
python3 <skill_dir>/scripts/stitch_reel.py reel_set1.mp4 s1_hook.mp4 s1_b1.mp4:3 s1_b2.mp4:2 s1_b3.mp4:2.5 s1_b4.mp4:2 \
    [--vo countdown.mp3 --vo-at 0]
```
`:N` keeps the first N seconds — choose N so the best part of the clip is inside it.
**Voice-over (ElevenLabs, when the user wants a spoken hook):** `creative_list_voices` (language + age filter),
`creative_generate_speech` with `eleven_v4` and audio tags, e.g.
`[excited whisper] Trzy... [whispering, giggling] dwa... [shouting excitedly] JEDEN!` (2 takes ≈ 83 EL credits each).
Find word timings with `ffmpeg -af silencedetect=n=-35dB:d=0.15` and pick the take whose key word lands on the
visual beat (e.g. "JEDEN" at the blanket pull ≈ 2.6 s); mix with `--vo`. You cannot listen — tell the user to.
Deliver N stitched reels (~16–17 s, 720×1280) + individual clips, and a summary:
> All done — 25 clips generated with Seedance and delivered as 5 stitched reels (one per set, ~17s each, 720p 9:16
> with native audio). How each reel is built: hook = …; then the four b-rolls follow your notes: … (trimmed to 2s) …
> One hiccup handled: … If any single clip needs a re-roll (e.g. "set 3, zip clip") — just say so. I can also drop
> the reels or the individual clips onto your Miro board.
Optional: upscale/finalise chosen reels at 1080p (ask, costs credits); voice-over with ElevenLabs if asked.
Final edit (text overlay, music, transitions) is usually done by the user in CapCut — offer the hook text/CTA.
Do not leave deliverables inside the git repo (no stray `output/` folders); keep them in the scratchpad and send them.

## Practical notes (learned in real runs)
- **Ask for the brief first, then build the Miro plan before spending anything** (user's preference): original
  frames, materials (product, avatars, background), shot plan with empty start-frame slots, hook prompt,
  audio/cost box. Generate only after "akceptuję".
- **Localisation:** for a Polish audience add Polish accents on request (flag as a cape, white-eagle scarf,
  highlander plaid blanket, oscypek + mulled wine, parzenica sweater, góral hat) and replace foreign text on
  clothes (e.g. "St. Moritz") — say it explicitly in every prompt, the model copies text from avatar photos.
- **Night background but product must be visible:** offer day vs evening; a night reference can be used as a
  *place* reference with "on a bright sunny day".
- **Avatar photos of real people:** say once that using a real person's face in an ad without consent is risky;
  the user decides.
- **Product with a printed face/graphic** (balaclavas, T-shirts): pass each product variant as its own reference
  (a collage gives cartoon results), say "photo-real print on fabric, NOT a cartoon mask", and in video prompts
  "the printed face is fabric and never animates, blinks or talks". Check where accessories sit (goggles over
  the eye panel, not on the forehead).
- **User's standing rules for masked characters** (apply in every image and video prompt):
  1) a balaclava with a see-through eye panel and NO goggles must show the wearer's real eyes through the panel
  ("the wearer's real human eyes are clearly visible through the sheer grey mesh eye panel") — never a blank
  panel; 2) characters do not bob, nod or shake their heads in any scene (say "heads stay still" in video
  prompts); 3) head + mask + hat in natural proportion to the body (no oversized heads), hats sit low on the head;
  4) **never two identical people in one clip** — the model likes to clone a face (same eyes, brows, skin, age)
  onto several people, very visible through eye openings. Give every character a distinct description (eye
  colour, brows, age, skin tone, build) in every prompt and check eyes side by side in QA; reject clones;
  5) **lighting must match the scene**: the product is lit by the same light as everything else (sun direction,
  shadows, white balance, exposure) — darker in shade, brighter in sun; it must not look pasted in, over-bright
  or flatly lit. Write it into every prompt ("lit by the same sunlight as the scene, matching shadows and colour
  temperature") and check it in QA.
- **NO EXTRA MOVEMENT unless the user asks for it** (hard rule): characters do exactly the one action in the
  brief and nothing else — no head shaking/nodding/bobbing, no waving or flapping arms/hands, no fidgeting,
  trembling or random gestures, no "dance-like" filler. Seedance invents idle motion when a prompt lists several
  verbs or words like "energetic / lean / move / bob" — write ONE calm action with a timeline, everything else
  "holds still", e.g. "they hold the pose completely still, only the flag moves in the wind". Prefer locked-off
  or very gentle handheld camera. QA video at 8 fps on the heads and hands (contact sheet of the head area) —
  2 fps sheets hide shaking. Reject and redo clips with jitter before showing them to the user.
- **When unsure, ask the user** (look, motion, which design, colours…) instead of guessing — they prefer a quick
  question to a wasted generation.
- **Product-fidelity QA is mandatory and done in close-up:** crop every masked/printed face at ≥2× and put it
  next to the product photos (a reference strip) before accepting a frame. Thumbnails hide wrong prints.
- **Fixed design-per-character map** (write it on the board) and name it in every prompt, e.g. "orange jacket =
  image 2 toothless; black jacket + flag = image 3 grumpy with cigarette, NO mustache; navy hoodie = image 4
  mustache". Always pass ALL product photos plus one approved close-up frame as the "eye/rim look" reference.
- **"Edit, change only X" drifts other people** in group shots (each edit re-renders everyone). If an edit fixes
  one person but breaks another, don't re-roll again: the edit keeps the layout pixel-aligned, so composite the
  correct heads from the two versions with Pillow (feathered ellipse mask, check alignment with a diff image),
  upload the composite (`media_upload` → PUT → `media_confirm`) and use that media_id as the start frame. Free.
- When eyes must show through a see-through eye panel, say "THICK BLACK OVAL RIM around the eye opening, the
  wearer's real eyes inside it" — "no goggles / eyes visible" alone makes the model drop the mask entirely.
- Group shots from far away (full body) lose print fidelity; prefer knees-up framing for 3–4 people.
- **No POV hands by default:** don't put the filmer's hands/sleeves in the foreground unless the user wants it.
- **Continuity:** for the hook end frame pass the approved start frame's job_id as reference image 1
  ("keep the same place, table, people…") — start/end then animate cleanly.
- **Fixing one detail:** re-roll with the rejected frame's job_id as reference image 1 + "edit, keep everything
  the same, only change X" (2 kr, the rest stays identical).
- Higgsfield may show `nano_banana_2` as the model for `nano_banana_pro` jobs — the cost matches the quote.
- A batch item may fail with "Out of credits" while the balance is fine: no job was created, so resubmit just
  that item.
- Seedance often makes a "dance" too subtle at full-body distance — describe big, concrete moves and frame
  closer (knees up) for dance b-rolls. Very fast reveals can happen between two frames — describe the pull
  as "over 0.5 s" if it should be visible.

### Hook countdown sync (learned)
- Measure the competitor hook first (whisper word timestamps + 6 fps sheet): e.g. "three" 0.0 s, "two" ~0.9 s,
  "one" ~1.6 s, cloth pulled ~2.9 s, reveal held ~1.3 s, cut. Copy that rhythm; ~0.9-1.0 s between words.
- Generate the hook video FIRST, find the frame where the pull starts (8 fps sheet), then place the voice-over so
  the stressed "JEDEN" starts on that frame. Cut each word out of the VO take (drop giggles/pauses between words).
- Seedance invents speech ("Cześć!") even with "no speech": transcribe the clip audio and replace speech parts with
  a loop of its own quiet wind. Trim the hook ~1.2 s after the reveal - no dead stop-frame.
- Colour jump: an end frame retouched separately has another grade, and Seedance shifts the whole picture
  towards it mid-clip (washed sky, redder). Measure mean RGB of the sky per frame; fix with
  `scripts/match_grade.py` (no new generation), or colour-match the end frame to the start frame BEFORE generating.
- Feet: check that every seated person is directly above their own pair of shoes in start AND end frame. If the
  model keeps the wrong layout, cut the people out (rembg u2net_human_seg), make a clean plate (people removed),
  paste them shifted over their shoes, then one Nano retouch pass to blend; re-paste details it loses (goggles).

### Miro mechanics
- **Update the board automatically after EVERY change** (new frame, new clip, new prompt, new decision) without being
  asked — the user must never have to remind you. Miro tools are pre-allowed in `.claude/settings.json`.
- Load `canvas_get_canvas_composer_skill` (no step → `design` → `dsl`; the dsl reply is long, read it from the
  saved file with jq). Frames: `<g data-frame>` + background rect; children use frame-relative coords.
- Images: `image_create` with `image_url` (Higgsfield result URLs are public) and `moveToWidget=<frameId>`;
  x/y = image **centre**, relative to the frame. For many local images build one composite strip with Pillow
  and upload it once (`image_get_upload_url` → curl PUT → `image_create(token)`).
- Swapping an image via `canvas_update_from_svg` `href` resets it to natural size (and moves it, the centre is
  kept). Fix in two more updates: first `width` only (height follows the aspect, never send `height`), then
  `x`, `y`, `width` again so the top-left lands back in its slot.
- When a frame grows, move the frames below it (update the frame `<g>` with `data-frame` + its rect).
- Deleting widgets needs the user's OK; to replace, prefer swapping `href` on the existing image (only public
  https URLs work — Higgsfield `d2ol…` upload URLs are rejected; then place a new image on top via upload token).
- Never send several `canvas_update_from_svg` calls in parallel for the same widgets — they conflict.
