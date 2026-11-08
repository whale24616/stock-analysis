"""EP09 line-art scenes ("Surviving the Kill Zone"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math
import random

from gfx import DIM, GREY, ORANGE, RED, WHITE, check, clamp, cross, ease, lerp, seg
from scenes import BG, CX, CY, backdrop, end_card, title_card
from scenes_ep03 import quad_top
from scenes_ep06 import shield, spear
from scenes_ep08 import waves


# ---------------- icons ----------------

def person(cv, c, s=1.0, col=WHITE, w=4):
    x, y = c
    cv.circle((x, y - 70 * s), 16 * s, w, col)
    cv.line([(x, y - 54 * s), (x, y - 10 * s)], w, col)
    cv.line([(x - 26 * s, y - 40 * s), (x + 26 * s, y - 40 * s)], w, col)
    cv.line([(x, y - 10 * s), (x - 18 * s, y + 30 * s)], w, col)
    cv.line([(x, y - 10 * s), (x + 18 * s, y + 30 * s)], w, col)


def ugv(cv, c, s=1.0, col=WHITE, w=4, load=None):
    """Side view of a small tracked ground robot; load: 'box' or 'stretcher'."""
    x, y = c
    cv.rect((x - 110 * s, y - 30 * s, x + 110 * s, y + 30 * s), w, col, radius=int(28 * s))
    for k in range(5):
        cv.circle((x - 80 * s + k * 40 * s, y), 12 * s, 2, col)
    cv.rect((x - 90 * s, y - 70 * s, x + 90 * s, y - 30 * s), w, col, radius=6)
    if load == "box":
        cv.rect((x - 60 * s, y - 120 * s, x + 20 * s, y - 70 * s), w, ORANGE, radius=4)
    if load == "stretcher":
        cv.line([(x - 120 * s, y - 84 * s), (x + 120 * s, y - 84 * s)], w, ORANGE)
        cv.circle((x + 80 * s, y - 100 * s), 14 * s, w, ORANGE)
        cv.line([(x - 90 * s, y - 96 * s), (x + 64 * s, y - 96 * s)], w, ORANGE)
    cv.line([(x + 60 * s, y - 70 * s), (x + 70 * s, y - 110 * s)], 3, col)


def netting(cv, box, col=GREY, step=36, w=2):
    """A square mesh clipped to box."""
    x0, y0, x1, y1 = box
    x = x0
    while x <= x1:
        cv.line([(x, y0), (x, y1)], w, col)
        x += step
    y = y0
    while y <= y1:
        cv.line([(x0, y), (x1, y)], w, col)
        y += step


def fpv_dive(cv, start, end, p, col=RED, s=0.35):
    pos = (lerp(start[0], end[0], p), lerp(start[1], end[1], p))
    quad_top(cv, pos, s, col, 3, spin=p * 40)
    return pos


# ---------------- cold open ----------------

def e9_weather(cv, s, T, ph=0):
    """ph0 clear sky: the drone sees everything, ph1 rain and fog hide the road."""
    backdrop(cv, s, "grid")
    gy = 760
    cv.line([(120, gy), (1800, gy)], 3, GREY)
    vx = 200 + (s * 120) % 1500
    cv.rect((vx - 60, gy - 50, vx + 60, gy - 6), 4, WHITE, radius=8)
    cv.circle((vx - 35, gy), 12, 3, WHITE)
    cv.circle((vx + 35, gy), 12, 3, WHITE)
    d = (CX + 200, 260)
    quad_top(cv, d, 0.35, RED, 3, spin=s * 30)
    if ph == 0:
        cv.line([d, (vx, gy - 50)], 2, RED)
        cv.circle((vx, gy - 28), 70, 3, RED)
        cv.text((CX, 140), "CLEAR SKY: THE DRONE SEES EVERYTHING", 44, RED, alpha=seg(s, 0.2, 0.3))
        return
    rnd = random.Random(4)
    for k in range(120):
        x, y = rnd.uniform(0, 1920), (rnd.uniform(0, 760) + s * 600) % 760
        cv.line([(x, y), (x - 8, y + 30)], 2, GREY)
    for k in range(5):
        cv.rect((100 + k * 360, 380 + (k % 2) * 60, 500 + k * 360, 470 + (k % 2) * 60), 0, fill=(70, 70, 72), radius=40)
    cv.text((CX, 140), "RAIN AND FOG: THE ROAD DISAPPEARS", 44, WHITE, alpha=seg(s, 0.2, 0.3))


def e9_intro(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    p = (s * 0.3) % 1
    for k in range(3):
        quad_top(cv, (lerp(1700, 300, (p + k * 0.33) % 1), 260 + k * 70), 0.25, RED, 2, spin=s * 30)
    cv.text((CX, CY), "THE KILL ZONE", 110, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, CY + 110), "WHERE DRONES HUNT EVERYTHING THAT MOVES", 38, ORANGE, alpha=seg(s, 0.6, 0.3))


def e9_title(cv, s, T, ph=0):
    title_card(cv, s, "EP09  ·  SURVIVING THE KILL ZONE", "grid")


# ---------------- the kill zone ----------------

def _km_x(km):
    return 300 + 1300 * km / 32


def e9_zone(cv, s, T, ph=0):
    """ph0 ~15 km (FT), ph1 20–25 km in some areas, ph2 a corps commander expects 30 km by year end."""
    backdrop(cv, s, "grid")
    y0, y1 = 300, 700
    cv.line([(_km_x(0), y0 - 40), (_km_x(0), y1 + 40)], 8, RED)
    cv.text((_km_x(0), y0 - 70), "FRONT LINE", 30, RED)
    for km in range(0, 31, 5):
        cv.line([(_km_x(km), y1 + 30), (_km_x(km), y1 + 50)], 3, GREY)
        cv.text((_km_x(km), y1 + 80), f"{km} KM", 24, GREY)
    depth = {0: 15, 1: 25, 2: 30}[ph]
    prev = {0: 0, 1: 15, 2: 25}[ph]
    p = ease(seg(s, 0.1, 1.0))
    d = prev + (depth - prev) * p
    cv.rect((_km_x(0), y0, _km_x(d), y1), 0, fill=(70, 30, 30), radius=4)
    cv.rect((_km_x(0), y0, _km_x(d), y1), 3, RED, radius=4)
    if ph == 1:
        cv.rect((_km_x(20), y0, _km_x(25), y1), 3, ORANGE, radius=4)
    lab = {0: "~15 KM KILL ZONE (FT)", 1: "20–25 KM IN SOME AREAS", 2: "30 KM BY YEAR END? (CORPS COMMANDER)"}[ph]
    cv.text((CX, 170), lab, 46, RED if ph == 0 else ORANGE, alpha=seg(s, 0.3, 0.3))
    q = (s * 0.25) % 1
    quad_top(cv, (_km_x(d * q), lerp(y0 + 60, y1 - 60, abs(math.sin(s)))), 0.25, RED, 2, spin=s * 30)


def e9_thermal(cv, s, T, ph=0):
    """ph0 a soldier glows on a thermal camera, the cloaked one barely shows; ph1 few cloaks, mixed results."""
    backdrop(cv, s, "grid")
    for k, (x, cloak) in enumerate(((620, False), (1300, True))):
        cv.rect((x - 260, 260, x + 260, 700), 4, GREY, radius=10)
        if not cloak:
            for r, c in ((150, (90, 45, 30)), (110, (160, 90, 50))):
                cv.circle((x, 500), r, 0, fill=c)
            person(cv, (x, 560), 2.4, (255, 220, 160), 10)
            cv.text((x, 760), "NO CLOAK", 34, WHITE)
        else:
            person(cv, (x, 560), 2.4, (75, 75, 75), 10)
            cv.text((x, 760), "THERMAL CLOAK", 34, ORANGE)
    cv.text((CX, 170), "WHAT A DRONE'S THERMAL CAMERA SEES", 42, WHITE)
    if ph >= 1:
        cv.tag((CX, 850), "STILL FEW CLOAKS · RESULTS MIXED", 36, RED, alpha=seg(s, 0.2, 0.3))


def e9_3days(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(300, 600), (1620, 600)], 3, DIM)
    p = clamp(seg(s, 0.1, 2.5), 0, 1)
    person(cv, (lerp(300, 1500, p), 560), 0.8, WHITE, 3)
    cv.rect((1560, 520, 1680, 600), 4, ORANGE, radius=6)
    cv.text((1620, 640), "POSITION", 28, ORANGE)
    for k, lab in enumerate(("DAY 1", "DAY 2", "DAY 3")):
        x = 300 + (k + 0.5) * 400
        cv.text((x, 680), lab, 32, GREY, alpha=seg(s, 0.3 + k * 0.5, 0.3))
    cv.text((CX, 200), "SOME POSITIONS: 3 DAYS ON FOOT", 54, WHITE, alpha=seg(s, 0.2, 0.3))


def e9_sparse(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(260, 520), (1660, 520)], 4, GREY)
    cv.line([(260, 490), (260, 550)], 4, GREY)
    cv.line([(1660, 490), (1660, 550)], 4, GREY)
    cv.text((CX, 600), "1 MILE (1.6 KM)", 34, GREY)
    xs = [380, 610, 900, 1180, 1500]
    for k, x in enumerate(xs):
        if seg(s, 0.1 + k * 0.2, 0.2) > 0.5:
            person(cv, (x, 470), 0.6, WHITE, 3)
            person(cv, (x + 40, 470), 0.6, WHITE, 3)
    cv.text((CX, 220), "FEWER THAN 10 SOLDIERS PER MILE", 54, ORANGE, alpha=seg(s, 0.3, 0.3))
    cv.text((CX, 290), "IN SOME AREAS (NPR)", 32, WHITE)


def e9_dugout(cv, s, T, ph=0):
    """ph0 soldiers hold out underground, ph1 the wounded may wait days or weeks."""
    backdrop(cv, s, "grid")
    gy = 360
    cv.line([(100, gy), (1820, gy)], 5, GREY)
    for k in range(18):
        cv.line([(150 + k * 95, gy + 10), (190 + k * 95, gy + 40)], 2, DIM)
    cv.rect((560, 520, 1360, 820), 5, WHITE, radius=10)
    cv.line([(700, gy), (700, 520)], 4, WHITE)
    cv.line([(760, gy), (760, 520)], 4, WHITE)
    for k in range(3):
        person(cv, (700 + k * 160, 760), 0.8, WHITE, 3)
    quad_top(cv, (1200 + 200 * math.sin(s * 0.7), 220), 0.3, RED, 3, spin=s * 30)
    if ph == 0:
        cv.text((CX, 140), "DIG DEEP · HOLD OUT UNDERGROUND", 46, WHITE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.line([(1080, 780), (1300, 780)], 5, ORANGE)
        cv.circle((1270, 760), 14, 4, ORANGE)
        cv.text((CX, 140), "THE WOUNDED CAN WAIT DAYS OR WEEKS", 46, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_supply(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    p = (s * 0.2) % 1
    quad_top(cv, (lerp(300, 1600, p), 300), 0.5, WHITE, 3, spin=s * 30)
    cv.rect((lerp(300, 1600, p) - 30, 360, lerp(300, 1600, p) + 30, 410), 4, ORANGE, radius=4)
    cv.text((CX, 180), "SUPPLIES BY DRONE", 44, WHITE)
    ugv(cv, (lerp(1600, 300, p), 760), 1.0, WHITE, 4, load="stretcher")
    cv.text((CX, 900), "THE WOUNDED BY ROBOT", 44, ORANGE)


def e9_reach(cv, s, T, ph=0):
    """ph0 danger behind the front, ph1 Kramatorsk ~19 km (Oct 2025), ph2 the Kramatorsk–Sloviansk road."""
    backdrop(cv, s, "grid")
    fx = 1500
    cv.line([(fx, 160), (fx - 60, 400), (fx + 20, 620), (fx - 30, 760)], 8, RED)
    cv.text((fx + 30, 150), "FRONT", 30, RED, anchor="lm")
    kr, sl = (fx - 520, 560), (fx - 640, 330)
    cv.circle(kr, 18, 4, WHITE)
    cv.text((kr[0], kr[1] + 50), "KRAMATORSK", 32, WHITE)
    cv.circle(sl, 18, 4, WHITE)
    cv.text((sl[0], sl[1] - 50), "SLOVIANSK", 32, WHITE)
    cv.line([kr, sl], 3, GREY)
    if ph == 0:
        cv.text((CX - 300, 830), "THE DANGER REACHES FAR BEHIND THE FRONT", 40, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph >= 1:
        cv.arrow((fx - 60, 560), (kr[0] + 30, kr[1]), 4, ORANGE, seg(s, 0.2, 0.5), 18)
        cv.text(((fx + kr[0]) / 2, 520), "~19 KM", 34, ORANGE)
        cv.text((CX - 300, 830), "OCT 2025: PICKUP HIT IN KRAMATORSK", 40, ORANGE, alpha=seg(s, 0.4, 0.3) if ph == 1 else 1)
    if ph >= 2:
        m = ((kr[0] + sl[0]) / 2, (kr[1] + sl[1]) / 2)
        cv.circle(m, 30, 4, RED)
        cv.text((CX - 300, 890), "LATER: CARS HIT ON THE KRAMATORSK–SLOVIANSK ROAD", 34, RED, alpha=seg(s, 0.2, 0.3))


def e9_both(cv, s, T, ph=0):
    """ph0 the kill zone works both ways, ph1 Ukraine's $880M Drone Line aims at 10–15 km."""
    backdrop(cv, s, "grid")
    cv.line([(CX, 220), (CX, 760)], 8, RED)
    cv.rect((CX - 600, 220, CX - 20, 760), 3, ORANGE, radius=6)
    cv.rect((CX + 20, 220, CX + 600, 760), 3, RED, radius=6)
    cv.text((CX - 310, 260), "UKRAINIAN SIDE", 30, ORANGE)
    cv.text((CX + 310, 260), "RUSSIAN SIDE", 30, RED)
    p = (s * 0.3) % 1
    quad_top(cv, (lerp(CX - 100, CX + 500, p), 500), 0.3, ORANGE, 3, spin=s * 30)
    quad_top(cv, (lerp(CX + 100, CX - 500, p), 620), 0.3, RED, 3, spin=s * 30)
    if ph == 0:
        cv.text((CX, 140), "A KILL ZONE ON BOTH SIDES", 50, WHITE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX, 140), "UKRAINE'S DRONE LINE · ~$880 MILLION", 46, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.tag((CX + 310, 720), "GOAL: NO FREE MOVEMENT IN 10–15 KM", 28, ORANGE, alpha=seg(s, 0.6, 0.3))


