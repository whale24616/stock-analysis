"""Line-art scenes for EP01. Each scene is fn(cv, s, T, ph) where
s = seconds since the shot started, T = shot length, ph = phase (int) for multi-step scenes.
On-screen labels are English; narration subtitles are added by render.py."""
import math
import random

from gfx import (BLACK, DIM, GREY, ORANGE, RED, WHITE, airbase_icon, car_icon, check, clamp, clock_icon,
                 coin_stack, cross, depot_icon, drone_side, drone_top, ease, ease_io, factory_icon, jet_icon,
                 lerp, lerp_pt, missile_icon, radar_dish, refinery_icon, satellite_icon, seg, sound_waves,
                 speedometer, stick_figure, tower_icon)

CX, CY = 960, 470  # visual centre (subtitle band sits below ~900)


def corner(cv, s, text):
    """Small top-left section label."""
    cv.text((90, 80), text, 26, GREY, anchor="lm", alpha=seg(s, 0.1, 0.4))


# ---------------- cold open ----------------

def radar(cv, s, T, ph=0):
    c, R = (CX, CY), 340
    corner(cv, s, "RADAR  ·  SOUTH OF MOSCOW")
    for r in (R, R * 0.66, R * 0.33):
        cv.circle(c, r, 3, DIM)
    cv.line([(c[0] - R, c[1]), (c[0] + R, c[1])], 2, DIM)
    cv.line([(c[0], c[1] - R), (c[0], c[1] + R)], 2, DIM)
    a = s * 1.6
    for k in range(14):
        aa = a - k * 0.035
        col = tuple(int(v * (1 - k / 14)) for v in (90, 90, 88))
        cv.line([c, (c[0] + R * math.cos(aa), c[1] + R * math.sin(aa))], 6, col)
    cv.line([c, (c[0] + R * math.cos(a), c[1] + R * math.sin(a))], 4, WHITE)
    cv.circle(c, R, 5, WHITE)
    rnd = random.Random(3)
    for i in range(6):
        x0 = c[0] - R * 0.9 + rnd.random() * 120
        y0 = c[1] - 160 + i * 60 + rnd.random() * 20
        x = x0 + (s + ph * 4) * 9
        if math.dist((x, y0), c) < R - 12:
            cv.dot((x, y0), 9, ORANGE)
            cv.line([(x - 40, y0), (x - 12, y0)], 2, (120, 70, 20))
    if ph:
        cv.tag((c[0] + R + 170, c[1] - 120), "~150 KM/H", 30, alpha=seg(s, 0.3, 0.4))


def speed(cv, s, T, ph=0):
    corner(cv, s, "SPEED")
    speedometer(cv, (CX, CY + 60), 260, 150 * seg(s, 0.1, 1.2), 400, band=(150, 200))
    cv.text((CX, CY + 130), "KM/H", 30, GREY)
    car_icon(cv, (CX - 520, CY + 120), 1.0)
    drone_side(cv, (CX + 520, CY + 110), 1.0, prop_spin=s * 20)
    for i in range(3):
        y = CY + 90 + i * 30
        off = (s * 300) % 160
        cv.line([(CX - 700 - off, y), (CX - 660 - off, y)], 3, GREY)
        cv.line([(CX + 300 - off, y - 30), (CX + 340 - off, y - 30)], 3, GREY)
    cv.text((CX - 520, CY + 220), "CAR ON A HIGHWAY", 28, WHITE, alpha=seg(s, 0.4, 0.4))
    cv.text((CX + 520, CY + 220), "LONG-RANGE DRONE", 28, ORANGE, alpha=seg(s, 0.6, 0.4))


