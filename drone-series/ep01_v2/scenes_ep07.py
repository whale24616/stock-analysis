"""EP07 line-art scenes ("Catch the Jet Drone"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math

from gfx import DIM, GREY, ORANGE, RED, WHITE, check, clamp, clock_icon, cross, ease, jet_icon, lerp, lerp_pt, seg
from scenes import BG, BG_O, CX, CY, backdrop, end_card, title_card
from scenes_ep03 import big_word, quad_top
from scenes_ep06 import geran


# ---------------- icons ----------------

def jet_geran(cv, c, s=1.0, col=RED, w=5, a=0.0):
    """Top view of the jet Geran: long tube body, straight wings, small tail, engine pod on top."""
    ca, sa = math.cos(a), math.sin(a)

    def P(dx, dy):
        return (c[0] + (dx * ca - dy * sa) * s, c[1] + (dx * sa + dy * ca) * s)

    cv.line([P(170, 0), P(140, -14), P(-150, -14), P(-150, 14), P(140, 14), P(170, 0)], w, col)
    cv.line([P(20, -14), P(-10, -150), P(-40, -150), P(-30, -14)], w, col)
    cv.line([P(20, 14), P(-10, 150), P(-40, 150), P(-30, 14)], w, col)
    cv.line([P(-120, -14), P(-150, -60), P(-160, -60), P(-150, -14)], w - 1, col)
    cv.line([P(-120, 14), P(-150, 60), P(-160, 60), P(-150, 14)], w - 1, col)
    cv.rect((min(P(-60, -8)[0], P(-140, 8)[0]), min(P(-60, -8)[1], P(-140, 8)[1]),
             max(P(-60, -8)[0], P(-140, 8)[0]), max(P(-60, -8)[1], P(-140, 8)[1])), 3, col, radius=4)


def interceptor(cv, c, s=1.0, col=ORANGE, w=4, a=0.0):
    """Small fast interceptor: dart body with short wings."""
    ca, sa = math.cos(a), math.sin(a)

    def P(dx, dy):
        return (c[0] + (dx * ca - dy * sa) * s, c[1] + (dx * sa + dy * ca) * s)

    cv.line([P(90, 0), P(-60, -12), P(-60, 12), P(90, 0)], w, col)
    cv.line([P(0, -6), P(-40, -60), P(-55, -60), P(-30, -8)], w, col)
    cv.line([P(0, 6), P(-40, 60), P(-55, 60), P(-30, 8)], w, col)


def burst(cv, c, r=60, col=ORANGE, w=4):
    for k in range(10):
        a = k * 0.63
        cv.line([(c[0] + r * 0.5 * math.cos(a), c[1] + r * 0.5 * math.sin(a)),
                 (c[0] + r * math.cos(a), c[1] + r * math.sin(a))], w, col)


# ---------------- cold open ----------------

def e7_radar_blip(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    c, R = (CX, CY), 380
    for r in (R, R * 0.66, R * 0.33):
        cv.circle(c, r, 3, GREY)
    a = s * 1.4
    cv.line([c, (c[0] + R * math.cos(a), c[1] + R * math.sin(a))], 3, ORANGE)
    p = (s * 0.35) % 1
    b = (lerp(c[0] + 340, c[0] - 300, p), lerp(c[1] - 220, c[1] + 140, p))
    for k in range(6):
        q = (lerp(c[0] + 340, c[0] - 300, max(0, p - k * 0.03)), lerp(c[1] - 220, c[1] + 140, max(0, p - k * 0.03)))
        cv.dot(q, 10 - k, RED)
    cv.dot(b, 12, RED)
    cv.text((CX, 840), "A FAST DOT ON THE RADAR", 40, WHITE, alpha=seg(s, 0.4, 0.3))


def e7_intro(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    p = (s * 0.25) % 1
    jet_geran(cv, (lerp(1800, 200, p), CY - 60), 0.8, RED, 4, a=math.pi)
    interceptor(cv, (lerp(200, 1800, p) * 0 + lerp(500, 900, ease(seg(s, 0.2, 2))), CY + 120), 0.9, ORANGE, 4,
                a=-0.4)
    cv.text((CX, 820), "THE SPEED RACE", 56, ORANGE, alpha=seg(s, 0.3, 0.4))


def e7_title(cv, s, T, ph=0):
    title_card(cv, s, "EP07  ·  CATCH THE JET DRONE", "radar")


# ---------------- the jet Geran ----------------

def e7_speed(cv, s, T, ph=0):
    """ph0 propeller Geran 185 km/h, ph1 Geran-5 450–600 km/h, ph2 ~3x."""
    backdrop(cv, s, "grid")
    rows = [("PROPELLER GERAN", 185, "~185 KM/H", GREY), ("GERAN-5 (JET)", 600, "450–600 KM/H", RED)]
    for i, (lab, v, txt, col) in enumerate(rows[:1 + (ph >= 1)]):
        y = 300 + i * 200
        new = i == ph and ph < 2
        p = ease(seg(s, 0.1, 1.0)) if new else 1.0
        cv.text((240, y - 60), lab, 34, col, anchor="lm")
        w = 1300 * v / 600
        if i == 1:
            cv.rect((240, y - 22, 240 + 1300 * 450 / 600 * p, y + 22), 0, fill=col, radius=6)
            cv.rect((240 + 1300 * 450 / 600 * p, y - 22, 240 + w * p, y + 22), 3, col, radius=6)
        else:
            cv.rect((240, y - 22, 240 + w * p, y + 22), 0, fill=col, radius=6)
        cv.text((240 + w * p + 30, y), txt, 38, col, anchor="lm", alpha=seg(s, 0.6, 0.3) if new else 1.0)
    if ph == 2:
        cv.text((CX, 760), "NEARLY 3× FASTER", 70, RED, alpha=seg(s, 0.1, 0.3))


def e7_shape(cv, s, T, ph=0):
    """ph0 the old delta Geran, ph1 the new jet Geran looks like a cruise missile."""
    backdrop(cv, s, "grid")
    geran(cv, (CX - 420, CY), 1.3, GREY if ph else RED, 5)
    cv.text((CX - 420, CY + 230), "DELTA WING · PROPELLER", 32, GREY)
    if ph >= 1:
        cv.arrow((CX - 130, CY), (CX + 80, CY), 5, ORANGE, seg(s, 0.1, 0.4), 22)
        jet_geran(cv, (CX + 420, CY), 1.2, RED, 5)
        cv.text((CX + 420, CY + 230), "TUBE BODY · STRAIGHT WINGS · JET", 32, RED, alpha=seg(s, 0.4, 0.3))
        cv.text((CX, 170), "LOOKS LIKE A CRUISE MISSILE", 46, WHITE, alpha=seg(s, 0.8, 0.3))


def e7_growth(cv, s, T, ph=0):
    """ph0 axis, ph1 June ~350 → August ~2,800, ph2 8x."""
    backdrop(cv, s, "grid")
    base = 720
    cv.line([(360, base), (1560, base)], 3, GREY)
    cv.text((CX, 170), "JET-DRONE ATTACKS PER MONTH (REPORTED)", 36, WHITE)
    vals = [("JUNE", 350), ("JULY", None), ("AUGUST", 2800)]
    for i, (m, v) in enumerate(vals):
        x = 560 + i * 400
        cv.text((x, base + 40), m, 30, GREY)
        if v and ph >= 1:
            p = ease(seg(s, 0.2 + i * 0.4, 1.0)) if ph == 1 else 1.0
            h = 460 * v / 2800 * p
            cv.rect((x - 80, base - h, x + 80, base), 0, fill=RED if v > 1000 else GREY, radius=6)
            if p > 0.9:
                cv.text((x, base - h - 40), f"~{v:,}", 40, WHITE)
    if ph == 2:
        cv.arrow((640, 560), (1060, 300), 5, ORANGE, seg(s, 0.1, 0.4), 22)
        cv.text((840, 360), "×8", 90, ORANGE, alpha=seg(s, 0.3, 0.3))


# ---------------- why speed hurts ----------------

def e7_time(cv, s, T, ph=0):
    """ph0 10 km to the city, ph1 185 km/h → 3+ min, ph2 500 km/h → ~1 min, ph3 nearly a third."""
    backdrop(cv, s, "grid")
    x0, x1 = 300, 1500
    for i, (y, lab, mins, col, show) in enumerate([(380, "185 KM/H", 3.2, GREY, ph >= 1), (580, "500 KM/H", 1.2, RED, ph >= 2)]):
        cv.line([(x0, y), (x1, y)], 3, DIM)
        cv.rect((x1 + 10, y - 50, x1 + 120, y + 10), 4, WHITE, radius=4)
        cv.text((x1 + 65, y + 40), "CITY", 24, WHITE)
        if not show:
            continue
        p = (s / (mins * 0.9)) % 1 if ph < 3 else 1.0
        x = lerp(x0, x1, min(1, p))
        if i == 0:
            geran(cv, (x, y - 20), 0.35, col, 3)
        else:
            jet_geran(cv, (x, y - 20), 0.35, col, 3)
        cv.text((240, y - 20), lab, 30, col, anchor="rm")
        cv.text((x1 + 220, y - 20), f"{'3+' if i == 0 else '~1'} MIN", 44, col, anchor="lm",
                alpha=seg(s, 0.4, 0.3))
    cv.text((CX, 200), "10 KM FROM SPOTTING TO THE CITY", 40, WHITE)
    if ph == 3:
        cv.text((CX, 760), "TIME TO REACT: NEARLY A THIRD", 54, ORANGE, alpha=seg(s, 0.1, 0.3))


def e7_ep2_link(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX - 430, 300), "EP02", 44, GREY)
    cv.text((CX - 430, 360), "UKRAINE'S JET MISSILE-DRONES", 28, GREY)
    cv.arrow((CX - 640, 470), (CX - 220, 470), 6, ORANGE, seg(s, 0.1, 0.5), 24)
    cv.text((CX - 430, 540), "→ RUSSIA", 32, ORANGE)
    cv.text((CX + 430, 300), "NOW", 44, WHITE)
    cv.text((CX + 430, 360), "THE SAME PRINCIPLE, REVERSED", 28, WHITE)
    cv.arrow((CX + 640, 470), (CX + 220, 470), 6, RED, seg(s, 0.5, 0.5), 24)
    cv.text((CX + 430, 540), "→ UKRAINE", 32, RED)
    cv.text((CX, 720), "SPEED SHRINKS THE TIME TO DEFEND", 44, WHITE, alpha=seg(s, 1.0, 0.3))


def e7_chase(cv, s, T, ph=0):
    """ph0 propeller interceptors chased from behind, ph1 a faster target can't be caught, ph2 wait ahead / faster hunter."""
    backdrop(cv, s, "grid")
    y = CY
    if ph == 0:
        p = (s * 0.3) % 1
        geran(cv, (lerp(500, 1500, p), y), 0.5, RED, 4)
        quad_top(cv, (lerp(500, 1500, p) - 180, y + 10), 0.4, ORANGE, 3, spin=s * 30)
        cv.text((CX, 760), "PROPELLER INTERCEPTORS: CHASE FROM BEHIND", 40, WHITE, alpha=seg(s, 0.3, 0.3))
        return
    if ph == 1:
        t = s
        jet_geran(cv, (300 + (t * 380) % 1500, y), 0.5, RED, 4)
        quad_top(cv, (300 + (t * 120) % 1500, y + 10), 0.4, ORANGE, 3, spin=s * 30)
        cv.text((CX, 760), "A FASTER TARGET CAN'T BE CAUGHT FROM BEHIND", 40, RED, alpha=seg(s, 0.3, 0.3))
        return
    p = ease(seg(s, 0.2, 2.0))
    jx = lerp(250, 1100, p)
    jet_geran(cv, (jx, y), 0.5, RED, 4)
    interceptor(cv, (lerp(1700, 1180, p), y + 4), 0.8, ORANGE, 4, a=math.pi)
    if p >= 1:
        burst(cv, (1140, y), 80)
    cv.text((CX, 760), "WAIT ACROSS ITS PATH · OR BUILD A FASTER HUNTER", 38, ORANGE, alpha=seg(s, 0.3, 0.3))