def e9_infiltrate(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for k in range(6):
        cv.rect((80 + k * 300, 340 + (k % 2) * 80, 520 + k * 300, 460 + (k % 2) * 80), 0, fill=(60, 60, 62), radius=50)
    p = (s * 0.12) % 1
    for k in range(3):
        person(cv, (lerp(1700, 300, p) + k * 60, 720), 0.7, GREY, 3)
    cv.text((CX, 160), "INFILTRATION IN TWOS AND THREES · IN BAD WEATHER", 40, RED, alpha=seg(s, 0.2, 0.3))


# ---------------- the shields ----------------

SHIELDS = [("NETS", "net"), ("JAMMING", "jam"), ("LAST LINE", "shot"), ("ROBOTS", "ugv")]


def e9_shields(cv, s, T, ph=0):
    """ph0 the four shields, ph1–4 highlight one."""
    backdrop(cv, s, "grid")
    for i, (lab, kind) in enumerate(SHIELDS):
        x = 330 + i * 420
        col = ORANGE if ph == i + 1 else (WHITE if ph == 0 else DIM)
        al = seg(s, 0.1 + i * 0.25, 0.3) if ph == 0 else 1.0
        if al <= 0:
            continue
        cv.rect((x - 170, 330, x + 170, 650), 5, col, radius=18)
        c = (x, 470)
        if kind == "net":
            netting(cv, (x - 120, 400, x + 120, 540), col, 30, 2)
        elif kind == "jam":
            waves(cv, (x - 60, 470), 30, 4, col, 4, -40, 40, phase=(s * 60) % 120, step=30)
        elif kind == "shot":
            for k in range(14):
                a = -0.5 + k * 0.07
                cv.dot((x - 80 + 170 * math.cos(a) * (0.5 + (k % 3) * 0.2), 520 + 170 * math.sin(a) * 0.8), 6, col)
        else:
            ugv(cv, (x, 520), 0.8, col, 4, load="box")
        cv.text((x, 610), f"{i + 1}. {lab}", 34, col)
    cv.text((CX, 180), "FOUR SHIELDS", 56, WHITE)


def e9_net_principle(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    gy = 800
    cv.line([(150, gy), (1770, gy)], 3, GREY)
    for x in (420, 1500):
        cv.line([(x, gy), (x, 460)], 5, WHITE)
    netting(cv, (420, 440, 1500, 470), WHITE, 40, 2)
    cv.rect((860, gy - 90, 1060, gy - 10), 4, WHITE, radius=10)
    p = clamp(seg(s, 0.1, 1.2), 0, 1)
    pos = fpv_dive(cv, (1200, 150), (980, 450), p, RED, 0.35)
    if p >= 1:
        for k in range(6):
            a = k * 1.05
            cv.line([pos, (pos[0] + 60 * math.cos(a), pos[1] + 30 * math.sin(a) + 20)], 2, ORANGE)
        cv.text((CX, 140), "CAUGHT IN THE NET · NEVER REACHES THE VEHICLE", 42, ORANGE)
    else:
        cv.text((CX, 140), "DRONES DIVE FROM ABOVE", 42, WHITE)


def e9_netkm(cv, s, T, ph=0):
    """ph0 1,640+ km since early 2026, ~87 km in October; ph1 goal: 4,000 km more."""
    backdrop(cv, s, "grid")
    x0, x1, y = 260, 1660, 480
    scale = (x1 - x0) / 5800
    p = ease(seg(s, 0.1, 1.2)) if ph == 0 else 1.0
    cv.rect((x0, y - 40, x0 + 1640 * scale * p, y + 40), 0, fill=ORANGE, radius=6)
    cv.text((x0, y - 80), "NETTED ROADS SINCE EARLY 2026", 32, WHITE, anchor="lm")
    cv.text((x0 + 1640 * scale + 30, y), "1,640+ KM", 44, ORANGE, anchor="lm", alpha=seg(s, 0.8, 0.3) if ph == 0 else 1)
    if ph == 0:
        cv.text((CX, 680), "+ ~87 KM IN OCTOBER ALONE", 44, WHITE, alpha=seg(s, 1.2, 0.3))
    if ph >= 1:
        q = ease(seg(s, 0.1, 1.2))
        cv.rect((x0 + 1640 * scale, y - 40, x0 + (1640 + 4000 * q) * scale, y + 40), 3, GREY, radius=6)
        cv.text((x0 + 1640 * scale + 2000 * scale, y + 90), "GOAL: +4,000 KM", 40, GREY)
        cv.text((CX, 720), "STILL A LONG WAY TO GO", 44, RED, alpha=seg(s, 0.8, 0.3))


def e9_netweak(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    netting(cv, (300, 300, 1620, 380), WHITE, 40, 2)
    cv.circle((700, 340), 70, 0, fill=BG)
    cv.circle((700, 340), 70, 3, RED)
    cv.text((700, 450), "BURNS · MELTS", 36, RED)
    quad_top(cv, (1250, 520), 0.3, RED, 3, spin=0)
    cv.text((1250, 600), "WAITING UNDER THE NET", 34, RED)
    cv.text((CX, 170), "NETS HAVE WEAKNESSES", 50, WHITE)


def e9_citynet(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    gy = 740
    for k, h in enumerate((380, 300, 440, 340, 400)):
        x = 220 + k * 320
        cv.rect((x, gy - h, x + 220, gy), 4, WHITE, radius=4)
        for r in range(3):
            cv.rect((x + 40, gy - h + 40 + r * 90, x + 90, gy - h + 80 + r * 90), 2, GREY, radius=2)
    netting(cv, (200, 280, 1720, 320), ORANGE, 40, 2)
    for x in (490, 810, 1130):
        person(cv, (x, gy - 30), 0.6, WHITE, 3)
    cv.text((CX, 170), "CITIES NEAR THE FRONT: NETS OVER THE STREETS", 42, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_jam(cv, s, T, ph=0):
    """ph0 an FPV is flown by radio, ph1 strong noise cuts the link."""
    backdrop(cv, s, "grid")
    pilot = (360, 700)
    person(cv, pilot, 1.2, WHITE, 4)
    d = (1400, 360)
    quad_top(cv, d, 0.45, RED, 3, spin=s * 30)
    if ph == 0:
        for k in range(6):
            q = ((s * 0.8 + k / 6) % 1)
            cv.dot((lerp(pilot[0] + 40, d[0], q), lerp(pilot[1] - 120, d[1], q)), 6, WHITE)
        cv.text((CX, 160), "FPV DRONES ARE FLOWN BY RADIO", 46, WHITE, alpha=seg(s, 0.2, 0.3))
        return
    jx = 860
    cv.rect((jx - 60, 760, jx + 60, 840), 4, ORANGE, radius=8)
    cv.text((jx, 880), "JAMMER", 30, ORANGE)
    waves(cv, (jx, 760), 60, 6, ORANGE, 3, 200, 340, phase=(s * 120) % 240, step=40)
    cross(cv, ((pilot[0] + d[0]) / 2, (pilot[1] + d[1]) / 2 - 60), 40, RED, 8, seg(s, 0.4, 0.3))
    cv.text((CX, 160), "STRONG NOISE CUTS THE LINK", 46, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_fiber(cv, s, T, ph=0):
    """ph0 Russia's answer, ph1 a hair-thin fiber line unspooling, ph2 jamming has no effect, ph3 tens of km."""
    backdrop(cv, s, "grid")
    pilot = (300, 760)
    person(cv, pilot, 1.0, WHITE, 4)
    p = clamp(seg(s, 0.1, 2.0), 0, 1) if ph >= 1 else 0.5
    d = (lerp(420, 1500, p), lerp(700, 300, p))
    pts = [(lerp(pilot[0] + 30, d[0], k / 30), lerp(pilot[1] - 60, d[1], k / 30) + 30 * math.sin(k * 0.6)) for k in range(31)]
    if ph >= 1:
        cv.line(pts, 2, ORANGE)
    quad_top(cv, d, 0.4, RED, 3, spin=s * 30)
    if ph == 0:
        cv.text((CX, 160), "RUSSIA'S ANSWER: FIBER-OPTIC DRONES", 46, RED, alpha=seg(s, 0.2, 0.3))
    if ph == 1:
        cv.text((CX, 160), "A HAIR-THIN FIBER LINE · UNSPOOLED FOR KILOMETRES", 42, ORANGE, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        jx = 1000
        waves(cv, (jx, 880), 60, 6, GREY, 3, 200, 340, phase=(s * 120) % 240, step=40)
        cv.text((jx, 950), "JAMMER", 28, GREY)
        cv.text((CX, 160), "SIGNALS TRAVEL THE LINE · JAMMING DOESN'T WORK", 42, RED, alpha=seg(s, 0.2, 0.3))
    if ph == 3:
        cv.text((CX, 160), "LONGER LINES · TENS OF KM (ANALYSES)", 46, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_syrskyi(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    if ph == 0:
        cv.text((CX, 360), "FIBER-OPTIC DRONES", 70, WHITE)
        cv.text((CX, 470), "RUSSIA AHEAD IN NUMBERS AND RANGE OF USE", 44, RED, alpha=seg(s, 0.3, 0.3))
        cv.text((CX, 560), "— GEN. SYRSKYI, UKRAINE'S COMMANDER-IN-CHIEF", 32, GREY)
    else:
        cv.text((CX, 400), "“STILL CATCHING UP”", 80, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.text((CX, 520), "SYRSKYI · JANUARY 2026", 36, GREY)


def e9_options(cv, s, T, ph=0):
    """ph0 no way yet to stop them at scale, ph1 shoot · entangle · block."""
    backdrop(cv, s, "grid")
    cv.text((CX, 260), "NO WAY YET TO STOP THEM AT SCALE", 52, RED)
    if ph >= 1:
        for k, lab in enumerate(("SHOOT DOWN", "ENTANGLE", "BLOCK")):
            cv.tag((CX - 520 + k * 520, 520), lab, 48, WHITE, alpha=seg(s, 0.2 + k * 0.4, 0.3))


def e9_shotgun(cv, s, T, ph=0):
    """ph0 pellets spread wide and ignore jamming, ph1 bigger new drones shrug off fine shot, ph2 heavier ammo tested."""
    backdrop(cv, s, "grid")
    g = (360, 760)
    person(cv, (g[0] - 40, g[1] + 60), 1.6, WHITE, 5)
    cv.line([(g[0] - 30, g[1]), (g[0] + 160, g[1] - 120)], 10, WHITE)
    p = clamp((s * 0.6) % 1.2, 0, 1)
    rnd = random.Random(9)
    for k in range(26):
        a = -0.62 + rnd.uniform(-0.18, 0.18)
        r = 1100 * p * rnd.uniform(0.85, 1.0)
        cv.dot((g[0] + 160 + r * math.cos(a), g[1] - 120 + r * math.sin(a)), 5, ORANGE)
    big = ph >= 1
    quad_top(cv, (1300, 260), 0.6 if big else 0.4, RED, 4 if big else 3, spin=s * 30)
    if ph == 0:
        cv.text((CX, 120), "PELLETS SPREAD WIDE · NO EFFECT FROM JAMMING", 42, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph == 1:
        cv.text((CX, 120), "NEWER RUSSIAN DRONES: BIGGER, TOUGHER", 44, RED, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        cv.text((CX, 120), "NEW AMMUNITION WITH HEAVIER MATERIALS · BEING TESTED", 40, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_wire(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    c = (CX, 600)
    cv.rect((c[0] - 70, c[1] + 40, c[0] + 70, c[1] + 120), 4, WHITE, radius=8)
    cv.text((c[0], c[1] + 160), "MOTOR", 28, WHITE)
    for k in range(10):
        a = s * 6 + k * 0.63
        cv.line([(c[0] + 30 * math.cos(a), c[1] + 30 * math.sin(a) * 0.4),
                 (c[0] + 260 * math.cos(a), c[1] + 260 * math.sin(a) * 0.4)], 2, ORANGE)
    cv.line([(200, 300), (c[0] - 20, c[1] - 10)], 2, WHITE)
    cv.line([(c[0] + 20, c[1] - 10), (1720, 260)], 2, DIM)
    cv.text((CX, 160), "SPINNING BARBED WIRE WINDS UP AND CUTS THE FIBER LINE", 38, WHITE, alpha=seg(s, 0.2, 0.3))


def _box_launcher(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.rect((x - 110 * s, y - 70 * s, x + 110 * s, y + 70 * s), w, col, radius=10)
    for k in range(3):
        for j in range(2):
            cv.circle((x - 60 * s + k * 60 * s, y - 25 * s + j * 50 * s), 18 * s, 3, col)
    cv.rect((x + 120 * s, y - 50 * s, x + 170 * s, y - 10 * s), 3, ORANGE, radius=4)


def e9_mangal(cv, s, T, ph=0):
    """ph0 Phantom Defense's Mangal, ph1 a weighted 6×6 m net, ph2 ~$45 a shot, ph3 at the front since
    March 2026, on robots too, heading for mass production, ph4 a second line when jamming fails."""
    backdrop(cv, s, "grid")
    lc = (460, 640)
    if ph == 3:
        ugv(cv, (lc[0], lc[1] + 140), 1.2, WHITE, 4)
    _box_launcher(cv, lc, 1.2, WHITE, 5)
    cv.text((lc[0], 470), "MANGAL NET LAUNCHER", 34, ORANGE)
    if ph == 0:
        cv.text((1250, 420), "PHANTOM DEFENSE", 54, WHITE, alpha=seg(s, 0.2, 0.3))
        cv.text((1250, 500), "UKRAINIAN COMPANY", 32, GREY)
        return
    if ph == 1:
        p = clamp(seg(s, 0.3, 0.8), 0, 1)
        c = (lerp(640, 1350, p), lerp(560, 330, p))
        r = 40 + 160 * p
        netting(cv, (c[0] - r, c[1] - r * 0.6, c[0] + r, c[1] + r * 0.6), ORANGE, 30, 2)
        quad_top(cv, (1350, 330), 0.35, RED, 3, spin=s * 30)
        cv.text((1350, 640), "WEIGHTED NET · 6 M × 6 M", 40, ORANGE)
    if ph == 2:
        cv.text((1250, 460), "~$45", 120, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.text((1250, 580), "PER NET SHOT", 40, WHITE)
    if ph == 3:
        cv.tag((1250, 380), "AT THE FRONT SINCE MAR 2026 (TRIALS)", 34, WHITE, alpha=seg(s, 0.1, 0.3))
        cv.tag((1250, 480), "ALSO ON GROUND ROBOTS", 34, WHITE, alpha=seg(s, 0.4, 0.3))
        cv.tag((1250, 580), "HEADING FOR MASS PRODUCTION", 34, ORANGE, alpha=seg(s, 0.7, 0.3))
    if ph == 4:
        cv.text((1250, 420), "SECOND LINE OF DEFENCE", 50, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.text((1250, 500), "WHEN JAMMING FAILS · EVEN FIBER-OPTIC", 32, WHITE)


def e9_spider(cv, s, T, ph=0):
    """ph0 WINFLY Spider nets a drone, then flies home; ph1 ~$27 a net shot."""
    backdrop(cv, s, "grid")
    p = (s * 0.3) % 1
    if p < 0.5:
        q = p / 0.5
        me = (lerp(300, 1150, q), lerp(700, 360, q))
    else:
        q = (p - 0.5) / 0.5
        me = (lerp(1150, 300, q), lerp(360, 700, q))
    quad_top(cv, me, 0.4, ORANGE, 3, spin=s * 30)
    if p >= 0.45:
        netting(cv, (1220, 320, 1420, 440), ORANGE, 26, 2)
        quad_top(cv, (1320, 380 + 200 * max(0, p - 0.5)), 0.3, RED, 3, spin=0)
    cv.text((CX, 150), "WINFLY SPIDER · NETS IT, THEN FLIES HOME", 44, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph >= 1:
        cv.text((CX, 860), "~$27 PER NET SHOT (DEVELOPER)", 46, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_claim(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 360), "PERFORMANCE & KILL RECORDS", 64, WHITE)
    cv.tag((CX, 500), "MOSTLY DEVELOPERS' CLAIMS · NOT INDEPENDENTLY VERIFIED", 34, RED, alpha=seg(s, 0.2, 0.3))


# ---------------- robots ----------------

def e9_ugv(cv, s, T, ph=0):
    """ph0 fewer people in the kill zone saves lives, ph1 unmanned ground vehicles."""
    backdrop(cv, s, "grid")
    gy = 760
    cv.line([(100, gy + 40), (1820, gy + 40)], 3, GREY)
    p = (s * 0.18) % 1
    if ph == 0:
        person(cv, (lerp(300, 1500, p), gy), 1.0, DIM, 3)
        cv.text((CX, 180), "FEWER TRIPS INTO THE KILL ZONE = MORE LIVES SAVED", 42, WHITE, alpha=seg(s, 0.2, 0.3))
    else:
        ugv(cv, (lerp(300, 1600, p), gy), 1.3, WHITE, 5, load="box")
        cv.text((CX, 180), "UNMANNED GROUND VEHICLES · “GROUND ROBOTS”", 46, ORANGE, alpha=seg(s, 0.2, 0.3))
    quad_top(cv, (1300 + 150 * math.sin(s), 380), 0.3, RED, 3, spin=s * 30)


UGV_MONTHS = [("JAN", 7511), ("FEB", 7960), ("MAR", 9072), ("APR", 11028), ("MAY", 14059), ("JUN", 16663),
              ("JUL", 19935), ("AUG", 25136), ("SEP", 28491), ("OCT", 31398)]


def e9_ugv_chart(cv, s, T, ph=0):
    """ph0 Jan ~7,500 → Oct 31,000+, ph1 more than 4× in ten months, ph2 22,000+ robots contracted this year."""
    backdrop(cv, s, "grid")
    base = 700
    cv.line([(240, base), (1680, base)], 3, GREY)
    cv.text((CX, 140), "GROUND-ROBOT SUPPLY & EVACUATION MISSIONS · 2026", 38, WHITE)
    for i, (m, v) in enumerate(UGV_MONTHS):
        x = 320 + i * 140
        p = ease(seg(s, 0.1 + i * 0.12, 0.5)) if ph == 0 else 1.0
        h = 400 * v / 31398 * p
        cv.rect((x - 45, base - h, x + 45, base), 0, fill=ORANGE if i == 9 else WHITE, radius=4)
        cv.text((x, base + 34), m, 24, GREY)
    cv.text((320, base - 400 * 7511 / 31398 - 30), "~7,500", 28, WHITE)
    cv.text((320 + 9 * 140, base - 425), "31,398", 34, ORANGE)
    if ph == 1:
        cv.text((CX, 240), "MORE THAN 4× IN TEN MONTHS", 50, ORANGE, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        cv.tag((CX, 240), "22,000+ GROUND ROBOTS CONTRACTED IN 2026", 40, ORANGE, alpha=seg(s, 0.2, 0.3))


def e9_ugv_evac(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    gy = 660
    cv.line([(100, gy + 40), (1820, gy + 40)], 3, GREY)
    for x in (500, 900, 1300):
        cv.line([(x - 20, gy + 40), (x, gy + 26), (x + 20, gy + 40)], 3, RED)
    p = (s * 0.15) % 1
    x = lerp(1700, 250, p)
    ugv(cv, (x, gy), 1.5, WHITE, 5)
    for k in range(4):
        y = gy - 110 - k * 28
        cv.line([(x - 130, y), (x + 130, y)], 4, ORANGE)
    quad_top(cv, (900 + 200 * math.sin(s * 0.8), 300), 0.3, RED, 3, spin=s * 30)
    cv.text((CX, 150), "ONE ROBOT · FOUR WOUNDED · THROUGH MINES AND DRONES", 40, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, 210), "SEPTEMBER 2026", 30, GREY)


def e9_1500(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 380), "1,500+", 140, ORANGE, alpha=seg(s, 0.1, 0.3))
    cv.text((CX, 520), "SUPPLY RUNS A MONTH BY HEAVY DRONES · ONE BRIGADE", 40, WHITE)


def e9_robot_vs_soldier(cv, s, T, ph=0):
    """ph0 robots get hit too, many never return; ph1 better to lose a robot than a soldier."""
    backdrop(cv, s, "grid")
    ugv(cv, (620, 620), 1.6, WHITE if ph else GREY, 5)
    if ph == 0:
        cross(cv, (620, 560), 120, RED, 10, seg(s, 0.2, 0.4))
        cv.text((CX, 170), "ROBOTS GET HIT TOO · MANY NEVER COME BACK", 44, RED, alpha=seg(s, 0.2, 0.3))
        return
    cv.text((960, 600), ">", 120, WHITE)
    person(cv, (1320, 640), 2.0, ORANGE, 6)
    cv.text((CX, 170), "BETTER TO LOSE A ROBOT THAN A SOLDIER", 50, ORANGE, alpha=seg(s, 0.2, 0.3))


# ---------------- outro ----------------

def e9_recap(cv, s, T, ph=0):
    """ph0 hide · cover · block · send machines, ph1 the layers, ph2 —."""
    backdrop(cv, s, "grid")
    words = ["HIDE", "COVER", "BLOCK", "SEND MACHINES"]
    for i, w in enumerate(words):
        x = 300 + i * 440
        cv.text((x, 380), w, 50 if i < 3 else 42, ORANGE if ph == 0 else WHITE, alpha=seg(s, 0.1 + i * 0.3, 0.3) if ph == 0 else 1)
    if ph >= 1:
        labs = ["NETS", "JAMMING", "SHOTGUNS + NET LAUNCHERS", "GROUND ROBOTS"]
        for i, lab in enumerate(labs):
            y = 520 + i * 80
            cv.rect((CX - 400, y - 30, CX + 400, y + 30), 3, ORANGE, radius=8)
            cv.text((CX, y), lab, 32, WHITE, alpha=seg(s, 0.1 + i * 0.25, 0.3))


def e9_spear(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    shield(cv, (CX - 300, CY), 1.0, WHITE, 6)
    spear(cv, (CX + 350, CY), 1.0, RED, 6)
    cv.text((CX, 840), "A NEW SHIELD · A NEW SPEAR · EVERY DAY", 44, ORANGE, alpha=seg(s, 0.3, 0.3))


def e9_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP10  ·  THE SHIELD UKRAINE EXPORTS", "grid")


SCENES = {k: v for k, v in globals().items() if k.startswith("e9_") and callable(v)}
