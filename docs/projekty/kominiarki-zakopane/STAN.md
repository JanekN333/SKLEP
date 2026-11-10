# Projekt: kominiarki z twarzami dziadków, Polana Szymoszkowa (Zakopane)

Stan na 2026-11-09. **Wstrzymany**, zostało tylko podbicie do 1080p i finalna rolka. Wznów od sekcji „Co dalej”.

## Brief
- Produkt: kominiarki z nadrukiem twarzy starszego pana. Wzory:
  - A: bezzębny, łysy, uśmiechnięty
  - B: zrzęda, siwy, z papierosem, BEZ wąsów
  - C: białe wąsy z papierosem
  - Referencja do porównań: `product_ref_strip.jpg`.
- Stałe przypisanie wzorów:
  - pomarańczowa kurtka + szalik z orłem = A
  - czarna kurtka + flaga jako peleryna = B
  - blondynka w granatowej bluzie = C
- Hook: głos „Trzy… dwa… JEDEN!”, ElevenLabs, głos Zofia, take 2 (`vo_b_zofia.mp3`).
  - Słowa wycięte z nagrania bez śmiechu i przerw: Trzy 0,05–0,85 s, Dwa 1,45–2,40 s, Jeden 2,50–3,45 s.
- Bez muzyki i napisów, tylko naturalny dźwięk. Polskie akcenty.
- Reguły użytkownika: patrz `.claude/skills/reel-replicate/SKILL.md`, w szczególności:
  - obowiązkowa kontrola przed każdą płatną generacją,
  - Miro aktualizowane automatycznie po każdej zmianie,
  - zero zbędnego ruchu,
  - oczy widoczne, gdy nie ma gogli.

## Zaakceptowana rolka v10 (480p, 14,5 s)
| # | Ujęcie | Klip (Higgsfield) | Fragment w rolce |
|---|---|---|---|
| 1 | Hook v10: koc góra-dół na „Trzy”, góra-dół na „Dwa”, zerwanie na „JEDEN” | job `af3364c9-c7b6-4dcb-8d21-db0d7d0996f7` | 0–5,0 s |
| 2 | B-roll 1 (gogle) | job `553de6f5-ec4e-45cc-82a2-fcdd3735203a` | 0–3,5 s |
| 3 | B-roll 3 | job `b3b1315d-6797-414f-8536-36d1604c23fd` | 0–2,5 s |
| 4 | Selfie, znak pokoju | job `b29841ab-5237-41fc-9add-37d534ad2f52` | **0,5–4,0 s** (ucięte pierwsze 0,5 s) |

- Usunięty z rolki: wyciąg krzesełkowy, job `9a47ad8c-c708-41a7-b7e2-3a48223e39d8`.
- URL klipu: `https://d8j0ntlcm91z4.cloudfront.net/user_3JhAeH6eJRWRDcxqlVnKJWJPXug/hf_<data>_<job>.mp4`. Pełne adresy są w historii sesji, np. hook `hf_20261107_175026_af3364c9-…mp4`. Można je też znaleźć w Higgsfield: show_generation_by_ids.
- Klatki hooka v10:
  - koniec: job `65de253d-cdfa-4d0d-868f-092b3382875b` (wariant B, jeden przebieg)
  - start: media `47a4f3b2-a7f9-4191-8682-fff1ea70081b` (wyprowadzony z końca, tło zablokowane)
- Odliczanie w v10 (moment, od którego słowo jest wstawione):
  - Trzy 0,17 s (start wycięcia 0,12)
  - Dwa 1,65 s (start wycięcia 0,05)
  - Jeden 3,35 s (start wycięcia 0,10)
  - Ruchy koca: uniesienia 0,25–1,2 s i 1,8–2,9 s, zerwanie 3,5–4,0 s.
- Złożenie rolki (ze ścieżkami lokalnymi):
  ```
  stitch_reel.py OUT hook.mp4:5.0 b1.mp4:3.5 b3.mp4:2.5 b4_cut.mp4:3.5 --size 480x854 \
    --vo vo_v9.wav --vo-at 0 --vo-vol 2.2 --bg-vol 0.9 --duck-until 4.3 --duck-vol 0.7
  ```
  Potem `volume=5.5dB,alimiter=limit=0.79`, co daje ok. −14 LUFS.

## Media Higgsfield (wejścia)
```
product: toothless 8fbcf69d-db0b-4cf9-8bb1-8ef6dd6649a6, cigarette f48de878-1885-4c67-aa33-887f4801c164,
         mustache a80871bf-f3c8-47e4-b002-a3d93cef49fa, all fd17f615-217c-4ccf-9dad-5f0076d0bd4a
avatars: orange 938109b0-14e0-4091-a8ee-f03f57606878, black 83a43939-46bd-410f-84a1-d74be985067c,
         blonde navy 293a7b6b-87aa-4137-bbd0-b153bf4daa36, women 9c3f4d6f-a817-4ba3-92dd-c264381a2b2b
background: Szymoszkowa 753402c5-9094-4f96-afe0-ee1a24f54afc
frames: B-roll 1 0a98813b-bd1b-46bc-ab6c-8c4e9a71e7a2, B-roll 3 ab5c93d7-07fe-436f-9e10-39d2e8862c38,
        selfie c40570fe-6f41-4e16-b3a3-45af02598dcf
```