def timer(cv, s, T, ph=0):
    corner(cv, s, "TIME IN THE AIR")
    secs = 4 * 3600 + 12 * 60 + s * 900
    h, m, sec = int(secs // 3600), int(secs % 3600 // 60), int(secs % 60)
    cv.text((CX, CY - 20), f"{h:02d}:{m:02d}:{sec:02d}", 190, ORANGE, kind="label")
    cv.line([(CX - 420, CY + 110), (CX - 420 + 840 * clamp(s / max(T, 0.1)), CY + 110)], 6, WHITE)
    cv.text((CX, CY + 170), "STILL FLYING", 34, WHITE, alpha=seg(s, 0.3, 0.4))


def _map_base(cv, s):
    # abstract map: UKRAINE (left) and RUSSIA (right) as soft outlines
    ukr = [(260, 520), (330, 430), (480, 400), (640, 420), (760, 470), (800, 560), (700, 640), (520, 670),
           (360, 640), (260, 520)]
    cv.line(ukr, 4, GREY, seg(s, 0, 0.6))
    cv.text((520, 540), "UKRAINE", 34, GREY, alpha=seg(s, 0.2, 0.4))
    return ukr


def distance(cv, s, T, ph=0):
    corner(cv, s, "DISTANCE")
    _map_base(cv, s)
    a, b = (700, 470), (1450, 250)
    mid = (1050, 250)
    p = seg(s, 0.4, max(T - 1.0, 0.8))
    pts = [lerp_pt(lerp_pt(a, mid, t / 30), lerp_pt(mid, b, t / 30), t / 30) for t in range(31)]
    cv.dashed(pts, 5, ORANGE, offset=s * 40, prog=p)
    cv.dot(a, 10, ORANGE)
    cv.dot(b, 14, WHITE)
    cv.circle(b, 30 + 10 * math.sin(s * 5), 3, WHITE)
    cv.text((b[0] + 50, b[1] - 10), "MOSCOW", 38, WHITE, anchor="lm")
    km = int(520 * p)
    cv.text((1080, 420), f"{km} KM+" if p >= 1 else f"{km} KM", 70, ORANGE, alpha=seg(s, 0.4, 0.3))


def deep2026(cv, s, T, ph=0):
    corner(cv, s, "2026")
    _map_base(cv, s)
    a = (700, 470)
    targets = [((1300, 260), "MOSCOW", "~500 KM"), ((1600, 420), "", ""), ((1780, 200), "OMSK", "2,000+ KM")]
    for i, (b, name, km) in enumerate(targets):
        p = seg(s, 0.3 + i * 0.35, 0.9)
        mid = ((a[0] + b[0]) / 2, min(a[1], b[1]) - 160)
        pts = [lerp_pt(lerp_pt(a, mid, t / 30), lerp_pt(mid, b, t / 30), t / 30) for t in range(31)]
        cv.dashed(pts, 5, ORANGE, offset=s * 40, prog=p)
        if p > 0.98:
            cv.dot(b, 12, WHITE)
            if name:
                cv.text((b[0], b[1] + 50), name, 32, WHITE)
                cv.text((b[0], b[1] + 92), km, 28, ORANGE)
    cv.text((CX, 760), "DEEP STRIKES", 40, WHITE, alpha=seg(s, 1.2, 0.4))


def omsk_label(cv, s, T, ph=0):
    pass


def xmarks(cv, s, T, ph=0):
    missile_icon(cv, (CX - 380, CY), 1.2)
    jet_icon(cv, (CX + 380, CY), 1.2)
    cv.text((CX - 380, CY + 160), "MISSILE", 34, WHITE)
    cv.text((CX + 380, CY + 160), "FIGHTER JET", 34, WHITE)
    cross(cv, (CX - 380, CY), 120, RED, 12, seg(s, 0.3, 0.5))
    cross(cv, (CX + 380, CY), 120, RED, 12, seg(s, 0.9, 0.5))


def analyst(cv, s, T, ph=0):
    cv.sprite("l30_analyst", (CX - 430, CY + 40), 640, alpha=seg(s, 0, 0.5))
    drone_side(cv, (CX + 380, CY - 10), 1.3, prog=seg(s, 0.3, 0.8), prop_spin=s * 18)
    cv.dashed([(CX - 320, CY - 185), (CX + 170, CY - 25)], 4, GREY, offset=s * 30, prog=seg(s, 0.6, 0.6))
    cv.text((CX + 380, CY + 120), "LONG-RANGE ONE-WAY ATTACK DRONE", 30, ORANGE, alpha=seg(s, 0.9, 0.4))


def title(cv, s, T, ph=0):
    p = seg(s, 0, 0.7)
    cv.line([(CX - 520 * p, CY - 90), (CX + 520 * p, CY - 90)], 4, ORANGE)
    cv.text((CX, CY), "DRONE WAR DECODED", 110, WHITE, alpha=seg(s, 0.2, 0.5))
    cv.text((CX, CY + 110), "EP01  ·  REACHING MOSCOW", 46, ORANGE, alpha=seg(s, 0.6, 0.5))
    cv.line([(CX - 520 * p, CY + 170), (CX + 520 * p, CY + 170)], 4, ORANGE)


# ---------------- background ----------------

def reach_asym(cv, s, T, ph=0):
    corner(cv, s, "EARLY WAR")
    cv.text((CX - 420, 200), "UKRAINE", 36, WHITE)
    cv.text((CX + 420, 200), "RUSSIA", 36, WHITE)
    cv.line([(CX, 170), (CX, 760)], 3, DIM)
    rnd = random.Random(5)
    for i in range(7):
        t = rnd.uniform(240, 720)
        cv.arrow((CX + 300, t), (CX - 260 - rnd.uniform(0, 300), rnd.uniform(240, 720)), 4, RED,
                 seg(s, 0.2 + i * 0.12, 0.5), 18)
    cv.arrow((CX - 300, 480), (CX - 60, 480), 6, ORANGE, seg(s, 1.2, 0.4))
    cv.text((CX + 80, 480), "?", 90, ORANGE, alpha=seg(s, 1.6, 0.3))


def cheap_many(cv, s, T, ph=0):
    n = int(1 + 23 * seg(s, 0.3, 1.6))
    for i in range(n):
        x = 420 + (i % 8) * 155
        y = 300 + (i // 8) * 150
        drone_top(cv, (x, y), 0.25, WHITE if i else ORANGE, 3)
    cv.text((CX - 300, 800), "CHEAP", 52, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX + 300, 800), "× MANY", 52, WHITE, alpha=seg(s, 0.8, 0.3))


def toy_vs_plane(cv, s, T, ph=0):
    x, y = CX - 420, CY
    for dx, dy in ((-60, -60), (60, -60), (-60, 60), (60, 60)):
        cv.circle((x + dx, y + dy), 40, 4, GREY)
    cv.line([(x - 60, y - 60), (x + 60, y + 60)], 6, GREY)
    cv.line([(x + 60, y - 60), (x - 60, y + 60)], 6, GREY)
    cv.text((x, y + 170), "TOY DRONE", 32, GREY)
    drone_side(cv, (CX + 360, CY), 1.4, col=WHITE, prop_col=ORANGE, prop_spin=s * 20, prog=seg(s, 0.2, 0.8))
    cv.text((CX + 360, CY + 170), "LIGHT AIRCRAFT", 36, ORANGE, alpha=seg(s, 0.7, 0.4))
    cv.text((CX - 10, CY), "≠", 90, WHITE, alpha=seg(s, 0.5, 0.3))


def names(cv, s, T, ph=0):
    labels = ["LIUTYI", "UJ-22 AIRBORNE", "BOBER", "FP-1"]
    for i, n in enumerate(labels):
        a = seg(s, 0.15 + i * 0.35, 0.3)
        x = 330 + i * 420
        y = CY + 30 * (1 - a)
        cv.rect((x - 180, y - 90, x + 180, y + 90), 4, WHITE if a >= 1 else GREY)
        cv.text((x, y), n, 40, WHITE, alpha=a)
    cv.text((CX, CY + 200), "MANY MANUFACTURERS", 30, ORANGE, alpha=seg(s, 1.6, 0.4))


def targets(cv, s, T, ph=0):
    items = [(refinery_icon, "OIL REFINERIES"), (airbase_icon, "AIRBASES"), (depot_icon, "AMMO DEPOTS")]
    for i, (fn, lab) in enumerate(items):
        a = seg(s, 0.1 + i * 0.4, 0.3)
        if a <= 0:
            continue
        x = 440 + i * 520
        fn(cv, (x, CY - 40), 1.0 * (0.7 + 0.3 * a))
        cv.text((x, CY + 120), lab, 32, WHITE, alpha=a)
    p = seg(s, 1.4, 1.0)
    cv.arrow((380, 780), (380 + 1160 * p, 780), 5, ORANGE, 1.0 if p > 0 else 0)
    cv.text((CX, 840), "100s – 1,000+ KM FROM THE FRONT", 30, ORANGE, alpha=seg(s, 1.8, 0.4))


# ---------------- segment 1: airframe ----------------

TRI = {"RANGE": (CX, 190), "PAYLOAD": (CX - 360, 760), "COST": (CX + 360, 760)}


def triangle(cv, s, T, ph=0):
    corner(cv, s, "THE DESIGNER'S TRIANGLE")
    pts = dict(TRI)
    if ph >= 2:
        k = ease_io(clamp((s - 0.3) / 1.2)) * (0.5 + 0.5 * math.sin(s * 2.0))
        pts["RANGE"] = (CX, 190 - 70 * k)
        pts["PAYLOAD"] = (CX - 360 + 90 * k, 760 - 40 * k)
        pts["COST"] = (CX + 360 - 90 * k, 760 - 40 * k)
    poly = [pts["RANGE"], pts["PAYLOAD"], pts["COST"], pts["RANGE"]]
    cv.line(poly, 5, WHITE, seg(s, 0, 1.0) if ph == 0 else 1)
    labels = {"RANGE": "FLY FAR", "PAYLOAD": "CARRY ENOUGH", "COST": "COST LITTLE"}
    for i, (k_, p) in enumerate(pts.items()):
        a = seg(s, 0.8 + i * 0.3, 0.3) if ph == 0 else 1
        cv.dot(p, 14, ORANGE)
        dy = -50 if k_ == "RANGE" else 60
        cv.text((p[0], p[1] + dy), labels[k_], 34, WHITE, alpha=a)
    if ph >= 2:
        cv.text((CX, 560), "IMPROVE ONE →", 30, ORANGE)
        cv.text((CX, 600), "THE OTHER TWO SUFFER", 30, ORANGE)


def wing(cv, s, T, ph=0):
    corner(cv, s, "TRICK #1 · THE WING")
    drone_top(cv, (CX, CY), 1.35, WHITE, 5, prog=seg(s, 0, 0.8) if ph == 0 else 1, wing_col=ORANGE,
              prop_spin=s * 20)
    if ph >= 1:
        p = seg(s, 0.2, 0.6)
        cv.arrow((CX + 120, CY), (CX + 120, CY - 300), 4, WHITE, p, 16)
        cv.arrow((CX + 120, CY), (CX + 120, CY + 300), 4, WHITE, p, 16)
        cv.text((CX + 290, CY - 200), "LONG SPAN", 32, WHITE, alpha=p)
        cv.text((CX + 290, CY + 200), "NARROW CHORD", 32, WHITE, alpha=p)
        cv.tag((CX - 420, CY + 330), "HIGH ASPECT RATIO", 30, alpha=seg(s, 0.8, 0.4))


def _spiral(cv, c, r, s, col, w=4, d=1):
    pts = []
    for i in range(60):
        t = i / 59
        a = d * (t * 4 * math.pi + s * 6)
        rr = r * t
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a) * 0.8))
    cv.line(pts, w, col)


