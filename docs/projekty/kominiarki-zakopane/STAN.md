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
