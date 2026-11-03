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
