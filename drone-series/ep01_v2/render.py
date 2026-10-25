"""Render EP01 (v2 style): pencil illustrations + line-art, Korean subtitles, English labels.

  python3 render.py                 # full episode -> out/ep01_v2.mp4 (silent, estimated timing)
  python3 render.py --first 12      # only the first 12 shots (quick check)
  python3 render.py --stills        # one PNG per shot -> out/stills/ (contact-sheet review)
  python3 render.py --audio voice.wav   # align to a recorded narration (see align.py) and mux it

Timing: without audio, each sentence lasts len(chars)/CPS seconds. With --timing timing.json
(written by align.py) the sentence start/end times from the real voice track are used.
"""
import argparse
import json
import math
import re
import subprocess
import sys
import urllib.request
from multiprocessing import Pool
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import gfx  # noqa: E402
from gfx import BLACK, GREY, ORANGE, WHITE, Canvas, H, W, ease, font  # noqa: E402
from scenes import SCENES  # noqa: E402
from shots import SHOTS, SOURCES  # noqa: E402  (EP01; set_episode() swaps these for other episodes)

FPS = 24
CPS = 7.0          # estimated Korean narration speed, characters per second
GAP = 0.25         # pause after each sentence (estimated mode)
SECTION_GAP = 0.6  # extra pause at section ends (estimated mode)
PREROLL = 3.0      # silent lead-in: the first picture fades up before the narration starts
NARRATION = sorted((HERE.parent / "narration_ko").glob("EP01_*_Narration_KO.txt"))[0]
NARRATION_EN = sorted((HERE.parent / "narration_en").glob("EP01_*_Narration_EN.txt"))[0]
LANG = "ko"  # "en": English subtitles (shot anchors still resolve on the Korean script, 1:1 by sentence)
IMG_DIR = HERE / "img"
OUT = HERE / "out"
EP = 1


def set_episode(ep):
    """Point the renderer at episode `ep`: its narration files, shot list (shots_epXX.py) and extra scenes."""
    global EP, NARRATION, NARRATION_EN, SHOTS, SOURCES
    import importlib
    EP = ep
    NARRATION = sorted((HERE.parent / "narration_ko").glob(f"EP{ep:02d}_*_Narration_KO.txt"))[0]
    NARRATION_EN = sorted((HERE.parent / "narration_en").glob(f"EP{ep:02d}_*_Narration_EN.txt"))[0]
    mod = importlib.import_module("shots" if ep == 1 else f"shots_ep{ep:02d}")
    SHOTS, SOURCES = mod.SHOTS, mod.SOURCES
    if ep != 1:
        SCENES.update(importlib.import_module(f"scenes_ep{ep:02d}").SCENES)


# ---------------- script & timing ----------------

def _split(path):
    out = []
    blocks = path.read_text(encoding="utf-8").strip().split("\n\n")
    for si, block in enumerate(blocks, 1):
        for line in block.splitlines():
            for s in re.split(r"(?<=[.?!])\s+", line.strip()):
                if s:
                    out.append({"sec": si, "text": s})
    return out


def sentences():
    out = _split(NARRATION)
    if LANG == "en":
        en = _split(NARRATION_EN)
        if [s["sec"] for s in en] != [s["sec"] for s in out]:
            raise SystemExit("EN script must match the Korean script sentence-for-sentence")
        for s, e in zip(out, en):
            s["disp"] = e["text"]
    for i, s in enumerate(out):
        s["last_in_sec"] = i + 1 == len(out) or out[i + 1]["sec"] != s["sec"]
    return out


def disp(s):
    return s.get("disp", s["text"])


def estimate(sents):
    for s in sents:
        d = max(1.3, len(disp(s)) / (CPS if LANG == "ko" else 15.0)) + GAP + (SECTION_GAP if s["last_in_sec"] else 0)
        s["dur"] = d


def build_timeline(sents, timing=None):
    """Resolve shots to absolute times. Returns list of shots with t0/t1 and their sentences."""
    idx = 0
    resolved = []
    for sh in SHOTS:
        sh = dict(sh)
        if "at" in sh:
            while idx < len(sents) and not sents[idx]["text"].startswith(sh["at"]):
                idx += 1
            if idx >= len(sents):
                raise SystemExit(f"shot anchor not found: {sh['at']!r}")
            sh["first"] = idx
            idx += 1
        resolved.append(sh)
    anchored = [s for s in resolved if "first" in s]
    if anchored[0]["first"] != 0:
        raise SystemExit("first shot must start at sentence 0")
    for a, b in zip(anchored, anchored[1:] + [None]):
        a["last"] = (b["first"] if b else len(sents)) - 1
    t = 0.0
    for sh in resolved:
        sh["t0"] = t
        if "first" in sh:
            rng = range(sh["first"], sh["last"] + 1)
            if timing:
                # real audio: shot spans from its first sentence start to the next shot's first sentence start
                pass
            sh["cues"] = []
            for i in rng:
                s = sents[i]
                sh["cues"].append((t, t + s["dur"] - GAP * 0.5, disp(s)))
                t += s["dur"]
        else:
            sh["cues"] = []
            t += sh["dur"]
        sh["t1"] = t
    return resolved