def vortex(cv, s, T, ph=0):
    corner(cv, s, "WINGTIP VORTEX")
    if ph < 2:
        y = CY
        cv.line([(CX - 420, y), (CX + 420, y)], 7, WHITE)
        cv.line([(CX - 40, y - 30), (CX + 40, y - 30), (CX + 40, y + 30), (CX - 40, y + 30), (CX - 40, y - 30)], 5, WHITE)
        for i in range(5):
            x = CX - 360 + i * 180
            cv.arrow((x, y + 40), (x, y + 140), 4, GREY, seg(s, 0.1, 0.4), 14)
        cv.text((CX, y + 200), "AIR PUSHED DOWN", 28, GREY, alpha=seg(s, 0.2, 0.4))
        g = seg(s, 0.6, 0.6)
        _spiral(cv, (CX - 470, y), 90 * g, s, ORANGE, 5, 1)
        _spiral(cv, (CX + 470, y), 90 * g, s, ORANGE, 5, -1)
        if ph == 1:
            cv.arrow((CX, y - 120), (CX, y - 300), 8, RED, seg(s, 0.2, 0.5), 30)
            cv.text((CX + 140, y - 230), "DRAG", 44, RED, alpha=seg(s, 0.4, 0.3))
    else:
        for k, (x, span, rad, lab) in enumerate(((CX - 450, 200, 110, "SHORT WING"), (CX + 380, 380, 45, "LONG, THIN WING"))):
            y = CY - 40
            cv.line([(x - span, y), (x + span, y)], 7, WHITE if k else GREY)
            _spiral(cv, (x - span - 40, y), rad, s, ORANGE, 4, 1)
            _spiral(cv, (x + span + 40, y), rad, s, ORANGE, 4, -1)
            cv.text((x, y + 160), lab, 32, WHITE if k else GREY)
        cv.text((CX, 770), "WEAKER VORTEX  =  LESS DRAG  =  LESS FUEL", 34, ORANGE, alpha=seg(s, 0.6, 0.4))


def pusher(cv, s, T, ph=0):
    corner(cv, s, "TRICK #2 · PUSHER PROPELLER")
    drone_side(cv, (CX, CY), 2.0, prop_col=ORANGE, prop_spin=s * 25)
    if ph == 0:
        for i in range(3):
            off = (s * 260 + i * 70) % 210
            cv.arrow((CX - 640 + off, CY - 40 + i * 40), (CX - 560 + off, CY - 40 + i * 40), 4, ORANGE, 1, 14)
        cv.text((CX - 380, CY + 170), "PUSHES FROM BEHIND", 32, ORANGE, alpha=seg(s, 0.4, 0.4))
    else:
        for i in range(4):
            y = CY - 140 - i * 26
            off = (s * 400) % 120
            cv.dashed([(CX - 700, y), (CX + 700, y)], 3, WHITE, dash=40, gap=20, offset=-off)
        cv.rect((CX + 120, CY - 60, CX + 330, CY + 50), 4, ORANGE, prog=seg(s, 0.2, 0.6))
        cv.text((CX + 225, CY + 100), "PAYLOAD · SENSORS", 28, ORANGE, alpha=seg(s, 0.6, 0.4))
        cv.text((CX - 300, CY - 280), "CLEAN AIR OVER THE WING", 30, WHITE, alpha=seg(s, 0.9, 0.4))


def materials(cv, s, T, ph=0):
    corner(cv, s, "TRICK #3 · MATERIALS")
    xs = (CX - 480, CX, CX + 480)
    a = [seg(s, 0.1 + i * 0.3, 0.3) for i in range(3)]
    x = xs[0]
    cv.rect((x - 110, CY - 110, x + 110, CY + 110), 5, WHITE, prog=a[0])
    for i in range(6):
        cv.line([(x - 110 + i * 40, CY + 110), (x - 110 + i * 40 + 100, CY - 110)], 2, GREY, a[0])
    x = xs[1]
    cv.circle((x, CY), 110, 5, WHITE, prog=a[1])
    rnd = random.Random(2)
    for i in range(int(18 * a[1])):
        cv.circle((x + rnd.uniform(-70, 70), CY + rnd.uniform(-70, 70)), rnd.uniform(6, 14), 2, GREY)
    x = xs[2]
    for dy in (-60, 0, 60):
        cv.line([(x - 130, CY + dy), (x + 130, CY + dy)], 14, WHITE, a[2])
    for i, lab in enumerate(("COMPOSITES", "FOAM", "SIMPLE TUBING")):
        cv.text((xs[i], CY + 180), lab, 32, WHITE, alpha=a[i])
    if ph:
        cv.text((CX, 790), "CHEAP  ·  LIGHT  ·  FAST TO BUILD", 40, ORANGE, alpha=seg(s, 0.2, 0.4))


