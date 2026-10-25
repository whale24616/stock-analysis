"""EP04 line-art scenes ("Sinking a Fleet Without a Navy"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math
import random

from gfx import DIM, GREY, ORANGE, RED, WHITE, check, clamp, clock_icon, coin_stack, cross, ease, lerp, lerp_pt, seg
from scenes import BG, BG_O, CX, CY, backdrop, end_card, title_card
from scenes_ep03 import big_word, controller, quad_top, waves

SEA = 640  # sea level for side-view scenes


# ---------------- icons ----------------

def warship(cv, c, s=1.0, col=WHITE, w=5, flip=False):
    """Side view of a warship, bow to the right (left when flip)."""
    x, y = c
    d = -1 if flip else 1

    def P(dx, dy):
        return (x + d * dx * s, y + dy * s)

    hull = [P(-260, 0), P(250, 0), P(300, -50), P(-250, -50), P(-260, 0)]
    cv.line(hull, w, col)
    cv.line([P(-150, -50), P(-150, -95), P(60, -95), P(60, -50)], w, col)
    cv.line([P(-90, -95), P(-90, -140), P(10, -140), P(10, -95)], w, col)
    cv.line([P(-40, -140), P(-40, -210)], w - 1, col)
    cv.line([P(-70, -185), P(-10, -185)], w - 2, col)
    cv.line([P(150, -50), P(150, -70), P(190, -70)], w, col)
    cv.line([P(190, -64), P(240, -76)], w - 1, col)


def drone_boat(cv, c, s=1.0, col=ORANGE, w=5, flip=False, wake=0.0):
    """Side view of a low uncrewed boat, bow to the right (left when flip)."""
    x, y = c
    d = -1 if flip else 1

    def P(dx, dy):
        return (x + d * dx * s, y + dy * s)

    cv.line([P(-80, 0), P(60, 0), P(95, -18), P(-80, -18), P(-80, 0)], w, col)
    cv.line([P(-20, -18), P(-10, -30), P(20, -30), P(30, -18)], w - 1, col)
    cv.line([P(0, -30), P(0, -46)], w - 2, col)
    if wake > 0:
        for k in range(4):
            L = 60 + 50 * k * wake
            cv.line([P(-90 - k * 30, 4 + k * 3), P(-90 - k * 30 - L, 10 + k * 6)], 3, WHITE)


def boat_top(cv, c, a, s=1.0, col=ORANGE, w=4):
    """Top view: small wedge pointing along angle a, with a wake."""
    x, y = c
    ca, sa = math.cos(a), math.sin(a)

    def P(u, v):
        return (x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)

    cv.poly([P(30, 0), P(-20, -11), P(-20, 11)], fill=col)
    cv.line([P(-24, -8), P(-90, -22)], 2, GREY)
    cv.line([P(-24, 8), P(-90, 22)], 2, GREY)


def ship_top(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 150 * s, y - 25 * s), (x + 120 * s, y - 25 * s), (x + 170 * s, y), (x + 120 * s, y + 25 * s),
             (x - 150 * s, y + 25 * s), (x - 150 * s, y - 25 * s)], w, col)
    cv.rect((x - 60 * s, y - 14 * s, x + 30 * s, y + 14 * s), w - 2, col, radius=4)


def sea_line(cv, s, y=SEA, x0=0, x1=1920, amp=8, col=GREY, speed=1.0):
    pts = [(x, y + amp * math.sin(x / 60 + s * 2 * speed)) for x in range(x0, x1 + 1, 20)]
    cv.line(pts, 3, col)


def heli(cv, c, s=1.0, col=WHITE, w=5, spin=0.0):
    x, y = c
    cv.line([(x - 60 * s, y), (x + 50 * s, y), (x + 70 * s, y + 25 * s), (x - 40 * s, y + 25 * s), (x - 60 * s, y)],
            w, col)
    cv.line([(x - 60 * s, y + 10 * s), (x - 170 * s, y + 5 * s)], w, col)
    cv.line([(x - 170 * s, y - 15 * s), (x - 170 * s, y + 20 * s)], w - 1, col)
    r = 150 * s * abs(math.cos(spin))
    cv.line([(x - r, y - 15 * s), (x + r, y - 15 * s)], w - 1, GREY)
    cv.line([(x, y - 15 * s), (x, y)], w - 1, col)


# ---------------- map ----------------

# rough Black Sea outline (screen coordinates)
SEA_OUTLINE = [(330, 470), (420, 330), (560, 300), (690, 330), (800, 300), (930, 330), (1060, 270), (1210, 290),
               (1350, 250), (1500, 300), (1600, 380), (1560, 520), (1420, 600), (1250, 660), (1050, 690), (830, 700),
               (620, 690), (440, 640), (330, 560), (330, 470)]
CRIMEA = [(880, 330), (950, 300), (1030, 320), (1050, 370), (990, 420), (920, 410), (870, 370), (880, 330)]
ODESA = (600, 300)
SEVASTOPOL = (930, 405)
NOVO = (1420, 330)
ROMANIA = (380, 470)


def black_sea(cv, s, labels=True):
    backdrop(cv, s, "grid")
    cv.line(SEA_OUTLINE, 4, GREY)
    cv.line(CRIMEA, 4, GREY)
    if labels:
        cv.text((960, 520), "BLACK SEA", 34, DIM)
        cv.text((965, 360), "CRIMEA", 24, GREY)
        cv.dot(ODESA, 9, WHITE)
        cv.text((ODESA[0], ODESA[1] - 30), "ODESA", 24, WHITE)


# ---------------- cold open ----------------

def e4_ship(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.circle((1500, 200), 40, 3, GREY)
    warship(cv, (CX, SEA), 1.6, WHITE, 5)
    sea_line(cv, s)
    sea_line(cv, s, SEA + 40, amp=5, col=DIM)
    for i in range(3):
        a = -0.4 + 0.1 * math.sin(s + i)
        x0 = CX + 20 + i * 70
        cv.line([(x0, SEA - 260), (x0 + 600 * math.cos(a), SEA - 260 + 600 * math.sin(-a) * 0.2 + 180)], 2,
                (70, 70, 60))


def e4_radar(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    c, R = (CX, CY - 10), 320
    for r in (R, R * 0.66, R * 0.33):
        cv.circle(c, r, 3, DIM)
    a = s * 1.8
    cv.line([c, (c[0] + R * math.cos(a), c[1] + R * math.sin(a))], 4, WHITE)
    cv.circle(c, R, 5, WHITE)
    cv.dot(c, 10, WHITE)
    angs = [0.6] if ph == 0 else [0.6, 2.2, 3.6, 5.0]
    for i, ang in enumerate(angs):
        d = R * (0.92 - 0.12 * clamp(s / max(T, 1)))
        p = (c[0] + d * math.cos(ang), c[1] + d * math.sin(ang))
        cv.dot(p, 8, ORANGE if (s * 2 + i) % 1 < 0.6 else (90, 60, 30))
    cv.text((c[0] + R + 170, c[1]), "SMALL · LOW · FAST" if ph == 0 else "MORE THAN ONE", 30, ORANGE,
            alpha=seg(s, 0.3, 0.3))


def e4_converge(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ship_top(cv, (CX, CY), 1.3)
    p = clamp(s / max(T, 1.0))
    for i, a in enumerate((0.3, 1.5, 2.7, 3.6, 5.6)):
        r = lerp(620, 260, ease(p))
        pos = (CX + r * math.cos(a), CY + r * math.sin(a) * 0.65)
        boat_top(cv, pos, math.atan2(CY - pos[1], CX - pos[0]), 1.2)
    cv.text((CX, 170), "FROM DIFFERENT DIRECTIONS", 34, ORANGE, alpha=seg(s, 0.4, 0.3))


def e4_size(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sea_line(cv, s, 600, amp=4)
    if ph == 0:
        drone_boat(cv, (CX - 300, 600), 2.2, ORANGE, 5, wake=0.6)
        cv.text((CX - 300, 700), "SEA DRONE", 34, ORANGE)
        drone_boat(cv, (CX + 350, 600), 2.2, WHITE, 5)
        cv.circle((CX + 350, 600 - 80), 18, 4, WHITE)
        cv.line([(CX + 350, 600 - 62), (CX + 350, 600 - 30)], 5, WHITE)
        cv.text((CX + 350, 700), "SPEEDBOAT", 34, WHITE)
        cv.text((CX, 250), "ABOUT THE SIZE OF A SPEEDBOAT", 36, WHITE, alpha=seg(s, 0.2, 0.3))
        return
    warship(cv, (CX + 250, 600), 1.5, GREY, 4)
    drone_boat(cv, (CX - 520, 600), 1.0, ORANGE, 5)
    cv.text((CX + 250, 700), "WARSHIP  ~100 M+", 30, GREY)
    if ph == 2:
        cv.line([(CX - 600, 650), (CX - 430, 650)], 3, ORANGE)
        cv.text((CX - 515, 700), "~5.5 M", 34, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, 250), "SMALL", 70, ORANGE, alpha=seg(s, 0.1, 0.3))


def e4_intro(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    drone_boat(cv, (CX - 40, CY), 3.0, ORANGE, 6, wake=0.5 + 0.5 * math.sin(s * 3))
    sea_line(cv, s, CY + 6, amp=5)
    cv.text((CX, CY + 160), "SEA DRONES", 46, ORANGE, alpha=seg(s, 0.3, 0.4))
    cv.text((CX, CY + 225), "HOW A COUNTRY WITHOUT A FLEET FOUGHT ONE", 30, WHITE, alpha=seg(s, 0.8, 0.4))


def e4_title(cv, s, T, ph=0):
    title_card(cv, s, "EP04  ·  SINKING A FLEET WITHOUT A NAVY", "radar")


# ---------------- background ----------------

def e4_map(cv, s, T, ph=0):
    black_sea(cv, s)
    for i, (x, y) in enumerate(((560, 420), (640, 470), (720, 430), (800, 480))):
        ship_top(cv, (x, y), 0.25, RED, 3)
    cv.dashed([(500, 380), (560, 470), (700, 520), (860, 470)], 3, RED, offset=s * 30, prog=seg(s, 0.2, 0.8))
    cv.text((680, 580), "BLOCKADE", 32, RED, alpha=seg(s, 0.5, 0.3))
    if ph:
        for k, tgt in enumerate(((560, 230), (700, 200), (430, 260))):
            a, b = (760, 470), tgt
            mid = ((a[0] + b[0]) / 2, min(a[1], b[1]) - 100)
            pts = [lerp_pt(lerp_pt(a, mid, t / 20), lerp_pt(mid, b, t / 20), t / 20) for t in range(21)]
            cv.line(pts, 3, RED, prog=seg(s, 0.2 + k * 0.3, 0.8))
        cv.text((1320, 760), "MISSILES FROM THE SEA", 30, RED, alpha=seg(s, 0.6, 0.3))
    cv.text((1500, 160), "2022", 60, WHITE, alpha=seg(s, 0, 0.3))


def e4_grain_world(cv, s, T, ph=0):
    backdrop(cv, s, "map")
    for k in range(5):
        x, y = 380 + k * 30, 520 - k * 20
        cv.rect((x - 50, y - 30, x + 50, y + 30), 4, ORANGE, radius=10)
    cv.text((440, 640), "UKRAINIAN GRAIN", 30, ORANGE)
    for i, (x, y) in enumerate(((1250, 260), (1450, 420), (1300, 620), (1600, 600))):
        cv.dashed([(560, 480), (x, y)], 3, GREY, offset=-s * 40, prog=seg(s, 0.2 + i * 0.2, 0.6))
        cv.circle((x, y), 30, 4, WHITE)
        cv.line([(x - 18, y), (x + 18, y)], 3, WHITE)
    cross(cv, (760, 470), 50, RED, 10, seg(s, 1.2, 0.4))
    cv.text((CX, 180), "FOOD FOR MANY COUNTRIES", 34, WHITE, alpha=seg(s, 0.3, 0.3))


def e4_fleets(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX - 420, 230), "RUSSIA", 40, RED)
    cv.text((CX + 420, 230), "UKRAINE", 40, WHITE)
    for k in range(int(1 + 11 * seg(s, 0.1, 1.0))):
        ship_top(cv, (CX - 560 + (k % 3) * 140, 330 + (k // 3) * 110), 0.35, RED, 3)
    ship_top(cv, (CX + 420, 400), 0.35, WHITE, 3)
    cv.text((CX + 420, 520), "ALMOST NOTHING", 40, ORANGE, alpha=seg(s, 1.0, 0.3))
    cv.line([(CX, 200), (CX, 800)], 3, DIM)


def e4_word(cv, s, T, ph=0):
    big_word(cv, s, {0: "ANOTHER WAY"}[ph], ORANGE, 150, "radar")


def e4_remote(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    controller(cv, (420, 560), 1.1, t=s)
    cv.dashed([(520, 480), (1250, 440)], 4, ORANGE, offset=-s * 120)
    sea_line(cv, s, 520, 1000, 1800, 5)
    drone_boat(cv, (1400, 520), 1.8, ORANGE, 5, wake=0.7)
    cv.text((CX, 260), "STEERED FROM FAR AWAY", 40, WHITE, alpha=seg(s, 0.2, 0.3))


def e4_names(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i, (name, who) in enumerate((("MAGURA", "MILITARY INTELLIGENCE (HUR)"), ("SEA BABY", "SECURITY SERVICE (SBU)"))):
        x = CX - 360 + i * 720
        a = seg(s, 0.2 + i * 0.5, 0.3)
        cv.rect((x - 300, 330, x + 300, 610), 5, ORANGE if i == 0 else WHITE, radius=16)
        drone_boat(cv, (x, 450), 1.6, ORANGE if i == 0 else WHITE, 5)
        cv.text((x, 520), name, 50, WHITE, alpha=a)
        cv.text((x, 575), who, 24, GREY, alpha=a)


def e4_price(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    drone_boat(cv, (CX - 420, 470), 1.6, ORANGE, 5)
    cv.text((CX - 420, 560), "~$250,000", 60, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX - 420, 630), "PER BOAT", 28, GREY)
    if ph:
        warship(cv, (CX + 420, 500), 0.9, WHITE, 4)
        cv.text((CX + 420, 600), "WARSHIP", 34, WHITE)
        cv.text((CX + 420, 660), "$ TENS TO HUNDREDS OF MILLIONS", 26, GREY, alpha=seg(s, 0.4, 0.3))
        cv.text((CX, 470), "≪", 90, GREY, alpha=seg(s, 0.3, 0.3))


# ---------------- hull ----------------

def e4_hull(cv, s, T, ph=0):
    """ph0 displacement hull pushing water, ph1 drag grows, ph2/3 planing hull rises, ph4 less wetted area."""
    backdrop(cv, s, "grid")
    y0 = 540
    planing = ph >= 2
    lift = 0 if not planing else 38 * seg(s, 0.2, 1.0) if ph == 3 else (38 if ph == 4 else 10)
    off = (s * (200 if planing else 70)) % 120
    for k in range(18):
        x = k * 120 - off
        cv.line([(x, y0 + 4), (x + 60, y0 + 4)], 3, GREY)
    x = CX
    hull = [(x - 260, y0 - 70 - lift), (x + 200, y0 - 70 - lift), (x + 300, y0 - 70 - lift + 20)]
    if planing:
        hull += [(x + 220, y0 + 10 - lift), (x - 260, y0 + 10 - lift)]
    else:
        hull += [(x + 230, y0 + 50), (x - 240, y0 + 50)]
    hull.append(hull[0])
    cv.line(hull, 6, ORANGE if planing else WHITE)
    under = y0 + 10 - lift if planing else y0 + 50
    if under > y0:
        cv.poly([(x - 240, y0), (x + 240, y0), (x + 230 if not planing else x + 220, under),
                 (x - 240, under)], fill=(80, 140, 220, 70))
    if not planing:
        for k in range(4):
            r = 40 + 30 * k + 20 * ((s * 1.5) % 1)
            cv.arc((x + 300, y0), r, 180, 330, 3, WHITE)
        if ph >= 1:
            n = int(4 + 6 * seg(s, 0.1, 1.0))
            for k in range(n):
                cv.arrow((x + 420 + k * 22, y0 - 20), (x + 330 + k * 22, y0 - 20), 3, RED, 1.0, 12)
            cv.text((x + 470, y0 - 90), "DRAG", 34, RED, alpha=seg(s, 0.2, 0.3))
        cv.text((CX, 220), "DISPLACEMENT HULL: PUSHES WATER ASIDE", 34, WHITE, alpha=seg(s, 0.1, 0.3))
    else:
        cv.text((CX, 220), "PLANING HULL: RISES AND SKIMS", 34, ORANGE, alpha=seg(s, 0.1, 0.3))
        if ph >= 3:
            cv.arrow((x, y0 + 80), (x, y0 + 10 - lift), 5, ORANGE, seg(s, 0.2, 0.4), 18)
            cv.text((x + 40, y0 + 120), "LIFT", 30, ORANGE, anchor="lm", alpha=seg(s, 0.4, 0.3))
        if ph == 4:
            cv.text((CX, 760), "LESS HULL IN THE WATER → LESS DRAG", 36, ORANGE, alpha=seg(s, 0.2, 0.3))


def e4_speed(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    from gfx import speedometer
    v = 85 * ease(clamp(s / 1.5))
    speedometer(cv, (CX, CY + 120), 300, v, 120, band=(80, 90))
    cv.text((CX, CY + 200), f"{int(v)} KM/H", 70, ORANGE)
    cv.text((CX, 170), "80–90 KM/H (MAKERS' CLAIMS)", 34, WHITE, alpha=seg(s, 0.3, 0.3))


def e4_radar_low(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    ant = (260, 300)
    cv.line([(ant[0], ant[1]), (ant[0], SEA)], 5, WHITE)
    cv.arc(ant, 40, 200, 340, 4, WHITE)
    sea_line(cv, s, SEA, amp=6 if ph == 0 else 22, speed=1.5)
    drone_boat(cv, (1300, SEA - 4), 1.4, ORANGE, 5)
    for k in range(5):
        u = (s * 0.6 + k / 5) % 1
        r = 200 + 1100 * u
        cv.arc(ant, r, 0, 30, 2, (90, 90, 90))
    if ph == 1:
        rnd = random.Random(int(s * 6))
        for i in range(60):
            x, y = rnd.uniform(600, 1800), SEA + rnd.uniform(-30, 10)
            cv.dot((x, y), 4, (150, 150, 150))
        cv.text((CX, 200), "LOST IN THE WAVE ECHOES", 40, ORANGE, alpha=seg(s, 0.3, 0.3))
    else:
        cv.text((CX, 200), "LITTLE ABOVE THE WATER = SMALL RADAR ECHO", 36, WHITE, alpha=seg(s, 0.3, 0.3))


def e4_tradeoff(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX - 400, 260), "SMALL", 50, ORANGE)
    cv.text((CX - 400, 360), "+ HARD TO HIT", 36, WHITE, alpha=seg(s, 0.2, 0.3))
    for i, t in enumerate(("− LESS FUEL", "− LESS PAYLOAD", "− WEAK IN HIGH WAVES")):
        cv.text((CX + 300, 300 + i * 100), t, 36, RED, alpha=seg(s, 0.5 + i * 0.3, 0.3))
    cv.line([(CX, 220), (CX, 640)], 3, DIM)


def e4_three(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i, t in enumerate(("FAST", "LOW", "SMALL")):
        x = 460 + i * 500
        a = seg(s, 0.1 + i * 0.3, 0.3)
        cv.rect((x - 190, 360, x + 190, 520), 5, ORANGE, radius=14)
        cv.text((x, 440), t, 60, ORANGE, alpha=a)
    cv.text((CX, 680), "= GET CLOSE WITHOUT BEING SEEN", 40, WHITE, alpha=seg(s, 1.0, 0.3))


# ---------------- control ----------------

def e4_horizon(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    R = 2400
    c = (CX, 700 + R)
    cv.arc(c, R, 245, 295, 5, WHITE)
    boat = (520, 700 - 22)
    drone_boat(cv, (boat[0], boat[1] + 18), 0.8, ORANGE, 4)
    ang = math.radians(270 + 12)
    tgt = (c[0] + R * math.cos(ang), c[1] + R * math.sin(ang) - 10)
    if ph == 0:
        cv.text((CX, 200), "AT SEA, THE HORIZON IS CLOSE", 40, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph >= 1:
        cv.line([boat, (boat[0] + 900, boat[1] + 60)], 3, GREY)
        cv.text((CX, 200), "ONLY A FEW KM FROM WATER LEVEL", 40, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        cv.dashed([(300, 640), (1300, 700)], 4, RED, offset=s * 50)
        cross(cv, (1320, 700), 30, RED, 8, seg(s, 0.4, 0.4))
        cv.text((CX, 820 - 20), "RADIO CAN'T BEND AROUND THE CURVE", 34, RED, alpha=seg(s, 0.5, 0.3))
    drone_boat(cv, (tgt[0] + 400, tgt[1] + 120), 0.6, GREY, 3)


def e4_range_map(cv, s, T, ph=0):
    black_sea(cv, s)
    p = seg(s, 0.2, 1.4)
    path = [(600, 330), (700, 440), (900, 520), (1150, 520), (1380, 400)]
    cv.dashed(path, 4, ORANGE, offset=-s * 40, prog=p)
    if p > 0:
        k = min(len(path) - 1, int(p * (len(path) - 1)))
        cv.dot(path[k], 10, ORANGE)
    cv.text((1150, 610), "HUNDREDS OF KM", 40, ORANGE, alpha=seg(s, 0.9, 0.3))


def e4_sat_relay(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    from gfx import satellite_icon
    sat = (CX, 200)
    satellite_icon(cv, sat, 1.0)
    sea_line(cv, s, 640, 1000, 1800, 5)
    drone_boat(cv, (1400, 640), 1.6, ORANGE, 5, wake=0.6)
    cv.rect((420 - 120, 560, 420 + 120, 640), 5, WHITE, radius=10)
    cv.text((420, 680), "OPERATOR ON LAND", 28, WHITE)
    cv.dashed([(1400, 590), sat], 4, ORANGE, offset=s * 80)
    cv.dashed([sat, (420, 560)], 4, ORANGE, offset=s * 80)
    cv.text((1120, 380), "VIDEO", 28, ORANGE)
    cv.text((700, 380), "COMMANDS", 28, ORANGE)


def e4_route(cv, s, T, ph=0):
    black_sea(cv, s, labels=False)
    pts = [(560, 360), (640, 460), (820, 540), (1040, 560), (1240, 500)]
    for p in pts[1:-1]:
        cv.circle(p, 14, 3, WHITE)
    cv.dashed(pts, 4, WHITE, offset=-s * 40)
    u = (s * 0.25) % 1
    i = min(len(pts) - 2, int(u * (len(pts) - 1)))
    f = u * (len(pts) - 1) - i
    pos = lerp_pt(pts[i], pts[i + 1], f)
    boat_top(cv, pos, math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]), 1.2)
    cv.text((CX, 180), "PRESET WAYPOINTS · STEERS ITSELF", 36, WHITE, alpha=seg(s, 0.2, 0.3))


def e4_final(cv, s, T, ph=0):
    box = (360, 150, 1560, 800)
    x0, y0, x1, y1 = box
    hz = 420 + 6 * math.sin(s * 2)
    cv.line([(x0, hz), (x1, hz)], 3, GREY)
    sc = 0.6 + 0.6 * clamp(s / max(T, 1.0))
    warship(cv, (CX + 60, hz + 10), sc, WHITE, 4)
    for k in range(6):
        yy = lerp(hz + 20, y1 - 20, (k + (s * 1.5) % 1) / 6)
        cv.line([(x0 + 40, yy), (x1 - 40, yy)], 2, DIM)
    cv.text((x0 + 40, y0 + 45), "LIVE CAMERA", 26, ORANGE, anchor="lm")
    if ph:
        cv.text((CX, y1 - 60), "A PERSON MAKES THE FINAL CALL", 34, ORANGE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX, y1 - 60), "FINAL APPROACH: HUMAN PILOT", 34, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.rect(box, 8, WHITE, radius=50)


# ---------------- tactics ----------------

def e4_multi(cv, s, T, ph=0):
    """ph0 one boat stopped, ph1 several from many sides, ph2 saturation label, ph3 others get through."""
    backdrop(cv, s, "grid")
    ship_top(cv, (CX, CY), 1.4)
    if ph == 0:
        a = 0.4
        r = lerp(600, 320, clamp(s / max(T, 1)))
        pos = (CX + r * math.cos(a), CY + r * math.sin(a) * 0.65)
        boat_top(cv, pos, math.atan2(CY - pos[1], CX - pos[0]), 1.3)
        cv.dashed([(CX + 60, CY), pos], 3, RED, offset=s * 60)
        cross(cv, pos, 30, RED, 8, seg(s, 0.8, 0.4))
        cv.text((CX, 170), "ONE BOAT IS EASY TO STOP", 34, WHITE, alpha=seg(s, 0.3, 0.3))
        return
    angs = (0.3, 1.5, 2.7, 3.6, 5.6)
    gun_target = int(s * 1.2) % len(angs)
    for i, a in enumerate(angs):
        r = lerp(620, 230 if ph == 3 else 320, ease(clamp(s / max(T, 1))))
        if ph == 3 and i == gun_target:
            r = lerp(620, 380, ease(clamp(s / max(T, 1))))
        pos = (CX + r * math.cos(a), CY + r * math.sin(a) * 0.65)
        boat_top(cv, pos, math.atan2(CY - pos[1], CX - pos[0]), 1.2)
        if i == gun_target:
            cv.dashed([(CX + 40, CY), pos], 3, RED, offset=s * 60)
    if ph == 2:
        cv.text((CX, 170), "SATURATION: MORE TARGETS THAN GUNS", 34, ORANGE, alpha=seg(s, 0.2, 0.3))
    elif ph == 3:
        cv.text((CX, 170), "WHILE ONE IS STOPPED, OTHERS CLOSE IN", 34, ORANGE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX, 170), "MANY BOATS · MANY DIRECTIONS", 34, ORANGE, alpha=seg(s, 0.2, 0.3))


def e4_both_sides(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sea_line(cv, s, SEA)
    warship(cv, (CX, SEA), 1.4, WHITE, 5)
    p = ease(clamp(s / max(T - 0.5, 1)))
    drone_boat(cv, (lerp(150, CX - 470, p), SEA), 1.0, ORANGE, 5, wake=0.7)
    drone_boat(cv, (lerp(1770, CX + 500, p), SEA), 1.0, ORANGE, 5, flip=True, wake=0.7)
    cv.text((CX, 220), "FROM BOTH SIDES AT ONCE", 40, ORANGE, alpha=seg(s, 0.3, 0.3))
    cv.text((CX, 280), "LANDING SHIP · FEB 2024 (UKRAINIAN VIDEO)", 26, GREY, alpha=seg(s, 0.6, 0.3))


# ---------------- evolution ----------------

STAGES = ("RAM A SHIP", "CARRY MISSILES", "LAUNCH FLYING DRONES")


def e4_evolution(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(260, 480), (1660, 480)], 4, GREY)
    for i, t in enumerate(STAGES):
        x = 360 + i * 600
        on = i <= (2 if ph == 0 else 0)
        a = seg(s, 0.1 + i * 0.4, 0.3) if ph == 0 else (1 if i == 0 else 0.3)
        cv.dot((x, 480), 14, ORANGE if on else DIM)
        drone_boat(cv, (x, 400), 1.0, ORANGE if (ph == 0 or i == 0) else DIM, 4)
        cv.text((x, 560), t, 30, WHITE if (ph == 0 or i == 0) else DIM, alpha=a)
    cv.text((CX, 220), "KEEPS EVOLVING" if ph == 0 else "AT FIRST: JUST RAM", 44, ORANGE, alpha=seg(s, 0.1, 0.3))


def e4_sky(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sea_line(cv, s, SEA)
    drone_boat(cv, (CX - 200, SEA), 2.0, ORANGE, 5)
    cv.arrow((CX - 160, SEA - 80), (CX + 250, 220), 5, ORANGE, seg(s, 0.2, 0.6), 24)
    heli(cv, (CX + 380, 200), 1.0, GREY, 4, spin=s * 20)
    cv.text((CX - 400, 260), "NOT ONLY ATTACK —", 36, WHITE, alpha=seg(s, 0.1, 0.3))
    cv.text((CX - 400, 320), "ALSO AIM AT THE SKY", 36, ORANGE, alpha=seg(s, 0.4, 0.3))


def e4_claim(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    heli(cv, (CX - 360, 380), 1.1, WHITE, 4, spin=s * 20)
    cv.text((CX - 360, 520), "HELICOPTERS · DEC 2024", 30, WHITE)
    cv.text((CX + 360, 380), "2 × FIGHTER JETS", 44, WHITE)
    cv.text((CX + 360, 520), "MAY 2025", 30, WHITE)
    cv.tag((CX, 680), "UKRAINIAN CLAIM · NOT INDEPENDENTLY VERIFIED", 32, RED, alpha=seg(s, 0.2, 0.3))


def e4_first(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    drone_boat(cv, (CX - 380, 480), 2.0, ORANGE, 5)
    cv.text((CX - 380, 580), "UNCREWED BOAT", 34, ORANGE)
    cv.arrow((CX - 140, 450), (CX + 140, 380), 6, ORANGE, seg(s, 0.3, 0.5), 24)
    heli(cv, (CX + 400, 380), 1.2, WHITE, 5, spin=s * 20)
    cv.text((CX + 400, 580), "CREWED AIRCRAFT", 34, WHITE)
    cv.text((CX, 220), "IF TRUE: A FIRST", 48, ORANGE, alpha=seg(s, 0.6, 0.3))


def e4_mothership(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sea_line(cv, s, SEA)
    cv.line([(1500, SEA), (1500, SEA - 120), (1800, SEA - 120)], 4, GREY)
    cv.text((1650, SEA - 160), "ENEMY COAST", 26, GREY)
    p = seg(s, 0, 1.6)
    bx = lerp(200, 1100, p)
    drone_boat(cv, (bx, SEA), 1.3, ORANGE, 5, wake=0.6)
    cv.dashed([(200, SEA + 40), (bx, SEA + 40)], 3, ORANGE)
    cv.text((650, SEA + 90), "LONG SEA LEG: BOAT", 28, ORANGE, alpha=seg(s, 0.3, 0.3))
    if p >= 1:
        q = seg(s, 1.7, 1.2)
        dpos = (lerp(1100, 1600, q), lerp(SEA - 60, SEA - 260, q) + 30 * math.sin(q * 3))
        quad_top(cv, dpos, 0.35, WHITE, 3, spin=s * 30)
        cv.dashed([(1100, SEA - 60), dpos], 3, WHITE, offset=s * 40)
        cv.text((1350, 220), "LAST FEW KM: FLYING DRONE", 28, WHITE, alpha=seg(s, 1.9, 0.3))


def e4_platform(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    drone_boat(cv, (CX, 470), 3.0, ORANGE, 6, wake=0.4)
    cv.text((CX, 260), "THE PLATFORM MATTERS MOST", 50, ORANGE, alpha=seg(s, 0.1, 0.3))
    for i, t in enumerate(("RAM", "MISSILES", "FLYING DRONES")):
        cv.tag((CX - 400 + i * 400, 640), t, 30, WHITE, alpha=seg(s, 0.4 + i * 0.2, 0.3))


# ---------------- results ----------------

def e4_timeline(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(260, 480), (1660, 480)], 4, GREY)
    for i, (yr, lab) in enumerate((("2023", "KERCH BRIDGE"), ("2024", "WARSHIPS SUNK"), ("2026", "TANKERS"))):
        x = 400 + i * 560
        a = seg(s, 0.1 + i * 0.4, 0.3)
        cv.dot((x, 480), 14, ORANGE)
        cv.text((x, 410), yr, 50, ORANGE, alpha=a)
        cv.text((x, 550), lab, 30, WHITE, alpha=a)


def e4_sunk(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    items = [("MISSILE CORVETTE", "FEB 1, 2024"), ("LANDING SHIP", "FEB 14, 2024"), ("PATROL SHIP", "MAR 5, 2024")]
    n = 1 if ph == 0 else 3
    for i in range(n):
        name, date = items[i]
        x = 400 + i * 560
        a = seg(s, 0.1 + (i - (0 if ph == 0 else 1)) * 0.4, 0.3) if (ph == 0 or i > 0) else 1
        sink = 30 * seg(s, 0.3 + i * 0.3, 1.0)
        warship(cv, (x, 520 + sink), 0.6, WHITE if a >= 1 else GREY, 4)
        sea_line(cv, s, 520, x - 200, x + 200, 5)
        cv.text((x, 620), name, 30, WHITE, alpha=a)
        cv.text((x, 670), date, 26, ORANGE, alpha=a)
    cv.tag((CX, 220), "UKRAINIAN CLAIMS", 30, RED, alpha=seg(s, 0.2, 0.3))


def e4_cost_ratio(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    rows = [("SEA DRONE", 0.25, ORANGE, "~$0.25M"), ("PATROL SHIP (UKRAINIAN ESTIMATE)", 65, WHITE, "~$65M")]
    for i, (lab, v, col, txt) in enumerate(rows):
        y = 380 + i * 170
        p = seg(s, 0.2 + i * 0.4, 0.8)
        cv.text((CX, y - 60), lab, 30, col)
        w = max(8, 1300 * v / 65)
        cv.rect((CX - 650, y - 30, CX - 650 + w * p, y + 30), 0, fill=col, radius=6)
        cv.text((CX - 650 + w * p + 20, y) if i == 0 else (CX - 650 + w * p - 20, y), txt, 32,
                col if i == 0 else (20, 20, 20), anchor="lm" if i == 0 else "rm", alpha=seg(s, 0.6 + i * 0.4, 0.3))
    if ph:
        cv.text((CX, 760), "HUNDREDS OF TIMES MORE", 50, ORANGE, alpha=seg(s, 0.2, 0.3))


def e4_fleet_move(cv, s, T, ph=0):
    black_sea(cv, s)
    cv.dot(SEVASTOPOL, 10, RED)
    cv.text((SEVASTOPOL[0] - 10, SEVASTOPOL[1] + 40), "SEVASTOPOL", 24, RED)
    cv.dot(NOVO, 10, RED)
    cv.text((NOVO[0], NOVO[1] - 40), "NOVOROSSIYSK", 24, RED)
    p = ease(seg(s, 0.3, 1.6))
    for k in range(5):
        a = (SEVASTOPOL[0] + 20 + k * 18, SEVASTOPOL[1] + 10 + (k % 2) * 16)
        pos = lerp_pt(a, (NOVO[0] - 40 + k * 14, NOVO[1] + 20 + (k % 2) * 12), p)
        ship_top(cv, pos, 0.18, RED, 3)
    cv.arrow((1000, 420), (1360, 360), 5, RED, seg(s, 0.2, 0.8), 22)
    if ph:
        cv.poly([(600, 380), (900, 500), (1150, 600), (800, 640), (500, 560)], fill=(255, 138, 31, 40))
        cv.text((800, 600), "PUSHED OUT · NO BIG NAVAL BATTLE", 30, ORANGE, alpha=seg(s, 0.4, 0.3))


def e4_corridor(cv, s, T, ph=0):
    black_sea(cv, s)
    path = [ODESA, (520, 360), (430, 430), (380, 520), (420, 640), (520, 700)]
    cv.dashed(path, 5, ORANGE, offset=-s * 60, prog=seg(s, 0.2, 1.2))
    u = (s * 0.2) % 1
    i = min(len(path) - 2, int(u * (len(path) - 1)))
    pos = lerp_pt(path[i], path[i + 1], u * (len(path) - 1) - i)
    boat_top(cv, pos, math.atan2(path[i + 1][1] - path[i][1], path[i + 1][0] - path[i][0]), 1.0, WHITE)
    cv.text((300, 760), "NEW SEA ROUTE ALONG THE COAST", 30, ORANGE, anchor="lm", alpha=seg(s, 0.6, 0.3))


def e4_calendar(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    x0, y0 = CX - 350, 260
    cv.text((CX, 200), "BLACK SEA FLEET MISSILE LAUNCHES · ONE MONTH", 30, GREY)
    for d in range(30):
        x = x0 + (d % 7) * 100
        y = y0 + (d // 7) * 100
        cv.rect((x, y, x + 84, y + 84), 3, DIM, radius=8)
        if d in (9, 22) and s > 0.5 + d * 0.03:
            cv.dot((x + 42, y + 42), 22, RED)
    cv.text((CX, 800 - 20), "ONCE OR TWICE A MONTH (UKRAINIAN NAVY CLAIM)", 30, ORANGE, alpha=seg(s, 1.0, 0.3))


# ---------------- reversal ----------------

def e4_mirror(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX - 420, 300), "UKRAINE", 44, WHITE)
    cv.text((CX + 420, 300), "RUSSIA", 44, RED)
    cv.arrow((CX - 250, 420), (CX + 250, 420), 6, ORANGE, seg(s, 0.2, 0.5), 26)
    if ph == 0:
        cv.text((CX, 600), "CHEAP WEAPONS CAN BE COPIED", 50, ORANGE, alpha=seg(s, 0.5, 0.3))
    else:
        cv.arrow((CX + 250, 520), (CX - 250, 520), 6, RED, seg(s, 0.2, 0.5), 26)
        cv.text((CX, 660), "THE SAME WEAPON, TURNED AROUND", 50, RED, alpha=seg(s, 0.5, 0.3))


def e4_export(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    base = 720
    cv.text((CX, 170), "2026/27 GRAIN EXPORT FORECAST (MILLION T)", 30, GREY)
    for i, (lab, v, col) in enumerate((("EARLIER", 43, WHITE), ("AUG 2026", 39, ORANGE))):
        x = CX - 220 + i * 440
        h = 11 * v * seg(s, 0.2 + i * 0.4, 0.8)
        cv.rect((x - 110, base - h, x + 110, base), 0, fill=col, radius=6)
        cv.text((x, base + 40), lab, 30, WHITE)
        cv.text((x, base - h - 40), str(v) if i == 0 else "38–40", 44, col, alpha=seg(s, 0.8 + i * 0.4, 0.3))
    cv.text((CX, 830 - 20), "CUT AFTER RUSSIAN STRIKES ON PORTS", 30, RED, alpha=seg(s, 1.4, 0.3))


def e4_ru_usv(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sea_line(cv, s, 560)
    for k in range(3):
        drone_boat(cv, (CX - 300 + k * 300, 560), 1.4, RED, 5, flip=True, wake=0.5)
    cv.text((CX, 260), "RUSSIA: ITS OWN SEA DRONE UNITS", 40, RED, alpha=seg(s, 0.2, 0.3))
    cv.tag((CX, 720), "REPORTED", 28, alpha=seg(s, 0.5, 0.3))


# ---------------- limits ----------------

LIMITS = ("HELICOPTERS", "GUNS · THERMAL · LIGHTS", "HARBOUR BARRIERS", "JAMMING", "THE SEA ITSELF")


def e4_limits(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 170), "LIMITS", 50, ORANGE)
    for i, t in enumerate(LIMITS):
        cv.text((CX, 270 + i * 100), t, 40, WHITE, alpha=seg(s, 0.2 + i * 0.25, 0.3))


def e4_heli_view(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    sea_line(cv, s, SEA)
    hp = (CX - 300 + 200 * math.sin(s * 0.5), 220)
    heli(cv, hp, 1.2, WHITE, 5, spin=s * 20)
    cv.poly([hp, (hp[0] - 300, SEA), (hp[0] + 500, SEA)], fill=(255, 255, 255, 25))
    bpos = (CX + 300 - 80 * s / max(T, 1), SEA)
    drone_boat(cv, bpos, 1.0, ORANGE, 5, wake=0.6)
    cv.text((CX + 420, 300), "HIGH · FAST · WIDE VIEW", 34, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph:
        cv.dashed([(hp[0] + 40, hp[1] + 40), bpos], 3, RED, offset=s * 60)
        cv.text((CX + 420, 360), "A GUNNER AIMS FROM ABOVE", 30, RED, alpha=seg(s, 0.2, 0.3))


def e4_boom(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(200, 300), (700, 300), (700, 520)], 6, WHITE)
    cv.line([(1720, 300), (1220, 300), (1220, 520)], 6, WHITE)
    cv.text((CX, 240), "HARBOUR", 34, GREY)
    for k in range(13):
        x = 720 + k * 38
        cv.circle((x, 520 + 4 * math.sin(s * 2 + k)), 12, 3, ORANGE)
    cv.line([(708, 520), (1212, 520)], 3, ORANGE)
    boat_top(cv, (CX, 700 - 40 * min(1, s / 2)), -math.pi / 2, 1.3)
    cv.text((CX, 820 - 20), "SAME IDEA AS AGAINST TORPEDO BOATS, 100+ YEARS AGO", 30, WHITE, alpha=seg(s, 0.4, 0.3))


def e4_jam(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    from gfx import satellite_icon, tower_icon
    sat = (CX, 200)
    satellite_icon(cv, sat, 1.0)
    sea_line(cv, s, 640, 1000, 1800, 5)
    drone_boat(cv, (1400, 640), 1.6, ORANGE, 5)
    cv.dashed([(1400, 590), sat], 4, ORANGE, offset=s * 80)
    tower_icon(cv, (520, 560), 1.0, RED)
    for k in range(3):
        waves(cv, (560, 460), 2.0, RED, 4, s * 1.5 + k * 0.33, -40, 20, 1)
    cross(cv, lerp_pt((1400, 590), sat, 0.5), 40, RED, 8, seg(s, 0.8, 0.4))
    cv.text((CX, 820 - 20), "JAMMING THE SATELLITE AND RADIO LINKS", 32, RED, alpha=seg(s, 0.4, 0.3))


def e4_waves(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    pts = [(x, 560 + 70 * math.sin(x / 110 + s * 2.2)) for x in range(0, 1921, 16)]
    cv.line(pts, 5, WHITE)
    bx = CX
    by = 560 + 70 * math.sin(bx / 110 + s * 2.2)
    slope = 70 / 110 * math.cos(bx / 110 + s * 2.2)
    drone_boat(cv, (bx, by - 6), 1.6, ORANGE, 5)
    cv.text((CX, 240), "SMALL, LOW HULLS STRUGGLE IN HIGH WAVES", 36, WHITE, alpha=seg(s, 0.2, 0.3))


def e4_weather(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i, (lab, ok) in enumerate((("CALM", True), ("CALM", True), ("STORM", False), ("STORM", False), ("CALM", True))):
        x = 360 + i * 300
        cv.rect((x - 110, 330, x + 110, 560), 4, WHITE if ok else RED, radius=12)
        cv.text((x, 400), lab, 30, WHITE if ok else RED)
        if ok:
            check(cv, (x, 480), 30, ORANGE, 8, seg(s, 0.2 + i * 0.2, 0.3))
        else:
            cross(cv, (x, 480), 30, RED, 8, seg(s, 0.2 + i * 0.2, 0.3))
    cv.text((CX, 720), "THE WEATHER CAN END A MISSION FIRST", 40, ORANGE, alpha=seg(s, 1.2, 0.3))


# ---------------- outro ----------------

def e4_recap(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    drone_boat(cv, (CX - 420, 500), 1.6, ORANGE, 5)
    cv.text((CX - 420, 600), "CHEAP BOAT", 36, ORANGE)
    cv.text((CX, 490), "VS", 50, GREY)
    warship(cv, (CX + 420, 520), 0.8, WHITE, 4)
    cv.text((CX + 420, 600), "EXPENSIVE WARSHIP", 36, WHITE)


def e4_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP05  ·  OPERATION SPIDERWEB", "map")


SCENES = {k: v for k, v in globals().items() if k.startswith("e4_") and callable(v)}
