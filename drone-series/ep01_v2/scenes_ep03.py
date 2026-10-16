"""EP03 line-art scenes ("The $500 Killer"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math
import random

from gfx import (DIM, GREY, ORANGE, RED, WHITE, car_icon, check, clamp, clock_icon, coin_stack, cross, drone_side,
                 ease, ease_io, lerp, lerp_pt, seg, tower_icon)
from scenes import BG, BG_O, CX, CY, backdrop, end_card, title_card


# ---------------- icons ----------------

def quad_top(cv, c, s=1.0, col=WHITE, w=5, spin=0.0, prog=1.0, prop_col=None):
    """Top view of an FPV quadcopter: X frame, four motors with spinning props, camera nose to the right."""
    x, y = c
    arms = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    r = 95 * s
    for i, (dx, dy) in enumerate(arms):
        p = (x + dx * r * 0.72, y + dy * r * 0.72)
        cv.line([(x, y), p], w + 2, col, prog)
        if prog >= 1:
            cv.circle(p, 13 * s, w - 1, col)
            a = spin * (1 if i % 2 else -1) + i
            pr = 46 * s
            pc = prop_col or GREY
            cv.line([(p[0] - pr * math.cos(a), p[1] - pr * math.sin(a)),
                     (p[0] + pr * math.cos(a), p[1] + pr * math.sin(a))], 3, pc)
            cv.circle(p, pr, 2, DIM)
    if prog >= 1:
        cv.rect((x - 34 * s, y - 20 * s, x + 34 * s, y + 20 * s), w - 1, col, radius=6)
        cv.rect((x + 34 * s, y - 9 * s, x + 50 * s, y + 9 * s), w - 2, ORANGE, radius=3)


def quad_side(cv, c, s=1.0, col=WHITE, w=5, spin=0.0, tilt=0.0, flip=False):
    """Side view of an FPV quad (camera on the leading side). tilt in radians, nose down = positive."""
    x, y = c
    d = -1 if flip else 1
    ca, sa = math.cos(tilt * d), math.sin(tilt * d)

    def P(dx, dy):
        dx *= d
        return (x + (dx * ca - dy * sa) * s, y + (dx * sa + dy * ca) * s)

    cv.line([P(-120, 0), P(120, 0)], w + 3, col)  # arms
    body = [P(-45, -40), P(45, -40), P(50, 12), P(-50, 12), P(-45, -40)]
    cv.line(body, w, col)
    cv.line([P(-38, 20), P(38, 20)], w + 4, GREY)  # battery strap
    cam = P(62, -14)
    cv.circle(cam, 13 * s, w - 1, ORANGE)
    cv.line([P(50, -14), P(66, -14)], w - 1, ORANGE)
    for mx in (-112, 112):
        cv.line([P(mx - 12, -6), P(mx + 12, -6), P(mx + 12, -26), P(mx - 12, -26), P(mx - 12, -6)], w - 1, col)
        h = 62 * (0.35 + 0.65 * abs(math.cos(spin + mx)))
        cv.line([P(mx - h, -34), P(mx + h, -34)], 4, GREY)
        cv.line([P(mx, -26), P(mx, -36)], 3, col)


def goggles(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.rect((x - 90 * s, y - 40 * s, x + 90 * s, y + 40 * s), w, col, radius=22)
    cv.line([(x - 10 * s, y + 40 * s), (x, y + 22 * s), (x + 10 * s, y + 40 * s)], w, col)
    cv.line([(x - 90 * s, y), (x - 130 * s, y - 6 * s)], w, col)
    cv.line([(x + 90 * s, y), (x + 130 * s, y - 6 * s)], w, col)


def controller(cv, c, s=1.0, col=WHITE, w=5, t=0.0):
    x, y = c
    cv.rect((x - 110 * s, y - 55 * s, x + 110 * s, y + 55 * s), w, col, radius=24)
    for k, sx in enumerate((-55, 55)):
        cv.circle((x + sx * s, y), 26 * s, 3, GREY)
        cv.dot((x + sx * s + 12 * s * math.sin(t * 2 + k), y + 12 * s * math.cos(t * 1.6 + k)), 8 * s, col)
    cv.line([(x + 90 * s, y - 55 * s), (x + 110 * s, y - 120 * s)], w, col)


def waves(cv, c, s, col, w, phase, a0=-40, a1=40, n=3):
    for i in range(n):
        r = (30 + 34 * i + 28 * (phase % 1)) * s
        cv.arc(c, r, a0, a1, w, col)


def noise(cv, box, amount, seed):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(int(900 * amount)):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        v = rnd.randint(60, 230)
        cv.line([(x, y), (x + rnd.uniform(2, 14), y)], 2, (v, v, v))


def big_word(cv, s, word, col=ORANGE, size=150, kind="grid"):
    backdrop(cv, s, kind)
    sc = 1 + 0.25 * (1 - seg(s, 0, 0.35))
    cv.text((CX, CY), word, int(size * sc), col)


# ---------------- cold open ----------------

def e3_scale(cv, s, T, ph=0):
    backdrop(cv, s, "map")
    cv.text((CX, 170), "HOW FAR THEY FLY", 34, GREY, alpha=seg(s, 0, 0.3))
    rows = [("LONG-RANGE DRONE (EP1)", 1500, WHITE), ("JET MISSILE-DRONE (EP2)", 700, WHITE), ("FPV DRONE", 15, ORANGE)]
    for i, (lab, km, col) in enumerate(rows):
        y = 320 + i * 150
        p = seg(s, 0.2 + i * 0.35, 0.7)
        cv.text((560, y), lab, 30, col, anchor="rm")
        cv.rect((600, y - 28, 600 + max(10, 0.7 * km) * p, y + 28), 0, fill=col, radius=6)
        cv.text((620 + max(10, 0.7 * km) * p, y), f"{km:,} KM" if i < 2 else "A FEW KM", 28, col, anchor="lm",
                alpha=seg(s, 0.6 + i * 0.35, 0.3))


def e3_fpv_fly(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ground = 640
    rnd = random.Random(2)
    off = (s * 900) % 240
    for i in range(12):
        x = i * 240 - off
        cv.line([(x, ground), (x + 120, ground)], 4, GREY)
        cv.line([(x + 60, ground + 40), (x + 100, ground + 40)], 3, DIM)
    for i in range(6):
        x = (rnd.uniform(0, 1920) - s * 700) % 2100 - 90
        cv.line([(x, ground), (x - 10, ground - 40), (x + 10, ground - 55)], 3, DIM)
    y = ground - 90 + 6 * math.sin(s * 7)
    quad_side(cv, (CX, y), 2.0, spin=s * 40, tilt=0.25)
    for i in range(5):
        cv.line([(CX - 180 - i * 60, y - 20 + i * 10), (CX - 140 - i * 60 - 160, y - 20 + i * 10)], 3, GREY)
    cv.text((CX, 260), "100+ KM/H · METRES ABOVE THE GROUND", 32, ORANGE, alpha=seg(s, 0.3, 0.4))


def e3_goggle_view(cv, s, T, ph=0):
    """First-person view inside goggles. ph1 = jammed (static)."""
    box = (360, 150, 1560, 800)
    x0, y0, x1, y1 = box
    hz = 470 + 40 * math.sin(s * 0.8)
    roll = 0.08 * math.sin(s * 1.3)
    cv.line([(x0, hz - (CX - x0) * roll), (x1, hz + (x1 - CX) * roll)], 4, GREY)
    for i in range(1, 9):  # ground lines rushing toward the viewer
        k = ((i + s * 2.2) % 9) / 9
        yy = lerp(hz + 10, y1 - 10, k ** 2)
        cv.line([(lerp(CX - 40, x0, k), yy), (lerp(CX + 40, x1, k), yy)], 2, DIM)
    cv.line([(CX - 30, 470), (CX + 30, 470)], 3, ORANGE)
    cv.line([(CX, 440), (CX, 500)], 3, ORANGE)
    cv.text((x0 + 30, y0 + 40), "REC", 24, RED, anchor="lm")
    cv.text((x1 - 30, y0 + 40), f"{int(110 + 6 * math.sin(s * 2))} KM/H", 24, WHITE, anchor="rm")
    cv.text((x1 - 30, y1 - 40), "BAT 78%", 22, GREY, anchor="rm")
    if ph:
        noise(cv, box, clamp(0.2 + s / 2.0), int(s * 24))
        cv.text((CX, 470), "SIGNAL LOST", 54, RED, alpha=seg(s, 1.0, 0.3))
    cv.rect(box, 8, WHITE, radius=60)
    cv.text((CX, 845), "WHAT THE PILOT SEES", 28, GREY, alpha=seg(s, 0.2, 0.3))


def e3_price(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    quad_top(cv, (CX - 360, CY - 20), 1.3, spin=s * 25)
    cv.text((CX - 360, CY + 190), "FPV DRONE", 34, WHITE)
    cv.text((CX, CY - 20), "≈", 90, GREY, alpha=seg(s, 0.4, 0.3))
    a = seg(s, 0.6, 0.4)
    if a > 0:
        cv.rect((CX + 300, CY - 170, CX + 420, CY + 130), 6, WHITE, radius=20)
        cv.line([(CX + 340, CY - 145), (CX + 380, CY - 145)], 4, WHITE)
        cv.dot((CX + 360, CY + 105), 9, WHITE)
        cv.text((CX + 360, CY + 190), "SMARTPHONE", 34, WHITE, alpha=a)
    cv.text((CX, 250), "~ $400", 90, ORANGE, alpha=seg(s, 0.1, 0.3))


def e3_fiber_vs_jam(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    tower = (360, 560)
    tower_icon(cv, (tower[0], tower[1] - 60), 0.9, RED)
    for k in range(4):
        waves(cv, (tower[0] + 40, tower[1] - 160), 1.5, RED, 4, s * 1.2 + k * 0.25, -30, 30, 1)
    pts = [(1650 - i * 60, 380 + 30 * math.sin(i * 0.6 + s)) for i in range(20)]
    cv.line(pts, 3, ORANGE, prog=seg(s, 0.1, 1.0))
    quad_side(cv, (1600, 380), 1.4, spin=s * 40, tilt=0.15)
    cv.text((1100, 260), "GLASS THREAD", 30, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.text((tower[0], tower[1] + 110), "JAMMER", 30, RED)
    check(cv, (1100, 560), 40, ORANGE, 10, seg(s, 1.0, 0.4))
    cv.text((1100, 650), "CAN'T BE JAMMED", 36, ORANGE, alpha=seg(s, 1.2, 0.3))


def e3_intro(cv, s, T, ph=0):
    backdrop(cv, s, "drones")
    quad_top(cv, (CX, CY - 60), 1.6, spin=s * 30)
    cv.text((CX, CY + 160), "FPV DRONES", 46, ORANGE, alpha=seg(s, 0.3, 0.4))
    cv.text((CX, CY + 225), "HOW THEY WORK · WHY THEY CHANGED THE WAR", 30, WHITE, alpha=seg(s, 0.8, 0.4))


def e3_title(cv, s, T, ph=0):
    title_card(cv, s, "EP03  ·  THE $500 KILLER", "drones")


# ---------------- background ----------------

def e3_spotter(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ground = 700
    cv.line([(150, ground), (1770, ground)], 4, GREY)
    d = (900, 260)
    quad_side(cv, d, 1.1, spin=s * 40)
    cv.poly([d, (1150, ground), (1350, ground)], fill=(255, 138, 31, 40))
    cv.dot((1250, ground - 20), 14, RED)
    cv.text((1250, ground + 50), "TARGET", 26, RED)
    gun = (300, ground - 30)
    cv.rect((gun[0] - 60, gun[1] - 20, gun[0] + 60, gun[1] + 30), 4, WHITE, radius=6)
    cv.line([gun, (gun[0] + 80, gun[1] - 70)], 8, WHITE)
    cv.text((gun[0], ground + 50), "ARTILLERY", 26, WHITE)
    p = seg(s, 0.6, 1.2)
    arc = [(lerp(gun[0] + 80, 1250, t / 30), gun[1] - 70 - 380 * math.sin(math.pi * t / 30) * 0.9 +
            (ground - 20 - gun[1] + 70) * t / 30) for t in range(31)]
    cv.dashed(arc, 4, ORANGE, offset=s * 40, prog=p)
    cv.text((d[0], d[1] - 90), "THE EYES", 34, ORANGE, alpha=seg(s, 0.2, 0.3))


def e3_idea(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    quad_top(cv, (CX - 260, CY), 1.3, spin=s * 25)
    cv.text((CX + 40, CY), "=", 100, GREY, alpha=seg(s, 0.2, 0.3))
    if ph == 0:
        cv.text((CX + 300, CY), "?", 200, ORANGE, alpha=seg(s, 0.4, 0.3))
    else:
        cv.text((CX + 330, CY), "WEAPON", 90, ORANGE, alpha=seg(s, 0.1, 0.3))
    cv.text((CX, 820 - 40), "WHAT IF THE DRONE ITSELF WERE THE WEAPON?", 32, WHITE, alpha=seg(s, 0.5, 0.4))


def e3_race_gates(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    gates = [(420, 600), (760, 420), (1100, 560), (1440, 380)]
    for i, (x, y) in enumerate(gates):
        cv.rect((x - 70, y - 90, x + 70, y + 90), 6, ORANGE if i % 2 else WHITE, radius=10)
    path = []
    for t in range(61):
        u = t / 60
        path.append((lerp(260, 1660, u), 520 + 120 * math.sin(u * 9.4 + 0.6)))
    k = int(60 * clamp((s % 3.0) / 3.0))
    cv.dashed(path[:k + 1], 3, GREY, offset=s * 40)
    if k:
        quad_top(cv, path[k], 0.45, spin=s * 40)
    cv.text((CX, 200), "HOBBY DRONE RACING", 44, WHITE, alpha=seg(s, 0.1, 0.3))


def e3_fpv_letters(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    words = (("F", "IRST"), ("P", "ERSON"), ("V", "IEW"))
    for i, (a, b) in enumerate(words):
        y = 300 + i * 130
        cv.text((640, y), a, 110, ORANGE, anchor="lm")
        cv.text((730, y + 12), b, 70, WHITE, anchor="lm", alpha=seg(s, 0.3 + i * 0.3, 0.3))
    goggles(cv, (1450, 420), 1.4)
    cv.line([(1450, 480), (1450, 640)], 3, GREY)
    cv.text((1450, 690), "SEE THROUGH THE DRONE", 28, ORANGE, alpha=seg(s, 1.2, 0.3))


def _front(cv, s, depth_px, label=None, a=1.0):
    y0, y1 = 150, 820
    xs = [CX + 30 * math.sin(y / 120) for y in range(y0, y1 + 1, 20)]
    pts = list(zip(xs, range(y0, y1 + 1, 20)))
    for side in (-1, 1):
        band = pts + [(x + side * depth_px, y) for x, y in reversed(pts)]
        cv.poly(band, fill=(235, 64, 52, int(55 * a)))
        edge = [(x + side * depth_px, y) for x, y in pts]
        cv.dashed(edge, 3, RED, offset=s * 30)
    cv.line(pts, 6, WHITE)
    cv.text((CX - 520, 180), "UKRAINE", 32, GREY)
    cv.text((CX + 520, 180), "RUSSIA", 32, GREY)
    rnd = random.Random(7)
    for i in range(10):
        x = CX + rnd.uniform(-depth_px, depth_px)
        y = rnd.uniform(220, 780)
        quad_top(cv, (x + 10 * math.sin(s * 2 + i), y), 0.18, RED, 3, spin=s * 30)
    if label:
        cv.text((CX, 860 - 30), label, 34, ORANGE)


def e3_killzone(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    if ph == 0:
        _front(cv, s, 140 * seg(s, 0, 1.0), None)
        cv.text((CX, 120), "THE KILL ZONE", 44, RED, alpha=seg(s, 0.4, 0.3))
    else:
        d = lerp(140, 420, seg(s, 0.1, 1.2))
        _front(cv, s, d)
        cv.arrow((CX, 470), (CX + d, 470), 5, ORANGE, seg(s, 1.0, 0.4))
        cv.arrow((CX, 520), (CX - d, 520), 5, ORANGE, seg(s, 1.0, 0.4))
        cv.text((CX + d / 2, 430), "25+ KM", 40, ORANGE, alpha=seg(s, 1.2, 0.3))
        cv.text((CX - d / 2, 480 + 80), "25+ KM", 40, ORANGE, alpha=seg(s, 1.2, 0.3))


# ---------------- anatomy ----------------

def e3_anatomy(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c = (CX, CY - 10)
    quad_top(cv, c, 2.6, spin=s * 30, prog=seg(s, 0, 1.0) if ph == 0 else 1)
    if ph >= 1:
        labs = [((CX - 420, 230), "4 ARMS"), ((CX + 420, 230), "4 PROPELLERS"), ((CX - 420, 720), "1 BATTERY"),
                ((CX + 420, 720), "CAMERA")]
        for i, (p, t) in enumerate(labs):
            cv.text(p, t, 34, WHITE, alpha=seg(s, 0.1 + i * 0.25, 0.3))
    if ph >= 2:
        cv.text((CX, 120), "CARBON FIBRE FRAME", 40, ORANGE, alpha=seg(s, 0.1, 0.3))
        for k in range(3):
            cv.text((CX + (k - 1) * 330, 840 - 30), ("LIGHT", "STIFF", "CHEAP")[k], 36, ORANGE,
                    alpha=seg(s, 0.6 + k * 0.4, 0.3))


def e3_vibration(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i, (x, stiff) in enumerate(((CX - 420, False), (CX + 420, True))):
        amp = 4 if stiff else 26
        pts = [(x - 260 + k * 26, 380 + amp * math.sin(k * 0.9 + s * 22) * math.sin(math.pi * k / 20))
               for k in range(21)]
        cv.line(pts, 8, WHITE if stiff else GREY)
        sig = [(x - 220 + k * 22, 600 + (4 if stiff else 30) * math.sin(k * 1.7 + s * 18) * (1 if stiff else
               random.Random(k + int(s * 10)).uniform(0.4, 1.2))) for k in range(21)]
        cv.line(sig, 4, ORANGE if stiff else RED)
        cv.text((x, 260), "STIFF FRAME" if stiff else "BENDY FRAME", 36, WHITE)
        cv.text((x, 700), "CLEAN SENSOR SIGNAL" if stiff else "CONFUSED SENSORS", 28, ORANGE if stiff else RED,
                alpha=seg(s, 0.5 + i * 0.4, 0.3))


def e3_motor(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c, R = (CX - 220, CY), 220
    cv.circle(c, R, 6, WHITE)
    cv.circle(c, R - 60, 4, GREY)
    n = 12
    active = int(s * 8) % n
    for i in range(n):
        a = 2 * math.pi * i / n
        p = (c[0] + (R - 95) * math.cos(a), c[1] + (R - 95) * math.sin(a))
        on = ph >= 1 and i % 3 == active % 3
        cv.circle(p, 22, 4, ORANGE if on else GREY, fill=(90, 50, 15) if on else None)
    rot = s * (12 if ph == 0 else 4)
    for i in range(14):
        a = rot + 2 * math.pi * i / 14
        cv.line([(c[0] + (R - 8) * math.cos(a), c[1] + (R - 8) * math.sin(a)),
                 (c[0] + (R + 14) * math.cos(a), c[1] + (R + 14) * math.sin(a))], 6, WHITE)
    cv.dot(c, 16, WHITE)
    if ph == 0:
        cv.text((CX + 330, CY - 40), "TENS OF THOUSANDS", 46, ORANGE, anchor="lm", alpha=seg(s, 0.3, 0.3))
        cv.text((CX + 330, CY + 30), "OF TURNS A MINUTE", 36, WHITE, anchor="lm", alpha=seg(s, 0.6, 0.3))
    else:
        cv.text((CX + 330, CY - 40), "SPEED CONTROLLER", 44, ORANGE, anchor="lm", alpha=seg(s, 0.2, 0.3))
        cv.text((CX + 330, CY + 30), "POWERS THE COILS IN ORDER", 32, WHITE, anchor="lm", alpha=seg(s, 0.5, 0.3))


def e3_swing(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    pivot = (CX - 200, 200)
    L = 420
    a = 0.6 * math.sin(s * 3.2)
    seat = (pivot[0] + L * math.sin(a), pivot[1] + L * math.cos(a))
    cv.line([(pivot[0] - 260, pivot[1]), (pivot[0] + 260, pivot[1])], 6, WHITE)
    cv.line([pivot, seat], 4, WHITE)
    cv.rect((seat[0] - 50, seat[1] - 8, seat[0] + 50, seat[1] + 12), 4, WHITE, radius=4)
    push = math.cos(s * 3.2) > 0.85
    if push:
        cv.arrow((seat[0] - 200, seat[1]), (seat[0] - 70, seat[1]), 8, ORANGE, 1.0, 26)
    cv.text((CX + 420, CY - 40), "PUSH AT THE", 40, WHITE, anchor="mm", alpha=seg(s, 0.3, 0.3))
    cv.text((CX + 420, CY + 30), "RIGHT MOMENT", 50, ORANGE, alpha=seg(s, 0.5, 0.3))
    cv.text((CX + 420, CY + 120), "× THOUSANDS PER SECOND", 32, GREY, alpha=seg(s, 0.9, 0.3))


def e3_gyro(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c = (CX - 250, CY)
    cv.rect((c[0] - 170, c[1] - 170, c[0] + 170, c[1] + 170), 6, WHITE, radius=16)
    cv.rect((c[0] - 50, c[1] - 50, c[0] + 50, c[1] + 50), 4, ORANGE, radius=6)
    for k in range(4):
        cv.dot((c[0] - 140 + 280 * (k % 2), c[1] - 140 + 280 * (k // 2)), 10, GREY)
    a = 0.4 * math.sin(s * 2.4)
    for r in (110,):
        cv.arc(c, r, -90 + math.degrees(a) - 30, -90 + math.degrees(a) + 30, 5, ORANGE)
    cv.text((CX + 250, CY - 60), "FLIGHT CONTROLLER", 44, WHITE, alpha=seg(s, 0.1, 0.3))
    cv.text((CX + 250, CY + 10), "FEELS TILT · FEELS SHAKING", 32, ORANGE, alpha=seg(s, 0.5, 0.3))


def e3_balance(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    if ph == 0:
        tilt = min(0.9, 0.05 * math.exp(s * 1.2))
        quad_side(cv, (CX, CY - 40), 1.6, spin=s * 40, tilt=tilt)
        cv.text((CX, 760), "NATURALLY UNSTABLE", 44, RED, alpha=seg(s, 0.6, 0.3))
        return
    tilt = 0.12 * math.sin(s * 6)
    quad_side(cv, (CX - 300, CY - 60), 1.4, spin=s * 40, tilt=tilt)
    ox = CX + 200
    for i in range(4):
        h = 120 + 70 * math.sin(s * 9 + i * 1.7)
        cv.rect((ox + i * 110, 600 - h, ox + i * 110 + 70, 600), 0, fill=ORANGE if i % 2 else WHITE, radius=6)
        cv.text((ox + i * 110 + 35, 640), f"M{i + 1}", 26, GREY)
    cv.text((ox + 200, 300), "HUNDREDS OF", 36, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.text((ox + 200, 350), "CORRECTIONS A SECOND", 36, ORANGE, alpha=seg(s, 0.4, 0.3))


def e3_pilot_vs_computer(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    controller(cv, (CX - 380, CY - 30), 1.3, t=s)
    cv.text((CX - 380, CY + 130), "PILOT", 36, WHITE)
    cv.text((CX - 380, CY + 190), "DIRECTION", 44, ORANGE, alpha=seg(s, 0.3, 0.3))
    c = (CX + 380, CY - 30)
    cv.rect((c[0] - 90, c[1] - 90, c[0] + 90, c[1] + 90), 6, WHITE, radius=12)
    for k in range(5):
        for side in (-1, 1):
            cv.line([(c[0] - 70 + k * 35, c[1] + side * 90), (c[0] - 70 + k * 35, c[1] + side * 115)], 4, GREY)
    cv.text((c[0], c[1] + 160), "COMPUTER", 36, WHITE)
    cv.text((c[0], c[1] + 220), "BALANCE", 44, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.text((CX, CY - 30), "+", 90, GREY)


def e3_links(cv, s, T, ph=0):
    """Two radio links. ph0 video only, ph1 control only, ph2 both, ph3 both = weak point."""
    backdrop(cv, s, "grid")
    d = (1450, 360)
    quad_side(cv, d, 1.4, spin=s * 40, flip=True)
    goggles(cv, (440, 500), 0.9)
    controller(cv, (440, 680), 0.8, t=s)
    vid = ph in (0, 2, 3)
    ctl = ph in (1, 2, 3)
    bad = ph == 3
    if vid:
        col = RED if bad else ORANGE
        cv.dashed([(1380, 380), (560, 490)], 5, col, offset=-s * 120)
        cv.text((980, 380), "VIDEO →  GOGGLES", 30, col, anchor="mm")
    if ctl:
        col = RED if bad else WHITE
        cv.dashed([(560, 660), (1380, 420)], 5, col, offset=s * 120)
        cv.text((1020, 600), "STICKS →  DRONE", 30, col)
    if bad:
        cv.text((CX, 170), "THE WEAK POINT", 50, RED, alpha=seg(s, 0.2, 0.3))
    elif ph == 2:
        cv.text((CX, 170), "TWO RADIO LINKS", 46, WHITE, alpha=seg(s, 0.1, 0.3))


# ---------------- supply chain ----------------

PARTS = ("MOTORS", "CAMERAS", "BATTERIES", "BOARDS")


def e3_supply(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i, p in enumerate(PARTS):
        y = 250 + i * 140
        cv.rect((260, y - 45, 560, y + 45), 4, WHITE, radius=10)
        cv.text((410, y), p, 30, WHITE)
        cv.dashed([(560, y), (1180, CY)], 3, GREY, offset=s * 60, prog=seg(s, 0.2 + i * 0.15, 0.6))
        u = (s * 0.6 + i * 0.25) % 1.0
        cv.dot(lerp_pt((560, y), (1180, CY), u), 7, ORANGE)
    quad_top(cv, (1380, CY), 1.3, spin=s * 30)
    if ph >= 1:
        cv.text((CX, 130), "MADE BY THE MILLIONS · MANY IN CHINA", 34, ORANGE, alpha=seg(s, 0.1, 0.3))
    if ph >= 2:
        for k, t in enumerate(("CHEAP", "STANDARD", "EASY TO SWAP")):
            cv.tag((560 + k * 400, 820), t, 32, alpha=seg(s, 0.2 + k * 0.3, 0.3))


def e3_crowdfund(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    coin_stack(cv, (420, 600), int(1 + 7 * seg(s, 0, 1.0)), 1.2, ORANGE)
    cv.text((420, 700), "DONATIONS", 30, WHITE)
    cv.arrow((560, 470), (780, 470), 5, GREY, seg(s, 0.5, 0.4))
    for k in range(4):
        cv.rect((830 + (k % 2) * 110, 380 + (k // 2) * 110, 920 + (k % 2) * 110, 460 + (k // 2) * 110), 4,
                WHITE, radius=8)
    cv.text((935, 700), "PARTS", 30, WHITE)
    cv.arrow((1100, 470), (1320, 470), 5, GREY, seg(s, 1.0, 0.4))
    quad_top(cv, (1500, 470), 1.0, spin=s * 30)
    cv.text((1500, 700), "BUILT BY VOLUNTEERS", 30, ORANGE, alpha=seg(s, 1.4, 0.3))


def e3_supply_bars(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    base = 760
    v24 = 1.2
    v25 = 3.0
    sc = 150
    cv.rect((CX - 330, base - v24 * sc * seg(s, 0.1, 0.6), CX - 110, base), 0, fill=(130, 130, 130), radius=6)
    cv.text((CX - 220, base + 40), "2024", 32, WHITE)
    if ph >= 1:
        cv.rect((CX + 110, base - v25 * sc * seg(s, 0.1, 0.8), CX + 330, base), 0, fill=ORANGE, radius=6)
        cv.text((CX + 220, base + 40), "2025", 32, WHITE)
        cv.text((CX + 220, base - v25 * sc - 50), "~3 MILLION", 50, ORANGE, alpha=seg(s, 0.8, 0.3))
    if ph >= 2:
        cv.arrow((CX - 100, base - v24 * sc - 30), (CX + 90, base - v25 * sc + 40), 5, WHITE, seg(s, 0.1, 0.5))
        cv.text((CX, base - 260 - 160), "× 2.5", 70, WHITE, alpha=seg(s, 0.4, 0.3))
    cv.text((CX, 140), "FPV DRONES SUPPLIED TO UKRAINE'S MILITARY", 32, GREY)


def e3_both_sides(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i, (x, lab) in enumerate(((CX - 400, "UKRAINE"), (CX + 400, "RUSSIA"))):
        cv.text((x, 230), lab, 40, WHITE)
        n = int(1 + 11 * seg(s, 0.2 + i * 0.2, 1.4))
        for k in range(n):
            quad_top(cv, (x - 220 + (k % 4) * 145, 360 + (k // 4) * 140), 0.38, ORANGE if i == 0 else RED, 3,
                     spin=s * 25)
    cv.line([(CX, 200), (CX, 780)], 3, DIM)


def e3_axes(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    labs = ("SPEED", "ANGLE", "HEIGHT")
    for i, lab in enumerate(labs):
        y = 300 + i * 150
        cv.text((640, y), lab, 40, WHITE, anchor="rm")
        cv.line([(700, y), (1300, y)], 4, GREY)
        move = ph >= 1 or i == 0
        v = 0.5 + 0.4 * math.sin(s * (2.2 + i * 0.9) + i) if move else 0.5
        cv.dot((lerp(700, 1300, v), y), 18, ORANGE)
    cv.text((CX, 780), "ALL AT ONCE" if ph else "FLYING FPV IS HARD", 46, ORANGE, alpha=seg(s, 0.4, 0.3))


def e3_formula(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    items = ("CHEAP PARTS", "MASS PRODUCTION", "SKILLED PILOTS")
    for i, it in enumerate(items):
        x = 360 + i * 480
        a = seg(s, 0.1 + i * 0.3, 0.3) if ph == 0 else 1
        cv.rect((x - 200, 300, x + 200, 440), 4, WHITE, radius=12)
        cv.text((x, 370), it, 32, WHITE, alpha=a)
        if i < 2:
            cv.text((x + 240, 370), "+", 60, GREY)
    if ph >= 1:
        cv.text((CX, 560), "= THE FPV FORMULA", 60, ORANGE, alpha=seg(s, 0.1, 0.3))
    if ph >= 2:
        cv.text((CX, 700), "ONE WEAKNESS", 48, RED, alpha=seg(s, 0.2, 0.3))


def e3_word_radio(cv, s, T, ph=0):
    big_word(cv, s, "RADIO", RED, 170, "radar")
    for k in range(2):
        waves(cv, (CX + 330, CY - 10), 1.6, RED, 5, s * 1.4 + k * 0.5, -40, 40, 2)
        waves(cv, (CX - 330, CY - 10), 1.6, RED, 5, s * 1.4 + k * 0.5, 140, 220, 2)


# ---------------- jamming / fibre / AI ----------------

def e3_jam(cv, s, T, ph=0):
    """ph0 jammer shouts, ph1 louder than pilot, ph2 jamming works on radio but not on fibre."""
    backdrop(cv, s, "grid")
    if ph < 2:
        quad_side(cv, (CX, 330), 1.5, spin=s * 40)
        controller(cv, (330, 640), 0.8, t=s)
        tower_icon(cv, (1590, 580), 0.9, RED)
        waves(cv, (450, 560), 1.0, WHITE, 3, s, -60, -20, 2)
        for k in range(3):
            waves(cv, (1560, 470), 1.8 + ph * 0.6, RED, 5, s * 1.5 + k * 0.33, 190, 250, 1)
        cv.text((330, 760), "PILOT", 30, WHITE)
        cv.text((1590, 760), "JAMMER", 30, RED)
        if ph == 1:
            for i, (lab, v, col) in enumerate((("PILOT", 0.25, WHITE), ("JAMMER", 0.9, RED))):
                y = 150 + i * 60
                cv.text((640, y), lab, 26, col, anchor="rm")
                cv.rect((660, y - 18, 660 + 600 * v * seg(s, 0.2, 0.6), y + 18), 0, fill=col, radius=4)
        else:
            cv.text((CX, 180), "JUST SHOUT LOUDER", 44, RED, alpha=seg(s, 0.3, 0.3))
        return
    for i, (x, fibre) in enumerate(((CX - 420, False), (CX + 420, True))):
        quad_side(cv, (x, 380), 1.3, spin=s * 40)
        if fibre:
            cv.line([(x - 100, 390), (x - 380, 520)], 3, ORANGE)
            check(cv, (x, 600), 40, ORANGE, 10, seg(s, 0.5, 0.4))
            cv.text((x, 700), "FIBRE: NOT AFFECTED", 32, ORANGE)
        else:
            waves(cv, (x + 150, 380), 1.0, RED, 4, s * 1.5, 150, 210, 3)
            cross(cv, (x, 600), 40, RED, 10, seg(s, 0.3, 0.4))
            cv.text((x, 700), "RADIO: JAMMED", 32, RED)
    cv.text((CX, 180), "JAMMING STILL WORKS ON RADIO DRONES", 36, WHITE, alpha=seg(s, 0.1, 0.3))


def e3_signal_dist(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ox, oy, w, h = 380, 720, 1160, 480
    cv.line([(ox, oy - h), (ox, oy), (ox + w, oy)], 4, WHITE)
    cv.text((ox + w, oy + 40), "PILOT  →  TARGET", 28, GREY, anchor="rm")
    cv.text((ox - 20, oy - h), "SIGNAL", 26, GREY, anchor="rm")
    pil = [(ox + w * t, oy - h * (0.9 / (1 + 4 * t))) for t in [i / 40 for i in range(41)]]
    jam = [(ox + w * t, oy - h * (0.1 + 0.85 * t ** 3)) for t in [i / 40 for i in range(41)]]
    cv.line(pil, 6, WHITE, seg(s, 0.1, 1.0))
    cv.line(jam, 6, RED, seg(s, 0.5, 1.0))
    cv.text((pil[-1][0] + 20, pil[-1][1]), "PILOT", 26, WHITE, anchor="lm", alpha=seg(s, 1.0, 0.3))
    cv.text((jam[-1][0] + 20, jam[-1][1]), "JAMMER", 26, RED, anchor="lm", alpha=seg(s, 1.3, 0.3))
    cv.d.rectangle(((ox + w * 0.8) * 2, (oy - h) * 2, (ox + w) * 2, oy * 2), fill=(235, 64, 52, 35))
    cv.text((ox + w * 0.9, oy - h - 30), "NEAR THE TARGET", 26, RED, alpha=seg(s, 1.5, 0.3))


def e3_word(cv, s, T, ph=0):
    word, col, kind = {0: ("NO RADIO", ORANGE, "grid"), 1: ("THE MATH", ORANGE, "grid")}[ph]
    big_word(cv, s, word, col, 150, kind)


def e3_fiber(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    y = CY
    pts = [(260 + i * 35, y + 40 * math.sin(i * 0.25)) for i in range(41)]
    cv.line(pts, 4, GREY)
    for k in range(6):
        u = (s * 0.45 + k / 6) % 1.0
        i = u * 40
        p = lerp_pt(pts[int(i)], pts[min(int(i) + 1, 40)], i - int(i))
        cv.dot(p, 12, ORANGE)
    quad_side(cv, (pts[-1][0] + 150, pts[-1][1] - 20), 1.2, spin=s * 40)
    controller(cv, (200, y + 40), 0.6, t=s)
    cv.text((CX, 260), "LIGHT TRAVELS THROUGH THE THREAD", 36, ORANGE, alpha=seg(s, 0.2, 0.3))
    if ph:
        for k in range(3):
            waves(cv, (CX, 760), 1.4, RED, 4, s * 1.2 + k * 0.33, 230, 310, 1)
        cv.text((CX, 820 - 10), "RADIO NOISE CAN'T GET IN", 34, RED, alpha=seg(s, 0.3, 0.3))


def e3_df(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    c = (CX + 380, CY)
    cv.circle(c, 220, 4, WHITE)
    a = s * 2.0
    cv.line([c, (c[0] + 220 * math.cos(a), c[1] + 220 * math.sin(a))], 4, RED)
    cv.text((c[0], c[1] + 270), "DIRECTION FINDER", 30, RED)
    cv.text((c[0], c[1] - 270), "NO SIGNAL FOUND", 34, WHITE, alpha=seg(s, 1.0, 0.3))
    controller(cv, (CX - 420, CY + 40), 1.0, t=s)
    cv.line([(CX - 330, CY - 30), (CX - 120, CY - 220)], 3, ORANGE)
    cv.text((CX - 420, CY + 170), "PILOT · NO RADIO", 30, ORANGE)


def e3_kursk_map(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ukr = [(260, 520), (330, 430), (480, 400), (640, 420), (760, 470), (800, 560), (700, 640), (520, 670),
           (360, 640), (260, 520)]
    cv.line(ukr, 4, GREY)
    cv.text((520, 540), "UKRAINE", 32, GREY)
    k = (860, 330)
    p = seg(s, 0.2, 0.5)
    cv.circle(k, 30 + 20 * math.sin(s * 4), 4, ORANGE, prog=p)
    cv.dot(k, 10, ORANGE)
    cv.text((k[0] + 60, k[1] - 10), "KURSK", 36, WHITE, anchor="lm")
    cv.text((k[0] + 60, k[1] + 40), "AUGUST 2024", 30, ORANGE, anchor="lm", alpha=seg(s, 0.5, 0.3))
    cv.text((1350, 600), "RUSSIA: FIRST IN COMBAT", 32, RED, alpha=seg(s, 0.9, 0.3))
    cv.text((1350, 660), "UKRAINE FOLLOWED", 32, ORANGE, alpha=seg(s, 1.5, 0.3))


def e3_spool_weight(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c = (CX, 520)
    tilt = 0.18 * seg(s, 0.3, 0.8)
    cv.line([(c[0], c[1]), (c[0], c[1] + 220)], 6, WHITE)
    cv.line([(c[0] - 120, c[1] + 220), (c[0] + 120, c[1] + 220)], 6, WHITE)
    l = (c[0] - 380 * math.cos(tilt), c[1] + 380 * math.sin(tilt))
    r = (c[0] + 380 * math.cos(tilt), c[1] - 380 * math.sin(tilt))
    cv.line([l, r], 6, WHITE)
    cv.circle((l[0], l[1] - 70), 60, 6, ORANGE)
    cv.circle((l[0], l[1] - 70), 20, 4, ORANGE)
    cv.text((l[0], l[1] + 50), "SPOOL", 30, ORANGE)
    quad_top(cv, (r[0], r[1] - 60), 0.5, spin=s * 30)
    cv.text((CX, 180), "LESS FLIGHT TIME · LESS LOAD", 40, RED, alpha=seg(s, 0.8, 0.3))


def e3_snag(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ground = 740
    cv.line([(120, ground), (1800, ground)], 4, GREY)
    for x in (900, 1050):
        cv.line([(x, ground), (x, 380)], 6, WHITE)
        for k in range(4):
            cv.line([(x, 450 + k * 60), (x + (-1) ** k * 110, 410 + k * 60)], 4, WHITE)
    cv.line([(1300, ground), (1300, 330)], 5, GREY)
    cv.line([(1300, 340), (1800, 360)], 3, GREY)
    p = seg(s, 0, 1.6)
    x = lerp(300, 980, p)
    yy = lerp(500, 420, p)
    pts = [(200, 600), (300, 520), (x, yy)]
    cv.line(pts, 3, ORANGE)
    if p >= 1:
        cv.circle((980, 420), 34, 4, RED)
        quad_side(cv, (980, 400), 0.9, spin=s * 40, tilt=0.5)
        cv.text((980, 260), "SNAGGED", 46, RED)
    else:
        quad_side(cv, (x + 40, yy - 20), 0.9, spin=s * 40)


def e3_fiber_range(cv, s, T, ph=0):
    backdrop(cv, s, "map")
    rows = [("EARLY ON", 10, GREY), ("2026 REPORTS", 40, ORANGE)]
    for i, (lab, km, col) in enumerate(rows):
        if i > ph:
            break
        y = 380 + i * 170
        p = seg(s, 0.2, 0.9)
        cv.text((520, y), lab, 32, col, anchor="rm")
        cv.rect((560, y - 32, 560 + 26 * km * p, y + 32), 0, fill=col, radius=6)
        cv.text((580 + 26 * km * p, y), "~10 KM" if i == 0 else "30–40 KM", 34, col, anchor="lm",
                alpha=seg(s, 0.9, 0.3))
    cv.text((CX, 200), "RANGE = LENGTH OF THE THREAD", 38, WHITE, alpha=seg(s, 0.1, 0.3))


def e3_ai(cv, s, T, ph=0):
    box = (360, 150, 1560, 800)
    x0, y0, x1, y1 = box
    hz = 380
    cv.line([(x0, hz), (x1, hz)], 3, GREY)
    zoom = 1 + (seg(s, 0.3, 2.5) if ph else 0)
    tc = (CX + 120 / zoom, 560 - 60 / zoom)
    w = 70 * zoom
    car_icon(cv, tc, 0.5 * zoom, WHITE, 4)
    cv.rect((tc[0] - w, tc[1] - w * 0.7, tc[0] + w, tc[1] + w * 0.7), 4, ORANGE, radius=2)
    cv.text((tc[0], tc[1] - w * 0.7 - 24), "LOCKED" if ph else "TARGET SELECTED BY PILOT", 24, ORANGE)
    if ph:
        noise(cv, (x0, y0, x0 + 300, y0 + 120), 0.15, int(s * 20))
        cv.text((x0 + 40, y0 + 50), "LINK LOST", 30, RED, anchor="lm")
        cv.text((x1 - 40, y0 + 50), "ON-BOARD TRACKING", 26, ORANGE, anchor="rm")
    cv.rect(box, 8, WHITE, radius=60)


def e3_human(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c = (CX - 360, CY)
    cv.circle((c[0], c[1] - 90), 50, 6, WHITE)
    cv.line([(c[0] - 90, c[1] + 120), (c[0] - 70, c[1]), (c[0] + 70, c[1]), (c[0] + 90, c[1] + 120)], 6, WHITE)
    cv.text((c[0], c[1] + 180), "A PERSON DECIDES", 36, ORANGE, alpha=seg(s, 0.2, 0.3))
    r = (CX + 360, CY)
    cv.rect((r[0] - 80, r[1] - 140, r[0] + 80, r[1] - 20), 6, GREY, radius=12)
    cv.dot((r[0] - 30, r[1] - 80), 10, GREY)
    cv.dot((r[0] + 30, r[1] - 80), 10, GREY)
    cv.rect((r[0] - 100, r[1], r[0] + 100, r[1] + 120), 6, GREY, radius=12)
    if ph == 0:
        cross(cv, (r[0], r[1]), 120, RED, 10, seg(s, 0.4, 0.4))
        cv.text((r[0], r[1] + 180), "NOT A ROBOT CHOOSING TARGETS", 30, RED, alpha=seg(s, 0.6, 0.3))
    else:
        cv.text((r[0], r[1] + 180), "MACHINE: HOLDS ON AFTER LINK LOSS", 28, WHITE, alpha=seg(s, 0.2, 0.3))
        cv.arrow((c[0] + 140, c[1] - 40), (r[0] - 140, r[1] - 40), 5, ORANGE, seg(s, 0.3, 0.6))


# ---------------- impact ----------------

def e3_loss_bars(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    rows = [("UKRAINIAN CLAIMS", 90, ORANGE, "UP TO 90%+"), ("INDEPENDENT ANALYST", 75, WHITE, "≈ 70–80%")]
    cv.text((CX, 170), "SHARE OF RUSSIAN LOSSES CAUSED BY DRONES", 32, GREY)
    for i, (lab, v, col, txt) in enumerate(rows):
        if i > ph:
            break
        y = 360 + i * 170
        p = seg(s, 0.2, 0.9)
        cv.text((620, y), lab, 30, col, anchor="rm")
        cv.rect((660, y - 34, 660 + 9 * v * p, y + 34), 0, fill=col, radius=6)
        cv.text((680 + 9 * v * p, y), txt, 32, col, anchor="lm", alpha=seg(s, 0.9, 0.3))
    if ph:
        cv.tag((CX, 760), "NOT INDEPENDENTLY VERIFIED", 30, RED, alpha=seg(s, 0.5, 0.3))


def e3_cost_ratio(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    quad_top(cv, (CX - 420, CY), 0.9, spin=s * 30)
    cv.text((CX - 420, CY + 160), "$ HUNDREDS", 44, ORANGE)
    x = CX + 380
    cv.rect((x - 200, CY - 60, x + 160, CY + 60), 6, WHITE, radius=14)
    cv.rect((x - 60, CY - 120, x + 60, CY - 60), 6, WHITE, radius=10)
    cv.line([(x + 40, CY - 95), (x + 220, CY - 110)], 6, WHITE)
    for k in range(4):
        cv.circle((x - 150 + k * 95, CY + 70), 34, 5, WHITE)
    cv.text((x, CY + 160), "$ MILLIONS", 44, WHITE)
    if ph:
        cv.arrow((CX - 300, CY - 20), (x - 230, CY - 20), 6, ORANGE, seg(s, 0.1, 0.5), 26)
        cross(cv, (x, CY), 120, RED, 10, seg(s, 0.6, 0.4))


def e3_heli_cost(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    rows = [("FPV DRONE", 0.4, ORANGE, "~$400"), ("ATTACK HELICOPTER", 19000, WHITE, "~$19 MILLION")]
    for i, (lab, v, col, txt) in enumerate(rows):
        y = 380 + i * 170
        p = seg(s, 0.2 + i * 0.4, 0.8)
        cv.text((560, y), lab, 32, col, anchor="rm")
        wpx = max(6, 1100 * v / 19000)
        cv.rect((600, y - 34, 600 + wpx * p, y + 34), 0, fill=col, radius=6)
        cv.text((620 + wpx * p, y) if i == 0 else (600 + wpx * p - 20, y), txt, 32, col if i == 0 else (20, 20, 20),
                anchor="lm" if i == 0 else "rm", alpha=seg(s, 0.8 + i * 0.4, 0.3))
    cv.tag((CX, 200), "UKRAINIAN CLAIM · HELICOPTER VALUE: DRONE MAKER'S ESTIMATE", 26, alpha=seg(s, 0.2, 0.3))
    if ph:
        cv.tag((CX, 760), "NOT INDEPENDENTLY CONFIRMED", 30, RED, alpha=seg(s, 0.2, 0.3))


def e3_seen_hit(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    steps = (("SEEN", WHITE), ("SPOTTED", ORANGE), ("HIT", RED))
    for i, (t, col) in enumerate(steps):
        x = 420 + i * 540
        a = seg(s, 0.1 + i * 0.5, 0.3)
        if i == 0:
            cv.circle((x, CY - 40), 70, 6, col)
            cv.dot((x, CY - 40), 24, col)
        elif i == 1:
            cv.circle((x, CY - 40), 70, 5, col)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                cv.line([(x + dx * 40, CY - 40 + dy * 40), (x + dx * 100, CY - 40 + dy * 100)], 5, col)
        else:
            clock_icon(cv, (x, CY - 40), 80, 0.1 + 0.1 * seg(s, 1.2, 1.0), accent=RED)
        cv.text((x, CY + 90), t, 44, col, alpha=a)
        if i < 2:
            cv.arrow((x + 120, CY - 40), (x + 420, CY - 40), 5, GREY, seg(s, 0.4 + i * 0.5, 0.3))
    cv.text((CX, 760), "WITHIN MINUTES", 46, RED, alpha=seg(s, 1.4, 0.3))


def hexa_top(cv, c, s=1.0, col=WHITE, w=5, spin=0.0):
    x, y = c
    for i in range(6):
        a = math.pi / 6 + i * math.pi / 3
        p = (x + 120 * s * math.cos(a), y + 120 * s * math.sin(a))
        cv.line([(x, y), p], w + 2, col)
        cv.circle(p, 50 * s, 2, DIM)
        b = spin * (1 if i % 2 else -1) + i
        cv.line([(p[0] - 50 * s * math.cos(b), p[1] - 50 * s * math.sin(b)),
                 (p[0] + 50 * s * math.cos(b), p[1] + 50 * s * math.sin(b))], 3, GREY)
    cv.circle((x, y), 40 * s, w, col)


def e3_size_scale(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    quad_top(cv, (CX - 450, CY), 0.8, spin=s * 30)
    cv.text((CX - 450, CY + 170), "FPV", 40, ORANGE)
    hexa_top(cv, (CX + 300, CY - 20), 1.8 * (0.5 + 0.5 * seg(s, 0.2, 0.8)), spin=s * 20)
    cv.text((CX + 300, CY + 300), "HEAVY BOMBER DRONE", 36, WHITE, alpha=seg(s, 0.6, 0.3))


def e3_babayaga(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c = (CX - 200, 330)
    hexa_top(cv, c, 0.9, spin=s * 20)
    cv.poly([c, (c[0] - 260, 780), (c[0] + 260, 780)], fill=(255, 138, 31, 30))
    cv.text((c[0], 820 - 20), "THERMAL CAMERA · AT NIGHT", 30, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX + 420, 300), "HEAVY LOADS", 40, WHITE, alpha=seg(s, 0.6, 0.3))
    cv.text((CX + 420, 380), "COMES BACK · REUSED", 40, WHITE, alpha=seg(s, 1.0, 0.3))
    pts = [(CX + 300 + 180 * math.cos(t / 20 * 2 * math.pi), 580 + 80 * math.sin(t / 20 * 2 * math.pi))
           for t in range(21)]
    cv.dashed(pts, 4, GREY, offset=s * 40, prog=seg(s, 1.0, 1.0))


# ---------------- counters ----------------

def e3_shield(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sh = [(CX, 220), (CX + 170, 280), (CX + 150, 520), (CX, 640), (CX - 150, 520), (CX - 170, 280), (CX, 220)]
    cv.line(sh, 8, WHITE, prog=seg(s, 0, 0.8))
    quad_top(cv, (CX + 420 - 200 * seg(s, 0.4, 0.8), 430), 0.6, RED, 4, spin=s * 30)
    cv.text((CX, 760), "THEY CAN BE STOPPED", 48, ORANGE, alpha=seg(s, 0.6, 0.3))


def e3_cage(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    x, y = 560, 600
    car_icon(cv, (x, y), 1.6, WHITE, 5)
    for k in range(9):
        cv.line([(x - 220 + k * 55, y - 210), (x - 220 + k * 55, y - 110)], 3, ORANGE)
    cv.line([(x - 240, y - 210), (x + 240, y - 210)], 5, ORANGE)
    cv.text((x, y + 150), "WELDED CAGE", 34, ORANGE, alpha=seg(s, 0.3, 0.3))
    road = 700
    cv.line([(1000, road), (1800, road)], 4, GREY)
    for k in range(5):
        px = 1040 + k * 180
        cv.line([(px, road), (px, 360)], 4, GREY)
    for k in range(4):
        cv.line([(1040 + k * 180, 360), (1220 + k * 180, 360)], 3, WHITE)
        for j in range(6):
            cv.line([(1040 + k * 180 + j * 30, 360), (1055 + k * 180 + j * 30, 420)], 2, WHITE)
    u = (s * 0.35) % 1.0
    quad_side(cv, (lerp(1820, 1480, min(1, u * 1.5)), 300), 0.7, spin=s * 40, flip=True)
    cv.text((1400, road + 70), "NETS OVER ROADS", 34, ORANGE, alpha=seg(s, 0.6, 0.3))


def e3_shot_pattern(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    o = (380, 760)
    tgt = (1400, 330 + 30 * math.sin(s * 3))
    quad_top(cv, tgt, 0.5, RED, 4, spin=s * 30)
    ang = math.atan2(tgt[1] - o[1], tgt[0] - o[0])
    L = math.dist(o, tgt)
    for k in (-1, 1):
        a = ang + k * 0.09
        cv.line([o, (o[0] + L * 1.05 * math.cos(a), o[1] + L * 1.05 * math.sin(a))], 2, DIM)
    rnd = random.Random(int(s * 2))
    u = (s * 0.8) % 1.0
    for i in range(30):
        a = ang + rnd.uniform(-0.08, 0.08)
        r = L * u * rnd.uniform(0.95, 1.05)
        cv.dot((o[0] + r * math.cos(a), o[1] + r * math.sin(a)), 5, ORANGE)
    cv.text((CX, 170), "A CLOUD OF PELLETS · EASIER TO HIT A SMALL, FAST TARGET", 32, WHITE, alpha=seg(s, 0.3, 0.3))


def e3_intercept(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    u = (s * 0.18) % 1.0
    tgt = (lerp(500, 1700, u), 360 + 80 * math.sin(u * 8))
    hunter = (tgt[0] - lerp(600, 90, clamp(s / max(T, 1.0))), tgt[1] + 60)
    quad_top(cv, tgt, 0.8, RED, 4, spin=s * 30)
    quad_top(cv, hunter, 0.9, ORANGE, 4, spin=s * 40)
    cv.dashed([hunter, tgt], 3, ORANGE, offset=s * 60)
    cv.text((CX, 760), "INTERCEPTOR DRONE", 46, ORANGE, alpha=seg(s, 0.3, 0.3))


CYCLE = ("JAMMING", "FIBRE OPTICS", "NETS", "NEXT IDEA")


def e3_cycle(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c, R = (CX, CY - 10), 270
    spin = s * (0.3 if ph < 2 else 1.4)
    cv.circle(c, R, 3, DIM)
    for i, t in enumerate(CYCLE):
        a = spin + i * math.pi / 2 - math.pi / 2
        p = (c[0] + R * math.cos(a), c[1] + R * math.sin(a))
        on = ph >= 1 and i <= int(s / 0.9) or ph == 0 and i == 0
        cv.text(p, t, 34, ORANGE if on else GREY)
        a2 = a + math.pi / 2 * 0.65
        cv.arrow((c[0] + R * math.cos(a + 0.35), c[1] + R * math.sin(a + 0.35)),
                 (c[0] + R * math.cos(a2), c[1] + R * math.sin(a2)), 4, GREY, 1.0, 18)
    if ph == 0:
        cv.text(c, "COUNTER  →  COUNTER", 36, WHITE)
    if ph == 2:
        cv.text(c, "MONTHS, NOT YEARS", 40, RED, alpha=seg(s, 0.2, 0.3))


# ---------------- outro ----------------

def e3_recap(cv, s, T, ph=0):
    backdrop(cv, s, "drones")
    if ph == 0:
        quad_top(cv, (CX - 420, CY - 30), 0.8, spin=s * 30)
        cv.text((CX - 420, CY + 130), "HOBBY", 44, WHITE)
        cv.arrow((CX - 230, CY - 30), (CX + 200, CY - 30), 6, ORANGE, seg(s, 0.3, 0.6))
        for k in range(6):
            quad_top(cv, (CX + 330 + (k % 3) * 110, CY - 90 + (k // 3) * 110), 0.3, ORANGE, 3, spin=s * 30)
        cv.text((CX + 440, CY + 130), "WARTIME INDUSTRY", 44, ORANGE, alpha=seg(s, 0.6, 0.3))
    else:
        cv.text((CX, CY - 40), "COUNTERMEASURES FOLLOW FAST", 56, WHITE, alpha=seg(s, 0.1, 0.3))
        cv.arrow((CX - 300, CY + 60), (CX + 300, CY + 60), 6, ORANGE, seg(s, 0.3, 0.5))


def e3_land_sea(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(200, 600), (900, 600)], 5, GREY)
    quad_side(cv, (550, 470), 1.3, spin=s * 40)
    cv.text((550, 680), "LAND", 40, WHITE)
    pts = [(1020 + i * 20, 600 + 14 * math.sin(i * 0.6 + s * 3)) for i in range(36)]
    cv.line(pts, 5, ORANGE, prog=seg(s, 0.3, 0.8))
    cv.text((1370, 680), "SEA?", 40, ORANGE, alpha=seg(s, 0.8, 0.3))


def e3_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP04  ·  SINKING A FLEET WITHOUT A NAVY", "radar")


SCENES = {k: v for k, v in globals().items() if k.startswith("e3_") and callable(v)}