def radar_reflect(cv, s, T, ph=0):
    corner(cv, s, "RADAR SIGNATURE")
    radar_dish(cv, (300, CY), 1.3)
    drone_side(cv, (CX + 380, CY - 20), 1.6, prop_spin=s * 20)
    for i in range(4):
        r = ((s * 420 + i * 250) % 1000)
        cv.arc((300, CY - 30), r, -12, 12, 4, WHITE)
    ret = GREY if ph == 0 else ORANGE
    for i in range(3):
        r = ((s * 420 + i * 300) % 900)
        cv.arc((CX + 380, CY - 20), r, 168, 192, 3, ret if ph else DIM)
    if ph == 0:
        cv.text((CX, 800), "LESS METAL  →  WEAKER ECHO", 36, WHITE, alpha=seg(s, 0.3, 0.4))
    else:
        cv.dot((CX + 380 - 300, CY - 20), 22, ORANGE)
        cv.dot((CX + 380 - 60, CY - 20), 22, ORANGE)
        cv.text((CX + 220, CY + 140), "ENGINE · FUEL TANK", 28, ORANGE)
        cv.tag((CX, 800), "NOT STEALTH", 40, RED, alpha=seg(s, 0.4, 0.3))


def cg(cv, s, T, ph=0):
    corner(cv, s, "TRICK #4 · BALANCE")
    tilt = 0.0 if ph == 0 else 0.03 * math.sin(s * 3) * (1 - seg(s, 0.5, 1.5))
    L = 520
    c = (CX, CY + 60)
    p0 = (c[0] - L * math.cos(tilt), c[1] - L * math.sin(tilt))
    p1 = (c[0] + L * math.cos(tilt), c[1] + L * math.sin(tilt))
    cv.line([p0, p1], 8, WHITE)
    cv.poly([(c[0], c[1] + 8), (c[0] - 60, c[1] + 120), (c[0] + 60, c[1] + 120)], col=WHITE, w=5)
    lvl = 1.0 if ph == 0 else 1 - 0.7 * seg(s, 0.3, max(T - 0.6, 0.5))
    cv.rect((c[0] - 80, c[1] - 170, c[0] + 80, c[1] - 10), 5, WHITE)
    cv.rect((c[0] - 74, c[1] - 10 - 154 * lvl, c[0] + 74, c[1] - 16), 0, fill=ORANGE, radius=8)
    cv.text((c[0], c[1] - 210), "FUEL + PAYLOAD", 30, ORANGE)
    cv.text((c[0], c[1] + 170), "CENTRE OF GRAVITY", 30, WHITE, alpha=seg(s, 0.3, 0.4))
    if ph:
        cv.text((CX, 820), "FUEL BURNS  →  STILL BALANCED", 34, WHITE, alpha=seg(s, 0.4, 0.4))


# ---------------- segment 2: engine & range ----------------

def _jet_engine(cv, c, s_, col=WHITE):
    x, y = c
    cv.line([(x - 150, y - 60), (x + 110, y - 45), (x + 150, y - 25), (x + 150, y + 25), (x + 110, y + 45),
             (x - 150, y + 60), (x - 150, y - 60)], 5, col)
    for i in range(5):
        cv.line([(x - 120 + i * 18, y - 50), (x - 120 + i * 18, y + 50)], 3, col)


def _piston(cv, c, col=WHITE):
    x, y = c
    cv.rect((x - 90, y - 110, x + 90, y + 40), 5, col)
    cv.rect((x - 60, y - 80, x + 60, y - 20), 4, col)
    cv.line([(x, y - 20), (x, y + 80)], 5, col)
    cv.circle((x, y + 100), 30, 5, col)


def engine_q(cv, s, T, ph=0):
    corner(cv, s, "WHY NOT A JET?")
    _jet_engine(cv, (CX - 420, CY), s)
    _piston(cv, (CX + 420, CY))
    cv.text((CX - 420, CY + 170), "JET ENGINE", 34, WHITE)
    cv.text((CX + 420, CY + 170), "SMALL PISTON ENGINE", 34, ORANGE)
    cv.text((CX, CY), "?", 140, ORANGE, alpha=seg(s, 0.4, 0.3))


def speedgauge(cv, s, T, ph=0):
    corner(cv, s, "CRUISE SPEED")
    speedometer(cv, (CX, CY + 110), 320, lerp(0, 175, seg(s, 0.1, 1.0)), 400, band=(150, 200))
    cv.text((CX, CY + 40), "150–200", 80, ORANGE)
    cv.text((CX, CY + 120), "KM/H", 34, WHITE)
    cv.tag((CX, 800), "REPORTED", 26, alpha=seg(s, 0.5, 0.4))


def eff_chart(cv, s, T, ph=0):
    corner(cv, s, "FUEL USED PER KM")
    ox, oy, w, h = 520, 760, 880, 520
    cv.line([(ox, oy - h), (ox, oy), (ox + w, oy)], 4, WHITE)
    cv.text((ox + w, oy + 40), "SPEED →", 28, GREY, anchor="rm")
    cv.text((ox - 30, oy - h), "FUEL / KM", 28, GREY, anchor="rm")
    px = [(ox + w * t, oy - h * (0.18 + 0.75 * t ** 2.2)) for t in [i / 40 for i in range(41)]]
    jx = [(ox + w * t, oy - h * (0.95 - 0.65 * t ** 0.6)) for t in [i / 40 for i in range(1, 41)]]
    cv.line(px, 6, ORANGE, seg(s, 0.1, 1.0))
    cv.line(jx, 6, WHITE, seg(s, 0.4, 1.0))
    cv.text((ox + w + 20, px[-1][1]), "PISTON + PROP", 26, ORANGE, anchor="lm", alpha=seg(s, 1.0, 0.3))
    cv.text((ox + w + 20, jx[-1][1]), "JET", 26, WHITE, anchor="lm", alpha=seg(s, 1.2, 0.3))
    bx = ox + w * 0.22
    cv.d.rectangle(((bx - 40) * 2, (oy - h) * 2, (bx + 40) * 2, oy * 2), fill=(255, 138, 31, 40))
    cv.text((bx, oy + 40), "150–200 KM/H", 24, ORANGE)
    if ph:
        cv.circle(jx[6], 26, 4, RED, prog=seg(s, 0.1, 0.4))
        cv.text((jx[6][0] + 50, jx[6][1] - 40), "THIRSTY WHEN SLOW", 30, RED, anchor="lm", alpha=seg(s, 0.3, 0.3))


def factors(cv, s, T, ph=0):
    corner(cv, s, "WHAT DECIDES RANGE")
    labs = ("ENGINE EFFICIENCY", "LOW DRAG", "FUEL FRACTION")
    for i, lab in enumerate(labs):
        a = seg(s, 0.1 + i * 0.35, 0.3) if ph == 0 else 1
        x = 430 + i * 530
        cv.rect((x - 210, CY - 170, x + 210, CY + 170), 4, WHITE if a >= 1 else GREY)
        cv.text((x, CY + 120), lab, 30, WHITE, alpha=a)
        if i == 0:
            _piston(cv, (x, CY - 30))
        elif i == 1:
            for k in range(3):
                cv.line([(x - 150, CY - 80 + k * 40), (x - 40, CY - 80 + k * 40), (x + 40, CY - 60 + k * 30),
                         (x + 150, CY - 60 + k * 30)], 3, GREY)
        else:
            cv.rect((x - 60, CY - 110, x + 60, CY + 50), 5, WHITE)
            cv.rect((x - 54, CY - 110 + 160 * 0.4, x + 54, CY + 44), 0, fill=ORANGE, radius=6)
        if ph:
            check(cv, (x + 170, CY - 130), 30, ORANGE, 8, seg(s, 0.2 + i * 0.3, 0.3))


