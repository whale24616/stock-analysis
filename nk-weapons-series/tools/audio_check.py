"""Narration audio checks.

  python3 tools/audio_check.py clicks a.mp3 [b.mp3 ...]
      Count click-like events (sudden jumps much larger than the local loudness).
      Run on the raw file and on the declicked file; the declicked one should show 0.

  python3 tools/audio_check.py gaps <audio.mp3> <timing.json> <script_ko.txt>
      For each sentence: flag speech rates outside 4.8–8.6 chars/s, and any sound louder than
      -22 dB (relative to the first 30 s) in the silence between sentences. A flagged gap is
      either a stray tail (cut it) or the next sentence starting earlier than the aligner said
      (move that sentence's start). Print the 30 ms energy profile to decide.

Declick (two passes) before checking:
  ffmpeg -i raw.mp3 -af "adeclick=w=55:o=75:a=2:t=2,adeclick=w=55:o=75:a=2:t=2" -ac 1 -ar 44100 -b:a 128k out.mp3
"""
import json
import re
import subprocess
import sys

import numpy as np


def load(path, sr):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)


def clicks(path):
    x = load(path, 48000)
    d = np.abs(np.diff(x))
    env = np.convolve(np.abs(x), np.ones(960) / 960, mode="same")[1:]
    s = d / (env + 50)
    ev = []
    for i in np.where(s > 12)[0]:
        if not ev or i - ev[-1][0] > 2400:
            ev.append([i, s[i]])
        else:
            ev[-1][1] = max(ev[-1][1], s[i])
    top = [round(i / 48000, 1) for i, _ in sorted(ev, key=lambda e: -e[1])[:8]]
    print(path.split("/")[-1][:40], "click-like events:", len(ev), top)


def gaps(audio, timing, script):
    t = json.load(open(timing))
    t = [[x["start"], x["end"]] if isinstance(x, dict) else x for x in t]
    s = [l.strip() for l in open(script, encoding="utf-8") if l.strip()]
    print(len(t), "timed sentences /", len(s), "script sentences")
    for i, ((a, b), txt) in enumerate(zip(t, s)):
        r = len(re.sub(r"\s", "", txt)) / max(0.01, b - a)
        if r < 4.8 or r > 8.6:
            print(f"rate  #{i + 1} {a:.2f}-{b:.2f} {r:.1f} c/s  {txt[:24]}")
    sr, w = 44100, 441
    x = load(audio, sr) / 32768
    peak = np.sqrt(np.mean(x[: sr * 30] ** 2))
    for i in range(len(t)):
        a = t[i][1] + 0.06
        b = (t[i + 1][0] - 0.04) if i + 1 < len(t) else len(x) / sr
        if b - a < 0.08:
            continue
        seg = x[int(a * sr): int(b * sr)]
        fr = seg[: len(seg) // w * w].reshape(-1, w)
        db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) / peak + 1e-9)
        if db.max() > -22:
            prof = " ".join(f"{d:.0f}" for d in db[::3])
            print(f"gap   after #{i + 1} {a:.2f}-{b:.2f} max {db.max():.0f} dB at {a + db.argmax() * 0.01:.2f} | {prof[:160]}")
    print("done")


if __name__ == "__main__":
    if sys.argv[1] == "clicks":
        for p in sys.argv[2:]:
            clicks(p)
    else:
        gaps(*sys.argv[2:5])