## Miro
Tablica „AI Video Dropshipping”: https://miro.com/app/board/uXjVESbL4Xw=/
- Ramka 3 (Plan ujęć): `3458764689347703154`.
- Opis hooka: `…703235`.
- Opis wyciągu (oznaczony jako USUNIĘTY): `…703243`.
- Opis selfie: `…703290`.

## Co dalej
1. Użytkownik akceptuje v10 (ostatnia wersja wysłana).
2. Topaz upscale do 1080p (`upscale_video`, provider topaz, 9:16): 4 klipy po ok. 3 kr, razem ok. 12 kr. Najpierw zapytać o zgodę.
3. Finalna rolka 1080×1920 z tymi samymi cięciami i dźwiękiem. Wysłać i zaktualizować Miro.
4. Do rozważenia: napis „POLSKA” na szaliku w klatce końcowej jest lekko poprzekręcany.

## WERSJA 2: projekt 1 od nowa, 1:1 z konkurencją (2026-11-10)
Prośba użytkownika: odtworzyć rolkę konkurencji 1:1, ale z naszym produktem, awatarami z projektu 1, Szymoszkową i polskimi akcentami. Koc z napisem POLSKA i orłem. Zakładanie maski jak w projekcie 2. Śnieżki z trafieniem. Taniec z wypchnięciem. Selfie grupowe.

### Konkurencja (12,8 s)
- Cięcia: 4,28 / 7,2 / 9,4 / 11,36 s.
- Głos hooka: „Three” 0,0 / „two” 0,56 / „one” 1,64 / „let's go” 2,64 s.
- Koc: uniesienia 0,7–1,1 i 1,8–2,1 s, zerwanie 2,9–3,1 s, odsłonięcie do 4,28 s.

### Klatki v2 (Nano Banana Pro, 36 kr + poprawki 10.11: 103, 307, 4085, 510, 511 i dalej 103, 101 ×3, 307 ×2, 4085, 409 ×2 – razem ok. 30 kr) – `v2_klatki.jpg`
| Klatka | Opis | Job |
|---|---|---|
| 101 | koc POLSKA na 3 głowach, tło przypięte do 103 v3 (lokalnie `p5/L2_101.png`, przed wideo wgrać jako media) | `1dd7bd07-df8c-4554-97a8-e81f20fe7324` |
| 103 | 3 głowy na białych manekinach, A/B/C 1:1 z produktem | `8737b92e-05c3-47ea-92b1-16a3977fc12b` |
| 201 | maska przy piersi, gogle na czole (pomarańczowa kurtka, wzór A) | `9dc41035-137c-41c5-862e-e7cfc1c71c9a` |
| 202 | maska na czubku głowy | `d7c6c08d-4ac5-411a-baf5-475352ff9d96` |
| 203 | oczy widoczne, gogle na czole | `ae90a8df-7fdd-4e71-9db4-98562afe650b` |
| 204 | gogle na oczach | `f839b47e-5eb1-4fdb-a9a8-b7643ed5fbdc` |
| 306 | śnieżki: biała z flagą, granatowa, czerwona, zielona | `4f21ac34-301f-46df-9f2a-ec3ae950097f` |
| 307 | trafienie śnieżką wielkości pięści, z kadru 306 (ta sama ściana) | `7259f143-8b4c-4eb8-aecd-ebb406fe269b` |
| 408 | bordowa kurtka, maska C 1:1 (zaczesane włosy, wąs, szlug) | `2eebabff-9e8c-442c-b893-a2d6e33dfc6c` |
| 4085 | biała kurtka z orłem wypycha bordową, maska B 1:1 (skrzywiony, szlug, bez wąsa) + czarne gogle | `a8d54402-8fd7-4831-b539-d98eeed90464` |
| 409 | biała kurtka tańczy sama, maska B | `d5028a84-c567-44ed-b726-a21b64a4e8b4` |
| 510 | selfie, granatowa kurtka z flagą, maska A, szyja w kołnierzu | `efb28167-560a-4b1a-ab57-83b5690ae0bc` |
| 511 | selfie: dokładnie 3 osoby A (granat), B (czerwona), C (zielona); złożone lokalnie (`p5/f511.png`: baza `043be499`, twarz A z 510, głowa B z `bafe6c5b`), przed wideo wgrać jako media | lokalnie |