def dimin(cv, s, T, ph=0):
    corner(cv, s, "THE FUEL TRAP")
    if ph == 0:
        cv.text((CX, CY), "!", 300, ORANGE, alpha=seg(s, 0.05, 0.2))
        cv.text((CX, CY + 220), "A CATCH", 40, WHITE, alpha=seg(s, 0.4, 0.3))
        return
    ox, oy, w, h = 520, 760, 880, 500
    cv.line([(ox, oy - h), (ox, oy), (ox + w, oy)], 4, WHITE)
    cv.text((ox + w, oy + 40), "FUEL ADDED →", 28, GREY, anchor="rm")
    cv.text((ox - 30, oy - h), "RANGE", 28, GREY, anchor="rm")
    pts = [(ox + w * t, oy - h * (1 - (1 - t) ** 2.4)) for t in [i / 40 for i in range(41)]]
    cv.line(pts, 6, ORANGE, seg(s, 0.1, 1.2))
    if ph >= 2:
        for i in range(int(1 + 5 * seg(s, 0.1, 1.2))):
            cv.rect((1520, 700 - i * 60, 1640, 750 - i * 60), 4, ORANGE, fill=(60, 35, 10))
        cv.text((1580, 790), "FUEL IS HEAVY", 28, ORANGE)


def payload_trade(cv, s, T, ph=0):
    corner(cv, s, "FUEL vs PAYLOAD")
    if ph == 0:
        k = 0.35 + 0.25 * ease_io(clamp(s / max(T, 0.5)))
        x0, x1, y = 460, 1460, CY - 40
        xm = lerp(x0, x1, k)
        cv.rect((x0, y - 70, xm, y + 70), 0, fill=ORANGE, radius=8)
        cv.rect((xm, y - 70, x1, y + 70), 0, fill=(70, 70, 70), radius=8)
        cv.rect((x0, y - 70, x1, y + 70), 4, WHITE)
        cv.text(((x0 + xm) / 2, y), "FUEL", 36, BLACK)
        cv.text(((xm + x1) / 2, y), "PAYLOAD", 36, WHITE)
        cv.text((CX, y + 160), "+1 KG FUEL  =  −1 KG PAYLOAD", 38, WHITE, alpha=seg(s, 0.3, 0.4))
    else:
        for i, (pl, rng, lab) in enumerate(((0.3, 1.0, "SMALL PAYLOAD → VERY FAR"), (1.0, 0.6, "BIG PAYLOAD → LESS FAR"))):
            y = CY - 120 + i * 240
            cv.rect((300, y - 30, 300 + 160 * pl, y + 30), 0, fill=WHITE, radius=6)
            cv.arrow((520, y), (520 + 900 * rng, y), 6, ORANGE, seg(s, 0.2 + i * 0.4, 0.8), 24)
            cv.text((520, y - 60), lab, 30, WHITE, anchor="lm", alpha=seg(s, 0.3 + i * 0.4, 0.3))


