"""Export Korean narration (EP01-EP10) as plain-text files for external TTS.

EP01 uses the easy Korean version (handoff/EP01_Narration_KO.txt).
EP02-EP10 use the Korean translation in scripts/epXX.json.
Format matches EP01: one sentence per line, blank line between sections,
no headings, [FACT-CHECK] markers and ** markup removed.

Usage: python3 drone-series/tools/make_narration_ko.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "narration_ko"


def clean(text):
    text = re.sub(r"\s*\[FACT-CHECK[^\]]*\]", "", text)
    text = text.replace("**", "")
    return re.sub(r"\s+", " ", text).strip()


def sentences(para):
    return [s for s in re.split(r"(?<=[.?!])\s+", clean(para)) if s]


def main():
    OUT.mkdir(exist_ok=True)
    combined = []
    for ep in range(1, 11):
        data = json.loads((ROOT / "scripts" / f"ep{ep:02d}.json").read_text(encoding="utf-8"))
        slug = re.sub(r"[^A-Za-z0-9]+", "-", data["title_en"]).strip("-")
        dest = OUT / f"EP{ep:02d}_{slug}_Narration_KO.txt"
        if ep == 1:
            shutil.copyfile(ROOT / "handoff" / "EP01_Narration_KO.txt", dest)
        else:
            blocks = ["\n".join(s for p in sec["paras_ko"] for s in sentences(p))
                      for sec in data["sections"]]
            dest.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
        body = dest.read_text(encoding="utf-8").strip()
        combined.append(f"===== {ep}편 · {data['title_ko']} ({data['title_en']}) =====\n\n{body}")
        print(f"{dest.name}: {len(body.replace(chr(10), ''))}자")
    (OUT / "EP01-EP10_Narration_KO_All.txt").write_text("\n\n\n".join(combined) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