def apply_preroll(shots):
    """Delay everything by PREROLL; the first shot starts at 0 so its picture can fade in first."""
    for k, sh in enumerate(shots):
        if k:
            sh["t0"] += PREROLL
        sh["t1"] += PREROLL
        sh["cues"] = [(c0 + PREROLL, c1 + PREROLL, txt) for c0, c1, txt in sh["cues"]]
    return shots


def build_timeline_audio(sents, timing):
    """timing: list of {start,end} per sentence (seconds in the voice track). Insert shots
    (title cards) push everything after them later; render.py inserts matching silence."""
    for s, tm in zip(sents, timing):
        s["a0"], s["a1"] = tm["start"], tm["end"]
        s["dur"] = tm["end"] - tm["start"]
    resolved = build_timeline(sents)  # resolves shot anchors; times are replaced below
    shift = 0.0
    out = []
    for k, sh in enumerate(resolved):
        if "first" not in sh:
            sh["t0"] = out[-1]["t1"] if out else 0.0
            sh["t1"] = sh["t0"] + sh["dur"]
            sh["cues"] = []
            sh["insert_at_audio"] = sents[resolved[k - 1]["last"]]["a1"] if k else 0.0
            shift += sh["dur"]
            out.append(sh)
            continue
        first, last = sh["first"], sh["last"]
        nxt = next((r for r in resolved[k + 1:] if "first" in r), None)
        a0 = 0.0 if first == 0 else sents[first]["a0"]
        a1 = sents[nxt["first"]]["a0"] if nxt else sents[last]["a1"] + 1.5
        sh["t0"], sh["t1"] = a0 + shift, a1 + shift
        sh["cues"] = [(sents[i]["a0"] + shift, sents[i]["a1"] + shift, disp(sents[i])) for i in range(first, last + 1)]
        out.append(sh)
    return out


# ---------------- subtitles ----------------

FORWARD_MODIFIERS = set("한두세네몇큰새첫각약총단이그저전매온서더잘")  # one-syllable words that belong to the NEXT word
BOUND_NOUNS = set("수데번것줄개대초분년곳때배")  # one-syllable words that belong to the PREVIOUS word
KEEP_TOGETHER = ("시 베이비", "디 인사이더", "1년 반", "이동 사격팀", "수백만 달러")  # multi-word names that must not be split across lines


def _cut_ok(p, cut):
    """A line break at p[cut] (a space) is fine unless it strands a one-syllable word on the wrong side."""
    before = p[:cut].split()[-1] if p[:cut].split() else ""
    after = p[cut:].split()[0] if p[cut:].split() else ""
    if before.endswith(","):
        return True
    if any(p.find(k) < cut < p.find(k) + len(k) for k in KEEP_TOGETHER if k in p):
        return False
    if len(before) == 1 and before in FORWARD_MODIFIERS:  # "크게 세 / 가지로"
        return False
    if after.rstrip(",.") in BOUND_NOUNS:  # "쏠 / 수 있고", "지나는 / 데", "수천 / 번"
        return False
    if after.startswith("것") and len(after.rstrip(",.")) <= 3:  # "인용한 / 것으로"
        return False
    if before in BOUND_NOUNS:  # "쏠 수 / 있고"
        return False
    return True


