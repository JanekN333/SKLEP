# Miro board layout — "AI Video Dropshipping"

One project = one area on the board (left → right, top → bottom):

```
[Project title: <product> — <date>]

ORIGINAL   | 01 0.0s | 02 1.2s | 03 … | (all extracted frames, label = number + time)

1          | S1-01 shocked hook | S1-02 cup drop | S1-03 whip pan | S1-05 rack | S1-06 … | … S1-14
2          | S2-01 …                                                                 (one row per set)
…
5          | S5-01 …

Hook 0-4sec                 brolls 4-16 sec
[hook frames per set]        [b-roll start frames per set, one column per clip]

[Prompt for the HOOK — filled template]     [First B-roll Clip: … 3–4sec]
                                            [Second B-roll Clip: … 2sec]
                                            [Third B-roll Clip: … 4sec]
                                            [Fourth B-roll Clip: … 3sec]
```

- Row label = set number; image title = `S{set}-{beat} {short name}` (e.g. `S3-09 zip + dog in hole`).
- Leave space between rows so the user can delete / drag frames.
- The user curates: deletes bad frames, moves the chosen ones under "Hook" / "brolls", edits the notes.
  Stage 4 reads exactly what is left there.
