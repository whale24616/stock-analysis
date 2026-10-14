"""Drawing toolkit for the line-art (black background, white strokes, one orange accent) look.

Everything is drawn in 1920x1080 coordinates on a 2x supersampled canvas and
downscaled once per frame, so strokes come out anti-aliased with plain Pillow.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
SS = 2
BLACK = (8, 8, 9)
WHITE = (240, 240, 236)
GREY = (120, 120, 118)
DIM = (60, 60, 60)
ORANGE = (255, 138, 31)
RED = (235, 64, 52)

FONT_DIR = Path(__file__).resolve().parent / "fonts"
_fonts = {}


def font(kind, size):
    key = (kind, size)
    if key not in _fonts:
        if kind == "label":
            f = ImageFont.truetype(str(FONT_DIR / "Inter.ttf"), size)
            try:
                f.set_variation_by_name("Bold")
            except Exception:
                pass
        elif kind == "label_light":
            f = ImageFont.truetype(str(FONT_DIR / "Inter.ttf"), size)
            try:
                f.set_variation_by_name("Regular")
            except Exception:
                pass
        elif kind == "sub":
            # subtitle font: Gmarket Sans Bold when available (downloaded in the render sandbox),
            # otherwise Noto Sans KR ExtraBold (bundled, OFL)
            gm = FONT_DIR / "GmarketSansTTFBold.ttf"
            if gm.exists():
                f = ImageFont.truetype(str(gm), size)
            else:
                f = ImageFont.truetype(str(FONT_DIR / "NotoSansKR.ttf"), size)
                f.set_variation_by_axes([800])
        else:
            f = ImageFont.truetype(str(FONT_DIR / "NanumGothic-ExtraBold.ttf"), size)
        _fonts[key] = f
    return _fonts[key]


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_io(t):
    t = clamp(t)
    return 3 * t * t - 2 * t * t * t


def seg(s, start, length):
    """Eased 0..1 progress of an animation that starts at `start` seconds and lasts `length`."""
    if length <= 0:
        return 1.0 if s >= start else 0.0
    return ease((s - start) / length)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_pt(p, q, t):
    return (lerp(p[0], q[0], t), lerp(p[1], q[1], t))


def _partial(pts, prog):
    """Polyline truncated to `prog` (0..1) of its total length."""
    if prog >= 1:
        return list(pts)
    if prog <= 0 or len(pts) < 2:
        return pts[:1]
    lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    target = sum(lens) * prog
    out = [pts[0]]
    for i, L in enumerate(lens):
        if target <= L:
            out.append(lerp_pt(pts[i], pts[i + 1], target / L if L else 0))
            return out
        target -= L
        out.append(pts[i + 1])
    return out


class Canvas:
    def __init__(self, bg=BLACK, base=None):
        if base is not None:
            self.im = base.resize((W * SS, H * SS), Image.BILINEAR) if base.size != (W * SS, H * SS) else base.copy()
        else:
            self.im = Image.new("RGB", (W * SS, H * SS), bg)
        self.d = ImageDraw.Draw(self.im, "RGBA")

    # -- primitives (all coordinates in 1920x1080 space) --
    def _p(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def line(self, pts, w=5, col=WHITE, prog=1.0):
        pts = _partial(pts, prog)
        if len(pts) < 2:
            return
        self.d.line(self._p(pts), fill=col, width=int(w * SS), joint="curve")
        r = w * SS / 2
        for x, y in (self._p([pts[0]])[0], self._p([pts[-1]])[0]):
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=col)

    def dashed(self, pts, w=4, col=WHITE, dash=16, gap=14, offset=0.0, prog=1.0):
        pts = _partial(pts, prog)
        period = dash + gap
        dist = 0.0  # distance travelled along the path so far
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            L = math.dist(a, b)
            if L == 0:
                continue
            s = ((offset - dist) % period) - period
            while s < L:
                s0, s1 = max(s, 0), min(s + dash, L)
                if s1 > s0:
                    self.line([lerp_pt(a, b, s0 / L), lerp_pt(a, b, s1 / L)], w, col)
                s += period
            dist += L

    def arc(self, c, r, a0, a1, w=5, col=WHITE):
        x, y = c
        self.d.arc(((x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS), a0, a1, fill=col, width=int(w * SS))

    def circle(self, c, r, w=5, col=WHITE, fill=None, prog=1.0):
        x, y = c
        box = ((x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS)
        if fill is not None and prog >= 1:
            self.d.ellipse(box, fill=fill)
        if w and prog > 0:
            if prog >= 1:
                self.d.ellipse(box, outline=col, width=int(w * SS))
            else:
                self.d.arc(box, -90, -90 + 360 * prog, fill=col, width=int(w * SS))

    def dot(self, c, r, col=WHITE):
        self.circle(c, r, 0, fill=col)

    def rect(self, box, w=5, col=WHITE, fill=None, radius=14, prog=1.0):
        x0, y0, x1, y1 = box
        if prog < 1:
            pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
            self.line(pts, w, col, prog)
            return
        self.d.rounded_rectangle((x0 * SS, y0 * SS, x1 * SS, y1 * SS), radius=radius * SS,
                                 outline=col if w else None, width=int(w * SS), fill=fill)

    def poly(self, pts, fill=None, col=None, w=0):
        self.d.polygon(self._p(pts), fill=fill, outline=None)
        if col and w:
            self.line(list(pts) + [pts[0]], w, col)

    def arrow(self, p0, p1, w=5, col=WHITE, prog=1.0, head=22):
        if prog <= 0:
            return
        p1 = lerp_pt(p0, p1, prog)
        self.line([p0, p1], w, col)
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        for da in (2.6, -2.6):
            self.line([p1, (p1[0] + head * math.cos(ang + da), p1[1] + head * math.sin(ang + da))], w, col)

    def text(self, xy, s, size=40, col=WHITE, kind="label", anchor="mm", alpha=1.0):
        if alpha <= 0:
            return
        f = font(kind, size * SS)
        c = col if alpha >= 1 else col + (int(255 * alpha),)
        self.d.text((xy[0] * SS, xy[1] * SS), s, font=f, fill=c, anchor=anchor)

    def text_w(self, s, size, kind="label"):
        return self.d.textlength(s, font=font(kind, size * SS)) / SS

    def tag(self, xy, s, size=26, col=ORANGE, alpha=1.0):
        """Small outlined label, e.g. REPORTED / ESTIMATE source tags."""
        if alpha <= 0:
            return
        w = self.text_w(s, size) + 28
        x, y = xy
        c = col + (int(255 * alpha),)
        self.d.rounded_rectangle(((x - w / 2) * SS, (y - size * 0.8) * SS, (x + w / 2) * SS, (y + size * 0.8) * SS),
                                 radius=8 * SS, outline=c, width=3 * SS)
        self.text(xy, s, size, col, alpha=alpha)

    def finish(self):
        return self.im.resize((W, H), Image.LANCZOS)


# ---------------- icons ----------------

def drone_top(cv, c, s=1.0, col=WHITE, w=5, prog=1.0, wing_col=None, prop_spin=0.0):
    """Top view of a long-wing pusher drone pointing right."""
    x, y = c
    body = [(x - 150 * s, y), (x + 150 * s, y)]
    nose = [(x + 150 * s, y), (x + 170 * s, y)]
    wing = [(x + 10 * s, y - 230 * s), (x + 40 * s, y - 230 * s), (x + 50 * s, y), (x + 40 * s, y + 230 * s),
            (x + 10 * s, y + 230 * s), (x - 10 * s, y), (x + 10 * s, y - 230 * s)]
    tail = [(x - 135 * s, y - 70 * s), (x - 115 * s, y - 70 * s), (x - 105 * s, y), (x - 115 * s, y + 70 * s),
            (x - 135 * s, y + 70 * s)]
    cv.line(body, w, col, prog)
    cv.line(nose, w + 4, col, prog)
    cv.line(wing, w, wing_col or col, prog)
    cv.line(tail, w, col, prog)
    if prog >= 1:
        px = x - 160 * s
        a = prop_spin
        cv.line([(px, y - 40 * s * math.cos(a)), (px, y + 40 * s * math.cos(a))], w, col)


def drone_side(cv, c, s=1.0, col=WHITE, w=5, prog=1.0, prop_col=None, prop_spin=0.0):
    """Side view, nose to the right, pusher prop at the back."""
    x, y = c
    body = [(x - 170 * s, y - 6 * s), (x - 60 * s, y - 22 * s), (x + 120 * s, y - 22 * s), (x + 175 * s, y),
            (x + 120 * s, y + 18 * s), (x - 60 * s, y + 14 * s), (x - 170 * s, y + 4 * s)]
    wing = [(x - 20 * s, y - 22 * s), (x + 40 * s, y - 30 * s), (x + 60 * s, y - 22 * s)]
    fin = [(x - 150 * s, y - 6 * s), (x - 170 * s, y - 70 * s), (x - 140 * s, y - 70 * s), (x - 115 * s, y - 14 * s)]
    cv.line(body, w, col, prog)
    cv.line(wing, w, col, prog)
    cv.line(fin, w, col, prog)
    if prog >= 1:
        px = x - 182 * s
        h = 55 * s * abs(math.cos(prop_spin))
        cv.line([(px, y - h), (px, y + h)], w + 1, prop_col or col)


def stick_figure(cv, c, s=1.0, col=WHITE, w=5, magnifier=False, think=False, prog=1.0, look=1):
    """Simple stick character (head with hair tuft, eyes, tie)."""
    x, y = c
    r = 55 * s
    hy = y - 230 * s
    cv.circle((x, hy), r, w, col, prog=prog)
    if prog < 1:
        return
    # hair
    cv.line([(x - r * 0.9, hy - r * 0.35), (x - r * 0.4, hy - r * 1.05), (x + r * 0.2, hy - r * 0.85),
             (x + r * 0.8, hy - r * 0.95), (x + r * 0.95, hy - r * 0.3)], w, col)
    ex = 14 * s * look
    cv.circle((x - 18 * s + ex, hy), 9 * s, 0, fill=col)
    cv.circle((x + 18 * s + ex, hy), 9 * s, 0, fill=col)
    cv.line([(x - 12 * s + ex, hy + 28 * s), (x + 12 * s + ex, hy + 26 * s)], 3, col)
    neck = (x, hy + r)
    hip = (x, y + 40 * s)
    cv.line([neck, hip], w, col)
    cv.poly([(x, neck[1] + 10 * s), (x - 12 * s, neck[1] + 70 * s), (x, neck[1] + 110 * s),
             (x + 12 * s, neck[1] + 70 * s)], fill=col)
    cv.line([hip, (x - 40 * s, y + 200 * s)], w, col)
    cv.line([hip, (x + 40 * s, y + 200 * s)], w, col)
    sh = (x, neck[1] + 40 * s)
    if think:
        cv.line([sh, (x - 50 * s, sh[1] + 70 * s), (x - 5 * s, hy + r + 5 * s)], w, col)
    else:
        cv.line([sh, (x - 70 * s, sh[1] + 120 * s)], w, col)
    if magnifier:
        hand = (x + 90 * s * look, sh[1] + 60 * s)
        cv.line([sh, hand], w, col)
        mc = (hand[0] + 70 * s * look, hand[1] - 60 * s)
        cv.line([hand, lerp_pt(hand, mc, 0.45)], w + 6, col)
        cv.circle(mc, 60 * s, w + 2, col)
    else:
        cv.line([sh, (x + 70 * s, sh[1] + 120 * s)], w, col)


def car_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 120 * s, y + 20 * s), (x - 120 * s, y - 20 * s), (x - 70 * s, y - 25 * s), (x - 40 * s, y - 70 * s),
             (x + 50 * s, y - 70 * s), (x + 85 * s, y - 25 * s), (x + 120 * s, y - 15 * s), (x + 120 * s, y + 20 * s),
             (x - 120 * s, y + 20 * s)], w, col)
    cv.circle((x - 65 * s, y + 25 * s), 26 * s, w, col, fill=BLACK)
    cv.circle((x + 65 * s, y + 25 * s), 26 * s, w, col, fill=BLACK)


def missile_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 140 * s, y - 16 * s), (x + 110 * s, y - 16 * s), (x + 150 * s, y), (x + 110 * s, y + 16 * s),
             (x - 140 * s, y + 16 * s), (x - 140 * s, y - 16 * s)], w, col)
    cv.line([(x - 140 * s, y - 16 * s), (x - 170 * s, y - 50 * s), (x - 110 * s, y - 16 * s)], w, col)
    cv.line([(x - 140 * s, y + 16 * s), (x - 170 * s, y + 50 * s), (x - 110 * s, y + 16 * s)], w, col)


def jet_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x + 160 * s, y), (x + 60 * s, y - 18 * s), (x - 140 * s, y - 18 * s), (x - 160 * s, y),
             (x - 140 * s, y + 18 * s), (x + 60 * s, y + 18 * s), (x + 160 * s, y)], w, col)
    cv.line([(x + 30 * s, y - 18 * s), (x - 50 * s, y - 120 * s), (x - 90 * s, y - 120 * s), (x - 50 * s, y - 18 * s)], w, col)
    cv.line([(x + 30 * s, y + 18 * s), (x - 50 * s, y + 120 * s), (x - 90 * s, y + 120 * s), (x - 50 * s, y + 18 * s)], w, col)
    cv.line([(x - 120 * s, y - 18 * s), (x - 160 * s, y - 65 * s), (x - 140 * s, y - 18 * s)], w, col)


def factory_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 120 * s, y + 80 * s), (x - 120 * s, y - 20 * s), (x - 60 * s, y + 10 * s), (x - 60 * s, y - 20 * s),
             (x, y + 10 * s), (x, y - 20 * s), (x + 60 * s, y + 10 * s), (x + 60 * s, y - 100 * s),
             (x + 100 * s, y - 100 * s), (x + 100 * s, y + 80 * s), (x - 120 * s, y + 80 * s)], w, col)


def refinery_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 130 * s, y + 80 * s), (x + 130 * s, y + 80 * s)], w, col)
    for dx, h in ((-90, 150), (-40, 110), (60, 170)):
        cv.rect(((x + dx * s - 18 * s), y + 80 * s - h * s, (x + dx * s + 18 * s), y + 80 * s), w, col, radius=8)
    cv.circle((x + 10 * s, y + 40 * s), 40 * s, w, col)


def airbase_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 140 * s, y + 70 * s), (x + 140 * s, y + 30 * s)], w + 4, col)
    jet_icon(cv, (x, y - 30 * s), 0.55 * s, col, w)


def depot_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 120 * s, y + 80 * s), (x - 120 * s, y - 20 * s), (x, y - 90 * s), (x + 120 * s, y - 20 * s),
             (x + 120 * s, y + 80 * s), (x - 120 * s, y + 80 * s)], w, col)
    cv.rect((x - 40 * s, y + 10 * s, x + 40 * s, y + 80 * s), w, col, radius=4)


def satellite_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.rect((x - 30 * s, y - 30 * s, x + 30 * s, y + 30 * s), w, col, radius=6)
    cv.rect((x - 150 * s, y - 25 * s, x - 50 * s, y + 25 * s), w, col, radius=4)
    cv.rect((x + 50 * s, y - 25 * s, x + 150 * s, y + 25 * s), w, col, radius=4)
    cv.line([(x - 50 * s, y), (x - 30 * s, y)], w, col)
    cv.line([(x + 30 * s, y), (x + 50 * s, y)], w, col)
    cv.line([(x, y + 30 * s), (x, y + 60 * s)], w, col)


def tower_icon(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 50 * s, y + 120 * s), (x, y - 100 * s), (x + 50 * s, y + 120 * s)], w, col)
    cv.line([(x - 30 * s, y + 30 * s), (x + 30 * s, y + 30 * s)], w, col)
    for r in (40, 75):
        cv.arc((x, y - 100 * s), r * s, -60, -20, w, col)
        cv.arc((x, y - 100 * s), r * s, -160, -120, w, col)


def radar_dish(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.arc((x, y), 70 * s, 200, 340, w, col)
    cv.line([(x - 66 * s, y - 24 * s), (x + 66 * s, y - 24 * s)], w, col)
    cv.line([(x, y - 24 * s), (x, y + 80 * s)], w, col)
    cv.line([(x - 50 * s, y + 80 * s), (x + 50 * s, y + 80 * s)], w, col)


def clock_icon(cv, c, r, frac, col=WHITE, w=5, accent=ORANGE):
    cv.circle(c, r, w, col)
    for i in range(12):
        a = math.radians(i * 30)
        cv.line([(c[0] + (r - 18) * math.sin(a), c[1] - (r - 18) * math.cos(a)),
                 (c[0] + (r - 6) * math.sin(a), c[1] - (r - 6) * math.cos(a))], 3, col)
    a = 2 * math.pi * frac
    cv.line([c, (c[0] + (r - 30) * math.sin(a), c[1] - (r - 30) * math.cos(a))], w + 1, accent)
    a2 = 2 * math.pi * frac * 12
    cv.line([c, (c[0] + (r - 50) * 0.7 * math.sin(a2), c[1] - (r - 50) * 0.7 * math.cos(a2))], w, col)


def coin_stack(cv, c, n, s=1.0, col=WHITE, w=4):
    x, y = c
    for i in range(n):
        cy = y - i * 22 * s
        cv.d.ellipse(((x - 50 * s) * SS, (cy - 14 * s) * SS, (x + 50 * s) * SS, (cy + 14 * s) * SS),
                     fill=BLACK, outline=col, width=int(w * SS))


def cross(cv, c, r, col=RED, w=10, prog=1.0):
    x, y = c
    cv.line([(x - r, y - r), (x + r, y + r)], w, col, clamp(prog * 2))
    cv.line([(x + r, y - r), (x - r, y + r)], w, col, clamp(prog * 2 - 1))


def check(cv, c, r, col=ORANGE, w=10, prog=1.0):
    x, y = c
    cv.line([(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)], w, col, prog)


def sound_waves(cv, c, s, col, w, phase):
    for i in range(3):
        r = (40 + 40 * i + 30 * (phase % 1)) * s
        cv.arc(c, r, -40, 40, w, col)


def speedometer(cv, c, r, value, vmax, col=WHITE, accent=ORANGE, w=5, band=None):
    """Half-dial gauge. `band` = (lo, hi) highlighted range."""
    cv.arc(c, r, 180, 360, w, col)
    if band:
        a0 = 180 + 180 * band[0] / vmax
        a1 = 180 + 180 * band[1] / vmax
        cv.arc(c, r - 16, a0, a1, 14, accent)
    for i in range(11):
        a = math.pi + math.pi * i / 10
        cv.line([(c[0] + (r - 30) * math.cos(a), c[1] + (r - 30) * math.sin(a)),
                 (c[0] + (r - 4) * math.cos(a), c[1] + (r - 4) * math.sin(a))], 3, col)
    a = math.pi + math.pi * clamp(value / vmax)
    cv.line([c, (c[0] + (r - 40) * math.cos(a), c[1] + (r - 40) * math.sin(a))], w + 2, accent)
    cv.dot(c, 12, col)