def chunks(text, maxlen=None):
    maxlen = maxlen or (26 if LANG == "ko" else 44)
    """Split a sentence into display chunks at commas/spaces, each <= maxlen chars."""
    if len(text) <= maxlen:
        return [text]
    parts = re.split(r"(?<=,)\s+", text)
    out = []
    for p in parts:
        while len(p) > maxlen:
            spaces = [i for i, ch in enumerate(p[:maxlen + 1]) if ch == " " and i > maxlen // 3]
            good = [i for i in spaces if _cut_ok(p, i)]
            cut = (good or spaces or [maxlen])[-1]
            out.append(p[:cut].strip())
            p = p[cut:].strip()
        if out and len(out[-1]) + len(p) + 1 <= maxlen:
            out[-1] = out[-1] + " " + p
        elif p:
            out.append(p)
    return out


def subtitle_at(cues, t):
    for c0, c1, text in cues:
        if c0 <= t < c1:
            parts = chunks(text)
            total = sum(len(p) for p in parts)
            acc = c0
            for p in parts:
                d = (c1 - c0) * len(p) / total
                if t < acc + d:
                    return p
                acc += d
            return parts[-1]
    return None


def draw_subtitle(im, text, boxed=True):
    """Reference style: white bold Korean text on a solid black box, bottom centre.
    Words are drawn one by one with a fixed gap, because the Gmarket web font has no space glyph."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(im, "RGBA")
    f = font("sub", 64 if LANG == "ko" else 58)
    words = text.split()
    gap = 64 * 0.28
    widths = [d.textlength(w, font=f) for w in words]
    total = sum(widths) + gap * (len(words) - 1)
    x0, y = W / 2 - total / 2, 935
    d.rectangle((x0 - 24, y - 55, x0 + total + 24, y + 55), fill=(0, 0, 0, 255))
    x = x0
    for w, ww in zip(words, widths):
        d.text((x, y), w, font=f, fill=(255, 255, 255, 255), anchor="lm")
        x += ww + gap


def draw_overlays(im, sh, s, pencil):
    from PIL import ImageDraw
    d = ImageDraw.Draw(im, "RGBA")
    a = int(255 * min(1.0, s / 0.35))
    if pencil:
        d.text((W - 40, 40), "AI ILLUSTRATION", font=font("label", 20), fill=(30, 30, 30, 170), anchor="ra")
        if sh.get("label"):
            f = font("label", 30)
            w = d.textlength(sh["label"], font=f)
            d.rectangle((60, 60, 60 + w + 44, 116), fill=(10, 10, 10, int(0.85 * a)))
            d.rectangle((60, 60, 68, 116), fill=ORANGE + (a,))
            d.text((88, 88), sh["label"], font=f, fill=(255, 255, 255, a), anchor="lm")
    if sh.get("src"):
        txt = SOURCES[sh["src"]]
        f = font("label", 22)
        w = d.textlength(txt, font=f)
        if pencil:
            d.rectangle((W - w - 64, 800, W - 36, 836), fill=(10, 10, 10, int(0.75 * a)))
        d.text((W - 50, 818), txt, font=f, fill=(200, 200, 200, a), anchor="rm")


# ---------------- frames ----------------

_img_cache = {}


def pencil_base(name):
    if name not in _img_cache:
        im = Image.open(IMG_DIR / f"{name}.png").convert("L")
        im = ImageOps.autocontrast(im, cutoff=0.5).convert("RGB")
        _img_cache[name] = im
    return _img_cache[name]


MOVES = {  # (zoom0, zoom1, (cx0, cy0), (cx1, cy1)) in normalised image coordinates
    "in": (1.0, 1.10, (0.5, 0.5), (0.5, 0.48)),
    "out": (1.12, 1.0, (0.5, 0.47), (0.5, 0.5)),
    "left": (1.12, 1.12, (0.56, 0.5), (0.44, 0.5)),
    "right": (1.12, 1.12, (0.44, 0.5), (0.56, 0.5)),
    "up": (1.12, 1.12, (0.5, 0.56), (0.5, 0.44)),
    "down": (1.12, 1.12, (0.5, 0.44), (0.5, 0.56)),
}


def pencil_frame(sh, s, T):
    src = pencil_base(sh["img"])
    iw, ih = src.size
    z0, z1, c0, c1 = MOVES[sh.get("move", "in")]
    k = ease(s / T) * 0.85 + (s / T) * 0.15     # quick start, gentle finish, never fully stops
    z = z0 + (z1 - z0) * k
    cx = (c0[0] + (c1[0] - c0[0]) * k) * iw
    cy = (c0[1] + (c1[1] - c0[1]) * k) * ih
    base = min(iw / W, ih / H)                   # cover-fit
    vw, vh = W * base / z, H * base / z
    x0 = min(max(cx - vw / 2, 0), iw - vw)
    y0 = min(max(cy - vh / 2, 0), ih - vh)
    return src.transform((W, H), Image.EXTENT, (x0, y0, x0 + vw, y0 + vh), Image.BICUBIC)


def lineart_frame(sh, s, T):
    cv = Canvas()
    SCENES[sh["scene"]](cv, s, T, sh.get("ph", 0))
    return cv.im.reduce(gfx.SS)


def render_shot(args):
    k, sh, scale, out_path = args
    n0, n1 = round(sh["t0"] * FPS), round(sh["t1"] * FPS)
    T = (n1 - n0) / FPS
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", str(out_path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    pencil = sh["kind"] == "P"
    for n in range(n0, n1):
        s = (n - n0) / FPS
        im = pencil_frame(sh, s, T) if pencil else lineart_frame(sh, s, T)
        draw_overlays(im, sh, s, pencil)
        if sh.get("fade_in") and s < sh["fade_in"]:
            im = Image.blend(Image.new("RGB", im.size, (0, 0, 0)), im, ease(s / sh["fade_in"]) ** 1.5)
        sub = subtitle_at(sh["cues"], n / FPS)
        if sub:
            draw_subtitle(im, sub, boxed=pencil)
        if scale != 1:
            im = im.resize((w, h), Image.BILINEAR)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()
    return k


def still(args):
    k, sh, out_path = args
    T = sh["t1"] - sh["t0"]
    s = min(T * 0.75, T - 0.05)
    pencil = sh["kind"] == "P"
    im = pencil_frame(sh, s, T) if pencil else lineart_frame(sh, s, T)
    draw_overlays(im, sh, s, pencil)
    sub = subtitle_at(sh["cues"], sh["t0"] + s) or (sh["cues"][0][2] if sh["cues"] else None)
    if sub:
        draw_subtitle(im, chunks(sub)[0], boxed=pencil)
    im.resize((640, 360), Image.LANCZOS).save(out_path)
    return k


def fetch_images():
    urls = json.loads((HERE / "images.json").read_text())
    IMG_DIR.mkdir(exist_ok=True)
    for name, url in urls.items():
        dst = IMG_DIR / f"{name}.png"
        if not dst.exists():
            print("download", name)
            urllib.request.urlretrieve(url, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first", type=int)
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--timing")
    ap.add_argument("--audio")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--lang", choices=["ko", "en"], default="ko")
    ap.add_argument("--ep", type=int, default=1)
    ap.add_argument("--out", default=str(OUT / "ep01_v2.mp4"))
    a = ap.parse_args()
    global LANG
    LANG = a.lang
    set_episode(a.ep)

    fetch_images()
    sents = sentences()
    if a.timing:
        shots = build_timeline_audio(sents, json.loads(Path(a.timing).read_text()))
    else:
        estimate(sents)
        shots = build_timeline(sents)
    shots = apply_preroll(shots)
    if a.first:
        shots = shots[:a.first]
    total = shots[-1]["t1"]
    print(f"{len(sents)} sentences, {len(shots)} shots, {total / 60:.1f} min")
    OUT.mkdir(exist_ok=True)

    if a.stills:
        d = OUT / "stills"
        d.mkdir(exist_ok=True)
        with Pool(a.jobs) as pool:
            pool.map(still, [(k, sh, d / f"{k:03d}.png") for k, sh in enumerate(shots)])
        return

    seg_dir = OUT / "seg"
    seg_dir.mkdir(exist_ok=True)
    jobs = [(k, sh, a.scale, seg_dir / f"{k:03d}.mp4") for k, sh in enumerate(shots)]
    jobs.sort(key=lambda j: -(j[1]["t1"] - j[1]["t0"]))
    with Pool(a.jobs) as pool:
        for k in pool.imap_unordered(render_shot, jobs):
            print("shot", k, "done", flush=True)
    lst = seg_dir / "list.txt"
    lst.write_text("".join(f"file '{seg_dir / f'{k:03d}.mp4'}'\n" for k in range(len(shots))))
    video = OUT / "video_only.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(video)], check=True)
    if a.audio:
        # rebuild the voice track with silence where insert shots (title card) sit
        voice = OUT / "voice_48k_mono.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.audio, "-ac", "1", "-ar", "48000", str(voice)],
                       check=True)
        a.audio = str(voice)
        parts, prev = ["[lead]"], 0.0
        filt = [f"anullsrc=r=48000:cl=mono,atrim=0:{PREROLL}[lead];"]
        inserts = [sh for sh in shots if "insert_at_audio" in sh]
        for i, sh in enumerate(inserts):
            filt.append(f"[0:a]atrim={prev}:{sh['insert_at_audio']},asetpts=PTS-STARTPTS[a{i}];"
                        f"anullsrc=r=48000:cl=mono,atrim=0:{sh['dur']}[s{i}];")
            parts += [f"[a{i}]", f"[s{i}]"]
            prev = sh["insert_at_audio"]
        filt.append(f"[0:a]atrim={prev},asetpts=PTS-STARTPTS[tail];")
        parts.append("[tail]")
        fc = "".join(filt) + "".join(parts) + f"concat=n={len(parts)}:v=0:a=1,apad[out]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", a.audio,
                        "-filter_complex", fc.replace("[0:a]", "[1:a]"), "-map", "0:v", "-map", "[out]",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", a.out], check=True)
    else:
        Path(a.out).unlink(missing_ok=True)
        video.rename(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
