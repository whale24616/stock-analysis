"""YouTube thumbnails (1280x720) for the Korean episodes: pencil illustration + bold Gmarket text.

  python3 drone-series/tools/make_thumbnails.py <out_dir>

Run from the repo root where drone-series/ep01_v2/img/ holds the illustrations and
drone-series/ep01_v2/fonts/GmarketSansTTFBold.ttf exists (the Higgsfield sandbox has both).
The Gmarket web font has no space glyph, so words are drawn one by one."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parent.parent / "ep01_v2"
FONT = ROOT / "fonts" / "GmarketSansTTFBold.ttf"
ORANGE = (255, 138, 31)
WHITE = (245, 245, 240)
W, H = 1280, 720

EPISODES = [
    dict(ep=1, img="p14_swarm", side="left", lines=["값싼 드론이", "모스크바까지"], sub="1,000km를 혼자 날아가는 비밀",
         tag="2026 우크라이나 실전 · 러시아 본토 타격"),
    dict(ep=2, img="e2_03_jet_climb", side="left", lines=["시속 700km", "미사일-드론"], sub="방공보다 빠르게",
         tag="2026 우크라이나 실전 · 방공 돌파 전술"),
    dict(ep=3, img="e3_01_pilot_goggles", side="right", lines=["400달러로", "전쟁을 바꾸다"], sub="FPV 드론의 모든 것",
         tag="2026 우크라이나 실전 · FPV 공격 전술"),
]


def font(size):
    return ImageFont.truetype(str(FONT), size)


def words_width(d, words, f, gap):
    return sum(d.textlength(w, font=f) for w in words) + gap * (len(words) - 1)


def draw_words(d, xy, text, f, fill, stroke=0, stroke_fill=(0, 0, 0), anchor_right=False):
    words = text.split()
    gap = f.size * 0.28
    total = words_width(d, words, f, gap)
    x, y = xy
    if anchor_right:
        x -= total
    for w in words:
        d.text((x, y), w, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += d.textlength(w, font=f) + gap
    return total


def fit(d, text, start, max_w):
    size = start
    while size > 40:
        f = font(size)
        if words_width(d, text.split(), f, size * 0.28) <= max_w:
            return f
        size -= 4
    return font(size)


def make(cfg, out_dir):
    im = Image.open(ROOT / "img" / f"{cfg['img']}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    im = ImageEnhance.Contrast(im).enhance(1.25)
    # darken the text side so the words stay readable on a phone screen
    shade = Image.new("L", (W, H))
    sd = ImageDraw.Draw(shade)
    for x in range(W):
        u = x / W if cfg["side"] == "right" else 1 - x / W
        sd.line([(x, 0), (x, H)], fill=int(205 * max(0.0, (u - 0.25) / 0.75) ** 1.2))
    im = Image.composite(Image.new("RGB", (W, H), (6, 6, 8)), im, shade)
    d = ImageDraw.Draw(im)
    right = cfg["side"] == "right"
    margin = 64
    max_w = 700
    x = W - margin if right else margin
    # series badge
    ep = f"EP{cfg['ep']:02d}"
    fb = font(40)
    bw = d.textlength(ep, font=fb) + 36
    brand = "드론 전쟁 해부"
    fbr = font(30)
    brw = words_width(d, brand.split(), fbr, fbr.size * 0.28)
    bx = x - (bw + 18 + brw) if right else x
    d.rounded_rectangle((bx, 52, bx + bw, 112), radius=8, fill=ORANGE)
    d.text((bx + 18, 84), ep, font=fb, fill=(10, 10, 10), anchor="lm")
    draw_words(d, (bx + bw + 18, 68), brand, fbr, WHITE)
    # "real battlefield" tag in red
    ft = fit(d, cfg["tag"], 36, max_w - 36)
    tw_ = words_width(d, cfg["tag"].split(), ft, ft.size * 0.28)
    tx0 = x - tw_ - 36 if right else x
    d.rounded_rectangle((tx0, 134, tx0 + tw_ + 36, 190), radius=8, fill=(214, 40, 40))
    draw_words(d, (tx0 + 18, 143), cfg["tag"], ft, WHITE)
    # headline
    y = 228
    for i, line in enumerate(cfg["lines"]):
        f = fit(d, line, 150, max_w)
        draw_words(d, (x, y), line, f, ORANGE if i else WHITE, stroke=8, anchor_right=right)
        y += f.size + 30
    # sub line on a black bar
    fs = fit(d, cfg["sub"], 54, max_w)
    tw = words_width(d, cfg["sub"].split(), fs, fs.size * 0.28)
    y += 26
    x0 = x - tw - 24 if right else x - 24
    d.rectangle((x0, y - 16, x0 + tw + 48, y + fs.size + 22), fill=(0, 0, 0))
    draw_words(d, (x, y), cfg["sub"], fs, WHITE, anchor_right=right)
    out = Path(out_dir) / f"EP{cfg['ep']:02d}_thumbnail_KO.jpg"
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for cfg in EPISODES:
        print(make(cfg, out_dir))
