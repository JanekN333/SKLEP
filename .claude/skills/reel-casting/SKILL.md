---
name: reel-casting
description: Pick a BETTER avatar and better backgrounds than the competitor's reel before replicating it — analyses the competitor's frames (person, setting, light, colours, what hurts the product's visibility), writes a casting brief tailored to the user's product and audience, then generates avatar variants and background options in Higgsfield for the user to choose (no Pinterest needed), and hands the chosen ones to reel-replicate. Use when the user says "find me an avatar/backgrounds", "pick a better avatar than the competitor", "casting", "what avatar/background should I use", or has frames from video-frame-extractor but no avatar/backgrounds yet.
---

# Reel casting

Sits between `video-frame-extractor` and `reel-replicate`:
**extract frames → casting (this skill) → replicate → Miro → animate.**
Goal: the replica should look *better* than the original — product pops more, person fits the audience,
settings feel aspirational yet believable. Talk to the user in their language. Keep a task list.

Requires the Higgsfield connector. Images cost credits → always quote and wait for a yes before generating.

## 1. Inputs
- Competitor frames + contact sheet (run `video-frame-extractor` first if only a video is given).
- The user's product / colour-variant image (and pet/prop if relevant).
- Optional: target audience, country/market, price point, how many sets (backgrounds) — default 5.
  Ask only if it changes the brief a lot; otherwise infer from the product and the reel.

## 2. Analyse the competitor (look at the frames yourself)
Write a short scorecard, 1–5 per row, with one concrete observation each:

| Element | What to check |
|---|---|
| Person | age, look, styling, energy, how relatable to the buyer, how readable the emotion in the hook is |
| Hook location | type of store, clutter, light, does the product display read instantly |
| Room backgrounds | style, tidiness, light, depth, aspirational vs relatable |
| Product contrast | does the product colour separate from the background and the outfit? |
| Framing / light | flat or dimensional, phone-native look, skin quality |
| Prop / pet | breed, size, cuteness, visibility |

Then list the **3–5 weaknesses to beat** (e.g. "beige hoodie on beige wall — product disappears",
"dark cluttered bedroom", "creator looks 35+, product targets 18–28 women", "dog barely visible").
Also list what **must stay** because it is why the reel works (the shock reaction, the in-store discovery, the reveal).

## 3. Casting brief
Turn the analysis into a brief and show it to the user before spending anything:
- **Avatar** — age range, vibe (girl-next-door, clean-girl, cozy-mom…), hair, skin tone range, makeup level,
  outfit for the in-store hook (neutral colour that contrasts the product), body language. A fictional person —
  never a celebrity or a real identifiable person's likeness.
- **Backgrounds × N** — one per set, each different but all on-brief: style, palette chosen to make the product
  colour pop (complementary / neutral), daylight direction, tidy but lived-in, phone-photo realism, empty of
  people, vertical 9:16, enough floor/space for the actions in the reel (sitting, standing, close-ups).
- **Store variants** for the hook (if the original hook is in a shop) — one per set, product category-appropriate.
- Cost estimate: (avatar variants) + (N backgrounds) [+ store variants] images.

## 4. Generate options
Model: pick a photoreal model with `models_explore` (action `recommend`; Nano Banana Pro or Soul-type models are
good for people). `aspect_ratio: "9:16"`. Use `generate_image_batch`, `jobs_wait`, ONE `show_generation_by_ids`.
- **Avatar**: 4 different candidates (one prompt each, varied within the brief). Prompt base:
  > Candid vertical 9:16 iPhone photo of a fictional [age]-year-old woman, [vibe], [hair], natural makeup, soft
  > smile, looking at camera, plain light background, chest-up, natural window light, realistic skin texture,
  > no filters, no text.
  After the user picks one, generate 1–2 extra angles of the SAME person (pass the chosen image as reference:
  side profile, three-quarter, full body in the hook outfit) — this makes identity hold in reel-replicate.
- **Backgrounds**: N empty rooms, one prompt each:
  > Vertical 9:16 iPhone photo of an empty [style] [room type], [palette], [light], tidy but lived-in, eye-level
  > from where a person would stand, no people, no text, realistic, not a render.
- **Store variants** (optional): empty aisle/rack area of a [store type] with space for a product display.

Self-check before showing: avatar looks like a real phone photo (no plastic skin), backgrounds have no people/
text/warping, palettes actually contrast the product colour. Re-roll weak ones (tell the user).

Present as: avatars A–D, backgrounds 1–N (+ stores), each with one line on *why it beats the original*.
User picks (e.g. "avatar B, backgrounds 1, 2, 4, 5, 6"). Offer to re-roll any slot.

## 5. Hand-off
Save `casting.json` next to the frames:
```json
{"avatar": {"media_id": "...", "extra_angles": ["..."], "brief": "..."},
 "backgrounds": [{"set": 1, "media_id": "...", "desc": "city-view bedroom, warm whites"}],
 "stores": [{"set": 1, "media_id": "...", "desc": "clothing store"}],
 "weaknesses_beaten": ["..."]}
```
Then offer: "Run reel-replicate with these now?" — reel-replicate uses these media_ids directly (no re-upload).

## Optional: virality check
After reel-replicate finishes, offer to compare the competitor reel and the new reels with Higgsfield
`virality_predictor` (check cost first). Report honestly — a score is a hint, not a guarantee.

## Prefer real photos instead?
If the user wants real references (e.g. from Pinterest), give 5–8 ready search phrases built from the brief
("aesthetic minimalist bedroom morning light vertical", "cozy beige living room fireplace", …) and wait for
them to drop the images; then continue with step 5 using those uploads.
