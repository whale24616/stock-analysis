"""EP05 line-art scenes ("Operation Spiderweb"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math

from gfx import (DIM, GREY, ORANGE, RED, WHITE, check, clamp, clock_icon, cross, ease, lerp, lerp_pt, missile_icon,
                 radar_dish, seg, tower_icon)
from scenes import BG, BG_O, CX, CY, backdrop, end_card, title_card
from scenes_ep03 import big_word, controller, quad_top
from scenes_ep04 import drone_boat, sea_line

ROAD = 640  # road level for side-view scenes


# ---------------- icons ----------------

def truck(cv, c, s=1.0, col=WHITE, w=5, roof=0.0, cabin_col=None):
    """Side view of a flatbed truck carrying a small wooden cabin, cab on the right.
    roof 0..1 lifts the cabin roof open."""
    x, y = c

    def P(dx, dy):
        return (x + dx * s, y + dy * s)

    cv.line([P(-300, -40), P(180, -40), P(180, -10), P(-300, -10), P(-300, -40)], w, col)  # flatbed
    cv.line([P(190, -10), P(190, -130), P(270, -130), P(310, -80), P(310, -10), P(190, -10)], w, col)  # cab
    cv.line([P(215, -115), P(265, -115), P(290, -82), P(215, -82), P(215, -115)], 3, col)
    for wx in (-220, -120, 250):
        cv.circle(P(wx, 5), 28 * s, w, col)
    cc = cabin_col or col
    cv.line([P(-280, -40), P(-280, -170), P(150, -170), P(150, -40)], w, cc)  # cabin walls
    for k in range(1, 4):
        cv.line([P(-280, -40 - k * 32), P(150, -40 - k * 32)], 2, DIM if cc == col else cc)
    cv.line([P(-80, -40), P(-80, -120), P(-20, -120), P(-20, -40)], 3, cc)  # door
    # roof: two panels hinged at the edges, swinging up
    a = roof * 1.15
    lx, rx, ry = -280, 150, -170
    mid = (lx + rx) / 2
    hl = (mid - lx) + 20
    cv.line([P(lx - 20, ry), P(lx - 20 + hl * math.cos(a), ry - 70 * (1 - roof) - hl * math.sin(a))], w, cc)
    cv.line([P(rx + 20, ry), P(rx + 20 - hl * math.cos(a), ry - 70 * (1 - roof) - hl * math.sin(a))], w, cc)


def bomber_top(cv, c, s=1.0, col=WHITE, w=4, a=0.0):
    """Top view of a swept-wing strategic bomber, nose pointing along angle a."""
    ca, sa = math.cos(a), math.sin(a)

    def P(dx, dy):
        return (c[0] + (dx * ca - dy * sa) * s, c[1] + (dx * sa + dy * ca) * s)

    cv.line([P(110, 0), P(-110, 0)], w + 1, col)
    cv.line([P(30, -8), P(-40, -120), P(-60, -120), P(-10, -8)], w, col)
    cv.line([P(30, 8), P(-40, 120), P(-60, 120), P(-10, 8)], w, col)
    cv.line([P(-90, -4), P(-115, -45), P(-122, -45), P(-110, -4)], w - 1, col)
    cv.line([P(-90, 4), P(-115, 45), P(-122, 45), P(-110, 4)], w - 1, col)


def bomber_side(cv, c, s=1.0, col=WHITE, w=4):
    x, y = c

    def P(dx, dy):
        return (x + dx * s, y + dy * s)

    cv.line([P(-200, 0), P(170, 0), P(210, -15), P(170, -30), P(-150, -30), P(-200, -110), P(-225, -110),
             P(-215, -30), P(-200, 0)], w, col)
    cv.line([P(-30, -12), P(-110, 30), P(-80, 30), P(40, -12)], w, col)


def phone(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.rect((x - 45 * s, y - 80 * s, x + 45 * s, y + 80 * s), w, col, radius=14)
    cv.line([(x - 15 * s, y + 62 * s), (x + 15 * s, y + 62 * s)], 3, col)


def cabin_house(cv, c, s=1.0, col=WHITE, w=5):
    x, y = c
    cv.line([(x - 120 * s, y), (x - 120 * s, y - 120 * s), (x, y - 190 * s), (x + 120 * s, y - 120 * s),
             (x + 120 * s, y), (x - 120 * s, y)], w, col)


# ---------------- map ----------------

RUSSIA = [(410, 470), (440, 310), (520, 150), (700, 125), (900, 170), (1100, 115), (1350, 95), (1600, 110),
          (1810, 200), (1840, 380), (1760, 520), (1650, 600), (1500, 645), (1300, 625), (1100, 605), (900, 590),
          (700, 615), (560, 625), (450, 570), (410, 470)]
UKRAINE = [(170, 560), (220, 495), (330, 475), (420, 500), (445, 570), (385, 635), (255, 640), (170, 560)]
UA = (300, 565)
BASES = {"OLENYA": (560, 190), "IVANOVO": (640, 390), "DYAGILEVO": (610, 445), "BELAYA": (1430, 560)}
UKRAINKA = (1700, 470)
CHEL = (960, 470)
ENGELS = (600, 520)
FAR_EAST = (1650, 420)


def russia_map(cv, s, alpha=1.0):
    backdrop(cv, s, "grid")
    cv.line(RUSSIA, 4, GREY)
    cv.line(UKRAINE, 4, WHITE)
    cv.text((300, 690), "UKRAINE", 26, WHITE)
    cv.text((1100, 300), "RUSSIA", 34, DIM)
    cv.text((1700, 760), "SCHEMATIC · NOT TO SCALE", 20, DIM)


def arc_pts(a, b, lift=160, n=30):
    mid = ((a[0] + b[0]) / 2, min(a[1], b[1]) - lift)
    return [lerp_pt(lerp_pt(a, mid, t / n), lerp_pt(mid, b, t / n), t / n) for t in range(n + 1)]


def base_mark(cv, p, name, col=ORANGE, s=0.0, pulse=True, below=False):
    cv.dot(p, 10, col)
    if pulse:
        cv.circle(p, 18 + 14 * ((s * 1.5) % 1), 3, col)
    cv.text((p[0], p[1] + (36 if below else -32)), name, 24, col)


# ---------------- cold open ----------------

def e5_truck(cv, s, T, ph=0):
    """ph0 truck drives in and stops, ph1 cabin highlighted, ph2 roof opens and drones rise."""
    backdrop(cv, s, "grid")
    cv.line([(0, ROAD + 34), (1920, ROAD + 34)], 3, GREY)
    for i in range(12):
        x = (i * 180 - s * (120 if ph == 0 and s < 2 else 0)) % 1920
        cv.line([(x, ROAD + 70), (x + 80, ROAD + 70)], 3, DIM)
    x = lerp(-400, CX, ease(clamp(s / 2.0))) if ph == 0 else CX
    roof = ease(seg(s, 0.4, 1.2)) if ph == 2 else 0.0
    truck(cv, (x, ROAD), 1.3, WHITE, 5, roof=roof, cabin_col=ORANGE if ph >= 1 else None)
    if ph == 1:
        cv.text((CX - 85, ROAD - 330), "A SMALL WOODEN CABIN?", 40, ORANGE, alpha=seg(s, 0.3, 0.4))
    if ph == 2:
        for i in range(9):
            t = seg(s, 1.2 + i * 0.12, 2.2)
            if t <= 0:
                continue
            sx = CX - 85 + (i - 4) * 46
            p = (sx + (i - 4) * 90 * t, ROAD - 230 - 420 * ease(t))
            quad_top(cv, p, 0.28, ORANGE, 3, spin=s * 30)


def e5_map(cv, s, T, ph=0):
    """ph0 distance to Belaya, ph1 all bases at once, ph2 out of reach, ph3 named bases,
    ph4 fifth base failed, ph5 bombers moved east, ph6 Engels 800 km."""
    russia_map(cv, s)
    if ph == 0:
        b = BASES["BELAYA"]
        p = seg(s, 0.3, 1.5)
        cv.dashed(arc_pts(UA, b, 200), 5, ORANGE, offset=s * 40, prog=p)
        base_mark(cv, b, "AIR BASE · SIBERIA", WHITE, s)
        cv.text((CX, 760), f"{int(4000 * p):,} KM+" if p >= 1 else f"{int(4000 * p):,} KM", 64, ORANGE,
                alpha=seg(s, 0.3, 0.3))
        return
    if ph == 2:
        r = 150 + 30 * ease(seg(s, 0, 1))
        cv.circle(UA, r, 3, ORANGE)
        cv.text((UA[0], UA[1] - r - 24), "WHAT UKRAINE COULD REACH", 24, ORANGE, alpha=seg(s, 0.3, 0.3))
        for k, (n, p) in enumerate(list(BASES.items())[:1] + [("BELAYA", BASES["BELAYA"])]):
            base_mark(cv, p, n, WHITE, s, pulse=False)
        cv.text((CX + 300, 760), "BASES FAR OUT OF REACH", 40, WHITE, alpha=seg(s, 0.6, 0.3))
        return
    if ph == 5:
        for i, (n, p) in enumerate(BASES.items()):
            cv.dashed(arc_pts(p, FAR_EAST, 120), 4, ORANGE, offset=s * 40, prog=seg(s, 0.3 + i * 0.2, 1.2))
        base_mark(cv, FAR_EAST, "FAR EAST", ORANGE, s)
        cv.text((CX, 760), "BOMBERS MOVED FARTHER EAST", 40, WHITE, alpha=seg(s, 0.8, 0.3))
        return
    if ph == 6:
        p = seg(s, 0.3, 1.2)
        cv.dashed(arc_pts(UA, ENGELS, 80), 5, ORANGE, offset=s * 40, prog=p)
        base_mark(cv, ENGELS, "ENGELS", WHITE, s, below=True)
        cv.text((CX, 760), "LONG-RANGE DRONES · ~800 KM · NOT TRUCKS", 40, ORANGE, alpha=seg(s, 0.8, 0.3))
        return
    # ph1, ph3, ph4: the bases
    for i, (n, p) in enumerate(BASES.items()):
        on = seg(s, 0.2 + (0 if ph == 1 else i * 0.25), 0.2)
        if on <= 0:
            continue
        base_mark(cv, p, n if ph >= 3 else "", ORANGE, s, below=n == "DYAGILEVO")
    if ph == 1:
        cv.text((CX, 760), "ALMOST AT THE SAME TIME", 40, WHITE, alpha=seg(s, 0.5, 0.3))
    if ph == 4:
        base_mark(cv, UKRAINKA, "UKRAINKA", GREY, s, pulse=False)
        cross(cv, UKRAINKA, 26, RED, 7, seg(s, 0.3, 0.4))
        cv.text((CX, 760), "5TH BASE · ATTACK FAILED", 40, RED, alpha=seg(s, 0.6, 0.3))


def e5_web(cv, s, T, ph=0):
    russia_map(cv, s)
    pts = list(BASES.values())
    for i, p in enumerate(pts):
        cv.dot(p, 9, ORANGE)
        for q in pts[i + 1:]:
            cv.line([p, q], 2, BG_O)
        cv.line([CHEL, p], 2, ORANGE, prog=seg(s, 0.2 + i * 0.15, 0.6))
    cv.text((CX, 760), "OPERATION SPIDERWEB", 64, ORANGE, alpha=seg(s, 0.4, 0.4))


def e5_intro(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    truck(cv, (CX + 40, CY + 60), 1.1, WHITE, 5, roof=0.6 + 0.1 * math.sin(s * 2), cabin_col=ORANGE)
    cv.text((CX, CY + 160), "HOW IT WAS PREPARED AND CARRIED OUT", 40, ORANGE, alpha=seg(s, 0.3, 0.4))
    cv.text((CX, CY + 220), "BASED ON PUBLISHED SOURCES", 28, WHITE, alpha=seg(s, 0.8, 0.4))


def e5_title(cv, s, T, ph=0):
    title_card(cv, s, "EP05  ·  OPERATION SPIDERWEB", "radar")


# ---------------- background ----------------

def e5_bomber_missile(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    bomber_side(cv, (1450, 300), 1.1, WHITE, 5)
    p = seg(s, 0.2, 1.4) * (0.62 if ph == 0 else 1.0)
    a, b = (1320, 330), (420, 560)
    m = lerp_pt(a, b, p)
    cv.dashed([a, m], 3, GREY, offset=s * 40)
    missile_icon(cv, m, 0.7, ORANGE, 4)
    cv.text((420, 650), "UKRAINIAN CITY", 28, WHITE)
    cv.line([(330, 610), (330, 560), (380, 560), (380, 520), (430, 520), (430, 600), (480, 600), (480, 610)], 4,
            WHITE)
    if ph == 0:
        cross(cv, m, 40, RED, 9, seg(s, 1.5, 0.4))
        cv.text((m[0], m[1] - 90), "SOME MISSILES STOPPED", 32, WHITE, alpha=seg(s, 1.5, 0.3))
    else:
        cv.circle((1450, 290), 170, 4, GREY)
        cv.text((1450, 520), "THE BOMBER: OUT OF REACH", 36, ORANGE, alpha=seg(s, 0.3, 0.3))


def e5_flip(cv, s, T, ph=0):
    """ph0 flying all the way fails, ph1 take off right next door."""
    russia_map(cv, s)
    b = BASES["BELAYA"]
    base_mark(cv, b, "BOMBERS", WHITE, s)
    if ph == 0:
        pts = arc_pts(UA, b, 200)
        cv.dashed(pts[:12], 4, ORANGE, offset=s * 40, prog=seg(s, 0.2, 1.0))
        cross(cv, pts[11], 26, RED, 7, seg(s, 1.2, 0.4))
        cv.text((CX, 760), "TOO FAR TO FLY", 44, WHITE, alpha=seg(s, 0.5, 0.3))
    else:
        start = (b[0] - 120, b[1] - 20)
        cv.dot(start, 10, ORANGE)
        cv.arrow(start, (b[0] - 18, b[1] - 6), 4, ORANGE, seg(s, 0.4, 0.6), 18)
        cv.text((CX, 760), "TAKE OFF RIGHT NEXT DOOR", 50, ORANGE, alpha=seg(s, 0.3, 0.3))


def e5_months(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i in range(18):
        x, y = CX - 540 + (i % 9) * 120, 360 + (i // 9) * 130
        on = seg(s, 0.1 + i * 0.06, 0.2)
        cv.rect((x, y, x + 90, y + 90), 3, ORANGE if on > 0.5 else DIM, radius=8)
    cv.text((CX, 230), "~18 MONTHS OF PREPARATION", 50, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, 720), "UKRAINIAN OFFICIALS", 28, GREY)


# ---------------- the Trojan horse ----------------

def e5_trojan(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    x0 = CX - 430
    cv.line([(x0 - 150, 560), (x0 - 150, 420), (x0 + 110, 420), (x0 + 110, 560)], 5, GREY)
    cv.line([(x0 + 110, 420), (x0 + 150, 330), (x0 + 200, 330), (x0 + 190, 380), (x0 + 120, 450)], 5, GREY)
    for lx in (x0 - 130, x0 - 70, x0 + 30, x0 + 90):
        cv.line([(lx, 560), (lx, 610)], 5, GREY)
    cv.text((x0, 690), "TROJAN HORSE", 34, GREY)
    cv.text((CX, 470), "=", 70, WHITE, alpha=seg(s, 0.4, 0.3))
    truck(cv, (CX + 470, 610), 0.9, WHITE, 5, cabin_col=ORANGE)
    cv.text((CX + 470, 690), "CARGO TRUCK", 34, ORANGE, alpha=seg(s, 0.6, 0.3))


def e5_range(cv, s, T, ph=0):
    """ph0 a small drone's reach, ph1 a truck's reach."""
    russia_map(cv, s)
    c = BASES["BELAYA"]
    if ph == 0:
        cv.circle(UA, 26 + 4 * math.sin(s * 3), 4, ORANGE)
        cv.text((UA[0] + 60, UA[1] - 60), "SMALL DRONE: TENS OF KM", 30, ORANGE, anchor="lm",
                alpha=seg(s, 0.3, 0.3))
        return
    cv.circle(UA, 26, 3, DIM)
    route = [UA, (520, 540), (760, 520), CHEL, (1150, 560), (1330, 590), (c[0] - 60, c[1] + 10)]
    cv.line(route, 6, WHITE, prog=seg(s, 0.2, 1.8))
    if s > 2.0:
        truck(cv, (c[0] - 60, c[1] - 20), 0.25, WHITE, 3, cabin_col=ORANGE)
        cv.circle((c[0] - 60, c[1] - 40), 40, 3, ORANGE)
    cv.text((CX, 760), "TRUCK: THOUSANDS OF KM", 44, WHITE, alpha=seg(s, 0.6, 0.3))


def e5_word(cv, s, T, ph=0):
    words = ["THE ROAD IS THE FUEL TANK", "SURPRISE WORKS ONLY ONCE"]
    big_word(cv, s, words[ph], ORANGE, 96)


def e5_source(cv, s, T, ph=0):
    """A 'according to' card: ph0 SBU chief Maliuk, ph1 Janes."""
    backdrop(cv, s, "grid")
    who, what = [("SBU CHIEF VASYL MALIUK", "HOW THE OPERATION WAS PREPARED"),
                 ("JANES · DEFENCE ANALYSTS", "WHAT THE RELEASED VIDEO SHOWS")][ph]
    cv.text((CX, CY - 120), "ACCORDING TO", 34, GREY, alpha=seg(s, 0, 0.3))
    cv.text((CX, CY - 30), who, 64, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.line([(CX - 420, CY + 30), (CX + 420, CY + 30)], 4, ORANGE, prog=seg(s, 0.3, 0.6))
    cv.text((CX, CY + 90), what, 36, ORANGE, alpha=seg(s, 0.6, 0.3))


def e5_chel(cv, s, T, ph=0):
    """ph0 office near the FSB in Chelyabinsk, ph1 the roof came off ~290 km out."""
    russia_map(cv, s)
    base_mark(cv, CHEL, "CHELYABINSK", ORANGE, s, below=True)
    if ph == 0:
        cv.rect((CHEL[0] + 40, CHEL[1] - 120, CHEL[0] + 120, CHEL[1] - 60), 4, ORANGE, radius=4)
        cv.text((CHEL[0] + 140, CHEL[1] - 90), "RENTED OFFICE + WAREHOUSE", 26, ORANGE, anchor="lm")
        cv.rect((CHEL[0] - 160, CHEL[1] - 130, CHEL[0] - 90, CHEL[1] - 70), 4, GREY, radius=4)
        cv.text((CHEL[0] - 180, CHEL[1] - 100), "FSB OFFICE NEARBY", 26, GREY, anchor="rm",
                alpha=seg(s, 0.6, 0.3))
        return
    p = seg(s, 0.2, 1.4)
    end = (CHEL[0] + 190, CHEL[1] + 50)
    cv.line([CHEL, lerp_pt(CHEL, end, p)], 6, WHITE)
    if p >= 1:
        cv.circle(end, 26, 4, RED)
        cv.text((end[0] + 40, end[1]), "~290 KM: A ROOF CAME OFF", 30, RED, anchor="lm")
    cv.text((CX, 760), "A CLOSE CALL", 44, WHITE, alpha=seg(s, 1.2, 0.3))


def e5_cabin(cv, s, T, ph=0):
    """Simple cross-section of the fake cabin: ph0 outline, ph1 hidden compartment, ph2 charging."""
    backdrop(cv, s, "grid")
    x0, x1, y0, y1 = CX - 420, CX + 420, 300, 700
    cv.line([(x0, y1), (x0, y0 + 80), (x1, y0 + 80), (x1, y1), (x0, y1)], 5, WHITE)
    cv.line([(x0 - 30, y0 + 80), (CX, y0), (x1 + 30, y0 + 80)], 5, WHITE)
    for k in range(1, 6):
        cv.line([(x0, y0 + 80 + k * 52), (x1, y0 + 80 + k * 52)], 2, DIM)
    cv.text((CX, 760), ["LOOKS LIKE A MOBILE WOODEN CABIN", "DRONES HIDDEN UNDER THE ROOF",
                        "BATTERIES + SOLAR PANELS KEPT THEM CHARGED"][ph], 36, ORANGE if ph else WHITE,
            alpha=seg(s, 0.3, 0.3))
    if ph >= 1:
        cv.rect((x0 + 20, y0 + 92, x1 - 20, y0 + 180), 4, ORANGE, fill=None, radius=4)
        for i in range(6):
            quad_top(cv, (x0 + 110 + i * 125, y0 + 136), 0.3, ORANGE, 3)
    if ph == 2:
        cv.rect((x0 + 60, y1 - 110, x0 + 220, y1 - 30), 4, WHITE, radius=6)
        cv.text((x0 + 140, y1 - 70), "BATTERY", 22, WHITE)
        for i in range(4):
            px = CX - 170 + i * 85
            cv.line([(px, y0 + 20 + i * 0), (px + 70, y0 + 20)], 4, WHITE)
        cv.text((CX, y0 - 30), "SOLAR PANELS", 22, WHITE)


def e5_driver(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.line([(0, ROAD + 34), (1920, ROAD + 34)], 3, GREY)
    truck(cv, (CX, ROAD), 1.2, WHITE, 5)
    cv.text((CX - 90, ROAD - 300), "?", 120, ORANGE, alpha=seg(s, 0.3, 0.3))
    cv.text((CX, 220), "THE DRIVERS DID NOT KNOW WHAT THEY CARRIED", 40, WHITE, alpha=seg(s, 0.5, 0.3))


def e5_count(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    n = int(117 * ease(seg(s, 0.1, 1.4)))
    for i in range(n):
        x, y = CX - 720 + (i % 30) * 50, 200 + (i // 30) * 60
        quad_top(cv, (x, y), 0.14, ORANGE, 2)
    cv.text((CX, 560), f"{n} DRONES", 90, WHITE)
    cv.text((CX, 650), "UKRAINIAN FIGURE · SBU CHIEF LATER SAID 150 WERE DELIVERED", 26, GREY,
            alpha=seg(s, 1.4, 0.3))


def e5_radar_road(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    radar_dish(cv, (CX - 520, 520), 1.3)
    for i in range(3):
        r = 120 + i * 90 + 40 * ((s * 0.8) % 1)
        cv.arc((CX - 520, 470), r, 220, 320, 3, GREY)
    cv.text((CX - 520, 650), "RADAR WATCHES THE SKY", 30, WHITE)
    cv.line([(CX - 60, 620), (1880, 620)], 3, GREY)
    for i in range(3):
        x = CX + 60 + ((i * 330 + s * 80) % 900)
        truck(cv, (x, 600), 0.42, DIM if i else ORANGE, 3)
    cv.text((CX + 460, 700), "NOBODY WATCHES EVERY TRUCK", 30, ORANGE, alpha=seg(s, 0.6, 0.3))


# ---------------- remote control ----------------

def e5_radio(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    controller(cv, (CX - 300, CY + 40), 1.0, WHITE, 5, s)
    r = 260
    cv.circle((CX - 300, CY + 40), r, 3, ORANGE)
    quad_top(cv, (CX - 300 + r * 0.6, CY - 120), 0.45, ORANGE, 3, spin=s * 30)
    cv.text((CX - 300, CY + 340), "RADIO: ONLY AS FAR AS THE SIGNAL REACHES", 32, WHITE, alpha=seg(s, 0.3, 0.3))
    cv.text((CX + 500, CY + 40), "THOUSANDS OF KM?", 44, ORANGE, alpha=seg(s, 0.8, 0.3))


def e5_software(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.rect((CX - 360, 240, CX + 360, 640), 5, WHITE, radius=12)
    cv.line([(CX - 420, 660), (CX + 420, 660)], 6, WHITE)
    route = [(CX - 280, 560), (CX - 160, 430), (CX + 20, 470), (CX + 180, 330), (CX + 280, 300)]
    cv.dashed(route, 3, GREY)
    p = seg(s, 0.3, 2.0)
    k = min(int(p * (len(route) - 1)), len(route) - 2)
    q = lerp_pt(route[k], route[k + 1], p * (len(route) - 1) - k)
    cv.dot(q, 10, ORANGE)
    cv.text((CX, 740), "ARDUPILOT · FREE, OPEN-SOURCE FLIGHT SOFTWARE", 36, ORANGE, alpha=seg(s, 0.4, 0.3))


def e5_signal(cv, s, T, ph=0):
    """ph0 over the map, ph1 the chain drone → tower → internet → pilot, ph2 delay."""
    if ph == 0:
        russia_map(cv, s)
        d = BASES["BELAYA"]
        quad_top(cv, (d[0] - 60, d[1] - 50), 0.3, ORANGE, 3, spin=s * 30)
        tower_icon(cv, (d[0] - 160, d[1] - 10), 0.5, WHITE, 3)
        pts = arc_pts((d[0] - 160, d[1] - 40), UA, 220)
        cv.dashed(pts, 4, ORANGE, offset=-s * 50, prog=seg(s, 0.3, 1.4))
        cv.text((CX, 760), "OVER RUSSIA'S OWN MOBILE NETWORKS", 40, WHITE, alpha=seg(s, 0.6, 0.3))
        return
    backdrop(cv, s, "grid")
    xs = [CX - 640, CX - 220, CX + 220, CX + 640]
    y = CY
    quad_top(cv, (xs[0], y), 0.6, ORANGE, 4, spin=s * 30)
    tower_icon(cv, (xs[1], y + 40), 1.0, WHITE, 4)
    for dx, dy, r in ((-40, 10, 50), (20, -20, 60), (70, 15, 45)):
        cv.circle((xs[2] + dx, y + dy), r, 4, WHITE)
    stick = (xs[3], y)
    cv.rect((stick[0] - 80, y - 50, stick[0] + 80, y + 50), 4, WHITE, radius=8)
    labels = ["DRONE", "CELL TOWER", "INTERNET", "PILOT"]
    for x, lab in zip(xs, labels):
        cv.text((x, y + 150), lab, 30, WHITE)
    for i in range(3):
        cv.arrow((xs[i] + 110, y), (xs[i + 1] - 110, y), 4, ORANGE, seg(s, 0.2 + i * 0.3, 0.4), 18)
    if ph == 2:
        clock_icon(cv, (CX, y - 330), 60, (s * 0.4) % 1)
        cv.text((CX, y - 230), "LONGER PATH = COMMANDS ARRIVE LATER", 34, ORANGE, alpha=seg(s, 0.3, 0.3))


def e5_radio_phone(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    controller(cv, (CX - 400, CY), 0.9, GREY, 4, s)
    cv.text((CX - 400, CY + 140), "WALKIE-TALKIE", 34, GREY)
    cross(cv, (CX - 400, CY), 90, RED, 8, seg(s, 0.4, 0.4))
    phone(cv, (CX + 400, CY), 1.3, ORANGE, 5)
    cv.text((CX + 400, CY + 160), "PHONE CALL", 34, ORANGE, alpha=seg(s, 0.6, 0.3))


def e5_autopilot(cv, s, T, ph=0):
    """ph0 software keeps balance and route, ph1 the human picks where and what."""
    backdrop(cv, s, "grid")
    route = [(260, 600), (620, 470), (980, 520), (1340, 380), (1660, 330)]
    cv.dashed(route, 4, GREY, offset=s * 30)
    p = clamp(s / max(T, 1))
    k = min(int(p * (len(route) - 1)), len(route) - 2)
    q = lerp_pt(route[k], route[k + 1], p * (len(route) - 1) - k)
    quad_top(cv, (q[0], q[1] + 8 * math.sin(s * 6)), 0.45, ORANGE, 3, spin=s * 30)
    cv.text((CX, 220), "SOFTWARE: BALANCE + ROUTE", 40, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph == 1:
        cv.circle(route[-1], 50, 4, ORANGE)
        cv.text((CX, 760), "HUMAN: WHERE TO GO, WHAT TO HIT", 44, ORANGE, alpha=seg(s, 0.2, 0.3))


def e5_ingredients(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    items = ["TRUCK", "WOODEN CABIN", "PHONE NETWORK", "FREE SOFTWARE", "SMALL DRONES"]
    if ph == 0:
        cv.text((CX, CY), "WORTH NOTICING", 70, WHITE, alpha=seg(s, 0.1, 0.3))
        return
    for i, it in enumerate(items):
        x = CX - 680 + i * 340
        a = seg(s, i * 0.25, 0.3) if ph == 1 else 1.0
        cv.rect((x - 150, 360, x + 150, 470), 4, WHITE if ph < 3 else ORANGE, radius=10)
        cv.text((x, 415), it, 28, WHITE, alpha=a)
    if ph == 2:
        cv.text((CX, 620), "NONE OF IT A SECRET WEAPON", 56, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph == 3:
        for i in range(4):
            x = CX - 680 + i * 340
            cv.line([(x + 150, 415), (x + 190, 415)], 5, ORANGE, prog=seg(s, 0.1 + i * 0.15, 0.3))
        cv.text((CX, 620), "WHAT WAS NEW: HOW THEY WERE COMBINED", 50, ORANGE, alpha=seg(s, 0.6, 0.3))


# ---------------- all at once ----------------

def e5_surprise(cv, s, T, ph=0):
    """ph0 one base hit, alarm spreads; ph1 all hit before the alarm spreads."""
    russia_map(cv, s)
    pts = list(BASES.values())
    if ph == 0:
        first = pts[0]
        cross(cv, first, 22, RED, 6)
        r = 60 + 700 * seg(s, 0.3, 2.5)
        cv.circle(first, r, 3, RED)
        for p in pts[1:]:
            if math.dist(first, p) < r:
                cv.circle(p, 22, 4, WHITE)
                cv.text((p[0], p[1] - 34), "ALERT", 22, WHITE)
        cv.text((CX, 760), "ONE HIT → EVERY BASE ON ALERT", 40, WHITE, alpha=seg(s, 0.4, 0.3))
    else:
        for p in pts:
            cross(cv, p, 22, ORANGE, 6, seg(s, 0.3, 0.3))
        cv.text((CX, 760), "STRIKE EVERYWHERE BEFORE THE ALARM SPREADS", 40, ORANGE, alpha=seg(s, 0.6, 0.3))


def e5_carrier(cv, s, T, ph=0):
    """ph0 EP4's drone boat, ph1 the truck, ph2 big carrier = distance, small drone = precision."""
    backdrop(cv, s, "grid")
    if ph == 0:
        sea_line(cv, s, ROAD)
        drone_boat(cv, (CX, ROAD), 2.2, WHITE, 5, wake=0.6)
        quad_top(cv, (CX + 40, ROAD - 210 - 20 * math.sin(s * 2)), 0.4, ORANGE, 3, spin=s * 30)
        cv.text((CX, 220), "EP04: A BOAT CARRYING A DRONE", 40, WHITE, alpha=seg(s, 0.2, 0.3))
        return
    cv.line([(0, ROAD + 34), (1920, ROAD + 34)], 3, GREY)
    truck(cv, (CX - 200, ROAD), 1.2, WHITE, 5, roof=1.0, cabin_col=ORANGE)
    for i in range(4):
        quad_top(cv, (CX - 300 + i * 120 + 60 * seg(s, 0.3, 1.5) * i, ROAD - 320 - 40 * (i % 2)), 0.3, ORANGE, 3,
                 spin=s * 30)
    if ph == 1:
        cv.text((CX, 170), "THIS TIME: A TRUCK", 44, ORANGE, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX - 520, 170), "BIG CARRIER = DISTANCE", 40, WHITE, alpha=seg(s, 0.2, 0.3))
        cv.text((CX + 420, 170), "SMALL DRONE = PRECISION", 40, ORANGE, alpha=seg(s, 0.6, 0.3))


