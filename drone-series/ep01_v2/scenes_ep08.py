"""EP08 line-art scenes ("The Robot Guns of Kyiv"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math

from gfx import DIM, GREY, ORANGE, RED, WHITE, check, clamp, cross, ease, lerp, radar_dish, seg
from scenes import BG, CX, CY, backdrop, end_card, title_card
from scenes_ep06 import geran, pickup, shield, ukraine_map
from scenes_ep07 import burst, interceptor, jet_geran


# ---------------- icons ----------------

def turret(cv, c, s=1.0, col=WHITE, w=5, a=-0.7):
    """Side view of a gun turret: base, rotating head with a camera box, barrel at angle a."""
    x, y = c
    cv.rect((x - 90 * s, y - 20 * s, x + 90 * s, y + 20 * s), w, col, radius=6)
    cv.line([(x, y - 20 * s), (x, y - 70 * s)], w, col)
    hx, hy = x, y - 100 * s
    cv.rect((hx - 60 * s, hy - 32 * s, hx + 60 * s, hy + 32 * s), w, col, radius=10)
    ca, sa = math.cos(a), math.sin(a)
    cv.line([(hx + 40 * s * ca, hy + 40 * s * sa), (hx + 230 * s * ca, hy + 230 * s * sa)], w + 3, col)
    px, py = -sa, ca
    bx, by = hx + 30 * px * s, hy + 30 * py * s
    cv.rect((bx - 26 * s, by - 18 * s, bx + 26 * s, by + 18 * s), 3, ORANGE, radius=4)


def mic_pole(cv, c, s=1.0, col=WHITE, w=4):
    x, y = c
    cv.line([(x, y), (x, y - 260 * s)], w, col)
    cv.rect((x - 30 * s, y - 300 * s, x + 30 * s, y - 250 * s), w, col, radius=6)
    cv.line([(x + 30 * s, y - 275 * s), (x + 70 * s, y - 295 * s), (x + 70 * s, y - 255 * s),
             (x + 30 * s, y - 275 * s)], w - 1, ORANGE)


def waves(cv, c, r0, n, col, w=3, a0=-40, a1=40, phase=0.0, step=40):
    for k in range(n):
        r = r0 + ((k * step + phase) % (n * step))
        cv.arc(c, r, a0, a1, w, col)


def ear(cv, c, s=1.0, col=WHITE, w=6):
    x, y = c
    cv.arc((x, y - 30 * s), 90 * s, 180, 360, w, col)
    cv.line([(x + 90 * s, y - 30 * s), (x + 80 * s, y + 40 * s), (x + 20 * s, y + 110 * s), (x - 20 * s, y + 120 * s)],
            w, col)
    cv.arc((x, y - 20 * s), 40 * s, 200, 360, w - 2, col)


# ---------------- cold open ----------------

def e8_turret_scan(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    a = -1.2 + 0.6 * math.sin(s * 0.9)
    turret(cv, (CX, 760), 1.6, WHITE, 6, a=a)
    cv.text((CX, 170), "NO HAND ON THE GUN · IT SCANS ON ITS OWN", 42, ORANGE, alpha=seg(s, 0.3, 0.3))


def e8_quote(cv, s, T, ph=0):
    """ph0 robot turrets down Geran-5, ph1 'I was a big skeptic', ph2 AI removes human error."""
    backdrop(cv, s, "grid")
    if ph == 0:
        cv.text((CX, 330), "ROBOT TURRETS", 90, WHITE)
        cv.text((CX, 450), "SHOOT DOWN JET DRONE GERAN-5", 50, ORANGE, alpha=seg(s, 0.3, 0.3))
        cv.text((CX, 560), "UKRAINE AIR FORCE · OCT 5, 2026", 32, GREY)
    elif ph == 1:
        cv.text((CX, 380), "“I WAS A BIG SKEPTIC MYSELF”", 70, WHITE, alpha=seg(s, 0.1, 0.4))
        cv.text((CX, 500), "— YURII IHNAT, AIR FORCE SPOKESMAN", 36, GREY, alpha=seg(s, 0.5, 0.3))
    else:
        cv.text((CX, 380), "“AI REMOVES HUMAN ERROR”", 70, ORANGE, alpha=seg(s, 0.1, 0.4))
        cv.text((CX, 500), "SO EVEN JET DRONES CAN BE HIT — IHNAT", 36, WHITE, alpha=seg(s, 0.5, 0.3))


def e8_intro(cv, s, T, ph=0):
    backdrop(cv, s, "radar")
    for i, lab in enumerate(("SOUND", "RADIO", "AI GUNS")):
        x = CX - 520 + i * 520
        cv.text((x, CY), lab, 64, ORANGE if i == 2 else WHITE, alpha=seg(s, 0.2 + i * 0.4, 0.3))
    cv.text((CX, 760), "THE INVISIBLE NET OVER KYIV", 44, GREY, alpha=seg(s, 1.4, 0.3))


def e8_title(cv, s, T, ph=0):
    title_card(cv, s, "EP08  ·  THE ROBOT GUNS OF KYIV", "radar")


# ---------------- why machines ----------------

def e8_mps(cv, s, T, ph=0):
    """ph0 ~500 km/h, ph1 almost 140 m every second."""
    backdrop(cv, s, "grid")
    cv.text((CX, 260), "~500 KM/H", 110, RED)
    if ph >= 1:
        x0, x1, y = 360, 1560, 560
        cv.line([(x0, y), (x1, y)], 3, GREY)
        p = (s % 1.0)
        jet_geran(cv, (lerp(x0, x1, p), y - 70), 0.35, RED, 3)
        for k in range(0, 141, 20):
            x = x0 + (x1 - x0) * k / 140
            cv.line([(x, y - 10), (x, y + 10)], 3, GREY)
        cv.text((CX, y + 70), "≈ 140 M EVERY SECOND", 54, WHITE, alpha=seg(s, 0.2, 0.3))


def e8_body(cv, s, T, ph=0):
    """ph0 the three parts, ph1 listen · mislead · shoot, ph2 ears, ph3 shield, ph4 hands."""
    backdrop(cv, s, "grid")
    items = [("EARS", "LISTEN"), ("SHIELD", "MISLEAD"), ("HANDS", "SHOOT")]
    hi = {2: 0, 3: 1, 4: 2}.get(ph, -1)
    for i, (lab, verb) in enumerate(items):
        x = CX - 560 + i * 560
        col = ORANGE if i == hi else (WHITE if hi < 0 else DIM)
        al = seg(s, 0.1 + i * 0.3, 0.3) if ph == 0 else 1.0
        if al <= 0:
            continue
        if i == 0:
            ear(cv, (x, CY - 60), 1.3, col, 6)
        elif i == 1:
            shield(cv, (x, CY - 60), 0.8, col, 6)
        else:
            turret(cv, (x - 40, CY + 60), 1.0, col, 5)
        cv.text((x, CY + 200), lab, 50, col)
        if ph >= 1:
            cv.text((x, CY + 270), verb, 32, col if i == hi else GREY)


def e8_mapnet(cv, s, T, ph=0):
    """ph0 Sky Fortress: microphones on poles across Ukraine, ph1 10,000+ sensors."""
    ukraine_map(cv, s)
    import random
    rnd = random.Random(8)
    n = int((60 if ph == 0 else 260) * ease(seg(s, 0.1, 1.5)))
    for k in range(n):
        x, y = rnd.uniform(380, 1500), rnd.uniform(300, 620)
        cv.dot((x, y), 5, ORANGE)
    cv.text((CX, 140), "SKY FORTRESS · ACOUSTIC NETWORK", 46, WHITE)
    if ph >= 1:
        cv.text((CX, 840), "10,000+ SENSORS ACROSS UKRAINE (REPORTED)", 44, ORANGE, alpha=seg(s, 0.6, 0.3))


def e8_radar_miss(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    gy = 780
    cv.line([(120, gy), (1800, gy)], 3, GREY)
    radar_dish(cv, (300, gy - 40), 1.0, WHITE, 4)
    cv.line([(330, gy - 120), (1800, gy - 520)], 3, ORANGE)
    cv.line([(330, gy - 120), (1800, gy - 260)], 3, ORANGE)
    p = (s * 0.25) % 1
    geran(cv, (lerp(1750, 500, p), gy - 70), 0.35, RED, 3, a=math.pi)
    cv.text((CX, 170), "SMALL DRONES FLYING LOW SLIP UNDER RADAR", 42, WHITE, alpha=seg(s, 0.3, 0.3))


def e8_sound(cv, s, T, ph=0):
    """ph0 a propeller drone makes a moped-like buzz, ph1 the pole hears it and AI says 'drone'."""
    backdrop(cv, s, "grid")
    d = (560, 380)
    geran(cv, d, 0.7, RED, 4, a=math.pi)
    waves(cv, d, 120, 5, RED, 3, -60, 60, phase=(s * 120) % 200, step=40)
    waves(cv, d, 120, 5, RED, 3, 120, 240, phase=(s * 120) % 200, step=40)
    cv.text((560, 640), "“BZZZZ” · LIKE A MOTORBIKE", 40, RED, alpha=seg(s, 0.2, 0.3))
    if ph >= 1:
        mic_pole(cv, (1300, 820), 1.4, WHITE, 5)
        cv.rect((1460, 340, 1780, 470), 4, ORANGE, radius=12)
        cv.text((1620, 380), "AI", 40, ORANGE)
        cv.text((1620, 435), "DRONE ✓", 36, WHITE, alpha=seg(s, 0.8, 0.3))


def e8_tdoa(cv, s, T, ph=0):
    """Several poles hear the same sound at different times → position and heading."""
    backdrop(cv, s, "grid")
    poles = [(520, 760), (1000, 820), (1440, 740)]
    d = (980, 360)
    for k, p in enumerate(poles):
        mic_pole(cv, p, 0.7, WHITE, 3)
        top = (p[0], p[1] - 200)
        dist = math.dist(top, d)
        r = dist * clamp(ease(seg(s, 0.1 + k * 0.3, 1.0)), 0, 1)
        cv.circle(top, r, 2, GREY)
    geran(cv, d, 0.5, RED, 4, a=math.pi)
    if seg(s, 1.4, 0.3) > 0:
        cv.circle(d, 70, 4, ORANGE)
    cv.text((CX, 140), "ARRIVAL-TIME DIFFERENCES → POSITION + DIRECTION", 40, WHITE)


def e8_cost(cv, s, T, ph=0):
    """ph0 the price, ph1 $400–500 per sensor, ph2 whole network < two Patriot missiles."""
    backdrop(cv, s, "grid")
    cv.text((CX, 180), "THE PRICE", 64, WHITE)
    if ph >= 1:
        mic_pole(cv, (520, 800), 1.3, WHITE, 5)
        cv.text((520, 860), "$400–500 PER SENSOR", 40, ORANGE, alpha=seg(s, 0.2, 0.3) if ph == 1 else 1.0)
    if ph >= 2:
        cv.text((1300, 460), "WHOLE NETWORK", 44, WHITE)
        cv.text((1300, 540), "<", 80, ORANGE)
        cv.text((1300, 640), "2 PATRIOT MISSILES", 48, RED, alpha=seg(s, 0.3, 0.3))


def e8_84(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 150), "ONE ATTACK: 84 DRONES", 48, WHITE)
    for k in range(84):
        x, y = 420 + (k % 14) * 80, 300 + (k // 14) * 80
        down = k < 80 and seg(s, 0.2 + k * 0.015, 0.2) > 0.5
        cv.dot((x, y), 14, GREY if down else RED)
        if down:
            cross(cv, (x, y), 14, ORANGE, 4)
    cv.text((CX, 840), "80 SHOT DOWN · NETWORK PLAYED A BIG ROLE", 42, ORANGE, alpha=seg(s, 1.6, 0.3))


def e8_interest(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.tag((CX, 380), "USA: WANTS TO TEST IT", 50, WHITE, alpha=seg(s, 0.1, 0.3))
    cv.tag((CX, 540), "NATO GENERAL: INVEST IN CHEAP ACOUSTIC SENSORS", 44, ORANGE, alpha=seg(s, 0.6, 0.3))


def e8_soundlag(cv, s, T, ph=0):
    """ph0 sound ~340 m/s, ph1 by the time you hear a jet drone it is already further on."""
    backdrop(cv, s, "grid")
    mic_pole(cv, (300, 820), 1.0, WHITE, 4)
    cv.text((CX, 160), "SOUND ≈ 340 M/S   ·   JET DRONE ≈ 140 M/S", 44, WHITE)
    src = (900, 360)
    p = clamp(seg(s, 0.2, 2.0), 0, 1)
    cv.circle(src, 40 + 620 * p, 3, GREY)
    if ph == 0:
        geran(cv, src, 0.5, RED, 4, a=math.pi)
        return
    jet_geran(cv, (src[0] - 420 * p, src[1] + 80 * p), 0.4, RED, 3, a=math.pi * 0.95)
    cv.dot(src, 10, GREY)
    cv.text((src[0], src[1] - 70), "HEARD HERE", 30, GREY)
    cv.text((CX, 820), "WHEN THE SOUND ARRIVES, THE DRONE IS FURTHER ON", 40, ORANGE, alpha=seg(s, 1.4, 0.3))


def e8_fusion(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    mic_pole(cv, (420, 640), 0.9, WHITE, 4)
    cv.text((420, 700), "SOUND", 36, WHITE)
    radar_dish(cv, (420, 860), 0.8, WHITE, 4)
    cv.text((420, 950), "RADAR", 36, WHITE)
    cv.arrow((560, 500), (1040, 600), 5, ORANGE, seg(s, 0.2, 0.4), 22)
    cv.arrow((560, 860), (1040, 680), 5, ORANGE, seg(s, 0.4, 0.4), 22)
    cv.rect((1080, 460, 1640, 820), 5, ORANGE, radius=16)
    cv.text((1360, 640), "ONE AIR PICTURE", 44, ORANGE, alpha=seg(s, 0.8, 0.3))


# ---------------- radio ----------------

def e8_radio(cv, s, T, ph=0):
    """ph0 a drone must emit radio, ph1 mesh modems, ph2 controlled from hundreds of km, ph3 the beacon."""
    backdrop(cv, s, "grid")
    d = (CX, 380)
    geran(cv, d, 0.6, RED, 4, a=math.pi)
    waves(cv, d, 110, 4, ORANGE if ph >= 3 else GREY, 3, 0, 360, phase=(s * 100) % 160, step=40)
    if ph == 0:
        cv.text((CX, 760), "REMOTE CONTROL OR DATA = RADIO SIGNALS", 44, WHITE, alpha=seg(s, 0.3, 0.3))
    if ph >= 1:
        cv.tag((CX, 640), "MESH MODEM", 44, WHITE)
    if ph == 1:
        cv.text((CX, 760), "STEADILY FITTED SINCE NOV 2025 (UKRAINIAN MILITARY)", 34, GREY, alpha=seg(s, 0.3, 0.3))
    if ph == 2:
        cv.text((CX, 760), "OPERATORS HUNDREDS OF KM AWAY", 44, RED, alpha=seg(s, 0.3, 0.3))
    if ph >= 3:
        cv.text((CX, 760), "STRONG SIGNAL = A BEACON THAT GIVES IT AWAY", 44, ORANGE, alpha=seg(s, 0.3, 0.3))


# ---------------- the shield ----------------

def _sats(cv, col=WHITE):
    for x in (520, 960, 1400):
        cv.rect((x - 30, 130, x + 30, 170), 3, col, radius=4)
        cv.line([(x - 80, 150), (x - 30, 150)], 3, col)
        cv.line([(x + 30, 150), (x + 80, 150)], 3, col)


def e8_gnss(cv, s, T, ph=0):
    """ph0 satellites guide the drone, ph1 jamming = noise, ph2 keeps flying on inertia,
    ph3 spoofing: fake position, wrong turn, ph4 leaves the zone and corrects."""
    backdrop(cv, s, "grid")
    _sats(cv, GREY if ph in (1, 3) else WHITE)
    tgt = (1650, 720)
    cv.circle(tgt, 40, 4, WHITE)
    cv.text((tgt[0], tgt[1] + 70), "TARGET", 28, WHITE)
    start = (250, 520)
    p = clamp((s * 0.3) % 1.2, 0, 1)
    if ph in (0, 1, 2):
        pos = (lerp(start[0], tgt[0], p), lerp(start[1], tgt[1], p))
        geran(cv, pos, 0.35, RED, 3, a=math.atan2(tgt[1] - start[1], tgt[0] - start[0]))
        if ph == 0:
            for x in (520, 960, 1400):
                cv.line([(x, 175), pos], 1, DIM)
            cv.text((CX, 900), "SATELLITE SIGNALS TELL IT WHERE IT IS", 40, WHITE, alpha=seg(s, 0.3, 0.3))
        if ph == 1:
            for k in range(14):
                x = 700 + (k * 97 + s * 300) % 520
                y = 300 + (k * 53) % 200
                cv.line([(x, y), (x + 20, y - 18), (x + 40, y)], 3, ORANGE)
            cv.text((CX, 900), "JAMMING: DROWN THE SIGNAL IN NOISE", 40, ORANGE, alpha=seg(s, 0.3, 0.3))
        if ph == 2:
            cv.text((CX, 900), "BUT IT KEEPS FLYING ON INERTIAL NAVIGATION", 40, RED, alpha=seg(s, 0.3, 0.3))
        return
    if ph == 3:
        mid = (900, 600)
        if p < 0.5:
            q = p / 0.5
            pos = (lerp(start[0], mid[0], q), lerp(start[1], mid[1], q))
            a = math.atan2(mid[1] - start[1], mid[0] - start[0])
        else:
            q = (p - 0.5) / 0.5
            end = (1300, 260)
            pos = (lerp(mid[0], end[0], q), lerp(mid[1], end[1], q))
            a = math.atan2(end[1] - mid[1], end[0] - mid[0])
        geran(cv, pos, 0.35, RED, 3, a=a)
        cv.circle((1100, 880), 26, 3, ORANGE)
        cv.text((1100, 820), "“YOU ARE HERE” (FAKE)", 30, ORANGE)
        cv.text((CX, 960), "SPOOFING: FAKE SATELLITE SIGNALS", 40, ORANGE, alpha=seg(s, 0.3, 0.3))
        return
    cv.rect((600, 260, 1100, 840), 3, ORANGE, radius=20)
    cv.text((850, 230), "SPOOFING ZONE", 28, ORANGE)
    mid = (1150, 380)
    if p < 0.6:
        q = p / 0.6
        pos = (lerp(start[0], mid[0], q), lerp(start[1], mid[1], q))
        a = math.atan2(mid[1] - start[1], mid[0] - start[0])
    else:
        q = (p - 0.6) / 0.4
        pos = (lerp(mid[0], tgt[0], q), lerp(mid[1], tgt[1], q))
        a = math.atan2(tgt[1] - mid[1], tgt[0] - mid[0])
    geran(cv, pos, 0.35, RED, 3, a=a)
    cv.text((CX, 960), "OUT OF THE ZONE · REAL SIGNAL · COURSE CORRECTED", 38, RED, alpha=seg(s, 0.3, 0.3))


def e8_pokrova(cv, s, T, ph=0):
    """ph0 the name, ph1 Air Force confirmed use in 2024, ph2 effect not independently verified."""
    backdrop(cv, s, "grid")
    shield(cv, (CX, 420), 1.0, ORANGE, 6)
    cv.text((CX, 720), "POKROVA", 80, WHITE)
    cv.text((CX, 800), "UKRAINIAN ELECTRONIC WARFARE · SPOOFING", 32, GREY)
    if ph == 1:
        cv.tag((CX, 900), "IN USE · CONFIRMED BY AIR FORCE, 2024", 36, ORANGE, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        cv.tag((CX, 900), "HOW WELL IT WORKS · NOT INDEPENDENTLY VERIFIED", 36, RED, alpha=seg(s, 0.2, 0.3))


def e8_lemonde(cv, s, T, ph=0):
    """ph0 Nov 2024: 95 of 188 lost their way, ph1 Nov 24–26: 43 towards Belarus."""
    backdrop(cv, s, "grid")
    if ph == 0:
        cv.text((CX, 170), "ONE ATTACK · NOVEMBER 2024", 44, WHITE)
        for k in range(188):
            x, y = 330 + (k % 24) * 54, 280 + (k // 24) * 64
            lost = k < 95 and seg(s, 0.2 + k * 0.008, 0.2) > 0.5
            cv.dot((x, y), 10, ORANGE if lost else RED)
        cv.text((CX, 860), "95 OF 188 LOST THEIR WAY", 54, ORANGE, alpha=seg(s, 1.0, 0.3))
        return
    ukraine_map(cv, s)
    cv.text((700, 200), "BELARUS", 36, GREY)
    for k in range(43):
        p = clamp(seg(s, 0.1 + k * 0.03, 1.2), 0, 1)
        sx, sy = 1300 + (k % 7) * 30, 520 + (k // 7) * 20
        cv.dot((lerp(sx, 650 + (k % 9) * 20, p), lerp(sy, 230 + (k // 9) * 12, p)), 6, ORANGE)
    cv.text((CX, 860), "NOV 24–26: 43 FLEW TOWARDS BELARUS", 48, ORANGE, alpha=seg(s, 0.8, 0.3))


# ---------------- the hands ----------------

def e8_turret_spec(cv, s, T, ph=0):
    """ph0 Sky Sentinel unveiled May 2025, ph1 12.7 mm heavy machine gun, 360°."""
    backdrop(cv, s, "grid")
    a = -0.9 + 0.5 * math.sin(s * 0.8)
    turret(cv, (560, 820), 2.0, WHITE, 6, a=a)
    cv.text((1250, 380), "SKY SENTINEL", 70, ORANGE)
    cv.text((1250, 460), "UKRAINIAN AI TURRET · UNVEILED MAY 2025", 32, WHITE)
    if ph >= 1:
        cv.tag((1250, 600), "12.7 MM HEAVY MACHINE GUN", 38, WHITE, alpha=seg(s, 0.2, 0.3))
        cv.tag((1250, 700), "TURNS 360°", 38, WHITE, alpha=seg(s, 0.5, 0.3))
        cv.arc((560, 620), 230, 200, 340 + 20 * math.sin(s), 3, ORANGE)


def e8_chain(cv, s, T, ph=0):
    """ph0 how it works, ph1 radar says roughly where, ph2 camera locks on, AI computes speed, direction, wind."""
    backdrop(cv, s, "grid")
    steps = [("RADAR", "ROUGHLY WHERE"), ("CAMERA", "LOCKS ON"), ("AI", "SPEED · DIRECTION · WIND"), ("GUN", "AIMS AHEAD")]
    show = {0: 4, 1: 1, 2: 3}[ph]
    for i, (lab, sub) in enumerate(steps):
        x = 300 + i * 440
        on = i < show
        col = ORANGE if (on and ph > 0 and i == show - 1) else (WHITE if on else DIM)
        cv.rect((x - 170, 380, x + 170, 560), 5, col, radius=16)
        cv.text((x, 450), lab, 50, col)
        cv.text((x, 610), sub, 26, col if on else DIM)
        if i < 3:
            cv.arrow((x + 180, 470), (x + 260, 470), 4, col if on else DIM, 1.0, 16)
    cv.text((CX, 200), "HOW IT WORKS", 56, WHITE)


def e8_lead(cv, s, T, ph=0):
    """ph0 aim where the drone will be, ph1 a short burst ahead builds a cloud of fragments."""
    backdrop(cv, s, "grid")
    t0 = (300, 860)
    turret(cv, t0, 1.0, WHITE, 5, a=-0.55)
    meet = (1150, 360)
    p = clamp((s * 0.35) % 1.3, 0, 1)
    jx = lerp(1850, meet[0] - 300, p)
    jet_geran(cv, (jx, meet[1]), 0.35, RED, 3, a=math.pi)
    cv.circle(meet, 30, 3, ORANGE)
    cv.line([(t0[0] + 190, t0[1] - 200), meet], 2, DIM)
    if ph == 0:
        cv.text((CX, 140), "AIM WHERE IT WILL BE, NOT WHERE IT IS", 44, ORANGE, alpha=seg(s, 0.2, 0.3))
        return
    import random
    rnd = random.Random(3)
    q = clamp(seg(s, 0.3, 0.8), 0, 1)
    for k in range(40):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(10, 120) * q
        cv.dot((meet[0] + r * math.cos(a), meet[1] + r * math.sin(a)), 4, ORANGE)
    if abs(jx - meet[0]) < 80:
        burst(cv, meet, 100)
    cv.text((CX, 140), "A SHORT BURST AHEAD · A CLOUD OF FRAGMENTS", 44, ORANGE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, 960), "ONE EXPERT'S EXPLANATION", 28, GREY)


def e8_six(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 200), "FIRST: PROPELLER SHAHEDS", 48, WHITE)
    for k in range(6):
        x = 460 + k * 200
        geran(cv, (x, 500), 0.4, RED, 3, a=math.pi)
        if seg(s, 0.2 + k * 0.25, 0.2) > 0.5:
            cross(cv, (x, 500), 60, ORANGE, 6)
    cv.text((CX, 760), "6 ENGAGEMENTS · 6 SHAHEDS DOWN (UNIT COMMANDER)", 40, ORANGE, alpha=seg(s, 1.6, 0.3))


def _kyiv(cv, s):
    backdrop(cv, s, "grid")
    river = [(1000, 160), (960, 330), (900, 470), (920, 620), (880, 780), (900, 940)]
    cv.line(river, 10, DIM)
    cv.circle((940, 540), 300, 3, GREY)
    cv.text((940, 210), "KYIV · SCHEMATIC", 26, GREY)


def e8_kyivmap(cv, s, T, ph=0):
    """ph0 12+ turrets in Kyiv, 8 more around it; ph1 10–30 per city."""
    _kyiv(cv, s)
    pts = [(780, 420), (860, 360), (1010, 400), (1080, 480), (1100, 600), (1020, 700), (900, 720), (790, 640),
           (740, 540), (960, 470), (900, 600), (1010, 560)]
    for k, p in enumerate(pts):
        if seg(s, 0.1 + k * 0.08, 0.2) > 0.5:
            cv.dot(p, 12, ORANGE)
    if ph == 0:
        ring = [(940 + 420 * math.cos(a), 540 + 360 * math.sin(a)) for a in [k * math.pi / 4 + 0.3 for k in range(8)]]
        for k, p in enumerate(ring):
            if seg(s, 1.2 + k * 0.1, 0.2) > 0.5:
                cv.circle(p, 12, 3, WHITE)
        cv.text((1550, 400), "12+ IN KYIV", 46, ORANGE, anchor="lm" if False else "mm")
        cv.text((1550, 480), "+8 AROUND IT", 40, WHITE, alpha=seg(s, 1.2, 0.3))
        cv.text((1550, 560), "OCT 4, 2026", 30, GREY)
    else:
        cv.text((1550, 460), "10–30 TURRETS", 50, ORANGE)
        cv.text((1550, 540), "PER CITY (DEVELOPERS)", 32, WHITE, alpha=seg(s, 0.3, 0.3))


def e8_price(cv, s, T, ph=0):
    """ph0 the price, ph1 ~$150,000 turret vs jet Geran (estimate), ph2 reusable vs one-shot missile."""
    backdrop(cv, s, "grid")
    turret(cv, (520, 640), 1.3, WHITE, 5)
    cv.text((520, 760), "TURRET", 40, WHITE)
    if ph == 0:
        cv.text((CX + 300, CY), "THE PRICE?", 70, WHITE, alpha=seg(s, 0.2, 0.3))
        return
    cv.text((520, 830), "~$150,000", 52, ORANGE)
    jet_geran(cv, (1350, 460), 0.8, RED, 4, a=math.pi)
    cv.text((1350, 760), "JET GERAN", 40, RED)
    cv.text((1350, 830), "~$100,000–200,000 (EST.)", 40, RED)
    if ph >= 2:
        cv.tag((CX, 180), "A TURRET FIRES AGAIN AND AGAIN · A MISSILE IS GONE AFTER ONE SHOT", 34, WHITE,
               alpha=seg(s, 0.2, 0.3))


def e8_claim(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 360), "KILL RECORDS", 70, WHITE)
    cv.tag((CX, 500), "UKRAINIAN CLAIMS · NOT INDEPENDENTLY VERIFIED", 36, RED, alpha=seg(s, 0.2, 0.3))


def e8_range(cv, s, T, ph=0):
    """ph0 reach just over 1 km, ph1 it can only guard what is right next to it."""
    backdrop(cv, s, "grid")
    c = (CX, 700)
    turret(cv, (c[0] - 20, c[1] + 60), 0.7, WHITE, 4)
    r = 300 * ease(seg(s, 0.1, 0.8))
    cv.arc(c, r, 180, 360, 5, ORANGE)
    cv.text((c[0] + 300, c[1] + 40), "~1 KM+", 40, ORANGE, anchor="lm")
    if ph >= 1:
        cv.rect((c[0] + 60, c[1] - 30, c[0] + 260, c[1] + 40), 4, WHITE, radius=4)
        cv.text((c[0] + 160, c[1] + 80), "BRIDGE", 28, WHITE)
        p = (s * 0.3) % 1
        jet_geran(cv, (lerp(1850, 70, p), 200), 0.3, RED, 3, a=math.pi)
        cv.text((CX, 120), "DISTANT DRONES ARE OUT OF REACH", 42, RED, alpha=seg(s, 0.3, 0.3))


def e8_layers(cv, s, T, ph=0):
    """ph0 not a cure-all, one layer of many; ph1 far: jets + missiles, middle: interceptors, last km: turrets."""
    backdrop(cv, s, "grid")
    c = (CX - 600, CY + 60)
    rings = [(460, "FAR: FIGHTERS + MISSILES", WHITE), (320, "MIDDLE: INTERCEPTOR DRONES", WHITE),
             (170, "LAST KM: AI TURRETS", ORANGE)]
    cv.rect((c[0] - 50, c[1] - 35, c[0] + 50, c[1] + 35), 4, WHITE, radius=6)
    for k, (r, lab, col) in enumerate(rings):
        if ph == 0 and k < 2:
            col = DIM
        al = seg(s, 0.1 + k * 0.4, 0.3) if ph == 1 else 1.0
        cv.arc(c, r, -55, 55, 5, col)
        ly = c[1] - r * 0.819
        cv.line([(c[0] + r * 0.574, ly), (c[0] + 520, ly)], 2, col if col != DIM else DIM)
        cv.text((c[0] + 540, ly), lab, 30, col, anchor="lm", alpha=al)
    if ph == 0:
        cv.text((CX + 350, CY + 260), "NOT A CURE-ALL · ONE LAYER OF MANY", 38, ORANGE, alpha=seg(s, 0.3, 0.3))


# ---------------- outro ----------------

def e8_recap(cv, s, T, ph=0):
    """ph0 the whole chain, ph1 ears + radio, ph2 shield + hands."""
    backdrop(cv, s, "radar")
    labs = [("EARS", "MICROPHONES"), ("RADIO", "SIGNAL HUNTERS"), ("SHIELD", "FAKE SATELLITE SIGNALS"),
            ("HANDS", "AI TURRETS")]
    for i, (lab, sub) in enumerate(labs):
        y = 260 + i * 150
        on = ph == 0 or (ph == 1 and i < 2) or (ph == 2 and i >= 2)
        col = ORANGE if on and ph > 0 else (WHITE if on else DIM)
        cv.rect((CX - 420, y - 55, CX + 420, y + 55), 4, col, radius=12)
        cv.text((CX - 250, y), lab, 44, col)
        cv.text((CX + 150, y), sub, 30, col)
    if ph == 0:
        cv.text((CX, 900), "CHEAP · MADE IN UKRAINE · FAST TO CHANGE", 40, ORANGE, alpha=seg(s, 0.6, 0.3))


def e8_endcard(cv, s, T, ph=0):
    end_card(cv, s, "NEXT  ·  EP09  ·  SURVIVING THE KILL ZONE", "radar")


SCENES = {k: v for k, v in globals().items() if k.startswith("e8_") and callable(v)}
