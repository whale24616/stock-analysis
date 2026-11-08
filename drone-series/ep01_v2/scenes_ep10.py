"""EP10 line-art scenes ("The Shield Ukraine Exports"). Same signature as scenes.py: fn(cv, s, T, ph)."""
import math

from gfx import DIM, GREY, ORANGE, RED, WHITE, check, clamp, cross, ease, lerp, seg
from scenes import BG, CX, CY, backdrop, end_card, title_card
from scenes_ep03 import quad_top
from scenes_ep06 import geran, photo_card, shield, spear
from scenes_ep07 import interceptor
from scenes_ep08 import mic_pole, turret
from scenes_ep09 import netting, person, ugv


# ---------------- maps ----------------

ME = {"JORDAN": (520, 380), "SAUDI ARABIA": (820, 600), "KUWAIT": (900, 380), "QATAR": (1180, 560),
      "UAE": (1320, 650)}
IRAN = (1220, 300)
UA = (420, 120)


def _me_map(cv, s):
    backdrop(cv, s, "grid")
    gulf = [(980, 420), (1080, 470), (1180, 520), (1260, 560), (1380, 590), (1430, 640)]
    cv.line(gulf, 30, (40, 48, 60))
    cv.text((1260, 470), "GULF", 22, DIM)
    cv.text((CX, 860), "MIDDLE EAST · SCHEMATIC", 22, DIM)


def e10_base(cv, s, T, ph=0):
    """ph0 a US base in the Jordanian desert, ph1 Iranian Shaheds attack US bases."""
    backdrop(cv, s, "grid")
    gy = 700
    for k in range(9):
        x = 160 + k * 200
        cv.arc((x, gy + 120), 160, 200, 340, 2, DIM)
    cv.line([(100, gy), (1820, gy)], 3, GREY)
    cv.rect((760, gy - 120, 1160, gy), 4, WHITE, radius=6)
    cv.rect((820, gy - 200, 900, gy - 120), 4, WHITE, radius=4)
    cv.line([(1100, gy - 120), (1100, gy - 230)], 3, WHITE)
    cv.text((960, gy + 50), "US BASE · JORDAN", 34, WHITE)
    if ph >= 1:
        p = (s * 0.25) % 1
        for k in range(3):
            q = (p + k * 0.3) % 1
            geran(cv, (lerp(1850, 1000, q), lerp(160 + k * 60, 420, q)), 0.3, RED, 3, a=math.pi + 0.3)
        cv.text((CX, 140), "2026: IRANIAN SHAHEDS ATTACK US BASES", 42, RED, alpha=seg(s, 0.2, 0.3))
    else:
        cv.text((CX, 140), "MARCH 2026 · A US BASE IN THE DESERT", 42, WHITE, alpha=seg(s, 0.2, 0.3))


