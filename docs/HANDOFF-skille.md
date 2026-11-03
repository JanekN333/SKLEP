# Handoff: skille `video-frame-extractor` i `reel-replicate`

Notatka przekazania z poprzedniej sesji (środowisko „Default” blokowało YouTube/TikTok/Instagram).
Użytkownik pisze po polsku – odpowiadaj po polsku. Gdy coś jest niejasne, PYTAJ zanim zgadniesz.

## Cel
Odtworzyć 1:1 dwa skille z filmu twórcy @estebanpoudrierbiz („how i made 11k in a day while working 3 hours this week”, YouTube):
1. **video-frame-extractor** – z cudzej rolki (TikTok/IG/YT/plik) wyciąga kluczowe klatki.
2. **reel-replicate** – odtwarza rolkę z produktem, tłem i awatarem użytkownika (Higgsfield + Seedance 2.5).

Użytkownik ma wysłać / podlinkować drugi film pokazujący dokładnie działanie reel-replicate.
**Nie budować skilli, dopóki go nie obejrzysz** (decyzja użytkownika).

## Co widać w filmie 1 (obejrzany klatka po klatce)
Claude desktop (Cowork), rozmowa „Video frame extractor and reel replicator”, załączniki
`videoframeextractor contents.pdf` i `reelreplicator SKILL.pdf`. Claude: „they're the contents of your
video-frame-extractor and reel-replicate skills… Run them / Review or improve them / Merge or connect them
(make the replicator automatically use the frame extractor's output)”.

Uruchomienie: użytkownik wrzuca ~13 s rolkę (cat-carrier hoodie) + „Extract all the images”. Wynik:
- „Coverage checks out — first (0.0s) and last (13.2s) frames present, the in-store rack shots (4–5) survived,
  and each cat-emerging beat got its own frame.” → krok weryfikacji pokrycia.
- „All 15 distinct beats extracted… structure: shocked hook in-store (1–3, incl. cup-drop), whip-pan to the
  product on the rack (4–5), 'it's a cat carrier hoodie' demo (6–9), close-ups of the cat popping out (10–13),
  'Comment Hoodie' CTA (14–15). The `frames.json` timing data is saved too, so each shot's duration is ready
  if you want to animate replicas to match.”
- „A couple of pairs are near-duplicates by design (8/9, 14/15) — I kept them since the pose shifts slightly.”
- „Want me to run these through reel-replicate next — swap in your product, background, and avatar?
  If so, tell me which frame numbers to use and what to swap in.”
- Outputy: **Contact sheet (PNG)** – siatka 4 kolumny, każda klatka z etykietą „N  T.Ts” (np. „1 0.0s”,
  „2 1.2s”, „7 4.2s”) na białym pasku nad klatką; potem **Frame 01, Frame 02 … (PNG)** osobno; `frames.json`.
- Pasek postępu: „Updated tasks, ran 3 commands, used a skill” → skill prowadzi listę zadań.

## Co widać na screenie z Miro (tablica „AI Video Dropshipping”)
Numerowane wiersze (np. „5”): klatki z oryginału (dziewczyna z kawą w sklepie, półka z produktem),
obok wygenerowane klatki z awatarem i nowym produktem (zielona bluza „dog carrier hoodie” z chihuahua).
Pod spodem prompt Seedance w szablonie:

```
Prompt for the HOOK
Single continuous handheld shot, 4 seconds, vertical 9:16, filmed like someone secretly recording a
stranger's reaction in a store on a phone — natural handheld sway, no cuts.

START FRAME: close side-profile chest-up shot of [PERSON — from the avatar reference], jaw dropped in shock,
sipping an iced drink held in one hand, staring at something off-screen to the right, unaware of the camera.
Setting: [STORE / RETAIL BACKGROUND — from the background reference].

CAMERA & ACTION TIMELINE:
0.0–1.2s — [PERSON] lowers the iced drink from their mouth and gasps a spontaneous "[HOOK LINE, e.g. 'no
wayyy']", eyes going even wider, eyebrows shooting up, a small backward rock of the head — genuine surprise.
The instant the words END, their free hand SHOOTS out fully extended, pointing at the off-screen [PRODUCT]
display — no more speech from here, mouth simply open in silent shock, the other hand still holding the iced
drink. They NEVER look at the camera.
1.2–2.0s — The camera WHIPS right in one fast pan with strong natural motion blur — the person leaves the
frame — and snaps to a stop on the [PRODUCT] display.
2.0–4.0s — THE PAYOFF, AT TRUE SCALE: a dense retail display of the [PRODUCT] from the reference image —
[CHOOSE: identical product boxes stacked face-out in 2–3 tight rows / multiple identical units of the product
hung or shelved face-out] filling the frame, logos/branding sharp and readable, a small price tag on the shelf
or rack edge. SIZE IS CRITICAL: render the [PRODUCT] at its TRUE real-world retail size, correct proportions,
every unit exactly equal, never miniaturized, never oversized. Then [PERSON]'s HAND enters the frame from the
side and grabs one off the display, lifting it slightly — in correct proportion to their hand, gripped as the
real product would be. Camera holds with slight handheld drift to the end.

AUDIO: ONLY the spontaneous excited gasp "[HOOK LINE]", voice matching the person in frame, real shock; a sharp
intake of breath after. Underneath: quiet busy store ambience (AC hum, distant shoppers, faint PA echo, a soft
rustle when the hand grabs the product). NO whoosh, NO transition sound, NO SFX on the camera move, NO music.

REALISM — HARD RULES: [PERSON]'s face and identity stay exactly as the start frame in every visible frame. The
grabbing hand matches their skin tone and sleeve. The [PRODUCT] is pixel-faithful to the reference image —
same logo, colors, spelling — text rigid and readable, never warping, size constant to the last frame. Motion
blur only during the whip pan. Correct finger count. No text overlays.
```
Obok lista B-rolli z długościami, np.:
- First B-roll Clip: she put the small dog in the dog carrier hoodie … actual clip is 3–4 sec
- Second B-roll Clip: she zip the hoodie, the clip is 2 sec long
- Third B-roll Clip: avatar holding the camera with 2 hands and the dog … out of the hoodie and then look at the camera slightly moving head
- Fourth B-roll Clip: her petting her dog that is still in the carrier hoodie … the clip is 3 sec long

## Decyzje użytkownika
- Skille zapisać w **obu miejscach**: repo SKLEP `.claude/skills/<nazwa>/SKILL.md` (+ skrypty) ORAZ paczki `.zip`
  do wgrania w Claude.ai/desktop (Settings → Capabilities → Skills).
- **Miro zawsze**: każdy projekt dostaje tablicę w układzie jak wyżej (klatki oryginału → nowe klatki →
  prompty Seedance → B-rolle z czasami).
- **Pełny pipeline z akceptacją**: generowanie nowych klatek startowych (Higgsfield, np. Nano Banana/Seedream)
  z awatarem/produktem → pokazanie do akceptacji → animacja każdego ujęcia w **Seedance 2.5** (Higgsfield
  `seedance_2_5`, mode t2v/omni_reference, 4–30 s, 480p/720p/1080p, draft 480p → finalizacja 1080p).
  ZAWSZE pytać przed wydaniem kredytów.
- Dźwięk/lektor opcjonalnie przez ElevenLabs (podłączony; 19 polskich głosów).

## Stan techniczny
- Repo zawiera już `seedance.js` / `server.js` (integracja Seedance 2.5 przez ModelArk).
- Higgsfield: plan Plus, ~1201 kredytów (stan z 29.10).
- W „Default” zablokowane: youtube.com, googlevideo.com, ytimg.com, tiktok.com, instagram.com, huggingface.co,
  elevenlabsusercontent.com. Środowisko „ez” ma mieć odblokowane domeny wideo – sprawdź na starcie (`curl`).
- Do pobierania z linków: `pip install yt-dlp`; ffmpeg jest zainstalowany.

## Film 2 – obejrzany 03.11 (YouTube ngdVTWySo8I, ten sam tytuł, 12:36; demo 4:20–10:50)
Przepływ pokazany w Claude desktop (Fable 5 High, konektory: Higgsfield MCP `https://mcp.higgsfield.ai/mcp`
jako custom connector „Esteban”, Miro):
1. Pobranie rolki konkurencji (SnapInsta) → wrzucenie do Claude + „extract all the images” → 15 klatek,
   contact sheet, Frame 01–15 PNG (wynik jak w filmie 1).
2. Wgranie: awatar (Pinterest „25 years old woman”), wariant produktu (zielona bluza z chihuahua), 5 teł
   (sypialnie/salony z Pinteresta). Prompt: „Do All the frame except frame: 4,7,8,12,15. And use the skill reel
   replicator to swap it for my avatar in image 1 … my color variant in image 2 and then Do all the frame 5 times
   once for background N1 … then 2, 3, 4, 5”.
3. Wynik (Nano Banana Pro, 9:16, galeria `show_generation_by_ids`): „All 60 frames… Each set now has 12 beats,
   numbered by the last two digits: 01 shocked hook, 02 cup drop, 03 whip pan, 05 product rack — all in-store —
   then in the room: 06 cradling the dog, 07 (new) dog climbing into the pouch, 09 (fixed) zipping with the dog's
   face in the hole, 10 peek close-up, 11 head fully out, 12 (new) extreme tight close-up, 13 head in profile,
   14 seated petting.” „What I locked down this round: every prompt pins the woman to your exact avatar reference
   (five spot-checks…), the missing beats were generated directly from the reference frames so the camera angles
   copy them…” „Set guide: 100s = original clothing store + city-view bedroom, 200s = superstore + mountain bedroom,
   300s = department store + wood-ceiling bedroom, 400s = boutique + fireplace living room, 500s = pet-supply
   store + open great room.” „Go through the gallery — if any single frame is off, give me its number and I'll
   re-roll just that one. When you're happy, tell me which set to animate…”
   → hook w sklepie też dostaje inny typ sklepu na zestaw (Claude sam je wymyślił).
4. „can you put all these images inside my miro board” → „All 60 images are now on your AI Video Dropshipping
   board… 5 rows, one per set…, 12 beats left to right in reel order. Each image is titled with its set and beat
   (e.g. "S3-09 zip + dog in hole")”. Użytkownik ręcznie usuwa złe klatki, układa „Hook 0-4sec | brolls 4-16 sec”,
   dopisuje prompt hooka (szablon wyżej) i opisy 4 B-rolli z długościami.
5. Zrzut tablicy + ponownie oryginalna rolka + „generate all the videos. So you judge how many different clip per
   video…” → „Three submissions got intercepted by a preset recommendation — declining it and resubmitting…”
   → „All done — 25 clips generated with Seedance 2.0 and delivered as 5 stitched reels (one per set, ~17s each,
   720p 9:16 with native audio). Hook = single continuous 4s shot driven by your written hook prompt, with your
   shocked frame as the start frame and your rack frame as the end frame… (I frame-checked set 1…). Then the four
   b-rolls follow your notes: dog getting into the pouch (4s), zipping with the dog's face in the hole (trimmed to
   2s), the two-hand selfie with the dog's head coming out and looking at camera (4s), petting (trimmed to 3s).
   One hiccup handled: set 2's dog-in clip got a false content flag; I reworded and regenerated it.”
6. Montaż końcowy w CapCut (poza Claude).