def e7_sept(cv, s, T, ph=0):
    """ph0 the question, ph1 2,100 jet drones in 3 weeks."""
    backdrop(cv, s, "grid")
    if ph == 0:
        big_word(cv, s, "THE NUMBERS", WHITE, 110)
        return
    n = int(2100 * ease(seg(s, 0.1, 1.6)) / 25)
    for i in range(n):
        x, y = CX - 660 + (i % 28) * 48, 180 + (i // 28) * 46
        cv.line([(x - 14, y), (x + 14, y)], 3, RED)
        cv.line([(x - 4, y - 10), (x - 4, y + 10)], 3, RED)
    cv.text((CX, 690), "~2,100 JET DRONES", 70, RED)
    cv.text((CX, 770), "FIRST THREE WEEKS OF SEPTEMBER · EACH MARK ≈ 25", 30, GREY)


def e7_word(cv, s, T, ph=0):
    big_word(cv, s, ["A NEW HUNTER", "A COMPLETELY NEW HUNTER"][ph], ORANGE, 110)


# ---------------- the hunters ----------------

def e7_brave(cv, s, T, ph=0):
    """ph0 22 teams (12 state-funded), ph1 7 types combat-tested, ph2 67 companies."""
    backdrop(cv, s, "grid")
    cv.text((CX, 150), "BRAVE1 · UKRAINE'S DEFENCE-TECH AGENCY", 34, GREY)
    if ph == 0:
        for i in range(22):
            x, y = CX - 560 + (i % 11) * 112, 330 + (i // 11) * 150
            cv.rect((x - 40, y - 40, x + 40, y + 40), 4, ORANGE if i < 12 else WHITE, radius=10)
        cv.text((CX, 720), "22 TEAMS · 12 STATE-FUNDED", 54, WHITE, alpha=seg(s, 0.3, 0.3))
    elif ph == 1:
        for i in range(7):
            x = CX - 600 + i * 200
            interceptor(cv, (x, 420), 0.7, ORANGE, 4, a=-math.pi / 2)
            check(cv, (x, 560), 26, ORANGE, 6, seg(s, 0.2 + i * 0.15, 0.3))
        cv.text((CX, 720), "7 TYPES ALREADY USED IN COMBAT", 54, WHITE, alpha=seg(s, 0.3, 0.3))
    else:
        n = int(67 * ease(seg(s, 0.1, 1.2)))
        for i in range(n):
            x, y = CX - 660 + (i % 17) * 82, 270 + (i // 17) * 90
            cv.rect((x - 22, y - 30, x + 22, y + 30), 3, WHITE, radius=4)
        cv.text((CX, 720), "67 COMPANIES ON JET-DRONE INTERCEPTORS", 48, WHITE)


def e7_designs(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    labs = ["SMALL JET ENGINE", "POWERFUL ELECTRIC PROPELLERS", "DUCTED FAN"]
    for i, lab in enumerate(labs):
        x = CX - 560 + i * 560
        a = seg(s, 0.1 + i * 0.4, 0.3)
        cv.rect((x - 230, 280, x + 230, 600), 4, ORANGE, radius=14)
        if i == 0:
            interceptor(cv, (x, 440), 1.2, WHITE, 4)
            cv.line([(x - 110, 440), (x - 220, 440)], 6, ORANGE)
        elif i == 1:
            quad_top(cv, (x, 440), 0.9, WHITE, 4, spin=s * 40)
        else:
            for dx in (-70, 70):
                cv.circle((x + dx, 440), 60, 5, WHITE)
                for k in range(6):
                    aa = s * 6 + k
                    cv.line([(x + dx, 440), (x + dx + 50 * math.cos(aa), 440 + 50 * math.sin(aa))], 3, GREY)
        cv.text((x, 650), lab, 30, WHITE, alpha=a)


def e7_k425(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 260), "LATE SEPTEMBER 2026", 36, GREY)
    cv.text((CX - 330, 420), "425 KM/H", 90, RED, alpha=seg(s, 0.1, 0.3))
    cv.text((CX + 330, 420), "3 KM+", 90, RED, alpha=seg(s, 0.4, 0.3))
    cv.text((CX - 330, 500), "SPEED", 30, GREY)
    cv.text((CX + 330, 500), "ALTITUDE", 30, GREY)
    cv.text((CX, 660), "GERAN-5 DOWNED · THAT INTERCEPTOR'S FIRST KILL", 40, ORANGE, alpha=seg(s, 0.8, 0.3))


# ---------------- Bars ----------------

def e7_reverse(cv, s, T, ph=0):
    """ph0 turn an attack weapon around, ph1 Bars: attack drone → interceptor."""
    backdrop(cv, s, "grid")
    a = math.pi * ease(seg(s, 0.3, 1.2)) if ph == 1 else 0.0
    interceptor(cv, (CX, CY), 2.2, ORANGE, 6, a=a)
    if ph == 0:
        cv.arrow((CX + 260, CY), (CX + 600, CY), 5, GREY, 1.0, 24)
        cv.text((CX + 430, CY + 80), "RUSSIA", 34, GREY)
        cv.text((CX, 170), "TURN AN ATTACK WEAPON AROUND", 50, WHITE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX, 170), "BARS: STRIKE DRONE → DRONE HUNTER", 50, ORANGE, alpha=seg(s, 0.2, 0.3))
        if s > 1.6:
            jet_geran(cv, (CX - 620, CY), 0.5, RED, 4)


def e7_rate30(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cx, cy, r = CX, CY + 20, 220
    cv.circle((cx, cy), r, 30, (40, 40, 40))
    p = 0.3 * ease(seg(s, 0.2, 1.2))
    for k in range(int(80 * p)):
        a = -math.pi / 2 + 2 * math.pi * k / 80
        cv.line([(cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a)),
                 (cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a))], 6, ORANGE)
    cv.text((cx, cy), "~30%", 90, ORANGE)
    cv.text((CX, 140), "BARS HIT RATE VS JET DRONES · BEST SO FAR", 38, WHITE)


def e7_bars_de(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    n = int(200 * ease(seg(s, 0.1, 1.6)))
    for i in range(n):
        x, y = CX - 735 + (i % 30) * 50, 180 + (i // 30) * 52
        interceptor(cv, (x, y), 0.18, ORANGE, 2, a=-math.pi / 2)
    cv.text((CX, 600), "2,000 BARS", 80, WHITE)
    cv.text((CX, 690), "JOINT PRODUCTION FUNDED BY GERMANY · EACH ICON ≈ 10", 30, GREY)


# ---------------- October 12 ----------------

def e7_oct12(cv, s, T, ph=0):
    """ph0 cold-open claim, ph1 Lasar's Group interceptor, two Geran-5s heading for Kyiv."""
    backdrop(cv, s, "grid")
    kyiv = (360, 520)
    cv.rect((kyiv[0] - 70, kyiv[1] - 50, kyiv[0] + 70, kyiv[1] + 50), 4, WHITE, radius=6)
    cv.text((kyiv[0], kyiv[1] + 90), "KYIV", 30, WHITE)
    for k in range(2):
        t0 = 0.3 + k * 1.2
        p = ease(seg(s, t0, 1.0))
        y = 360 + k * 220
        jx = lerp(1750, 900 + k * 150, p)
        if p < 1:
            jet_geran(cv, (jx, y), 0.45, RED, 4, a=math.pi)
            interceptor(cv, (lerp(500, jx - 90, p), y + 10), 0.6, ORANGE, 4)
        else:
            burst(cv, (jx, y), 70)
            cross(cv, (jx, y), 30, RED, 6)
    cv.text((CX, 150), "OCTOBER 2026 · 2 × GERAN-5 DOWNED" if ph == 0 else "LASAR'S GROUP · NEW INTERCEPTOR", 42,
            ORANGE, alpha=seg(s, 0.2, 0.3))


def e7_month(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(360, CY), (1560, CY)], 5, GREY)
    p = ease(seg(s, 0.2, 1.4))
    cv.line([(360, CY), (lerp(360, 1560, p), CY)], 7, ORANGE)
    cv.dot((360, CY), 14, WHITE)
    cv.text((360, CY - 60), "IDEA", 36, WHITE)
    cv.dot((1560, CY), 14, ORANGE if p >= 1 else DIM)
    cv.text((1560, CY - 60), "REAL KILLS", 36, ORANGE if p >= 1 else DIM)
    cv.text((CX, CY + 110), "ONE MONTH", 70, ORANGE, alpha=seg(s, 1.4, 0.3))


def e7_hundreds(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    n = int(300 * ease(seg(s, 0.1, 1.6)))
    for i in range(n):
        x, y = CX - 735 + (i % 30) * 50, 170 + (i // 30) * 44
        interceptor(cv, (x, y), 0.16, ORANGE, 2, a=-math.pi / 2)
    cv.text((CX, 680), "HUNDREDS A MONTH BY END OF 2026 · PLAN", 46, WHITE)


def e7_claim(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 360), "KILL RECORDS", 70, WHITE)
    cv.tag((CX, 500), "MOSTLY UKRAINIAN CLAIMS · NOT INDEPENDENTLY VERIFIED", 36, RED, alpha=seg(s, 0.2, 0.3))


# ---------------- the engine bottleneck ----------------

def e7_engine(cv, s, T, ph=0):
    """ph0 the engine, ph1 mostly imported → bottleneck."""
    backdrop(cv, s, "grid")
    x, y = CX, CY
    cv.rect((x - 260, y - 90, x + 200, y + 90), 6, WHITE, radius=40)
    cv.circle((x - 260, y), 90, 6, WHITE)
    for k in range(8):
        a = s * 8 + k * 0.785
        cv.line([(x - 260, y), (x - 260 + 80 * math.cos(a), y + 80 * math.sin(a))], 3, GREY)
    cv.line([(x + 200, y - 60), (x + 280, y - 40), (x + 280, y + 40), (x + 200, y + 60)], 6, WHITE)
    if ph == 0:
        cv.text((CX, 170), "THE ENGINE", 70, ORANGE, alpha=seg(s, 0.1, 0.3))
        return
    for k in range(5):
        cv.arrow((x - 900 + k * 40, y - 260 + k * 130), (x - 420, y), 3, GREY, seg(s, 0.2 + k * 0.1, 0.4), 16)
    cv.text((CX - 650, 230), "MOSTLY IMPORTED", 40, WHITE, alpha=seg(s, 0.4, 0.3))
    cv.text((CX, 760), "KEY BOTTLENECK · TOO FEW MADE AT HOME", 44, RED, alpha=seg(s, 0.8, 0.3))


def e7_orders(cv, s, T, ph=0):
    """ph0 1,000+ ordered vs production ramping, ph1 ~6 months last time."""
    backdrop(cv, s, "grid")
    cv.text((300, 300), "ORDERED", 36, WHITE, anchor="lm")
    cv.rect((300, 330, 1500, 390), 0, fill=ORANGE, radius=6)
    cv.text((1530, 360), "1,000+", 40, ORANGE, anchor="lm")
    cv.text((300, 480), "PRODUCED", 36, WHITE, anchor="lm")
    p = 0.2 + 0.15 * math.sin(s * 2) ** 2
    cv.rect((300, 510, 300 + 1200 * p, 570), 0, fill=WHITE, radius=6)
    cv.text((300 + 1200 * p + 30, 540), "RAMPING UP", 34, WHITE, anchor="lm")
    if ph == 1:
        cv.text((CX, 720), "PROPELLER INTERCEPTORS TOOK ~6 MONTHS TO MASS-PRODUCE", 38, GREY, alpha=seg(s, 0.2, 0.3))


# ---------------- the race goes on ----------------

def e7_ru800(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 360), "800 KM/H?", 120, RED)
    cv.tag((CX, 520), "RUSSIAN EXPERT CLAIM · NOT VERIFIED", 40, RED, alpha=seg(s, 0.3, 0.3))


def e7_spiral(cv, s, T, ph=0):
    """ph0 faster → faster → faster, ph1 EP03's cycle, now in the sky."""
    backdrop(cv, s, "radar")
    c = (CX, CY)
    for k in range(3):
        r = 140 + k * 90
        a0 = s * (40 + k * 20)
        cv.arc(c, r, a0, a0 + 250, 5, ORANGE if k % 2 == 0 else RED)
    cv.text((CX, CY), "FASTER", 48, WHITE)
    if ph == 1:
        cv.text((CX, 840), "EP03'S ATTACK–COUNTER CYCLE · NOW A SPEED RACE", 38, ORANGE, alpha=seg(s, 0.2, 0.3))


# ---------------- outro ----------------

def e7_recap(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    cv.text((CX - 380, CY - 40), "SPEED", 80, RED, alpha=seg(s, 0.1, 0.3))
    cv.text((CX, CY - 40), "+", 80, GREY, alpha=seg(s, 0.4, 0.3))
    cv.text((CX + 380, CY - 40), "TIME", 80, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.text((CX, CY + 100), "MORE, FASTER HUNTERS · BUILT MORE QUICKLY", 40, WHITE, alpha=seg(s, 1.0, 0.3))


def e7_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP08  ·  THE ROBOT GUNS OF KYIV", "radar")


SCENES = {k: v for k, v in globals().items() if k.startswith("e7_") and callable(v)}