def e10_dates(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    x0, x1, y = 400, 1520, 500
    cv.line([(x0, y), (x1, y)], 4, GREY)
    for k, (x, d, lab, col) in enumerate(((x0 + 100, "MAR 5", "US REQUEST", WHITE), (x1 - 100, "MAR 9", "UKRAINIAN TEAM LEAVES", ORANGE))):
        a = seg(s, 0.2 + k * 0.6, 0.3)
        cv.circle((x, y), 16, 0, fill=col)
        cv.text((x, y - 60), d, 44, col, alpha=a)
        cv.text((x, y + 60), lab, 30, col, alpha=a)
    cv.arrow((x1 - 60, y + 130), (x1 + 200, y + 130), 4, ORANGE, seg(s, 1.0, 0.5), 20)
    cv.text((x1 + 70, y + 180), "TO JORDAN", 28, ORANGE)


def e10_intro(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    shield(cv, (CX, CY - 60), 1.0, ORANGE, 6)
    for k in range(6):
        a = s * 0.6 + k * math.pi / 3
        cv.arrow((CX + 200 * math.cos(a), CY - 60 + 200 * math.sin(a)),
                 (CX + 330 * math.cos(a), CY - 60 + 330 * math.sin(a)), 3, GREY, 1.0, 14)
    cv.text((CX, 830), "A SHIELD BUILT IN WAR · NOW SPREADING WORLDWIDE", 40, WHITE, alpha=seg(s, 0.4, 0.3))


def e10_title(cv, s, T, ph=0):
    title_card(cv, s, "EP10  ·  THE SHIELD UKRAINE EXPORTS", "grid")


# ---------------- the math ----------------

def e10_cost(cv, s, T, ph=0):
    """ph0 a Shahed $20k–50k, ph1 one PAC-3 $3.8M, ph2 the more you stop, the more you lose,
    ph3 Ukraine's interceptor $1k–2k."""
    backdrop(cv, s, "grid")
    rows = [("SHAHED", 50_000, "$20,000–50,000", RED), ("PATRIOT PAC-3", 3_800_000, "~$3.8 MILLION", WHITE),
            ("UKRAINIAN INTERCEPTOR", 2_000, "$1,000–2,000", ORANGE)]
    show = {0: [0], 1: [0, 1], 2: [0, 1], 3: [0, 1, 2]}[ph]
    for i in show:
        lab, v, txt, col = rows[i]
        y = 300 + i * 170
        new = (ph == 0 and i == 0) or (ph == 1 and i == 1) or (ph == 3 and i == 2)
        p = ease(seg(s, 0.1, 1.0)) if new else 1.0
        w = max(8, 1200 * math.log10(v / 1000) / math.log10(3800)) * p
        cv.text((300, y - 50), lab, 32, col, anchor="lm")
        cv.rect((300, y - 20, 300 + w, y + 20), 0, fill=col, radius=6)
        cv.text((300 + w + 24, y), txt, 34, col, anchor="lm", alpha=seg(s, 0.6, 0.3) if new else 1)
    cv.text((CX, 140), "PRICE PER UNIT (LOG SCALE)", 30, GREY)
    if ph == 2:
        cv.text((CX, 760), "THE MORE YOU STOP, THE MORE YOU LOSE", 48, RED, alpha=seg(s, 0.2, 0.3))


def e10_axios(cv, s, T, ph=0):
    """ph0 last year: offer turned down, ph1 after Shahed attacks: a change of mind."""
    backdrop(cv, s, "grid")
    cv.text((CX - 420, 300), "LAST YEAR", 40, GREY)
    cv.text((CX - 420, 380), "UKRAINE'S OFFER", 36, WHITE)
    cross(cv, (CX - 420, 520), 80, RED, 10, seg(s, 0.2, 0.4))
    if ph >= 1:
        cv.arrow((CX - 200, 450), (CX + 200, 450), 5, ORANGE, seg(s, 0.1, 0.4), 22)
        cv.text((CX + 420, 300), "AFTER SHAHED ATTACKS", 36, ORANGE)
        check(cv, (CX + 420, 520), 80, ORANGE, 10, seg(s, 0.4, 0.4))
    cv.text((CX, 820), "ACCORDING TO AXIOS", 30, GREY)


# ---------------- the Gulf ----------------

def e10_gulf(cv, s, T, ph=0):
    """ph0 201 specialists (Mar 17), ph1 228 ten days later, ph2 the five countries."""
    _me_map(cv, s)
    for k, (name, p) in enumerate(ME.items()):
        al = seg(s, 0.1 + k * 0.2, 0.3) if ph == 2 else 1.0
        cv.circle(p, 14, 0, fill=ORANGE)
        if ph == 2:
            cv.text((p[0], p[1] + 40), name, 28, WHITE, alpha=al)
        cv.line([UA, p], 1, DIM)
    cv.circle(UA, 18, 0, fill=WHITE)
    cv.text((UA[0] + 30, UA[1]), "UKRAINE", 30, WHITE, anchor="lm")
    if ph == 0:
        cv.text((1500, 200), "201", 120, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.text((1500, 300), "SPECIALISTS · MAR 17", 32, WHITE)
    if ph == 1:
        cv.text((1500, 200), "228", 120, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.text((1500, 300), "TEN DAYS LATER", 32, WHITE)


def e10_deals(cv, s, T, ph=0):
    """ph0 Mar 26, Jeddah: first security pact with a Gulf state; ph1 ten-year pacts with UAE and Qatar."""
    backdrop(cv, s, "grid")
    cv.rect((CX - 360, 260, CX + 360, 520), 5, ORANGE, radius=16)
    cv.text((CX, 330), "UKRAINE  ×  SAUDI ARABIA", 46, WHITE)
    cv.text((CX, 410), "MAR 26 · JEDDAH", 34, ORANGE)
    cv.text((CX, 470), "FIRST SECURITY PACT WITH A GULF STATE", 28, WHITE)
    if ph >= 1:
        for k, lab in enumerate(("UAE · 10 YEARS", "QATAR · 10 YEARS")):
            x = CX - 330 + k * 660
            cv.rect((x - 260, 600, x + 260, 720), 4, WHITE, radius=12)
            cv.text((x, 660), lab, 36, WHITE, alpha=seg(s, 0.2 + k * 0.3, 0.3))


def e10_trade(cv, s, T, ph=0):
    """ph0 Ukraine shares its air-defence know-how, ph1 receives oil, diesel and interceptor missiles."""
    backdrop(cv, s, "grid")
    cv.rect((180, 340, 680, 600), 5, WHITE, radius=16)
    cv.text((430, 470), "UKRAINE", 54, WHITE)
    cv.rect((1240, 340, 1740, 600), 5, WHITE, radius=16)
    cv.text((1490, 470), "GULF STATES", 50, WHITE)
    labs = ["SEA DRONES", "ELECTRONIC WARFARE", "INTERCEPTION TECH"]
    for k, lab in enumerate(labs):
        cv.text((960, 230 + k * 50), lab, 30, ORANGE, alpha=seg(s, 0.1 + k * 0.2, 0.3))
    cv.arrow((700, 420), (1220, 420), 5, ORANGE, seg(s, 0.1, 0.5), 22)
    if ph >= 1:
        cv.arrow((1220, 540), (700, 540), 5, WHITE, seg(s, 0.1, 0.5), 22)
        for k, lab in enumerate(("CRUDE OIL", "DIESEL", "INTERCEPTOR MISSILES")):
            cv.text((960, 640 + k * 50), lab, 30, WHITE, alpha=seg(s, 0.3 + k * 0.2, 0.3))


def e10_turn(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX - 380, 420), "RECEIVING HELP", 50, GREY)
    cv.arrow((CX - 80, 420), (CX + 80, 420), 6, ORANGE, seg(s, 0.3, 0.4), 24)
    cv.text((CX + 380, 420), "SHARING KNOW-HOW", 50, ORANGE, alpha=seg(s, 0.6, 0.3))
    cv.text((CX, 560), "11 COUNTRIES INTERESTED · JOINT PRODUCTION DISCUSSED", 34, WHITE, alpha=seg(s, 1.0, 0.3))


# ---------------- Sky Map ----------------

def e10_skymap(cv, s, T, ph=0):
    """ph0 Reuters: Sky Map at Prince Sultan Air Base, ph1 finds drones and sends interceptors,
    ph2 Ukrainians train US troops, ph3 no comment · still a trial."""
    backdrop(cv, s, "grid")
    box = (260, 220, 1000, 700)
    cv.rect(box, 5, ORANGE, radius=14)
    cv.text((630, 190), "SKY MAP · COMMAND SOFTWARE", 30, ORANGE)
    for r in (80, 160, 240):
        cv.circle((630, 460), r, 2, DIM)
    p = (s * 0.3) % 1
    d = (lerp(960, 700, p), lerp(260, 430, p))
    geran(cv, d, 0.38, RED, 3, a=math.pi * 0.8)
    if ph >= 1:
        cv.rect((d[0] - 30, d[1] - 30, d[0] + 30, d[1] + 30), 2, RED, radius=2)
        i = (lerp(400, d[0] - 40, p), lerp(640, d[1] + 20, p))
        interceptor(cv, i, 0.55, ORANGE, 3, a=math.atan2(d[1] - i[1], d[0] - i[0]))
    cv.text((1430, 300), "PRINCE SULTAN", 40, WHITE)
    cv.text((1430, 350), "AIR BASE · SAUDI ARABIA", 30, GREY)
    if ph == 0:
        cv.text((1430, 450), "INSTALLED BY THE US MILITARY", 32, ORANGE, alpha=seg(s, 0.2, 0.3))
        cv.text((1430, 500), "REUTERS · APRIL 2026", 28, GREY)
    if ph == 1:
        cv.text((1430, 450), "FINDS DRONES", 34, WHITE, alpha=seg(s, 0.1, 0.3))
        cv.text((1430, 500), "SENDS INTERCEPTORS", 34, ORANGE, alpha=seg(s, 0.4, 0.3))
    if ph == 2:
        for k in range(3):
            person(cv, (1300 + k * 90, 560), 0.9, ORANGE if k == 0 else WHITE, 3)
        cv.text((1430, 660), "UKRAINIANS TRAIN US TROOPS", 32, ORANGE, alpha=seg(s, 0.2, 0.3))
    if ph == 3:
        cv.tag((1430, 480), "NO COMMENT · STILL A TRIAL?", 32, RED, alpha=seg(s, 0.2, 0.3))


# ---------------- Europe ----------------

def e10_europe(cv, s, T, ph=0):
    """ph0 Lithuania tests Sky Fortress (Oct 2), ph1 sound + radio signals + AI, ph2 adopt rather than build."""
    backdrop(cv, s, "grid")
    lt, ua = (760, 260), (1060, 640)
    cv.circle(ua, 18, 0, fill=WHITE)
    cv.text((ua[0] + 34, ua[1]), "UKRAINE", 32, WHITE, anchor="lm")
    cv.circle(lt, 18, 0, fill=ORANGE)
    cv.text((lt[0] - 34, lt[1]), "LITHUANIA", 32, ORANGE, anchor="rm")
    cv.arrow((ua[0] - 20, ua[1] - 30), (lt[0] + 20, lt[1] + 30), 4, ORANGE, seg(s, 0.2, 0.5), 20)
    mic_pole(cv, (1400, 640), 1.0, WHITE, 4)
    if ph == 0:
        cv.text((CX, 140), "OCT 2, 2026 · LITHUANIA STARTS TESTING SKY FORTRESS", 40, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph == 1:
        cv.text((CX, 140), "LOW-FLYING DRONES & CRUISE MISSILES · SOUND + RADIO SIGNALS + AI", 34, WHITE, alpha=seg(s, 0.2, 0.3))
    if ph == 2:
        cv.text((CX, 140), "WHY BUILD FROM SCRATCH? ADOPT A WAR-PROVEN SYSTEM", 40, ORANGE, alpha=seg(s, 0.2, 0.3))


def e10_germany(cv, s, T, ph=0):
    """ph0 Germany pays, Ukraine builds; ph1 15,000 STRILA (Mar 2026), ph2 Quantum Systems + WIY Drones,
    ph3 just over $2,000 each, ph4 biggest plant outside Germany is in Ukraine, ph5 tens of thousands more (Oct)."""
    backdrop(cv, s, "grid")
    cv.rect((180, 300, 640, 520), 5, WHITE, radius=16)
    cv.text((410, 410), "GERMANY", 52, WHITE)
    cv.rect((1280, 300, 1740, 520), 5, ORANGE, radius=16)
    cv.text((1510, 410), "UKRAINE", 52, ORANGE)
    cv.arrow((660, 410), (1260, 410), 5, WHITE, seg(s, 0.1, 0.5), 22)
    cv.text((960, 370), "€ FUNDING", 32, WHITE)
    texts = {0: ("PAYS FOR DRONES MADE IN UKRAINE", WHITE), 1: ("15,000 STRILA INTERCEPTORS · MARCH 2026", ORANGE),
             2: ("QUANTUM SYSTEMS (DE) + WIY DRONES (UA)", WHITE), 3: ("JUST OVER $2,000 EACH (REPORTED)", ORANGE),
             4: ("QUANTUM SYSTEMS' BIGGEST PLANT ABROAD: IN UKRAINE · ~1,000 STAFF", WHITE),
             5: ("OCT: TENS OF THOUSANDS MORE · MERZ", ORANGE)}
    txt, col = texts[ph]
    cv.text((CX, 680), txt, 40 if ph != 4 else 32, col, alpha=seg(s, 0.2, 0.3))
    if ph in (1, 3, 5):
        for k in range(24 if ph != 5 else 32):
            x = 360 + (k % 16) * 70
            y = 750 + (k // 16) * 34
            if seg(s, 0.3 + k * 0.01, 0.2) > 0.5:
                cv.dot((x, y), 8, ORANGE)


def e10_offices(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for k in range(10):
        x = 330 + (k % 5) * 315
        y = 380 + (k // 5) * 200
        a = seg(s, 0.1 + k * 0.1, 0.2)
        if a > 0:
            cv.rect((x - 110, y - 70, x + 110, y + 70), 4, ORANGE, radius=10)
            cv.text((x, y), "EXPORT", 28, WHITE)
    cv.text((CX, 170), "PLAN: 10 ARMS-EXPORT OFFICES IN EUROPE BY END-2026", 40, WHITE)


# ---------------- the dilemma ----------------

def e10_ban(cv, s, T, ph=0):
    """ph0 2022: exports banned, ph1 Feb 2026: licensed export of surplus only, proceeds buy interceptors."""
    backdrop(cv, s, "grid")
    cv.rect((CX - 220, 280, CX + 220, 520), 6, RED if ph == 0 else GREY, radius=16)
    cv.text((CX, 380), "ARMS EXPORTS", 44, WHITE)
    cv.text((CX, 450), "BANNED SINCE 2022", 34, RED)
    if ph == 0:
        cross(cv, (CX, 400), 160, RED, 8, seg(s, 0.2, 0.4))
        cv.text((CX, 680), "EVERY WEAPON COUNTS IN A WAR", 44, WHITE, alpha=seg(s, 0.5, 0.3))
        return
    cv.arrow((CX + 240, 400), (CX + 430, 400), 5, ORANGE, seg(s, 0.1, 0.4), 20)
    cv.text((CX + 620, 360), "FEB 2026 PLAN", 32, ORANGE)
    cv.text((CX + 620, 410), "SURPLUS ONLY", 30, WHITE)
    cv.text((CX + 620, 450), "APPROVED COUNTRIES", 30, WHITE)
    cv.text((CX, 680), "PROCEEDS → BUY INTERCEPTOR DRONES", 44, ORANGE, alpha=seg(s, 0.5, 0.3))


def e10_plants(cv, s, T, ph=0):
    """ph0 ~10 plants abroad behind the state's back, ph1 1,000 interceptors for $3.5M,
    ph2 'could have given them away' · our forces first, ph3 2,000 a day possible, money for 1,000,
    ph4 warheads stay with the military, ph5 a European request for pilots refused."""
    backdrop(cv, s, "grid")
    if ph == 0:
        for k in range(10):
            x = 300 + (k % 5) * 330
            y = 380 + (k // 5) * 220
            if seg(s, 0.1 + k * 0.1, 0.2) > 0.5:
                cv.rect((x - 90, y - 50, x + 90, y + 50), 4, WHITE, radius=6)
                cv.line([(x - 60, y - 50), (x - 60, y - 90), (x - 30, y - 90), (x - 30, y - 50)], 3, WHITE)
        cv.text((CX, 170), "~10 PLANTS ABROAD · “BEHIND THE STATE'S BACK”", 42, RED, alpha=seg(s, 0.2, 0.3))
        cv.text((CX, 230), "ZELENSKY · MARCH 28, 2026", 28, GREY)
        return
    if ph == 1:
        cv.text((CX, 380), "1,000 INTERCEPTORS", 70, WHITE)
        cv.text((CX, 500), "FOR $3.5 MILLION", 70, ORANGE, alpha=seg(s, 0.3, 0.3))
        cv.text((CX, 600), "SOLD ABROAD BY ONE COMPANY", 32, GREY)
        return
    if ph == 2:
        cv.text((CX, 380), "“WE COULD HAVE GIVEN THEM AWAY”", 56, WHITE, alpha=seg(s, 0.1, 0.3))
        cv.tag((CX, 520), "UKRAINE'S OWN FORCES FIRST", 44, ORANGE, alpha=seg(s, 0.5, 0.3))
        return
    if ph == 3:
        for k, (lab, v, col) in enumerate((("CAN PRODUCE / DAY", 2000, WHITE), ("FUNDED / DAY", 1000, ORANGE))):
            y = 380 + k * 180
            p = ease(seg(s, 0.1 + k * 0.4, 0.8))
            cv.text((300, y - 50), lab, 32, col, anchor="lm")
            cv.rect((300, y - 25, 300 + 1200 * v / 2000 * p, y + 25), 0, fill=col, radius=6)
            cv.text((300 + 1200 * v / 2000 * p + 24, y), f"{v:,}", 40, col, anchor="lm")
        return
    if ph == 4:
        interceptor(cv, (CX - 300, 440), 1.2, WHITE, 5)
        cv.rect((CX + 200, 360, CX + 420, 520), 5, ORANGE, radius=10)
        cv.text((CX + 310, 440), "WARHEAD", 32, ORANGE)
        cv.text((CX, 680), "WARHEADS ARE KEPT BY UKRAINE'S MILITARY", 42, WHITE, alpha=seg(s, 0.3, 0.3))
        return
    cv.text((CX, 360), "DRONES WITHOUT WARHEADS + UKRAINIAN PILOTS?", 44, WHITE)
    cross(cv, (CX, 520), 80, RED, 10, seg(s, 0.3, 0.4))
    cv.text((CX, 680), "REQUEST REFUSED", 50, RED, alpha=seg(s, 0.5, 0.3))


def e10_week(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    cv.text((CX, 180), "ONE WEEK OVER UKRAINE · EARLY NOVEMBER 2026", 40, WHITE)
    cv.text((CX - 380, 420), "115", 140, RED, alpha=seg(s, 0.2, 0.3))
    cv.text((CX - 380, 540), "MISSILES", 40, WHITE)
    cv.text((CX + 380, 420), "3,000+", 140, RED, alpha=seg(s, 0.5, 0.3))
    cv.text((CX + 380, 540), "ATTACK DRONES", 40, WHITE)


def e10_patriot(cv, s, T, ph=0):
    """ph0 Patriot interceptors still short, ph1 sale approved, arrival maybe early 2030s."""
    backdrop(cv, s, "grid")
    x0, x1, y = 300, 1620, 520
    cv.line([(x0, y), (x1, y)], 4, GREY)
    for k, yr in enumerate(range(2026, 2033)):
        x = x0 + (x1 - x0) * k / 6
        cv.line([(x, y - 14), (x, y + 14)], 3, GREY)
        cv.text((x, y + 50), str(yr), 26, GREY)
    cv.text((CX, 170), "PATRIOT INTERCEPTORS FOR UKRAINE: STILL SHORT", 42, RED)
    if ph >= 1:
        cv.circle((x0 + 30, y), 16, 0, fill=WHITE)
        cv.text((x0 + 30, y - 60), "OCT 2026: SALE APPROVED", 30, WHITE, anchor="lm")
        a, b = x0 + (x1 - x0) * 4 / 6, x1
        cv.rect((a, y - 30, a + (b - a) * ease(seg(s, 0.3, 0.8)), y + 30), 3, ORANGE, radius=8)
        cv.text(((a + b) / 2, y - 70), "ARRIVAL: EARLY 2030s? (REUTERS)", 32, ORANGE, alpha=seg(s, 0.6, 0.3))


def e10_irony(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    shield(cv, (CX - 380, CY - 40), 0.9, ORANGE, 6)
    cv.text((CX - 380, CY + 200), "SHIELDS FOR OTHERS", 40, ORANGE)
    shield(cv, (CX + 380, CY - 40), 0.9, GREY, 6)
    cv.rect((CX + 300, CY - 120, CX + 460, CY + 40), 0, fill=BG)
    cv.text((CX + 380, CY + 200), "ITS OWN SKY: STILL SHORT", 40, RED)


# ---------------- what Ukraine showed ----------------

def e10_lesson(cv, s, T, ph=0):
    """ph0 not a few expensive weapons, but many cheap layers; ph1 the proof."""
    backdrop(cv, s, "grid")
    if ph == 0:
        cv.rect((300, 360, 560, 460), 5, GREY, radius=10)
        cv.text((430, 520), "A FEW EXPENSIVE", 32, GREY)
        for k in range(5):
            cv.rect((1100 + k * 30, 300 + k * 50, 1600 - k * 30, 330 + k * 50), 0, fill=ORANGE, radius=6)
        cv.text((1350, 600), "MANY CHEAP LAYERS", 36, ORANGE)
        cv.text((CX, 170), "THE SHIELD OF THE DRONE ERA", 50, WHITE, alpha=seg(s, 0.2, 0.3))
        return
    items = [lambda c: mic_pole(cv, (c[0], c[1] + 100), 0.5, WHITE, 3),
             lambda c: interceptor(cv, c, 0.5, ORANGE, 3),
             lambda c: turret(cv, (c[0], c[1] + 60), 0.6, WHITE, 4),
             lambda c: netting(cv, (c[0] - 80, c[1] - 40, c[0] + 80, c[1] + 40), WHITE, 20, 2),
             lambda c: ugv(cv, (c[0], c[1] + 30), 0.6, WHITE, 3)]
    labs = ["MICROPHONES", "INTERCEPTORS", "AI TURRETS", "NETS", "GROUND ROBOTS"]
    for k, (f, lab) in enumerate(zip(items, labs)):
        x = 260 + k * 350
        if seg(s, 0.1 + k * 0.25, 0.2) > 0.5:
            f((x, 460))
            cv.text((x, 620), lab, 28, WHITE)
    cv.text((CX, 170), "THE PROOF · REFINED ON A BATTLEFIELD, NOT IN A LAB", 40, ORANGE, alpha=seg(s, 0.2, 0.3))


# ---------------- series finale ----------------

SPEAR_EPS = [("EP01", "LONG-RANGE", "p14_swarm"), ("EP02", "JET DRONES", "e2_03_jet_climb"),
             ("EP03", "FPV", "e3_01_pilot_goggles"), ("EP04", "SEA DRONES", "e3_34_boat_vs_warship"),
             ("EP05", "SPIDERWEB", "e5_01_roof_opening")]
SHIELD_EPS = [("EP06", "NIGHT SKY", "e6_11_searchlight_catch"), ("EP07", "JET DRONES", "e7_02_interceptor_rise"),
              ("EP08", "ROBOT GUNS", "e8_02_turret_firing"), ("EP09", "KILL ZONE", "e8_20_netted_road"),
              ("EP10", "EXPORTS", "e6_21_command_post")]


def e10_series(cv, s, T, ph=0):
    """ph0 the end of Drone War Decoded, ph1 EP01–05 the spear, ph2 EP06–10 the shield."""
    backdrop(cv, s, "grid")
    if ph == 0:
        spear(cv, (CX - 380, CY), 1.0, RED, 6)
        shield(cv, (CX + 380, CY), 1.0, ORANGE, 6)
        cv.text((CX, 840), "DRONE WAR DECODED · THE END", 50, WHITE, alpha=seg(s, 0.3, 0.3))
        return
    eps = SPEAR_EPS if ph == 1 else SHIELD_EPS
    col = RED if ph == 1 else ORANGE
    cv.text((CX, 170), "THE SPEAR · EP01–05" if ph == 1 else "THE SHIELD · EP06–10", 50, col)
    for k, (ep, lab, img) in enumerate(eps):
        x = 140 + k * 340
        a = seg(s, 0.1 + k * 0.25, 0.3)
        photo_card(cv, img, (x, 330, x + 300, 500), alpha=a)
        cv.text((x + 150, 550), ep, 30, col, alpha=a)
        cv.text((x + 150, 595), lab, 26, WHITE, alpha=a)


def e10_race(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    p = (s * 0.4) % 1
    spear(cv, (lerp(400, 1100, p), CY - 60), 0.8, RED, 6)
    shield(cv, (lerp(800, 1500, p), CY - 60), 0.8, ORANGE, 6)
    cv.text((CX, 820), "SPEAR AND SHIELD · CHASING EACH OTHER EVERY DAY", 40, WHITE, alpha=seg(s, 0.2, 0.3))


def e10_people(cv, s, T, ph=0):
    backdrop(cv, s, "grid")
    for k in range(7):
        person(cv, (420 + k * 180, 620), 1.3, ORANGE if k == 3 else WHITE, 4)
    cv.text((CX, 260), "AT THE HEART OF THE RACE", 50, WHITE, alpha=seg(s, 0.2, 0.3))
    cv.text((CX, 340), "PEOPLE PROTECTING PEOPLE · ONE MORE DAY", 40, ORANGE, alpha=seg(s, 0.6, 0.3))


def e10_endcard(cv, s, T, ph=0):
    end_card(cv, s, "THANK YOU FOR WATCHING  ·  DRONE WAR DECODED", "grid")


SCENES = {k: v for k, v in globals().items() if k.startswith("e10_") and callable(v)}