# ---------------- results ----------------

def e5_claim(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 300), "41 AIRCRAFT HIT", 80, WHITE, alpha=seg(s, 0.1, 0.3))
    cv.text((CX, 380), "INCLUDING BOMBERS AND EARLY-WARNING PLANES", 30, GREY)
    if ph >= 1:
        cv.text((CX, 520), "~$7 BILLION IN DAMAGE", 64, ORANGE, alpha=seg(s, 0.2 if ph == 1 else 0, 0.3))
    if ph == 2:
        cv.tag((CX, 660), "UKRAINIAN CLAIMS", 40, RED, alpha=seg(s, 0.2, 0.3))


def e5_compare(cv, s, T, ph=0):
    """Claim vs independent assessments (aircraft destroyed / hit)."""
    backdrop(cv, s, "grid")
    rows = [("UKRAINE (CLAIM): HIT", 41, RED, "41"),
            ("THE INSIDER: DESTROYED, SATELLITE-CONFIRMED", 15, ORANGE, "15"),
            ("US OFFICIALS: DESTROYED / DAMAGED", 10, WHITE, "~10 / UP TO 20")]
    for i, (lab, v, col, txt) in enumerate(rows[:2 + ph]):
        y = 250 + i * 170
        p = seg(s, 0.2 + (i - (1 + ph if ph else 0)) * 0.1 if i > ph else 0, 0.8) if i > ph else 1.0
        cv.text((CX - 700, y - 50), lab, 28, col, anchor="lm")
        w = 1300 * v / 41
        cv.rect((CX - 700, y - 22, CX - 700 + w * p, y + 22), 0, fill=col, radius=6)
        if i == 2 and p > 0.5:
            cv.rect((CX - 700 + w, y - 22, CX - 700 + w * 2 * p, y + 22), 3, col, radius=6)
        cv.text((CX - 700 + (w * 2 if i == 2 else w) * p + 24, y), txt, 32, col, anchor="lm")


