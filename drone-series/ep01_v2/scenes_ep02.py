"""EP02 line-art scenes ("Faster Than Defense"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math
import random

from gfx import (DIM, GREY, ORANGE, RED, WHITE, car_icon, check, clamp, clock_icon, cross, drone_side, ease,
                 ease_io, jet_icon, lerp, lerp_pt, missile_icon, satellite_icon, seg, speedometer, tower_icon)
from scenes import BG_O, CX, CY, backdrop, corner, end_card, title_card


def jet_drone(cv, c, s=1.0, col=WHITE, w=5, flip=False, flame=0.0):
    """Side view of the cylindrical jet missile-drone (nose right unless flip)."""
    x, y = c
    d = -1 if flip else 1

    def P(dx, dy):
        return (x + d * dx * s, y + dy * s)

    body = [P(-190, -18), P(120, -22), P(200, -6), P(215, 0), P(200, 6), P(120, 22), P(-190, 18), P(-190, -18)]
    wing = [P(-10, 10), P(-80, 70), P(-40, 70), P(50, 14)]
    fin = [P(-170, -18), P(-205, -80), P(-175, -80), P(-130, -20)]
    intake = [P(-40, -22), P(-20, -38), P(40, -38), P(55, -22)]
    for pts in (body, wing, fin, intake):
        cv.line(pts, w, col)
    if flame > 0:
        L = 60 + 50 * flame
        cv.line([P(-190, -10), P(-190 - L, 0), P(-190, 10)], 4, ORANGE)


def booster(cv, c, s, col=ORANGE):
    x, y = c
    cv.rect((x - 60 * s, y - 14 * s, x + 60 * s, y + 14 * s), 4, col, radius=6)


# ---------------- cold open ----------------

def e2_radar_fast(cv, s, T, ph=0):
    c, R = (CX, CY), 330
    corner(cv, s, "RADAR")
    for r in (R, R * 0.66, R * 0.33):
        cv.circle(c, r, 3, DIM)
    a = s * 1.6
    cv.line([c, (c[0] + R * math.cos(a), c[1] + R * math.sin(a))], 4, WHITE)
    cv.circle(c, R, 5, WHITE)
    if ph == 0:
        for i in range(4):
            x = c[0] - 240 + s * 10
            cv.dot((x, c[1] - 120 + i * 70), 9, GREY)
        cv.text((c[0] + R + 160, c[1]), "SLOW: MINUTES", 30, GREY)
    else:
        p = clamp((s - 0.3) / 0.9) if ph == 2 else 0.0
        x = lerp(c[0] - R + 20, c[0] + R - 20, p)
        if ph == 2:
            cv.line([(max(c[0] - R + 20, x - 260), c[1] + 30), (x, c[1] + 30)], 6, ORANGE)
        cv.dot((x, c[1] + 30), 12, ORANGE)
        cv.text((c[0] + R + 170, c[1]), "FAST: SECONDS", 34, ORANGE, alpha=seg(s, 0.2, 0.3))


def e2_seconds(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    corner(cv, s, "TIME TO REACT")
    t = max(0.0, 20 - s * 4)
    cv.text((CX - 300, CY - 20), "MINUTES", 60, GREY)
    cross(cv, (CX - 300, CY - 20), 110, RED, 8, seg(s, 0.2, 0.4))
    cv.text((CX + 300, CY - 20), f"{t:04.1f} s", 110, ORANGE, alpha=seg(s, 0.4, 0.3))


def e2_like_drone(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    items = ("BUILT LIKE A DRONE", "LAUNCHED LIKE A DRONE", "FAR CHEAPER THAN A CRUISE MISSILE")
    for i, it in enumerate(items):
        a = seg(s, 0.2 + i * 0.5, 0.3)
        y = 300 + i * 150
        check(cv, (520, y), 30, ORANGE, 8, a)
        cv.text((600, y), it, 46, WHITE, anchor="lm", alpha=a)


def e2_flies_missile(cv, s, T, ph=0):
    x = lerp(300, 1500, ease(s / max(T, 0.5)))
    for i in range(5):
        cv.line([(x - 420 - i * 30, CY - 40 + i * 20), (x - 160, CY - 40 + i * 20)], 3, GREY)
    jet_drone(cv, (x, CY), 1.0, WHITE, 5, flame=1)
    cv.text((CX, 800), "…BUT IT FLIES LIKE A MISSILE", 46, ORANGE, alpha=seg(s, 0.5, 0.4))


def e2_intro(cv, s, T, ph=0):
    jet_drone(cv, (CX - 120, CY - 40), 1.4, WHITE, 5, flame=0.5 + 0.5 * math.sin(s * 9))
    cv.text((CX, CY + 170), "JET-POWERED MISSILE-DRONE", 40, ORANGE, alpha=seg(s, 0.4, 0.4))
    cv.text((CX, CY + 230), "WHY SPEED CHANGES THE MATH", 30, WHITE, alpha=seg(s, 0.9, 0.4))


def e2_title(cv, s, T, ph=0):
    title_card(cv, s, "EP02  ·  FASTER THAN DEFENSE", "jets")


# ---------------- background ----------------

SITES = {"VOTKINSK": (1500, 250), "KOTLUBAN": (1250, 600), "ROSTOV": (980, 700)}


def e2_strike_map(cv, s, T, ph=0):
    corner(cv, s, "2026 · STRIKES ON WEAPONS PLANTS")
    ukr = [(260, 520), (330, 430), (480, 400), (640, 420), (760, 470), (800, 560), (700, 640), (520, 670),
           (360, 640), (260, 520)]
    cv.line(ukr, 4, GREY)
    cv.text((520, 540), "UKRAINE", 34, GREY)
    a = (700, 480)
    show = {0: ("VOTKINSK", "KOTLUBAN", "ROSTOV"), 1: ("VOTKINSK", "KOTLUBAN"), 2: ("ROSTOV",)}[ph]
    labels = {"VOTKINSK": "MISSILE PLANT · FEB", "KOTLUBAN": "ARSENAL · FEB", "ROSTOV": "PARTS PLANT · SEP"}
    for i, n in enumerate(show):
        b = SITES[n]
        p = seg(s, 0.2 + i * 0.4, 0.9)
        mid = ((a[0] + b[0]) / 2, min(a[1], b[1]) - 140)
        pts = [lerp_pt(lerp_pt(a, mid, t / 30), lerp_pt(mid, b, t / 30), t / 30) for t in range(31)]
        cv.dashed(pts, 5, ORANGE, offset=s * 50, prog=p)
        if p > 0.98:
            cv.dot(b, 12, RED)
            cv.text((b[0], b[1] + 44), n, 30, WHITE)
            if ph:
                cv.text((b[0], b[1] + 80), labels[n], 24, ORANGE)


def e2_term(cv, s, T, ph=0):
    backdrop(cv, s, "jets")
    cv.text((CX, CY - 40), "MISSILE-DRONE", 120, WHITE, alpha=seg(s, 0.1, 0.4))
    cv.text((CX, CY + 80), "“RAKETA-DRON”", 44, ORANGE, alpha=seg(s, 0.6, 0.4))


def e2_cards(cv, s, T, ph=0):
    corner(cv, s, "THE FAMILY")
    cards = [("PALIANYTSIA", "UNVEILED AUG 2024", ""), ("PEKLO", "“HELL” · LATE 2024", "REPORTED"),
             ("RUTA", "", ""), ("FLAMINGO", "FIRE POINT · MUCH LARGER", "")]
    shown = {0: 1, 1: 2, 2: 4}[ph]
    for i in range(shown):
        name, sub, tag = cards[i]
        fresh = i >= {0: 0, 1: 1, 2: 2}[ph]
        a = seg(s, 0.1 + (i - {0: 0, 1: 1, 2: 2}[ph]) * 0.4, 0.3) if fresh else 1
        x = 300 + i * 440
        big = name == "FLAMINGO"
        h = 120 if big else 90
        cv.rect((x - 190, CY - h, x + 190, CY + h), 5 if fresh else 3, ORANGE if fresh else GREY)
        cv.text((x, CY - 15), name, 40 if big else 36, WHITE, alpha=a)
        if sub:
            cv.text((x, CY + 40), sub, 22, ORANGE if fresh else GREY, alpha=a)
        if tag:
            cv.tag((x, CY + h + 50), tag, 22, alpha=a)


def _doc(cv, s):
    """Faint spec sheet with a magnifier drifting over it (background for the caveat cards)."""
    col = (44, 44, 44)
    for k, (x, y) in enumerate(((200, 290), (1720, 310))):
        cv.rect((x - 150, y - 190, x + 150, y + 190), 3, col, radius=10)
        for i in range(8):
            cv.line([(x - 110, y - 140 + i * 40), (x + (110 if i % 3 else 40), y - 140 + i * 40)], 3, col)
        m = (x + 60 * math.sin(s * 0.8 + k), y + 40 * math.cos(s * 0.6 + k))
        cv.circle(m, 60, 4, BG_O)
        cv.line([(m[0] + 42, m[1] + 42), (m[0] + 100, m[1] + 100)], 7, BG_O)


def e2_caution(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    corner(cv, s, "A CAVEAT")
    _doc(cv, s)
    if ph == 0:
        cv.text((CX, CY - 20), "!", 260, ORANGE, alpha=seg(s, 0, 0.2))
        return
    if ph == 1:
        cv.tag((CX - 330, CY), "MANUFACTURER CLAIM", 36, alpha=seg(s, 0.1, 0.3))
        cv.tag((CX + 330, CY), "OFFICIAL CLAIM", 36, alpha=seg(s, 0.5, 0.3))
    if ph == 2:
        cv.text((CX, CY - 60), "INDEPENDENTLY VERIFIED", 50, WHITE)
        cv.text((CX, CY + 40), "VERY LITTLE", 80, RED, alpha=seg(s, 0.3, 0.3))
    if ph == 3:
        for i, t in enumerate(("REPORTED", "MANUFACTURER CLAIM", "OFFICIAL CLAIM", "ESTIMATE")):
            cv.tag((CX, 300 + i * 120), t, 34, alpha=seg(s, 0.1 + i * 0.25, 0.3))


def e2_adapt(cv, s, T, ph=0):
    corner(cv, s, "RUSSIA ADAPTS")
    labs = ("MACHINE-GUN TRUCKS", "ROOFTOP AIR DEFENCE", "LAYERED RADAR")
    for i, lab in enumerate(labs):
        a = seg(s, 0.2 + i * 0.5, 0.3)
        x = 420 + i * 540
        cv.rect((x - 200, CY - 150, x + 200, CY + 150), 4, WHITE if a >= 1 else DIM)
        cv.text((x, CY + 200), lab, 28, WHITE, alpha=a)
        if a <= 0:
            continue
        if i == 0:
            car_icon(cv, (x, CY + 20), 1.0)
            cv.line([(x - 20, CY - 50), (x + 60, CY - 90)], 6, RED)
        elif i == 1:
            cv.rect((x - 100, CY - 10, x + 100, CY + 110), 4, WHITE)
            cv.rect((x - 45, CY - 70, x + 45, CY - 10), 4, RED)
        else:
            for r in (40, 80, 120):
                cv.arc((x, CY + 60), r, 200, 340, 4, RED)
            cv.dot((x, CY + 60), 10, RED)


# ---------------- segment 1: turbojet ----------------

def e2_prop_vs_jet(cv, s, T, ph=0):
    corner(cv, s, "PROPELLER vs JET")
    if ph == 0:
        x, y = CX - 200, CY
        cv.rect((x - 120, y - 60, x + 80, y + 60), 5, WHITE)
        h = 140 * abs(math.cos(s * 18))
        cv.line([(x - 140, y - h), (x - 140, y + h)], 7, ORANGE)
        for i in range(8):
            off = (s * 220 + i * 60) % 480
            cv.line([(x - 180 - off, y - 120 + i * 34), (x - 150 - off, y - 120 + i * 34)], 4, GREY)
        cv.text((CX, 800), "PROPELLER PUSHES AIR BACK", 40, WHITE, alpha=seg(s, 0.3, 0.4))
    else:
        x, y = CX + 100, CY
        cv.line([(x - 260, y - 70), (x + 160, y - 50), (x + 200, y - 30), (x + 200, y + 30), (x + 160, y + 50),
                 (x - 260, y + 70), (x - 260, y - 70)], 5, WHITE)
        for i in range(4):
            off = (s * 1100 + i * 150) % 700
            cv.line([(x - 280 - off, y - 30 + i * 20), (x - 220 - off, y - 30 + i * 20)], 5, ORANGE)
        cv.text((CX, 800), "JET THROWS AIR BACK DIRECTLY — MUCH FASTER", 38, ORANGE, alpha=seg(s, 0.3, 0.4))


STAGES = [("COMPRESSOR", 560, 820), ("COMBUSTION", 820, 1080), ("TURBINE", 1080, 1260), ("NOZZLE", 1260, 1460)]


def _rotor_side(cv, x, y, R, ang, col, lean, n=8):
    """Bladed disc seen edge-on: blades sweep up and down as it turns; blades on the far side are dimmed."""
    for i in range(n):
        a = ang + 2 * math.pi * i / n
        h = R * math.sin(a)
        if abs(h) < 12:
            continue
        near = math.cos(a) > 0
        c = col if near else tuple(int(v * 0.35) for v in col)
        cv.line([(x, y - h), (x + lean, y - math.copysign(10, h))], 4 if near else 3, c)


def _rotor_face(cv, c, R, ang, col, label):
    """Front view of the same rotor, spinning (inset)."""
    cv.circle(c, R, 4, col)
    cv.circle(c, 14, 4, col)
    for i in range(9):
        a = ang + 2 * math.pi * i / 9
        pts = []
        for j in range(6):
            r = lerp(16, R - 6, j / 5)
            aa = a + 0.5 * j / 5
            pts.append((c[0] + r * math.cos(aa), c[1] + r * math.sin(aa)))
        cv.line(pts, 3, col)
    cv.text((c[0], c[1] + R + 34), label, 22, col)


def e2_turbojet(cv, s, T, ph=0):
    """Cut-away turbojet. ph 0 = overview, 1 compressor, 2 combustion, 3 turbine, 4 shaft, 5 nozzle."""
    corner(cv, s, "TURBOJET")
    y = CY - 20
    top = [(460, y - 150), (560, y - 170), (1080, y - 170), (1260, y - 140), (1460, y - 90)]
    bot = [(x, 2 * y - yy) for x, yy in top]
    cv.line(top, 6, WHITE)
    cv.line(bot, 6, WHITE)
    cv.line([(560, y), (1260, y)], 8 if ph == 4 else 4, ORANGE if ph == 4 else GREY)
    spin = s * 6.0  # compressor and turbine share the shaft, so they turn together
    for k in range(5):  # compressor stages
        _rotor_side(cv, 580 + k * 48, y, 140 - k * 10, spin + k * 0.3, ORANGE if ph in (1, 4) else WHITE, 18)
    for k in range(3):  # turbine stages
        _rotor_side(cv, 1110 + k * 50, y, 120, spin + k * 0.3, ORANGE if ph in (3, 4) else WHITE, -18)
    if ph in (1, 4):
        _rotor_face(cv, (300, y - 250), 85, spin, ORANGE, "COMPRESSOR")
    if ph in (3, 4):
        _rotor_face(cv, (1650, y - 250), 85, spin, ORANGE, "TURBINE")
    cv.rect((860, y - 110, 1040, y - 40), 4, ORANGE if ph == 2 else GREY, radius=20)
    cv.rect((860, y + 40, 1040, y + 110), 4, ORANGE if ph == 2 else GREY, radius=20)
    rnd = random.Random(1)
    n = 26
    for i in range(n):
        u = (s * (0.35 if ph != 5 else 0.6) + i / n) % 1.0
        x = lerp(380, 1640, u)
        lane = rnd.uniform(-1, 1)
        if x < 820:
            yy = y + lane * lerp(140, 70, clamp((x - 560) / 260))
            col, r = WHITE, 5
        elif x < 1080:
            yy = y + lane * 80
            col, r = (ORANGE if ph >= 2 else WHITE), 7
        else:
            yy = y + lane * lerp(80, 60, clamp((x - 1080) / 380))
            col, r = ORANGE, 5
        cv.dot((x, yy), r, col)
    for i, (name, x0, x1) in enumerate(STAGES):
        on = ph == 0 or ph == i + 1 or (ph == 4 and name in ("COMPRESSOR", "TURBINE")) or (ph == 5 and i == 3)
        a = seg(s, 0.2 + 0.25 * i, 0.3) if ph == 0 else 1
        cv.text(((x0 + x1) / 2, y + 230), f"{i + 1}. {name}", 28, ORANGE if on and ph else (WHITE if on else DIM),
                alpha=a)
    if ph == 4:
        cv.arrow((1170, y - 210), (690, y - 210), 5, ORANGE, seg(s, 0.2, 0.6), 18)
        cv.text((930, y - 250), "TURBINE DRIVES COMPRESSOR", 26, ORANGE, alpha=seg(s, 0.5, 0.3))
    if ph == 5:
        cv.arrow((1500, y), (1760, y), 8, ORANGE, seg(s, 0.1, 0.4), 28)


def _balloon_state(t, T):
    """Position, heading and radius of the released balloon at time t (deterministic, so the
    exhaust trail can be drawn from past states)."""
    t0 = 0.9  # held, fully inflated, until released
    if t <= t0:
        return (420, CY + 40), 0.0, 120.0
    u = clamp((t - t0) / max(T - t0 - 0.4, 1.5))

    def pos(v):
        return (lerp(420, 1820, ease(v) * 0.55 + v * 0.45), CY + 40 - 120 * v + 70 * math.sin(v * 11) * v)

    (x, y), (x2, y2) = pos(u), pos(min(u + 0.01, 1.0) if u < 1 else u)
    if u >= 1:
        (x2, y2), (x, y) = pos(1.0), pos(0.99)
        x, y, x2, y2 = x2, y2, 2 * x2 - x, 2 * y2 - y
    return (x, y), math.atan2(y2 - y, x2 - x), lerp(120, 42, u)


def e2_balloon(cv, s, T, ph=0):
    """Balloon released: air rushes out the back, the balloon shoots forward and shrinks."""
    backdrop(cv, s, "grid")
    (x, y), a, R = _balloon_state(s, T)
    ca, sa = math.cos(a), math.sin(a)

    def P(u, v):  # balloon-local (u forward, v sideways) -> screen
        return (x + u * ca - v * sa, y + u * sa + v * ca)

    # exhaust: puffs emitted at earlier moments, drifting backwards from where the nozzle was
    if s > 0.9:
        for k in range(1, 22):
            te = s - k * 0.06
            if te <= 0.9:
                break
            (px, py), pa, pr = _balloon_state(te, T)
            age = s - te
            d = pr * 1.25 + 30 + 500 * age
            q = (px - d * math.cos(pa) + 18 * math.sin(k * 2.1), py - d * math.sin(pa) + 18 * math.cos(k * 1.7))
            col = tuple(int(v * (1 - k / 22)) for v in WHITE)
            cv.circle(q, 6 + 14 * age, 3, col)
        # dashed trail of the path
        trail = [_balloon_state(te, T)[0] for te in [0.9 + (s - 0.9) * i / 30 for i in range(31)]]
        cv.dashed(trail, 3, DIM, offset=-s * 40)
    # body: slightly pear-shaped, nozzle at the back
    pts = []
    for i in range(41):
        th = 2 * math.pi * i / 40
        rr = R * (1 + 0.12 * math.cos(th))
        pts.append(P(rr * 1.1 * math.cos(th), rr * math.sin(th)))
    wob = 0.06 * R * math.sin(s * 30) if s > 0.9 else 0
    pts = [(px + wob * math.sin(i), py) for i, (px, py) in enumerate(pts)]
    cv.poly(pts, fill=(60, 34, 12), col=ORANGE, w=5)
    cv.line([P(R * 0.35, -R * 0.45), P(R * 0.6, -R * 0.15)], 5, (255, 200, 150))  # highlight
    neck = [P(-R * 0.95, -12), P(-R * 0.95 - 26, -16), P(-R * 0.95 - 26, 16), P(-R * 0.95, 12)]
    cv.line(neck, 4, ORANGE)
    if s <= 0.9:  # fingers pinching the neck
        n = P(-R * 0.95 - 34, 0)
        cv.line([(n[0] - 10, n[1] - 40), (n[0] + 4, n[1] - 6)], 7, WHITE)
        cv.line([(n[0] - 10, n[1] + 40), (n[0] + 4, n[1] + 6)], 7, WHITE)
        cv.line([(n[0] - 10, n[1] - 40), (n[0] - 140, n[1] - 70)], 7, WHITE)
        cv.line([(n[0] - 10, n[1] + 40), (n[0] - 140, n[1] + 60)], 7, WHITE)
        return
    if s > 1.2:
        cv.arrow(P(-R * 1.2 - 60, 0), P(-R * 1.2 - 230, 0), 5, WHITE, seg(s, 1.2, 0.3), 20)
        cv.arrow(P(R * 1.2 + 30, 0), P(R * 1.2 + 200, 0), 6, ORANGE, seg(s, 1.4, 0.3), 24)
    cv.text((560, 220), "AIR RUSHES OUT ←", 34, WHITE, alpha=seg(s, 1.3, 0.3))
    cv.text((1360, 220), "→ BALLOON SHOOTS FORWARD", 34, ORANGE, alpha=seg(s, 1.7, 0.3))


def e2_newton(cv, s, T, ph=0):
    corner(cv, s, "ACTION · REACTION")
    jet_drone(cv, (CX + 80, CY), 1.2, WHITE, 5, flame=1)
    cv.arrow((CX - 180, CY), (CX - 600, CY), 8, ORANGE, seg(s, 0.1, 0.5), 28)
    cv.text((CX - 420, CY - 60), "GAS BACK", 34, ORANGE, alpha=seg(s, 0.3, 0.3))
    cv.arrow((CX + 340, CY - 120), (CX + 700, CY - 120), 8, WHITE, seg(s, 0.6, 0.5), 28)
    cv.text((CX + 520, CY - 170), "DRONE FORWARD", 34, WHITE, alpha=seg(s, 0.8, 0.3))


def e2_small_strong(cv, s, T, ph=0):
    corner(cv, s, "SMALL JET ENGINE")
    cv.rect((CX - 420, CY - 60, CX - 180, CY + 60), 5, WHITE, radius=30)
    cv.arrow((CX - 140, CY), (CX + 460, CY), 14, ORANGE, seg(s, 0.2, 0.7), 40)
    cv.text((CX + 160, CY - 80), "BIG THRUST", 40, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.text((CX, 800), "SMALL · SIMPLE · POWERFUL FOR ITS WEIGHT", 38, WHITE, alpha=seg(s, 0.3, 0.4))


def e2_fuel(cv, s, T, ph=0):
    corner(cv, s, "THE CATCH")
    c = (CX, CY)
    cv.rect((c[0] - 120, c[1] - 200, c[0] + 120, c[1] + 200), 6, WHITE, radius=20)
    lvl = 1 - 0.85 * seg(s, 0.2, max(T - 0.3, 0.6))
    cv.rect((c[0] - 110, c[1] + 190 - 380 * lvl, c[0] + 110, c[1] + 190), 0, fill=ORANGE, radius=14)
    cv.text((c[0] + 260, c[1]), "FUEL", 70, ORANGE, anchor="lm")


# ---------------- segment 2: fuel vs speed ----------------

def e2_airmass(cv, s, T, ph=0):
    corner(cv, s, "SAME PUSH, DIFFERENT FUEL")
    rows = [(CY - 200, 18, 120, "PROPELLER: LOTS OF AIR, SLOWLY", WHITE),
            (CY + 20, 5, 520, "JET: LITTLE AIR, VERY FAST", ORANGE)]
    for k, (y, n, v, lab, col) in enumerate(rows):
        if ph == 0 and k == 1:
            continue
        for i in range(n):
            off = (s * v + i * (900 / n)) % 900
            yy = y - 50 + (i * 37) % 100
            cv.dot((1400 - off, yy), 8, col)
        cv.text((CX, y - 90), lab, 32, col)
    if ph == 2:
        cv.rect((620, 660, 620 + 220 * seg(s, 0.2, 0.5), 700), 0, fill=WHITE, radius=6)
        cv.rect((620, 730, 620 + 900 * seg(s, 0.4, 0.8), 770), 0, fill=ORANGE, radius=6)
        cv.text((600, 680), "FUEL · PROPELLER", 24, WHITE, anchor="rm")
        cv.text((600, 750), "FUEL · JET", 24, ORANGE, anchor="rm")


def e2_fuel_bars(cv, s, T, ph=0):
    corner(cv, s, "FUEL BURNED, SAME JOB")
    base = 760
    cv.rect((CX - 330, base - 140 * seg(s, 0.1, 0.5), CX - 110, base), 0, fill=WHITE, radius=6)
    cv.rect((CX + 110, base - 520 * seg(s, 0.4, 0.9), CX + 330, base), 0, fill=ORANGE, radius=6)
    cv.text((CX - 220, base + 40), "PROPELLER", 30, WHITE)
    cv.text((CX + 220, base + 40), "SMALL JET", 30, ORANGE)
    cv.text((CX + 220, base - 580), "FAR MORE", 44, ORANGE, alpha=seg(s, 1.0, 0.3))


def e2_tradeoff(cv, s, T, ph=0):
    corner(cv, s, "THE PRICE OF A THIRSTY ENGINE")
    opts = ("MORE FUEL", "SHORTER RANGE", "BOTH") if ph == 0 else ("LESS RANGE", "LESS PAYLOAD", "BIGGER · PRICIER")
    for i, o in enumerate(opts):
        a = seg(s, 0.2 + i * 0.4, 0.3)
        x = 400 + i * 560
        cv.rect((x - 230, CY - 90, x + 230, CY + 90), 5, ORANGE if i == 2 else WHITE, prog=a)
        cv.text((x, CY), o, 38, WHITE, alpha=a)


def e2_range_bars(cv, s, T, ph=0):
    corner(cv, s, "RANGE")
    rows = [("PEKLO (JET)", 700, ORANGE, "~700 KM · UKRAINIAN GOV'T"), ("PROPELLER DRONES", 1500, WHITE, "UP TO 1,500+ KM · REPORTED")]
    for i, (lab, km, col, note) in enumerate(rows):
        y = CY - 100 + i * 200
        p = seg(s, 0.2 + i * 0.4, 0.8)
        cv.text((520, y), lab, 32, col, anchor="rm")
        cv.rect((560, y - 35, 560 + 0.75 * km * p, y + 35), 0, fill=col, radius=6)
        cv.text((560, y + 70), note, 24, col, anchor="lm", alpha=seg(s, 0.6 + i * 0.4, 0.3))


def e2_word(cv, s, T, ph=0):
    word = {0: "SPEED", 1: "KEY IDEA", 2: "QUICK MATH", 3: "KEY POINT", 4: "CHEAP MISSILE"}[ph]
    backdrop(cv, s, {0: "jets", 1: "radar", 2: "grid", 3: "radar", 4: "jets"}[ph])
    if ph == 2:
        for i, tok in enumerate(("4 KM", "÷", "150 KM/H", "=", "95 s", "4 KM", "÷", "700 KM/H", "=", "20 s")):
            x, y = 260 + (i % 5) * 350, (230 if i < 5 else 720)
            cv.text((x, y - s * 6), tok, 44, (52, 52, 52))
    sc = 1 + 0.25 * (1 - seg(s, 0, 0.35))
    cv.text((CX, CY), word, int(150 * sc), ORANGE)


def e2_two_gauges(cv, s, T, ph=0):
    corner(cv, s, "CRUISE SPEED")
    speedometer(cv, (CX - 420, CY + 120), 250, lerp(0, 175, seg(s, 0.1, 0.8)), 1000, band=(150, 200))
    cv.text((CX - 420, CY + 200), "PROPELLER  150–200 KM/H", 30, WHITE)
    if ph:
        speedometer(cv, (CX + 420, CY + 120), 250, lerp(0, 700, seg(s, 0.1, 1.0)), 1000, band=(650, 900))
        cv.text((CX + 420, CY + 200), "JET  ~700 KM/H (UP TO ~900)", 30, ORANGE)
        cv.tag((CX + 420, CY + 270), "REPORTED / CLAIMED", 24, alpha=seg(s, 0.6, 0.3))


def e2_flight_time(cv, s, T, ph=0):
    corner(cv, s, "TIME IN THE AIR")
    cv.rect((420, CY - 120, 420 + 1080 * seg(s, 0.1, 1.0), CY - 40), 0, fill=WHITE, radius=8)
    cv.text((400, CY - 80), "PROPELLER", 30, WHITE, anchor="rm")
    cv.text((1520, CY - 80), "~5 H", 40, WHITE, anchor="lm", alpha=seg(s, 1.0, 0.3))
    cv.rect((420, CY + 60, 420 + 240 * seg(s, 0.6, 0.5), CY + 140), 0, fill=ORANGE, radius=8)
    cv.text((400, CY + 100), "JET", 30, ORANGE, anchor="rm")
    cv.text((700, CY + 100), "~1 H", 40, ORANGE, anchor="lm", alpha=seg(s, 1.0, 0.3))


# ---------------- segment 3: engagement window ----------------

def _gun(cv, c, col=WHITE):
    x, y = c
    cv.rect((x - 40, y - 20, x + 40, y + 20), 4, col, radius=6)
    cv.line([(x, y - 10), (x + 70, y - 70)], 6, col)


def e2_bubble(cv, s, T, ph=0):
    corner(cv, s, "THE BUBBLE")
    c = (CX - 150, CY + 40)
    _gun(cv, c)
    R = 300 * seg(s, 0.1, 0.6)
    cv.circle(c, R, 4, RED)
    cv.d.ellipse(((c[0] - R) * 2, (c[1] - R) * 2, (c[0] + R) * 2, (c[1] + R) * 2), fill=(235, 64, 52, 35))
    if ph >= 1:
        x = 1700 - (s * 220) % 1500
        inside = abs(x - c[0]) < 300
        drone_side(cv, (x, c[1] - 40), 0.35, col=RED if inside else WHITE, flip=True)
        cv.text((CX + 420, 230), "DANGER ONLY INSIDE", 34, RED, alpha=seg(s, 0.4, 0.3))


def e2_window(cv, s, T, ph=0):
    """ph 0: setup (4 km). 1: slow pass 95 s. 2: fast pass 20 s. 3: both side by side. 4: reaction time eats window."""
    corner(cv, s, "ENGAGEMENT WINDOW")
    if ph == 0:
        g = (CX + 400, CY + 60)
        _gun(cv, g)
        cv.arrow((g[0] - 60, g[1] + 120), (g[0] - 860, g[1] + 120), 4, WHITE, seg(s, 0.2, 0.6), 18)
        cv.text((g[0] - 460, g[1] + 170), "≈ 4 KM  (ASSUMED FOR SIMPLICITY)", 30, WHITE, alpha=seg(s, 0.5, 0.3))
        drone_side(cv, (g[0] - 1000 + s * 60, g[1] - 60), 0.4, flip=False)
        return
    rows = [] if ph == 4 else ([("150 KM/H", 95, WHITE)] if ph == 1 else [("700 KM/H", 20, ORANGE)] if ph == 2
                               else [("150 KM/H", 95, WHITE), ("700 KM/H", 20, ORANGE)])
    for i, (lab, secs, col) in enumerate(rows):
        y = CY - 60 + i * 220 if len(rows) == 2 else CY
        cv.line([(400, y + 60), (1520, y + 60)], 3, DIM)
        prog = clamp(s / max(T * 0.9, 1.0)) if ph != 3 else 1.0
        x = lerp(400, 1520, prog)
        drone_side(cv, (x, y), 0.35, col=col)
        cv.text((300, y), lab, 30, col, anchor="rm")
        left = secs * (1 - prog)
        cv.text((1640, y), f"{left:4.0f} s" if ph != 3 else f"≈ {secs:.0f} s", 56, col, anchor="lm")
    if ph == 3:
        cv.text((CX, 850 - 60), "≈ 1/5 OF THE TIME", 44, ORANGE, alpha=seg(s, 0.5, 0.3))
    if ph == 4:
        x0, x1, y = 420, 1500, CY
        cv.rect((x0, y - 50, x1, y + 50), 4, ORANGE)
        cv.text((CX, y - 100), "20 SECONDS", 40, ORANGE)
        parts = (("DETECT", 0.25), ("TURN THE GUN", 0.22), ("AIM", 0.2))
        acc = x0
        for i, (lab, frac) in enumerate(parts):
            a = seg(s, 0.2 + i * 0.4, 0.4)
            w = (x1 - x0) * frac * a
            cv.rect((acc, y - 46, acc + w, y + 46), 0, fill=(110, 40, 30), radius=4)
            if a > 0.5:
                cv.text((acc + w / 2, y), lab, 24, WHITE)
            acc += (x1 - x0) * frac
        cv.text((CX, y + 120), "WHAT'S LEFT TO SHOOT", 32, WHITE, alpha=seg(s, 1.4, 0.3))


def e2_lead(cv, s, T, ph=0):
    corner(cv, s, "AIM WHERE IT WILL BE")
    g = (420, 800)
    _gun(cv, g)
    speed = 1 if ph == 0 else 3.2
    x = 700 + (s * 90 * speed) % 700
    tgt = (x, 320)
    fut = (x + 160 * speed, 320)
    drone_side(cv, tgt, 0.35, col=ORANGE if ph else WHITE)
    cv.circle(fut, 26, 3, RED)
    cv.dashed([(g[0] + 60, g[1] - 70), fut], 3, RED, offset=s * 40)
    cv.dashed([tgt, fut], 3, GREY)
    cv.text((fut[0], 260), "AIM POINT", 24, RED)
    if ph:
        cv.text((CX + 300, 860), "FASTER → AIM FURTHER AHEAD → SMALL ERRORS MISS", 30, ORANGE, alpha=seg(s, 0.4, 0.3))


def e2_key(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    if ph == 0:
        cv.text((CX, CY - 40), "NOT INVISIBLE", 90, WHITE, alpha=seg(s, 0.1, 0.3))
        cv.circle((CX, CY + 120), 40, 5, WHITE)
        cv.dot((CX, CY + 120), 14, WHITE)
    else:
        clock_icon(cv, (CX - 300, CY), 160, 0.9 - 0.8 * seg(s, 0.1, 1.0), accent=RED)
        cv.text((CX + 220, CY - 30), "IT STEALS", 70, WHITE, anchor="lm")
        cv.text((CX + 220, CY + 60), "THE DEFENDER'S TIME", 50, ORANGE, anchor="lm")


# ---------------- segment 4: drone or cruise missile ----------------

def e2_venn(cv, s, T, ph=0):
    corner(cv, s, "DRONE OR CRUISE MISSILE?")
    sep = lerp(300, 170, seg(s, 0.1, 1.0)) if ph >= 1 else 300
    l, r = (CX - sep, CY), (CX + sep, CY)
    cv.circle(l, 280, 5, WHITE)
    cv.circle(r, 280, 5, ORANGE)
    cv.text((l[0] - 120, CY - 300), "DRONE", 40, WHITE)
    cv.text((r[0] + 120, CY - 300), "CRUISE MISSILE", 40, ORANGE)
    if ph == 0:
        cv.text((CX, CY), "?", 140, WHITE)
    if ph == 2:
        for i, t in enumerate(("WINGS", "FINDS ITS OWN WAY", "ONE-WAY")):
            cv.text((CX, CY - 70 + i * 70), t, 28, WHITE, alpha=seg(s, 0.2 + i * 0.3, 0.3))
    if ph == 3:
        for i, t in enumerate(("SPEED", "SIZE", "PRICE")):
            cv.tag((CX, 820 - 40 + 0 * i) if False else (CX - 400 + i * 400, 860), t, 34, alpha=seg(s, 0.2 + i * 0.3, 0.3))


def e2_cost_fraction(cv, s, T, ph=0):
    corner(cv, s, "PRICE (FEW RELIABLE FIGURES)")
    y1, y2 = CY - 90, CY + 90
    cv.text((520, y1), "CRUISE MISSILE", 32, WHITE, anchor="rm")
    cv.text((520, y2), "MISSILE-DRONE", 32, ORANGE, anchor="rm")
    cv.rect((560, y1 - 40, 560 + 1100 * seg(s, 0.1, 0.8), y1 + 40), 0, fill=WHITE, radius=8)
    cv.rect((560, y2 - 40, 560 + 260 * seg(s, 0.5, 0.6), y2 + 40), 0, fill=ORANGE, radius=8)
    cv.text((860, y2), "A FRACTION?", 34, ORANGE, anchor="lm", alpha=seg(s, 1.0, 0.3))
    cv.tag((CX, 820), "ESTIMATE", 26, alpha=seg(s, 0.8, 0.3))


def e2_flamingo(cv, s, T, ph=0):
    corner(cv, s, "FP-5 FLAMINGO")
    x, y = CX, CY - 40
    cv.line([(x - 420, y - 40), (x + 360, y - 40), (x + 470, y), (x + 360, y + 40), (x - 420, y + 40),
             (x - 420, y - 40)], 6, WHITE)
    cv.line([(x - 300, y - 40), (x - 250, y - 110), (x - 60, y - 110), (x - 20, y - 40)], 5, WHITE)
    cv.line([(x - 40, y + 40), (x - 150, y + 170), (x - 80, y + 170), (x + 60, y + 40)], 5, WHITE)
    if ph == 0:
        cv.text((CX - 300, 760), "~3,000 KM", 64, ORANGE, alpha=seg(s, 0.3, 0.3))
        cv.text((CX + 300, 760), "~1 T WARHEAD", 64, ORANGE, alpha=seg(s, 0.7, 0.3))
        cv.tag((CX, 850), "MANUFACTURER CLAIM", 26, alpha=seg(s, 1.0, 0.3))
    elif ph == 1:
        cv.text((CX, 780), "≈ A CRUISE MISSILE", 64, ORANGE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX, 740), "~100 / MONTH", 80, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.tag((CX, 840), "REPORTED · ESTIMATES RANGE ~90–200", 26, alpha=seg(s, 0.6, 0.3))


def e2_booster(cv, s, T, ph=0):
    corner(cv, s, "ROCKET BOOSTER LAUNCH")
    rail0, rail1 = (380, 820), (900, 560)
    cv.line([rail0, rail1], 8, GREY)
    t = clamp((s - 0.4) / max(T - 0.6, 0.8))
    path = lambda u: lerp_pt(rail1, (1700, 260), u)  # noqa: E731
    pos = rail0 if t <= 0 else path(ease_io(t))
    jet_drone(cv, pos, 0.7, WHITE, 4, flame=1 if t > 0 else 0)
    sep = t > 0.35
    if not sep:
        booster(cv, (pos[0] - 60, pos[1] + 30), 1.0)
        if t > 0:
            cv.line([(pos[0] - 120, pos[1] + 30), (pos[0] - 260, pos[1] + 50)], 10, ORANGE)
        cv.text((CX, 900 - 60), "BOOSTER PUSHES FOR A FEW SECONDS", 30, ORANGE)
    else:
        bp = path(0.35)
        fall = (t - 0.35) * 500
        booster(cv, (bp[0] - 60, bp[1] + 30 + fall), 1.0, GREY)
        cv.text((CX, 840), "…THEN DROPS AWAY", 34, WHITE)


def e2_rail(cv, s, T, ph=0):
    corner(cv, s, "OFF A RAIL")
    rail0, rail1 = (420, 800), (1100, 460)
    cv.line([rail0, rail1], 10, WHITE)
    for k in range(8):
        p = lerp_pt(rail0, rail1, k / 7)
        cv.line([p, (p[0], 860)], 4, GREY)
    u = seg(s, 0.3, 1.0)
    pos = lerp_pt(rail0, (1500, 260), u)
    jet_drone(cv, pos, 0.6, ORANGE, 4, flame=1)
    booster(cv, (pos[0] - 50, pos[1] + 26), 0.9)


# ---------------- limits ----------------

def e2_limits(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    corner(cv, s, "LIMITS")
    items = ("1. COST", "2. RANGE", "3. HEAT · NOISE · RADAR")
    for i, it in enumerate(items):
        on = i == ph
        cv.text((CX, 320 + i * 150), it, 64 if on else 44, ORANGE if on else DIM,
                alpha=seg(s, 0.05, 0.3) if on else 1)


def e2_parts_cost(cv, s, T, ph=0):
    corner(cv, s, "PARTS")
    left = ("PISTON ENGINE", "FOAM WINGS")
    right = ("JET ENGINE", "ROCKET BOOSTER", "FAST AIRFRAME")
    for i, t in enumerate(left):
        cv.text((CX - 420, 360 + i * 100), t, 34, WHITE, alpha=seg(s, 0.1, 0.3))
    for i, t in enumerate(right):
        cv.text((CX + 420, 330 + i * 100), t, 34, ORANGE, alpha=seg(s, 0.4 + i * 0.2, 0.3))
    cv.text((CX - 420, 700), "$", 90, WHITE)
    cv.text((CX + 420, 700), "$$$$", 90, ORANGE, alpha=seg(s, 1.0, 0.3))


def e2_one_vs_many(cv, s, T, ph=0):
    corner(cv, s, "SAME MONEY")
    jet_drone(cv, (CX - 450, CY), 0.9, ORANGE, 5)
    cv.text((CX - 120, CY), "=", 100, WHITE)
    n = int(1 + 9 * seg(s, 0.3, 1.2))
    for i in range(n):
        x = CX + 120 + (i % 5) * 150
        y = CY - 80 + (i // 5) * 160
        drone_side(cv, (x, y), 0.3)
    cv.text((CX + 420, CY + 230), "SEVERAL PROPELLER DRONES", 30, WHITE, alpha=seg(s, 1.0, 0.3))


def e2_speed_ladder(cv, s, T, ph=0):
    corner(cv, s, "FAST… COMPARED TO WHAT?")
    rows = [("PROPELLER DRONE", 180, WHITE), ("JET MISSILE-DRONE", 700, ORANGE), ("FIGHTER JET", 2000, GREY),
            ("AIR-DEFENCE MISSILE", 3500, RED)]
    for i, (lab, v, col) in enumerate(rows):
        y = 300 + i * 140
        p = seg(s, 0.1 + i * 0.25, 0.6)
        cv.text((560, y), lab, 30, col, anchor="rm")
        cv.rect((600, y - 30, 600 + 0.33 * v * p, y + 30), 0, fill=col, radius=6)
    cv.tag((CX, 840), "ILLUSTRATIVE SPEEDS (KM/H)", 24, alpha=seg(s, 1.0, 0.3))
    if ph:
        cv.arrow((600 + 0.33 * 3500, 720), (600 + 0.33 * 700 + 40, 460), 6, RED, seg(s, 0.3, 0.6), 24)
        cv.text((1400, 640), "CAN STILL INTERCEPT", 30, RED, alpha=seg(s, 0.7, 0.3))


def e2_who_stops(cv, s, T, ph=0):
    corner(cv, s, "WHO HAS TO STOP IT")
    _gun(cv, (CX - 450, CY))
    cv.text((CX - 450, CY + 110), "CHEAP GUN", 32, WHITE)
    if ph:
        cross(cv, (CX - 430, CY - 20), 110, RED, 10, seg(s, 0.1, 0.4))
        missile_icon(cv, (CX + 300, CY - 120), 0.7, RED)
        jet_icon(cv, (CX + 300, CY + 120), 0.6, RED)
        cv.text((CX + 300, CY + 260), "EXPENSIVE MISSILES & JETS", 32, RED, alpha=seg(s, 0.4, 0.3))


def e2_recap(cv, s, T, ph=0):
    corner(cv, s, "EPISODES 1 & 2")
    drone_side(cv, (CX - 420, CY - 40), 0.8)
    cv.text((CX - 420, CY + 120), "SLOW · THRIFTY", 44, WHITE, alpha=seg(s, 0.2, 0.3))
    jet_drone(cv, (CX + 420, CY - 40), 0.8, ORANGE, 5, flame=1)
    cv.text((CX + 420, CY + 120), "FAST · EXPENSIVE", 44, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.text((CX, CY - 40), "OR", 50, GREY)


def e2_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP03  ·  THE $500 KILLER", "drones")


SCENES = {k: v for k, v in globals().items() if k.startswith("e2_") and callable(v)}
