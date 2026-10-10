# Drone War Decoded — production repo

Educational YouTube series (English) on Ukraine's offensive and defensive drone technology, 10 episodes × ~10 min.

```
drone-series/
└── ep01/
    ├── EP01_Reaching-Moscow.md   script + cut list + budget + checklists
    ├── narration.json            narration text per section (as sent to TTS)
    ├── assets.md                 Higgsfield job IDs, prompts, measured credit costs
    ├── graphics.py               explainer diagrams → gfx/*.png
    ├── build.py                  edit plan → per-shot ffmpeg jobs + narration track
    └── render.sh                 full render → ep01_test_720p.mp4
```

## Low-cost pipeline (EP01 test: ~88 credits)

1. **Script** — write `EPxx_*.md`; mark unverified facts `[FACT-CHECK]`.
2. **Narration** — Higgsfield `seed_audio`, one job per script section (~3.7 credits / 100 words).
3. **Keyframes** — Higgsfield `gpt_image_2_5` (0.25 credits each), batches of ≤ 6.
4. **Motion** — only hero shots: `kling3_0` std, 5 s, sound off (7.5 credits each).
5. **Diagrams** — `graphics.py` (free; never AI-generate technical diagrams).
6. **Edit** — in the Higgsfield sandbox: put files in `audio/`, `img/`, `vid/` next to the scripts, run `./render.sh`.
   Stills get a slow Ken Burns move; AI shots get an `AI VISUALIZATION` label.
7. **Upload** — `media_upload` + `curl PUT` from the sandbox → appears in the Higgsfield library.

Before publishing: resolve all `[FACT-CHECK]` items, tick YouTube's altered/synthetic content disclosure, add sources to the description.

No payments, top-ups, auto-refill, or personal data connections are used in this workflow.
