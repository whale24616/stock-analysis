"""Align the recorded Korean narration to the script sentences -> timing.json.

  python3 align.py voice.wav            # Korean voice -> timing.json
  python3 align.py voice_en.mp3 en      # English voice -> timing_en.json (then render.py --lang en)
  python3 render.py --timing timing.json --audio voice.wav

Uses faster-whisper word timestamps (preinstalled in the Higgsfield sandbox), then matches the
recognised characters to the script characters, so small recognition errors don't matter.
"""
import difflib
import json
import re
import sys
from pathlib import Path

import render
from render import sentences

HERE = Path(__file__).resolve().parent


def norm(s):
    return re.sub(r"[^0-9a-z가-힣]", "", s.lower())


def main():
    audio = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "ko"
    render.LANG = lang
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, language=lang, word_timestamps=True, vad_filter=True)
    chars, times = [], []
    for seg in segs:
        for w in seg.words:
            t = norm(w.word)
            for i, ch in enumerate(t):
                chars.append(ch)
                times.append(w.start + (w.end - w.start) * (i + 0.5) / max(len(t), 1))
    heard = "".join(chars)

    sents = sentences()
    script, owner = [], []
    for k, s in enumerate(sents):
        for ch in norm(render.disp(s)):
            script.append(ch)
            owner.append(k)
    sm = difflib.SequenceMatcher(None, "".join(script), heard, autojunk=False)
    mapped = [None] * len(script)
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            mapped[a + i] = times[b + i]

    out = []
    for k in range(len(sents)):
        ts = [mapped[i] for i in range(len(script)) if owner[i] == k and mapped[i] is not None]
        out.append({"start": min(ts) - 0.15, "end": max(ts) + 0.3} if ts else None)
    # fill sentences that could not be matched by interpolating between neighbours
    for k, v in enumerate(out):
        if v is None:
            prev = next((out[j]["end"] for j in range(k - 1, -1, -1) if out[j]), 0.0)
            nxt = next((out[j]["start"] for j in range(k + 1, len(out)) if out[j]), prev + 2.0)
            out[k] = {"start": prev, "end": nxt}
            print("unmatched sentence", k, sents[k]["text"][:30])
    for k in range(1, len(out)):
        out[k]["start"] = max(out[k]["start"], out[k - 1]["end"] - 0.05)
    (HERE / ("timing.json" if lang == "ko" else "timing_en.json")).write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("matched", sum(1 for m in mapped if m is not None), "/", len(script), "chars -> timing.json")


if __name__ == "__main__":
    main()