def e5_no_new(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    rows = [("TU-95", "NO LONGER BUILT"), ("TU-22M3", "NO LONGER BUILT"), ("TU-160", "ONLY A FEW BUILT")]
    for i, (n, st) in enumerate(rows[:2 + ph]):
        y = 300 + i * 150
        bomber_side(cv, (CX - 450, y + 30), 0.55, WHITE, 3)
        cv.text((CX - 150, y), n, 44, WHITE, anchor="lm")
        cv.text((CX + 200, y), st, 36, ORANGE if i < 2 else WHITE, anchor="lm", alpha=seg(s, 0.2 + i * 0.2, 0.3))
    if ph == 1:
        cv.text((CX, 760), "HARD TO REPLACE", 50, ORANGE, alpha=seg(s, 0.8, 0.3))


def e5_scale(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for i in range(3):
        quad_top(cv, (CX - 520 + i * 90, CY + 40), 0.25, ORANGE, 3, spin=s * 30)
    cv.text((CX - 430, CY + 160), "A FEW SMALL DRONES", 32, ORANGE)
    cv.text((CX, CY + 40), "VS", 50, GREY)
    bomber_top(cv, (CX + 430, CY + 40), 1.6, WHITE, 5, a=-math.pi / 2)
    cv.text((CX + 430, CY + 260), "IRREPLACEABLE BOMBER", 32, WHITE)


def e5_front_rear(cv, s, T, ph=0):
    """ph0 front vs safe rear, ph1 the rear disappears."""
    backdrop(cv, s, "grid")
    cv.rect((160, 240, 760, 700), 4, RED, radius=12)
    cv.text((460, 470), "FRONT", 60, RED)
    cv.text((460, 540), "DANGEROUS", 30, RED)
    a = 1.0 - (seg(s, 0.4, 1.2) if ph == 1 else 0.0)
    cv.rect((860, 240, 1760, 700), 4, WHITE if a > 0.2 else DIM, radius=12)
    cv.text((1310, 470), "REAR", 60, WHITE if a > 0.2 else DIM)
    cv.text((1310, 540), "SAFE", 30, WHITE if a > 0.2 else DIM)
    if ph == 1:
        cross(cv, (1310, 500), 120, ORANGE, 10, seg(s, 0.8, 0.4))
        cv.text((CX, 790), "NO SAFE REAR FOR PARKED AIRCRAFT", 44, ORANGE, alpha=seg(s, 1.0, 0.3))


# ---------------- 2026 ----------------

def e5_shelters(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    n = int(17 * ease(seg(s, 0.1, 1.5)))
    for i in range(n):
        x, y = CX - 720 + (i % 9) * 180, 320 + (i // 9) * 200
        cv.arc((x + 70, y + 90), 70, 180, 360, 4, ORANGE)
        cv.line([(x, y + 90), (x + 140, y + 90)], 3, ORANGE)
    cv.text((CX, 220), "ENGELS · AT LEAST 17 SHELTERS UNDER CONSTRUCTION", 40, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, 760), "SATELLITE IMAGE · JUNE 2026", 28, GREY)


# ---------------- limits & defenses ----------------

def e5_limits(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 260), "LIMITS", 70, ORANGE, alpha=seg(s, 0, 0.3))
    cv.text((CX, 420), "IT DEPENDED ALMOST ENTIRELY ON SURPRISE", 40, WHITE, alpha=seg(s, 0.3, 0.3))
    if ph == 1:
        cv.text((CX, 540), "ONCE SEEN, HARD TO REPEAT", 48, ORANGE, alpha=seg(s, 0.2, 0.3))


def e5_blackout(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    phone(cv, (CX - 400, CY), 1.6, WHITE, 5)
    for i in range(4):
        h = 20 + i * 18
        cv.rect((CX - 450 + i * 28, CY + 20 - h, CX - 432 + i * 28, CY + 20), 0, fill=DIM, radius=2)
    cross(cv, (CX - 400, CY - 40), 50, RED, 8, seg(s, 0.3, 0.4))
    cv.text((CX + 300, CY - 60), "MOBILE INTERNET CUT", 48, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX + 300, CY + 20), "IN MANY REGIONS SINCE MAY 2025", 32, GREY, alpha=seg(s, 0.4, 0.3))
    cv.text((CX + 300, CY + 100), "OFFICIAL REASON: STOP DRONES", 32, ORANGE, alpha=seg(s, 0.8, 0.3))


def e5_defense(cv, s, T, ph=0):
    """ph0 a strong roof, ph1 cheaper: nets and dispersal."""
    backdrop(cv, s, "grid")
    cards = [("STRONG ROOF", "HARDENED SHELTER"), ("NETS", "COVER THE PLANE"), ("DISPERSAL", "SPREAD ACROSS BASES")]
    for i, (a, b) in enumerate(cards[:1 if ph == 0 else 3]):
        x = CX - 560 + i * 560 if ph else CX
        on = seg(s, 0.1 + (i - 1) * 0.3, 0.3) if ph and i else 1.0
        col = ORANGE if i == 0 else WHITE
        cv.rect((x - 230, 300, x + 230, 620), 4, col, radius=12)
        if i == 0:
            cv.arc((x, 540), 140, 180, 360, 6, col)
            bomber_top(cv, (x, 520), 0.5, WHITE, 3, a=-math.pi / 2)
        elif i == 1:
            bomber_top(cv, (x, 470), 0.6, WHITE, 3, a=-math.pi / 2)
            for k in range(-3, 4):
                cv.line([(x + k * 40, 380), (x + k * 40 + 60, 560)], 2, GREY)
        else:
            for k, (dx, dy) in enumerate(((-120, -60), (100, -30), (-40, 70))):
                cv.dot((x + dx, 470 + dy), 10, WHITE)
        cv.text((x, 660), a, 36, col, alpha=on)
        cv.text((x, 705), b, 24, GREY, alpha=on)


def e5_cost_compare(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.arc((CX - 420, 560), 200, 180, 360, 7, WHITE)
    cv.line([(CX - 640, 560), (CX - 200, 560)], 5, WHITE)
    cv.text((CX - 420, 640), "CONCRETE SHELTER", 34, WHITE)
    cv.text((CX, 470), "VS", 50, GREY)
    truck(cv, (CX + 430, 560), 0.8, ORANGE, 4, roof=0.5, cabin_col=ORANGE)
    cv.text((CX + 430, 640), "ONE TRUCK OF CHEAP DRONES", 34, ORANGE)


# ---------------- outro ----------------

def e5_recap(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    truck(cv, (CX - 380, 560), 0.9, WHITE, 4, roof=1.0, cabin_col=ORANGE)
    cv.text((CX - 380, 640), "BIG CARRIER", 34, WHITE)
    cv.arrow((CX - 60, 470), (CX + 140, 470), 5, ORANGE, seg(s, 0.3, 0.5), 22)
    quad_top(cv, (CX + 400, 470), 0.7, ORANGE, 4, spin=s * 30)
    cv.text((CX + 400, 640), "SMALL DRONES, BROUGHT CLOSE", 34, ORANGE)


def e5_both_ways(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX - 520, CY - 40), "UKRAINE", 50, WHITE)
    cv.text((CX + 520, CY - 40), "RUSSIA", 50, RED)
    cv.arrow((CX - 300, CY - 60), (CX + 300, CY - 60), 5, ORANGE, seg(s, 0.2, 0.5), 22)
    cv.arrow((CX + 300, CY + 40), (CX - 300, CY + 40), 5, RED, seg(s, 0.8, 0.5), 22)
    cv.text((CX, CY + 180), "DRONES FLY BOTH WAYS", 44, WHITE, alpha=seg(s, 1.0, 0.3))


def e5_geran(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    x, y = CX, CY - 20
    sc = 2.2
    cv.line([(x + 140 * sc, y), (x - 90 * sc, y - 120 * sc), (x - 110 * sc, y - 120 * sc), (x - 70 * sc, y),
             (x - 110 * sc, y + 120 * sc), (x - 90 * sc, y + 120 * sc), (x + 140 * sc, y)], 5, RED)
    cv.line([(x + 140 * sc, y), (x - 100 * sc, y)], 5, RED)
    cv.circle((x - 110 * sc, y), 22, 3, GREY)
    cv.text((CX, 760), "GERAN · IRANIAN DESIGN, MASS-PRODUCED IN RUSSIA", 40, RED, alpha=seg(s, 0.3, 0.3))


def e5_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP06  ·  GUARDING THE NIGHT SKY", "radar")


SCENES = {k: v for k, v in globals().items() if k.startswith("e5_") and callable(v)}