def range_bars(cv, s, T, ph=0):
    corner(cv, s, "KNOWN FIGURES")
    cv.text((CX, CY - 120), "PAYLOAD: TENS OF KG", 60, WHITE, alpha=seg(s, 0.1, 0.3))
    cv.text((CX, CY + 20), "RANGE: 100s – 1,500+ KM", 60, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.tag((CX, CY + 160), "REPORTED · VARIES BY TYPE", 26, alpha=seg(s, 1.0, 0.3))


def clock(cv, s, T, ph=0):
    corner(cv, s, "1,000 KM")
    frac = lerp(5 / 12, 7 / 12, ease_io(clamp(s / max(T - 0.3, 0.5))))
    clock_icon(cv, (CX - 250, CY), 230, frac)
    cv.text((CX + 280, CY - 40), "5–7", 150, ORANGE)
    cv.text((CX + 280, CY + 90), "HOURS", 50, WHITE)


# ---------------- segment 3: navigation ----------------

def no_pilot(cv, s, T, ph=0):
    corner(cv, s, "AUTONOMOUS FLIGHT")
    cv.sprite("l31_operator", (CX - 450, CY + 40), 640, alpha=seg(s, 0, 0.5))
    a, b = (CX - 250, CY - 40), (CX + 200, CY - 40)
    cv.dashed([a, b], 4, GREY, offset=-s * 40, prog=seg(s, 0.2, 0.5))
    cross(cv, lerp_pt(a, b, 0.5), 50, RED, 10, seg(s, 0.6, 0.4))
    drone_side(cv, (CX + 400, CY - 40), 1.3, prop_spin=s * 20, prop_col=ORANGE)
    cv.text((CX + 400, CY + 110), "FLIES ITSELF", 36, ORANGE, alpha=seg(s, 0.9, 0.4))


def earth_los(cv, s, T, ph=0):
    corner(cv, s, "LINE OF SIGHT")
    R = 2600
    c = (CX, 760 + R - 40)
    cv.arc(c, R, 245, 295, 6, WHITE)
    gs = (420, 742)
    tower_icon(cv, (gs[0], gs[1] - 120), 0.9)
    t = clamp(s / max(T, 0.5)) if ph else 0.15 + 0.2 * clamp(s / max(T, 0.5))
    ang = math.radians(260 + 30 * lerp(0.1, 1.0, t))
    dpos = (c[0] + (R + 90) * math.cos(ang), c[1] + (R + 90) * math.sin(ang))
    drone_side(cv, dpos, 0.45, prop_spin=s * 20, col=ORANGE)
    src = (gs[0], gs[1] - 220)
    blocked = dpos[0] > 1480
    cv.dashed([src, (src[0] + 1400, src[1] + 180)] if blocked else [src, dpos], 4, WHITE if not blocked else RED,
              offset=s * 50)
    cv.text((CX, 230), "RADIO TRAVELS IN STRAIGHT LINES", 32, WHITE, alpha=seg(s, 0.2, 0.4))
    if ph and blocked:
        cv.text((dpos[0], dpos[1] - 120), "NO SIGNAL", 36, RED)


def ins_title(cv, s, T, ph=0):
    cv.text((CX, CY - 60), "METHOD 1", 40, GREY, alpha=seg(s, 0, 0.3))
    cv.text((CX, CY + 40), "INERTIAL NAVIGATION", 100, WHITE, alpha=seg(s, 0.15, 0.4))
    for i in range(int(6 * seg(s, 0.3, 1.0))):
        x = CX - 300 + i * 120
        cv.circle((x, CY + 200 + (20 if i % 2 else -20)), 16, 4, ORANGE)


def ins_path(cv, s, T, ph=0):
    corner(cv, s, "DEAD RECKONING")
    true_pts = [(260 + i * 35, CY + 60 * math.sin(i / 7)) for i in range(41)]
    cv.line(true_pts, 5, WHITE, seg(s, 0, 1.0) if ph == 0 else 1)
    cv.text((true_pts[-1][0] + 20, true_pts[-1][1]), "TRUE PATH", 26, WHITE, anchor="lm")
    drift = 0.0 if ph < 2 else 1.0
    est = [(x, y - (drift * (i / 40) ** 2 * 230)) for i, (x, y) in enumerate(true_pts)]
    p = seg(s, 0.3, 1.2)
    cv.dashed(est, 5, ORANGE, offset=s * 40, prog=p)
    if ph == 1:
        cv.rect((CX - 330, 760, CX + 330, 840), 4, ORANGE)
        cv.text((CX, 800), "NO OUTSIDE SIGNAL NEEDED", 32, ORANGE)
    if ph == 2:
        e = est[-1]
        cv.circle(e, 60 + 60 * seg(s, 0.5, 1.2), 3, RED)
        cv.text((e[0], e[1] - 160), "ERROR GROWS", 34, RED, alpha=seg(s, 0.8, 0.3))


def gnss(cv, s, T, ph=0):
    corner(cv, s, "METHOD 2 · SATELLITE NAVIGATION")
    sats = [(520, 200), (CX, 150), (1400, 200)]
    for x, y in sats:
        satellite_icon(cv, (x, y), 0.6)
    d = (CX, CY + 170)
    for x, y in sats:
        cv.dashed([(x, y + 40), d], 3, WHITE, offset=-s * 60, prog=seg(s, 0.1, 0.6))
    ghost = (CX + 140, CY + 90)
    k = seg(s, 0.8, 0.6)
    drone_top(cv, lerp_pt(ghost, d, k), 0.3, ORANGE, 4)
    cv.text((CX, 830), "GPS / GNSS  →  POSITION FIXED", 34, WHITE, alpha=seg(s, 1.0, 0.4))


def jam(cv, s, T, ph=0):
    corner(cv, s, "JAMMING" if ph == 0 else "SPOOFING")
    tw = (330, CY + 100)
    tower_icon(cv, tw, 1.1)
    rnd = random.Random(int(s * 12))
    for k in range(4):
        r = (s * 360 + k * 220) % 900
        pts = [(tw[0] + r * math.cos(math.radians(a)) + rnd.uniform(-10, 10),
                tw[1] - 100 + r * math.sin(math.radians(a)) + rnd.uniform(-10, 10)) for a in range(-30, 31, 4)]
        cv.line(pts, 3, RED)
    d = (CX + 330, CY - 20)
    drone_top(cv, d, 0.45, WHITE, 4)
    if ph == 0:
        cv.text((d[0], d[1] + 170), "SIGNAL DROWNED IN NOISE", 30, RED, alpha=seg(s, 0.4, 0.3))
    else:
        g = (d[0] + 260, d[1] - 220)
        a = seg(s, 0.2, 0.5)
        if a > 0:
            drone_top(cv, g, 0.45, ORANGE, 3)
            cv.dashed([d, g], 3, ORANGE, offset=s * 30)
        cv.text((g[0], g[1] + 150), "FAKE POSITION", 30, ORANGE, alpha=a)


def crpa(cv, s, T, ph=0):
    corner(cv, s, "ANTI-JAM ANTENNA (CRPA)")
    c = (CX, CY + 80)
    for i in range(7):
        a = i * math.pi / 3
        p = c if i == 6 else (c[0] + 80 * math.cos(a), c[1] + 80 * math.sin(a))
        cv.circle(p, 18, 4, WHITE)
    jam_dir = math.radians(200)
    for k in range(3):
        r = (s * 300 + k * 200) % 600 + 100
        cv.arc((c[0] + 0, c[1]), r, 180 + 5, 220 - 5, 3, RED)
    cv.text((260, CY + 40), "JAMMER", 30, RED)
    if ph:
        for a in range(0, 360, 8):
            rad = math.radians(a)
            dd = abs(((rad - jam_dir + math.pi) % (2 * math.pi)) - math.pi)
            r = 260 * (0.15 + 0.85 * clamp(dd / 0.9)) * seg(s, 0.1, 0.6)
            cv.dot((c[0] + r * math.cos(rad), c[1] + r * math.sin(rad) * 0.8), 4, ORANGE)
        cv.text((CX + 420, CY - 200), "NULL TOWARD THE JAMMER", 30, ORANGE, alpha=seg(s, 0.6, 0.4))
    for x in (CX + 200, CX + 420):
        satellite_icon(cv, (x, 170), 0.4)
        cv.dashed([(x, 200), c], 3, WHITE, offset=-s * 60)


def vision(cv, s, T, ph=0):
    corner(cv, s, "METHOD 3 · CAMERA + MAP")
    d = (CX - 360, 230)
    drone_top(cv, d, 0.35, WHITE, 4)
    cv.line([d, (CX - 600, 760)], 3, GREY)
    cv.line([d, (CX - 120, 760)], 3, GREY)
    for i in range(6):
        cv.line([(CX - 640 + i * 110, 600), (CX - 640 + i * 110, 820)], 2, DIM)
    for j in range(3):
        cv.line([(CX - 660, 600 + j * 110), (CX + 0, 600 + j * 110)], 2, DIM)
    rnd = random.Random(8)
    feats = [(rnd.uniform(-600, -100), rnd.uniform(620, 800)) for _ in range(6)]
    for x, y in feats:
        cv.circle((CX + x, y), 10, 3, WHITE)
    mx = CX + 420
    cv.rect((mx - 260, 330, mx + 260, 700), 4, WHITE)
    cv.text((mx, 300), "STORED MAP", 28, GREY)
    for x, y in feats:
        cv.circle((mx + (x + 350) * 0.8, 360 + (y - 600) * 1.2), 9, 3, GREY)
    a = seg(s, 0.6, 0.5)
    cv.rect((mx - 200, 360, mx + 200, 640), 6, ORANGE, prog=a)
    cv.text((mx, 760), "MATCH → POSITION", 34, ORANGE, alpha=seg(s, 1.0, 0.3))


def layers(cv, s, T, ph=0):
    corner(cv, s, "THREE LAYERS")
    labs = ("INERTIAL", "SATELLITE", "CAMERA")
    for i, lab in enumerate(labs):
        a = seg(s, 0.1 + i * 0.3, 0.3)
        y = 260 + i * 190
        cv.rect((CX - 330, y - 70, CX + 330, y + 70), 5, ORANGE if ph else WHITE, prog=a)
        cv.text((CX, y), lab, 44, WHITE, alpha=a)
    if ph:
        for i in range(2):
            y = 260 + i * 190 + 70
            cv.arrow((CX + 380, y - 30), (CX + 380, y + 80), 5, ORANGE, seg(s, 0.3, 0.4), 16)
            cv.arrow((CX - 380, y + 80), (CX - 380, y - 30), 5, ORANGE, seg(s, 0.5, 0.4), 16)
        cv.text((CX, 850), "EACH COVERS THE OTHERS' WEAKNESS", 32, ORANGE, alpha=seg(s, 0.6, 0.4))


# ---------------- segment 4: getting through ----------------

RADARS = [(1150, 300, 150), (1350, 520, 170), (1600, 330, 160), (1500, 700, 130), (1750, 560, 140), (1200, 720, 110)]


def ad_net(cv, s, T, ph=0):
    corner(cv, s, "AIR DEFENCE NETWORK")
    for i, (x, y, r) in enumerate(RADARS):
        a = seg(s, 0.1 + i * 0.15, 0.4)
        cv.circle((x, y), r * a, 3, RED if a >= 1 else GREY)
        cv.dot((x, y), 8, RED)
    cv.dot((1500, 480), 14, WHITE)
    cv.text((1500, 440), "MOSCOW", 30, WHITE)
    cv.text((480, CY - 30), "ONE OF THE DENSEST", 40, WHITE, alpha=seg(s, 0.8, 0.4))
    cv.text((480, CY + 30), "IN THE WORLD", 40, WHITE, alpha=seg(s, 0.8, 0.4))


def route(cv, s, T, ph=0):
    corner(cv, s, "ROUTE PLANNING")
    for x, y, r in RADARS:
        cv.circle((x, y), r, 3, RED)
        cv.dot((x, y), 8, RED)
    pts = [(250, 600), (700, 560), (1000, 520), (1180, 480), (1250, 420), (1380, 360), (1470, 450), (1500, 480)]
    smooth = []
    for i in range(len(pts) - 1):
        for k in range(10):
            smooth.append(lerp_pt(pts[i], pts[i + 1], k / 10))
    smooth.append(pts[-1])
    cv.dashed(smooth, 5, ORANGE, offset=s * 50, prog=seg(s, 0.2, max(T - 0.8, 0.6)))
    cv.text((500, 760), "THROUGH THE GAPS · LOW", 34, ORANGE, alpha=seg(s, 0.6, 0.4))


def low_alt(cv, s, T, ph=0):
    corner(cv, s, "LOW = LATE")
    R = 3000
    c = (CX, 800 + R)
    cv.arc(c, R, 250, 290, 6, WHITE)
    radar_dish(cv, (380, 700), 0.8)
    cv.line([(380, 660), (1800, 520)], 4, RED)
    cv.text((1300, 520), "RADAR BEAM", 26, RED)
    x = 1750 - (s * 140) % 1300
    drone_side(cv, (x, 730), 0.45, col=ORANGE, prop_spin=s * 20)
    seen = x < 700
    cv.text((CX, 300), "DETECTED LATE" if seen else "BELOW THE BEAM", 54, RED if seen else ORANGE)


def saturation(cv, s, T, ph=0):
    corner(cv, s, "SATURATION")
    cap = 4
    for i in range(cap):
        cv.rect((300 + i * 90, 160, 370 + i * 90, 230), 4, WHITE)
    cv.text((300 + cap * 90 + 30, 195), "TARGETS IT CAN ENGAGE AT ONCE", 26, WHITE, anchor="lm")
    c = (CX + 200, CY + 80)
    cv.circle(c, 90, 5, WHITE)
    rnd = random.Random(4)
    n = 14
    for i in range(n):
        ang = rnd.uniform(-2.6, 2.6) + math.pi
        dist0 = 780
        p = clamp(s / max(T, 1.0) * rnd.uniform(0.7, 1.0) + rnd.uniform(0, 0.15))
        r = lerp(dist0, 120 if i < cap else -200, p)
        pos = (c[0] + r * math.cos(ang), c[1] + r * math.sin(ang) * 0.7)
        decoy = ph and i % 3 == 0
        if decoy:
            cv.circle(pos, 10, 3, ORANGE)
        else:
            cv.dot(pos, 10, ORANGE)
        if i < cap and p > 0.5:
            cross(cv, pos, 16, RED, 4)
    if ph:
        cv.text((CX - 500, 820), "○ DECOYS  ● ATTACK DRONES", 30, ORANGE, alpha=seg(s, 0.3, 0.4))


def cost(cv, s, T, ph=0):
    corner(cv, s, "THE MATH")
    y1, y2 = CY - 100, CY + 100
    cv.text((420, y1), "DRONE", 36, WHITE, anchor="rm")
    cv.text((420, y2), "INTERCEPTOR", 36, WHITE, anchor="rm")
    cv.rect((460, y1 - 40, 460 + 180 * seg(s, 0.1, 0.4), y1 + 40), 0, fill=ORANGE, radius=8)
    if ph >= 1:
        cv.rect((460, y2 - 40, 460 + 1200 * seg(s, 0.1, 1.0), y2 + 40), 0, fill=RED, radius=8)
        cv.text((1700, y2), "× SEVERAL", 34, RED, anchor="lm", alpha=seg(s, 0.9, 0.3))
    cv.tag((CX, 800), "ESTIMATE · VARIES BY SYSTEM", 26, alpha=seg(s, 0.4, 0.3))
    if ph >= 2:
        cv.text((CX, 240), "DEFENDER WINS · STILL PAYS MORE", 44, WHITE, alpha=seg(s, 0.2, 0.4))


def ad_pull(cv, s, T, ph=0):
    corner(cv, s, "STRETCHED THIN")
    cv.line([(560, 160), (560, 820)], 6, WHITE)
    cv.text((560, 120), "FRONT LINE", 28, WHITE)
    cv.dot((1550, 420), 14, WHITE)
    cv.text((1550, 380), "MOSCOW", 30, WHITE)
    k = seg(s, 0.3, max(T - 0.8, 0.8))
    for i in range(5):
        a = (640, 220 + i * 130)
        b = (1450 + (i % 3) * 70, 360 + (i % 2) * 120)
        p = lerp_pt(a, b, k)
        cv.rect((p[0] - 26, p[1] - 18, p[0] + 26, p[1] + 18), 4, RED)
    cv.text((800, 860), "GAPS AT THE FRONT", 34, ORANGE, alpha=seg(s, 1.0, 0.4))


# ---------------- real-world results ----------------

def strike_cal(cv, s, T, ph=0):
    corner(cv, s, "REFINERY STRIKES · 2026")
    for d in range(30):
        x = 520 + (d % 10) * 90
        y = 240 + (d // 10) * 110
        hit = d % 3 == 2
        a = seg(s, 0.1 + d * 0.035, 0.2)
        cv.rect((x - 36, y - 40, x + 36, y + 40), 3, GREY)
        if hit and a > 0:
            cv.dot((x, y), 22 * a, ORANGE)
    cv.text((CX, 680), "≈ ONE HIT EVERY 3 DAYS", 54, ORANGE, alpha=seg(s, 1.0, 0.4))
    cv.tag((CX, 780), "IEA ANALYSIS", 26, alpha=seg(s, 1.3, 0.3))


def refine_drop(cv, s, T, ph=0):
    corner(cv, s, "RUSSIAN CRUDE RUNS · JUNE")
    base = 760
    h1 = 460
    h2 = h1 * (1 - 0.30 * seg(s, 0.5, 1.0))
    cv.rect((CX - 330, base - h1, CX - 110, base), 0, fill=(120, 120, 120), radius=6)
    cv.rect((CX + 110, base - h2, CX + 330, base), 0, fill=ORANGE, radius=6)
    cv.text((CX - 220, base + 40), "2025", 32, WHITE)
    cv.text((CX + 220, base + 40), "2026", 32, WHITE)
    cv.text((CX + 220, base - h2 - 60), "−30%", 70, ORANGE, alpha=seg(s, 1.0, 0.3))
    cv.tag((CX + 600, 300), "IEA", 26, alpha=seg(s, 1.2, 0.3))


def capacity_claim(cv, s, T, ph=0):
    corner(cv, s, "REFINING CAPACITY OFFLINE")
    c, R = (CX, CY + 120), 300
    cv.arc(c, R, 180, 360, 30, (60, 60, 60))
    p = seg(s, 0.2, 1.0)
    cv.arc(c, R, 180, 180 + 180 * 0.51 * p, 30, ORANGE)
    cv.text((c[0], c[1] - 80), f"{int(51 * p)}%", 120, ORANGE)
    cv.tag((CX, 820), "UKRAINIAN MoD CLAIM · NOT INDEPENDENTLY VERIFIED", 24, alpha=seg(s, 0.8, 0.3))


def cost_imposed(cv, s, T, ph=0):
    corner(cv, s, "COST IMPOSED")
    c = (CX - 300, CY)
    cv.circle(c, 160, 4, WHITE)
    cv.circle(c, 80, 4, WHITE)
    cv.dot(c, 14, WHITE)
    rnd = random.Random(9)
    for i in range(8):
        ang = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(220, 320)
        pos = (c[0] + r * math.cos(ang), c[1] + r * math.sin(ang))
        cv.dot(pos, 9, ORANGE)
        cross(cv, pos, 14, RED, 4, seg(s, 0.1 + i * 0.1, 0.2))
    items = ("AIRPORTS CLOSED", "AIR DEFENCE MOVED", "MISSILES SPENT")
    for i, it in enumerate(items):
        cv.text((CX + 120, CY - 120 + i * 110), "+ " + it, 38, ORANGE, anchor="lm", alpha=seg(s, 0.5 + i * 0.35, 0.3))


# ---------------- limits ----------------

WEAK = ("SLOW", "LOUD", "VISIBLE ON RADAR", "SMALL WARHEAD")


def weak(cv, s, T, ph=0):
    corner(cv, s, "WEAKNESSES")
    if ph < 0:
        cv.text((CX, CY - 40), "BUT…", 160, ORANGE, alpha=seg(s, 0.05, 0.3))
        cv.text((CX, CY + 120), "CLEAR WEAKNESSES", 50, WHITE, alpha=seg(s, 0.4, 0.3))
        return
    for i, w in enumerate(WEAK):
        if i > ph:
            break
        y = 260 + i * 130
        on = i == ph
        cv.text((CX - 300, y), f"0{i + 1}", 44, ORANGE if on else GREY, anchor="lm")
        cv.text((CX - 180, y), w, 56, WHITE if on else GREY, anchor="lm", alpha=seg(s, 0.05, 0.25) if on else 1)
    if ph == 1:
        sound_waves(cv, (CX + 420, 390), 1.0, ORANGE, 4, s * 1.5)


def counters(cv, s, T, ph=0):
    corner(cv, s, "RUSSIA ADAPTS")
    labs = ("MOBILE FIRE GROUPS", "ROOFTOP AIR DEFENCE", "JAMMERS", "INTERCEPTOR DRONES")
    for i, lab in enumerate(labs):
        a = seg(s, 0.2 + i * 0.6, 0.3)
        x = 330 + i * 420
        cv.rect((x - 180, CY - 150, x + 180, CY + 150), 4, WHITE if a >= 1 else DIM)
        cv.text((x, CY + 200), lab, 26, WHITE, alpha=a)
        if a <= 0:
            continue
        if i == 0:
            car_icon(cv, (x, CY + 20), 0.9)
        elif i == 1:
            cv.rect((x - 90, CY - 20, x + 90, CY + 100), 4, WHITE)
            cv.rect((x - 40, CY - 80, x + 40, CY - 20), 4, RED)
        elif i == 2:
            tower_icon(cv, (x, CY), 0.8)
        else:
            drone_top(cv, (x, CY), 0.3, RED, 4)


def question(cv, s, T, ph=0):
    drone_side(cv, (520, CY), 0.9, prop_spin=s * 20)
    cv.arrow((680, CY), (820, CY), 4, GREY, seg(s, 0.1, 0.4))
    cv.text((CX, CY), "?", 200, ORANGE, alpha=seg(s, 0.4, 0.3))
    x = 1150 + (s * 900) % 900
    for i in range(5):
        cv.line([(x - 300 - i * 40, CY - 40 + i * 20), (x - 60, CY - 40 + i * 20)], 3, ORANGE)
    cv.text((1450, CY + 160), "FASTER?", 50, ORANGE, alpha=seg(s, 0.8, 0.3))


def ep2(cv, s, T, ph=0):
    cv.text((CX, 200), "NEXT  ·  EP02  ·  FASTER THAN DEFENSE", 40, ORANGE, alpha=seg(s, 0, 0.3))
    labels = ["PALIANYTSIA", "PEKLO", "FLAMINGO"]
    for i, n in enumerate(labels):
        a = seg(s, 0.2 + i * 0.4, 0.3)
        x = 460 + i * 500
        cv.rect((x - 210, CY - 90, x + 210, CY + 90), 4, WHITE if a >= 1 else GREY)
        cv.text((x, CY), n, 44, WHITE, alpha=a)


def endcard(cv, s, T, ph=0):
    cv.text((CX, CY - 100), "DRONE WAR DECODED", 80, WHITE, alpha=seg(s, 0, 0.4))
    p = seg(s, 0.2, 0.7)
    cv.line([(CX - 420 * p, CY - 10), (CX + 420 * p, CY - 10)], 4, ORANGE)
    cv.text((CX, CY + 60), "NEXT  ·  EP02  ·  FASTER THAN DEFENSE", 38, ORANGE, alpha=seg(s, 0.6, 0.4))


SCENES = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_") and k not in (
    "corner", "clamp", "ease", "ease_io", "seg", "lerp", "lerp_pt")}
