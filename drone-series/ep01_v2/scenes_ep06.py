"""EP06 line-art scenes ("Guarding the Night Sky"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math

from gfx import DIM, GREY, ORANGE, RED, WHITE, check, clamp, cross, ease, jet_icon, lerp, lerp_pt, radar_dish, seg
from scenes import BG, BG_O, CX, CY, backdrop, end_card, title_card
from scenes_ep03 import big_word, quad_top
from scenes_ep05 import missile_dir

GROUND = 660


# ---------------- icons ----------------

def geran(cv, c, s=1.0, col=RED, w=5, a=0.0):
    """Top view of a delta-wing one-way attack drone, nose along angle a, pusher prop at the back."""
    ca, sa = math.cos(a), math.sin(a)

    def P(dx, dy):
        return (c[0] + (dx * ca - dy * sa) * s, c[1] + (dx * sa + dy * ca) * s)

    cv.line([P(140, 0), P(-90, -120), P(-110, -120), P(-70, 0), P(-110, 120), P(-90, 120), P(140, 0)], w, col)
    cv.line([P(140, 0), P(-100, 0)], w, col)
    cv.circle(P(-110, 0), 18 * s, 3, col)


def pickup(cv, c, s=1.0, col=WHITE, w=5, gun_a=-0.6):
    """Side view of a pickup truck with a machine gun on a post in the bed, cab on the right."""
    x, y = c

    def P(dx, dy):
        return (x + dx * s, y + dy * s)

    cv.line([P(-200, -30), P(-200, -80), P(20, -80), P(20, -30)], w, col)  # bed
    cv.line([P(20, -30), P(20, -140), P(120, -140), P(170, -85), P(210, -80), P(210, -30), P(-220, -30),
             P(-220, -60), P(-200, -60)], w, col)
    cv.line([P(40, -125), P(110, -125), P(145, -88), P(40, -88), P(40, -125)], 3, col)
    for wx in (-140, 140):
        cv.circle(P(wx, -10), 28 * s, w, col)
    cv.line([P(-90, -80), P(-90, -150)], w, col)  # post
    cv.line([P(-90, -150), P(-90 + 150 * math.cos(gun_a), -150 + 150 * math.sin(gun_a))], w + 2, col)


def ukraine_map(cv, s):
    backdrop(cv, s, "grid")
    ua = [(300, 420), (420, 300), (640, 250), (900, 230), (1180, 260), (1400, 300), (1560, 400), (1600, 520),
          (1450, 600), (1240, 640), (1050, 720), (860, 700), (700, 640), (520, 620), (380, 560), (300, 420)]
    cv.line(ua, 4, GREY)
    cv.text((900, 760), "UKRAINE · SCHEMATIC", 22, DIM)


KYIV = (930, 330)


# ---------------- cold open ----------------

def e6_siren(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for k in range(4):
        r = 60 + 140 * (((s * 0.7) + k / 4) % 1)
        cv.circle((CX, CY), r * 2.2, 3, tuple(int(v * (1 - ((s * 0.7 + k / 4) % 1))) for v in (255, 80, 60)))
    cv.circle((CX, CY), 70, 6, RED)
    cv.text((CX, CY), "!", 90, RED)
    cv.text((CX, CY + 230), "AIR-RAID ALERT", 54, WHITE, alpha=seg(s, 0.2, 0.3))


def e6_count(cv, s, T, ph=0):
    """ph0 463 launched, ph1 418 stopped, ph2 nine in ten, ph3 45 got through."""
    backdrop(cv, s, "grid")
    n, stop = 463, 418
    cols, sz = 31, 34
    x0 = CX - cols * sz / 2
    shown = n if ph else int(n * ease(seg(s, 0.1, 1.6)))
    hit = 0 if ph == 0 else (stop if ph >= 2 else int(stop * ease(seg(s, 0.2, 1.6))))
    for i in range(shown):
        x, y = x0 + (i % cols) * sz, 170 + (i // cols) * 30
        col = DIM if i < hit else RED
        if ph == 3 and i >= stop:
            col = RED
        elif ph == 3:
            col = (40, 40, 40)
        cv.line([(x - 9, y), (x + 9, y)], 3, col)
        cv.line([(x, y - 7), (x, y + 7)], 2, col)
    if ph == 0:
        cv.text((CX, 700), f"{shown} ATTACK DRONES · ONE DAY", 52, WHITE)
    elif ph == 1:
        cv.text((CX, 700), f"{hit} STOPPED", 60, ORANGE)
    elif ph == 2:
        cv.text((CX, 700), "9 OUT OF 10", 70, ORANGE, alpha=seg(s, 0.1, 0.3))
    else:
        cv.text((CX, 700), "45 GOT THROUGH", 64, RED, alpha=seg(s, 0.2, 0.3))


def e6_intro(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    for i in range(5):
        a = -0.5 + i * 0.25
        geran(cv, (CX + 520 * math.cos(a + math.pi) + 300, CY - 120 + 260 * math.sin(a)), 0.3, DIM, 3, a=math.pi)
    cv.text((CX, CY + 40), "WHO GUARDS THE SKY, AND HOW", 52, ORANGE, alpha=seg(s, 0.3, 0.4))


def e6_title(cv, s, T, ph=0):
    title_card(cv, s, "EP06  ·  GUARDING THE NIGHT SKY", "radar")


# ---------------- the opponent ----------------

def e6_geran(cv, s, T, ph=0):
    """ph0 the Geran, ph1 Iranian design → Russian mass production, ph2 how it flies."""
    backdrop(cv, s, "grid")
    if ph == 1:
        cv.text((CX - 420, 260), "IRAN", 44, GREY)
        geran(cv, (CX - 420, 470), 1.0, GREY, 4)
        cv.text((CX - 420, 660), "SHAHED (DESIGN)", 32, GREY)
        cv.arrow((CX - 180, 470), (CX + 160, 470), 5, ORANGE, seg(s, 0.3, 0.5), 22)
        cv.text((CX + 420, 260), "RUSSIA", 44, RED)
        for k in range(3):
            geran(cv, (CX + 340 + k * 80, 420 + k * 50), 0.55, RED, 3)
        cv.text((CX + 420, 660), "GERAN (MASS-PRODUCED)", 32, RED, alpha=seg(s, 0.6, 0.3))
        return
    geran(cv, (CX, CY - 20), 2.0, RED, 5)
    if ph == 0:
        cv.text((CX, 760), "GERAN · ONE-WAY ATTACK DRONE", 44, RED, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX + 330, CY - 200), "DELTA WING", 30, WHITE, anchor="lm")
        cv.text((CX - 330, CY + 120), "REAR PROPELLER", 30, WHITE, anchor="rm")
        cv.text((CX, 760), "FLIES ITSELF TO SET COORDINATES", 40, ORANGE, alpha=seg(s, 0.3, 0.3))


def e6_decoy(cv, s, T, ph=0):
    """ph0 decoys mixed in, ph1 to waste missiles, ph2 some decoys armed."""
    backdrop(cv, s, "grid")
    pts = [(420, 300), (700, 220), (980, 330), (1250, 240), (1520, 330), (560, 520), (860, 470), (1140, 540),
           (1420, 480)]
    for i, p in enumerate(pts):
        real = i % 3 == 0
        x = p[0] + 30 * math.sin(s + i)
        geran(cv, (x, p[1]), 0.45, RED if real else GREY, 3 if real else 2, a=math.pi)
        if ph == 2 and not real and i % 2:
            cv.text((x, p[1] + 70), "ARMED?", 22, RED)
    cv.text((CX - 300, 720), "REAL", 34, RED)
    cv.text((CX + 300, 720), "DECOY (GERBERA)", 34, GREY)
    if ph == 1:
        cv.text((CX, 140), "CONFUSE DEFENCES · WASTE MISSILES", 40, ORANGE, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        cv.text((CX, 140), "SOME DECOYS NOW CARRY EXPLOSIVES", 40, RED, alpha=seg(s, 0.2, 0.3))


def e6_routes(cv, s, T, ph=0):
    ukraine_map(cv, s)
    cv.dot(KYIV, 10, WHITE)
    cv.text((KYIV[0], KYIV[1] - 34), "KYIV", 26, WHITE)
    starts = [(1880, 160), (1880, 420), (1700, 760), (1150, 900), (1880, 640)]
    for i, a in enumerate(starts):
        mid = ((a[0] + KYIV[0]) / 2 + 120 * math.sin(i * 2), (a[1] + KYIV[1]) / 2 + 160 * math.cos(i * 3))
        pts = [lerp_pt(lerp_pt(a, mid, t / 30), lerp_pt(mid, KYIV, t / 30), t / 30) for t in range(31)]
        cv.dashed(pts, 3, RED, offset=s * 40, prog=seg(s, 0.2 + i * 0.3, 1.5))
    cv.text((CX, 820), "AFTER DARK · MANY DIRECTIONS · HOURS", 36, WHITE, alpha=seg(s, 0.5, 0.3))


def e6_saturate(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    n = int(40 * ease(seg(s, 0.1, 2.0)))
    for i in range(n):
        a = i * 2.4
        r = 600 - (s * 60 + i * 13) % 480
        geran(cv, (CX + r * math.cos(a), CY + r * math.sin(a) * 0.6), 0.18, RED, 2, a=a + math.pi)
    cv.circle((CX, CY), 40, 4, WHITE)
    cv.text((CX, 820), "SWARM IN AT ONCE · WEAR DEFENCES OUT (EP01)", 36, WHITE, alpha=seg(s, 0.5, 0.3))


# ---------------- the cost dilemma ----------------

def e6_cost(cv, s, T, ph=0):
    """Cost bars on a log-ish scale: ph0 Geran, ph1 decoy, ph2 Patriot, ph3 interceptor drone, ph4 ratio."""
    backdrop(cv, s, "grid")
    rows = [("GERAN", "~$20K–50K", RED, 0.35), ("DECOY", "~$10K", GREY, 0.25), ("PATRIOT MISSILE", "$4M+", WHITE, 1.0),
            ("INTERCEPTOR DRONE", "~$1K–2K", ORANGE, 0.08)]
    show = {0: 1, 1: 2, 2: 3, 3: 4, 4: 4}[ph]
    for i, (lab, txt, col, v) in enumerate(rows[:show]):
        y = 220 + i * 140
        new = i == show - 1 and ph < 4
        p = ease(seg(s, 0.1, 0.8)) if new else 1.0
        cv.text((260, y - 40), lab, 30, col, anchor="lm")
        cv.rect((260, y - 16, 260 + 1300 * v * p + 4, y + 16), 0, fill=col, radius=6)
        cv.text((260 + 1300 * v * p + 30, y), txt, 34, col, anchor="lm", alpha=seg(s, 0.5, 0.3) if new else 1.0)
    if ph == 4:
        cv.text((CX, 800), "A FEW THOUSANDTHS OF A MISSILE", 44, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((1660, 820), "BAR LENGTHS NOT TO SCALE", 20, DIM)


def e6_calc(cv, s, T, ph=0):
    """ph0 the question, ph1 463 × $4M, ph2 = KRW, ph3 night after night."""
    backdrop(cv, s, "grid")
    cv.text((CX, 220), "463 DRONES  ×  ~$4 MILLION PER PATRIOT", 48, WHITE, alpha=seg(s, 0.1, 0.3))
    if ph >= 1:
        v = 1.85 * ease(seg(s, 0.2, 1.2)) if ph == 1 else 1.85
        cv.text((CX, 400), f"≈ ${v:.2f} BILLION", 110, RED)
        cv.text((CX, 500), "IN ONE NIGHT", 40, WHITE)
    if ph >= 2:
        cv.text((CX, 600), "≈ 2.5 TRILLION KRW", 50, ORANGE, alpha=seg(s, 0.2, 0.3) if ph == 2 else 1.0)
    if ph == 3:
        for k in range(7):
            x = CX - 420 + k * 140
            cv.circle((x, 740), 28, 3, GREY)
            cv.arc((x + 8, 732), 22, 200, 340, 3, GREY)
        cv.text((CX, 820), "NIGHT AFTER NIGHT · NO COUNTRY CAN KEEP THIS UP", 36, RED, alpha=seg(s, 0.3, 0.3))


def e6_save(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for k in range(4):
        missile_dir(cv, (CX - 300, 330 + k * 90), 0.8, WHITE, 4, a=-math.pi / 2 * 0)
    cv.rect((CX - 520, 260, CX - 80, 650), 4, ORANGE, radius=12)
    cv.text((CX - 300, 700), "SAVE THE MISSILES", 36, ORANGE)
    cv.arrow((CX - 40, 450), (CX + 200, 450), 5, GREY, seg(s, 0.3, 0.5), 22)
    cv.text((CX + 430, 450), "BALLISTIC MISSILES", 40, RED, alpha=seg(s, 0.6, 0.3))


def e6_rule(cv, s, T, ph=0):
    if ph == 0:
        big_word(cv, s, "THE RULE", WHITE, 120)
        return
    big_word(cv, s, "CHEAP DRONE → CHEAP WEAPON", ORANGE, 90)


# ---------------- mobile fire teams ----------------

def e6_truck_gun(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(0, GROUND), (1920, GROUND)], 3, GREY)
    pickup(cv, (CX, GROUND), 1.6, WHITE, 5, gun_a=-0.7 + 0.08 * math.sin(s))
    cv.text((CX, 180), "PICKUP OR OLD TRUCK + MACHINE GUN", 44, ORANGE, alpha=seg(s, 0.2, 0.3))


def e6_ambush(cv, s, T, ph=0):
    """ph0 wait on the route, ph1 alert → scan, ph2 route shifts, ambush misses."""
    ukraine_map(cv, s)
    route = [(1880, 260), (1500, 360), (1200, 380), KYIV]
    alt = [(1880, 260), (1500, 470), (1200, 520), KYIV]
    team = (1350, 400)
    pickup(cv, (team[0], team[1] + 20), 0.25, ORANGE, 3)
    use = alt if ph == 2 else route
    cv.dashed(use, 3, RED, offset=s * 40, prog=seg(s, 0.2, 1.4))
    if ph == 1:
        for k in range(3):
            r = 60 + 50 * (((s * 0.8) + k / 3) % 1)
            cv.arc((team[0], team[1] - 10), r, 200, 340, 3, ORANGE)
        cv.text((CX, 820), "ALERT → SCAN WITH THERMAL CAMERAS + SEARCHLIGHTS", 34, WHITE, alpha=seg(s, 0.3, 0.3))
    elif ph == 2:
        cross(cv, team, 30, RED, 6, seg(s, 1.2, 0.4))
        cv.text((CX, 820), "A FEW KM OFF THE ROUTE = EMPTY AMBUSH", 38, RED, alpha=seg(s, 1.0, 0.3))
    else:
        cv.text((CX, 820), "WAIT WHERE THE DRONES WILL PASS", 38, WHITE, alpha=seg(s, 0.3, 0.3))


def e6_ceiling(cv, s, T, ph=0):
    """ph0 machine gun reach ~2 km, ph1 drones fly higher and faster."""
    backdrop(cv, s, "grid")
    cv.line([(0, GROUND), (1920, GROUND)], 3, GREY)
    ceil = 330
    cv.rect((200, ceil, 1800, GROUND - 4), 0, fill=(40, 26, 12), radius=0)
    cv.dashed([(200, ceil), (1800, ceil)], 3, ORANGE)
    cv.text((1780, ceil + 34), "~2 KM", 30, ORANGE, anchor="rm")
    pickup(cv, (420, GROUND), 0.8, WHITE, 4, gun_a=-0.9)
    y = lerp(500, 180, ease(seg(s, 0.3, 1.2))) if ph == 1 else 500
    x = 1700 - (s * 220) % 1500
    geran(cv, (x, y), 0.45, RED, 3, a=math.pi)
    if ph == 1:
        cv.text((CX, 120), "HIGHER AND FASTER", 48, RED, alpha=seg(s, 0.6, 0.3))
    else:
        cv.text((CX, 120), "MACHINE GUNS BARELY REACH ABOVE ~2 KM", 40, WHITE, alpha=seg(s, 0.2, 0.3))


# ---------------- guns and fighters ----------------

def e6_gepard(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(0, GROUND), (1920, GROUND)], 3, GREY)
    x, y = 520, GROUND
    cv.line([(x - 220, y - 20), (x + 220, y - 20), (x + 250, y - 80), (x - 250, y - 80), (x - 220, y - 20)], 5, WHITE)
    for k in range(5):
        cv.circle((x - 160 + k * 80, y - 20), 26, 4, WHITE)
    cv.rect((x - 110, y - 170, x + 110, y - 80), 5, WHITE, radius=8)
    radar_dish(cv, (x - 60, y - 230), 0.6)
    a = -0.55
    for dy in (-130, -110):
        cv.line([(x + 60, y + dy), (x + 60 + 330 * math.cos(a), y + dy + 330 * math.sin(a))], 6, WHITE)
    for k in range(6):
        t = ((s * 1.5) + k / 6) % 1
        p0 = (x + 60 + (360 + 900 * t) * math.cos(a), y - 120 + (360 + 900 * t) * math.sin(a))
        cv.line([p0, (p0[0] + 40 * math.cos(a), p0[1] + 40 * math.sin(a))], 4, ORANGE)
    cv.text((1350, 240), "GEPARD (FROM GERMANY)", 44, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.text((1350, 310), "RADAR + TWIN CANNONS", 34, ORANGE, alpha=seg(s, 0.5, 0.3))
    cv.text((1350, 370), "RELIABLE AGAINST LOW-FLYING DRONES", 30, GREY, alpha=seg(s, 0.8, 0.3))


def e6_fighter(cv, s, T, ph=0):
    """ph0 F-16 and Mirage hunt at night, ph1 getting close is dangerous."""
    backdrop(cv, s, "radar")
    if ph == 0:
        jet_icon(cv, (CX - 350, CY), 1.3, WHITE, 5)
        jet_icon(cv, (CX + 350, CY), 1.3, WHITE, 5)
        cv.text((CX - 350, CY + 170), "F-16", 44, WHITE)
        cv.text((CX + 350, CY + 170), "MIRAGE", 44, WHITE)
        cv.text((CX, 180), "NIGHT HUNTERS", 48, ORANGE, alpha=seg(s, 0.2, 0.3))
        return
    jet_icon(cv, (CX - 300, CY), 1.0, WHITE, 5)
    d = lerp(500, 220, ease(seg(s, 0.2, 1.5)))
    geran(cv, (CX - 300 + d + 150, CY), 0.5, RED, 3, a=0)
    if d < 260:
        for k in range(10):
            a = k * 0.63
            cv.line([(CX + 70 + 60 * math.cos(a), CY + 60 * math.sin(a)), (CX + 70 + 110 * math.cos(a),
                                                                            CY + 110 * math.sin(a))], 3, ORANGE)
    cv.text((CX, 760), "CLOSE-RANGE CANNON: RISKY FOR THE PILOT", 40, RED, alpha=seg(s, 0.6, 0.3))


def e6_one_left(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 200), "MAY 2025 · ONE F-16 RETURNS", 40, WHITE)
    for k in range(6):
        x = CX - 500 + k * 200
        if k < 5:
            missile_dir(cv, (x, 430), 0.45, DIM, 3, a=-math.pi / 2)
            check(cv, (x, 560), 30, ORANGE, 7, seg(s, 0.3 + k * 0.2, 0.3))
        else:
            missile_dir(cv, (x, 430), 0.45, WHITE, 4, a=-math.pi / 2)
            cv.text((x, 560), "LEFT", 30, WHITE)
    cv.text((CX, 720), "5 MISSILES FIRED · 5 TARGETS HIT", 50, ORANGE, alpha=seg(s, 1.4, 0.3))


# ---------------- interceptor drones ----------------

def e6_interceptor(cv, s, T, ph=0):
    """ph0 the drone that catches drones, ph1 FPV skills (EP03) now guard the sky."""
    backdrop(cv, s, "radar")
    p = ease(seg(s, 0.2, 2.0))
    g = (lerp(1700, 1100, p), lerp(260, 330, p))
    geran(cv, g, 0.6, RED, 4, a=math.pi)
    q = (lerp(300, g[0] - 80, p), lerp(700, g[1] + 20, p))
    quad_top(cv, q, 0.5, ORANGE, 4, spin=s * 30)
    cv.dashed([(300, 700), q], 3, ORANGE, offset=s * 40)
    if p >= 1:
        for k in range(8):
            a = k * 0.8
            cv.line([(g[0] + 40 * math.cos(a), g[1] + 40 * math.sin(a)), (g[0] + 90 * math.cos(a),
                                                                          g[1] + 90 * math.sin(a))], 4, ORANGE)
    cv.text((CX, 820), "THE DRONE THAT CATCHES DRONES" if ph == 0 else "EP03'S FPV SKILLS, NOW GUARDING THE SKY",
            44, ORANGE, alpha=seg(s, 0.3, 0.3))


def e6_germany(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    n = int(150 * ease(seg(s, 0.1, 1.6)))
    for i in range(n):
        quad_top(cv, (CX - 735 + (i % 30) * 50, 170 + (i // 30) * 60), 0.13, ORANGE, 2)
    cv.text((CX, 560), "15,000 INTERCEPTOR DRONES", 70, WHITE)
    cv.text((CX, 650), "FUNDED BY GERMANY · FOR UKRAINE'S NATIONAL GUARD", 34, GREY)
    cv.text((CX, 720), "EACH ICON ≈ 100 DRONES", 24, DIM)


def e6_unverified(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 330), "~70% OF SHAHED-TYPE KILLS BY INTERCEPTORS", 48, WHITE)
    cv.text((CX, 400), "JANUARY 2026 · ONE MEDIA REPORT, CITED SECOND-HAND", 30, GREY)
    cv.tag((CX, 520), "NOT OFFICIALLY CONFIRMED", 40, RED, alpha=seg(s, 0.2, 0.3))


# ---------------- the layered net ----------------

def e6_layers(cv, s, T, ph=0):
    """ph0 command splits the work, ph1 fighters far / guns near, ph2 interceptors fill gaps, ph3 layer after layer."""
    backdrop(cv, s, "grid")
    c = (CX - 600, CY + 40)
    rings = [(420, "FIGHTERS", WHITE), (300, "INTERCEPTOR DRONES", ORANGE), (180, "GUNS + FIRE TEAMS", WHITE)]
    cv.rect((c[0] - 60, c[1] - 40, c[0] + 60, c[1] + 40), 4, WHITE, radius=6)
    cv.text((c[0], c[1] + 80), "CITY", 26, WHITE)
    show = {0: 0, 1: 2, 2: 3, 3: 3}[ph]
    order = [0, 2, 1]
    for k in range(show):
        r, lab, col = rings[order[k]]
        cv.arc(c, r, -55, 55, 5, col)
        cv.text((c[0] + r * 0.574 + 20, c[1] - r * 0.819 - 26), lab, 26, col, anchor="lm")
    if ph == 0:
        cv.text((CX + 350, CY - 40), "COMMAND POST", 50, WHITE)
        cv.text((CX + 350, CY + 30), "WHICH LAYER TAKES WHICH DRONE", 34, ORANGE, alpha=seg(s, 0.3, 0.3))
    if ph == 3:
        p = (s * 0.35) % 1
        x = lerp(1850, c[0] + 80, p)
        geran(cv, (x, c[1]), 0.35, RED, 3, a=math.pi)
        for r, _, col in rings:
            if abs(x - (c[0] + r)) < 30:
                cv.circle((x, c[1]), 40, 3, col)
        cv.text((CX + 300, 160), "GET THROUGH ONE · THE NEXT IS WAITING", 38, ORANGE, alpha=seg(s, 0.3, 0.3))


# ---------------- what gets through ----------------

def e6_rate_warning(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 330), "90% STOPPED", 90, ORANGE)
    cv.text((CX, 470), "≠ COMPLETE SAFETY", 70, RED, alpha=seg(s, 0.4, 0.3))


def e6_speed(cv, s, T, ph=0):
    """ph0 jet Geran 2–3× faster, ph1 hard to catch for guns and propeller interceptors."""
    backdrop(cv, s, "grid")
    rows = [("PROPELLER GERAN", 1.0, GREY), ("JET GERAN", 2.6, RED)]
    for i, (lab, v, col) in enumerate(rows):
        y = 330 + i * 200
        x = 220 + ((s * 180 * v) % 1500)
        cv.text((220, y - 70), lab, 34, col, anchor="lm")
        cv.line([(200, y), (1720, y)], 2, DIM)
        geran(cv, (x, y), 0.4, col, 3, a=0)
        cv.line([(x - 220 * v * 0.4, y), (x - 70, y)], 3, col)
    cv.text((CX, 120), "2–3× FASTER", 54, RED, alpha=seg(s, 0.2, 0.3))
    if ph == 1:
        cv.text((CX, 800), "TOO FAST FOR MACHINE GUNS AND PROPELLER INTERCEPTORS", 34, WHITE, alpha=seg(s, 0.2, 0.3))


def e6_jet_rate(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cx, cy, r = CX, CY + 20, 220
    cv.circle((cx, cy), r, 30, (40, 40, 40))
    p = 0.58 * ease(seg(s, 0.2, 1.2))
    n = int(80 * p)
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / 80
        cv.line([(cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a)), (cx + (r + 14) * math.cos(a),
                                                                              cy + (r + 14) * math.sin(a))], 6, ORANGE)
    cv.text((cx, cy), "55–60%", 80, ORANGE)
    cv.text((CX, 140), "JET DRONES SHOT DOWN · ZELENSKY, OCT 17", 40, WHITE)


# ---------------- outro ----------------

def e6_recap(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    labels = ["FIRE TEAMS", "GUNS", "FIGHTERS", "INTERCEPTORS", "COMMAND"]
    for i, lab in enumerate(labels):
        y = 220 + i * 110
        a = seg(s, 0.1 + i * 0.25, 0.3)
        cv.rect((CX - 330, y - 40, CX + 330, y + 40), 4, ORANGE if i == 4 else WHITE, radius=10)
        cv.text((CX, y), lab, 36, WHITE, alpha=a)
    cv.text((CX, 820), "MANY PEOPLE, LAYER UPON LAYER", 40, ORANGE, alpha=seg(s, 1.4, 0.3))


def e6_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP07  ·  CATCH THE JET DRONE", "radar")


SCENES = {k: v for k, v in globals().items() if k.startswith("e6_") and callable(v)}
