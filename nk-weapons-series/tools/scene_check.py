"""Contact sheets for an episode's line-art scenes + overlap check against the source label.

  cd drone-series/ep01_v2 && python3 ../tools/scene_check.py <ep> <out_dir>

Renders every distinct (scene, ph) used in shots_epNN.py at s=0.6 and s=3.5 into
<out_dir>/sheetN.jpg (4×6 tiles), prints any scene that raises an error, and prints every
scene whose drawing falls under the bottom-right source label (y 796–840) — move those up.
Open the sheets with the Read tool and look at every tile before rendering.
"""
import importlib
import sys
import traceback
from pathlib import Path

HERE = Path.cwd()
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import render  # noqa: E402
from gfx import Canvas  # noqa: E402

ep, out = int(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
render.set_episode(ep)
S = importlib.import_module(f"shots_ep{ep:02d}")
C = importlib.import_module(f"scenes_ep{ep:02d}")
f = render.font("label", 22)
d = ImageDraw.Draw(Image.new("RGB", (10, 10)))

seen = []
for sh in S.SHOTS:
    if sh["kind"] == "L":
        k = (sh["scene"], sh.get("ph", 0), sh.get("src"))
        if k not in seen:
            seen.append(k)
tiles = []
for name, ph, src in seen:
    for s in (0.6, 3.5):
        try:
            cv = Canvas()
            C.SCENES[name](cv, s, 6.0, ph)
            im = cv.finish()
        except Exception:
            print("ERROR", name, ph)
            traceback.print_exc()
            im = Image.new("RGB", (1920, 1080), (255, 0, 0))
        if src:
            w = d.textlength(S.SOURCES[src], font=f)
            a = np.asarray(im.convert("L")).astype(int)
            if (a[796:840, int(1920 - w - 60):1880] > 110).sum() > 30:
                print("OVERLAPS SOURCE LABEL:", name, "ph", ph, "s", s)
        tiles.append(im.resize((480, 270)))
for p in range(0, len(tiles), 24):
    sheet = Image.new("RGB", (480 * 4, 270 * 6), "white")
    for i, t in enumerate(tiles[p:p + 24]):
        sheet.paste(t, ((i % 4) * 480, (i // 4) * 270))
    sheet.save(out / f"sheet{p // 24}.jpg", quality=80)
print(len(seen), "scene/phase combinations ->", out)