### Kadry konkurencji (media)
| Kadr | Media |
|---|---|
| 05 | `4cb933dc` |
| 07 | `2b10aabe` |
| 09 | `98ef6910` |
| bump | `40f1e461` |
| 10 | `c21daa38` |
| 11 | `f036024b` |

### Przed wideo
- ~~Przypiąć tło 101 do 103~~ zrobione (maska różnic, tylko koc i ręce z 101).
- Wyrównać tła 201–204.

### Miro
Ramka P1v2 `3458764689945840110` (y = 16600), arkusz klatek `3458764689946836564`.

### Poprawki v3 (10.11, po uwagach użytkownika: produkt nie 1:1, „wklejone w paincie”)
- Zasada: każda maska dostaje zdjęcie swojego produktu (A `8fbcf69d`, B `f48de878`, C `a80871bf`) i wzór realizmu z projektu 2 (`bea656cf` trójka, `8f25129c` H2). W prompcie: nadruk jest nieruchomy, cienki elastyczny poliester z lekkim połyskiem, szyja schowana w kołnierz, światło i cienie ze słońca sceny, bez HDR.
- Gdy edycja psuje inną maskę (model zamienia A na B), składam lokalnie z elipsą i miękką krawędzią.
- Koszt v3: ok. 34 kr.
- Porównanie z produktem: `v2_maski_zblizenia.jpg` (Miro `3458764689947710122`), arkusz klatek `3458764689947710111`.
- Do sprawdzenia przed wideo: maski w 306/307 (A/B/C/A) przy zbliżeniu.

### Okrzyk hooka „Trzy! Dwa! JEDEN!” (10.11)
- Decyzja użytkownika: wspólny okrzyk, głosy męskie i damskie (ekipa za stołem).
- ElevenLabs, flow `VSWcmFxhDdvcDpRImRXe`, model eleven_v4, tag [shouting excitedly]: Radek, Bartosz (powiedział „trzy” 2×, biorę 1., 3. i 4. fragment), Patryk, Zofia, Katarzyna. Jarosław i Kinga nie poszły (darmowe generowanie zajęte).
- Pliki źródłowe: scratchpad `proj1/chant/`. Miks: `tools/mix_chant.py <dir> <out> t_trzy t_dwa t_jeden [długość]` – przesunięcia 0–42 ms, kobiety ciszej, „JEDEN” +25%, potem aecho + kompresja + loudnorm.
- Podgląd: `okrzyk_3_2_1_podglad.mp4` (czasy robocze 0,15 / 1,15 / 2,35 s). Docelowo czasy słów ustawiam po wygenerowaniu klipu hooka: mierzę ruch koca (różnice klatek) i kładę każde słowo tuż przed uniesieniem, „JEDEN” na zerwanie.

### Wideo v2 (10.11) – podgląd `v2_podglad_720p.mp4` (12,9 s, −14 LUFS)
Zakładanie od nowa (ta sama osoba i chata co 201): 201 `bd588c3a` (otwór pokazuje kurtkę), 202 `f4399313` (maska na czubku + gogle), 203 `83210c5f`, 204 `130c6503`.
| Ujęcie | Klip (Kling 3.0 std, dźwięk) | Fragment w rolce |
|---|---|---|
| Hook 101→103, 5 s | `604fb1bb-cc37-456c-89e0-eeb23b3d6420` | 0–4,28 s; okrzyk na 0,05 / 0,90 / 2,35 s (ruch koca: 0,2–0,6, 1,05–1,35, zerwanie 2,35–3,45) |
| Zakładanie A (tylko start 201) | `d05d9921-afeb-4466-8dd6-c9083c2a19c5` | 1,95–2,60 |
| Zakładanie B 202→203 | `ead5eb7b-6b72-4839-a36f-8c4bdb936bb7` | 0,45–1,75 |
| Zakładanie C 203→204 | `f4531657-ca74-4698-aa6b-a8e318fcbd4b` | 0,30–1,27, kolor dopasowany do B |
| Śnieżki 306→307 | `9f9529be-da59-4024-bb02-4a0164674aab` | 0,8–3,0 |
| Taniec 408→4085 | `c9d631ca-3a39-44c2-bc50-d38f5177ccf1` | 1,7–3,04 |
| Taniec 4085→409 | `6485cdeb-1cf2-407b-ab69-3c7c8a757188` | 0,04–0,66 |
| Selfie 510→511 | `d154b762-9621-4b19-8b5e-d7ff91e4af14` | 0,9–2,34 |
- Dźwięk zakładania: czysty szum z klipu A (B i C miały podejrzane „Thank you” w whisperze).
- Koszt wideo: 52 kr. Klatki dodatkowe (201–204): 10 kr.
- Dalej: akceptacja, potem Topaz 1080p (9 klipów × 3 kr = 27 kr).
