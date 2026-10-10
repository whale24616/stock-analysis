"""EP01 explainer graphics (1920x1080 PNG) -> gfx/*.png

Run from this folder:  python3 graphics.py
Needs Pillow and DejaVu fonts (preinstalled in the Higgsfield sandbox).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('gfx', exist_ok=True)

W,H=1920,1080
BG=(11,18,21); AC=(63,208,201); WA=(232,163,61); TX=(230,237,240); MU=(120,140,148); GR=(30,44,50)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FM='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def F(s,b=True,m=False): return ImageFont.truetype(FM if m else (FB if b else FR),s)
def base(title=None,tag=None):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    for x in range(0,W,80): d.line([(x,0),(x,H)],fill=(16,26,30))
    for y in range(0,H,80): d.line([(0,y),(W,y)],fill=(16,26,30))
    if title: d.text((120,90),title,font=F(56),fill=TX); d.line([(120,170),(420,170)],fill=AC,width=6)
    if tag: d.text((120,H-90),tag,font=F(26,m=True),fill=MU)
    return im,d
def ctext(d,xy,t,f,c=TX):
    b=d.textbbox((0,0),t,font=f); d.text((xy[0]-(b[2]-b[0])/2,xy[1]-(b[3]-b[1])/2),t,font=f,fill=c)
def arrow(d,a,b,c=AC,w=6):
    d.line([a,b],fill=c,width=w); ang=math.atan2(b[1]-a[1],b[0]-a[0])
    for s in (2.6,-2.6): d.line([b,(b[0]+28*math.cos(ang+s),b[1]+28*math.sin(ang+s))],fill=c,width=w)
def dashed(d,pts,c=AC,w=6,dl=24):
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        L=math.hypot(x2-x1,y2-y1); n=int(L/dl)
        for i in range(0,n,2):
            t0,t1=i/n,min((i+1)/n,1); d.line([(x1+(x2-x1)*t0,y1+(y2-y1)*t0),(x1+(x2-x1)*t1,y1+(y2-y1)*t1)],fill=c,width=w)
def plane(d,cx,cy,s=1.0,c=TX,pusher=True):
    d.rectangle([cx-260*s,cy-14*s,cx+200*s,cy+14*s],fill=c)  # fuselage side
    d.polygon([(cx-60*s,cy-14*s),(cx+40*s,cy-14*s),(cx+20*s,cy-40*s),(cx-50*s,cy-40*s)],fill=c)
    px=cx-275*s if pusher else cx+215*s
    d.ellipse([px-8*s,cy-70*s,px+8*s,cy+70*s],outline=AC,width=int(5*s))
def save(n,im): im.save(f'gfx/{n}.png')
# radar
im,d=base(); cx,cy=W//2,H//2
for r in (120,240,360,480): d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(20,90,60),width=3)
d.line([(cx-480,cy),(cx+480,cy)],fill=(20,90,60),width=2); d.line([(cx,cy-480),(cx,cy+480)],fill=(20,90,60),width=2)
d.pieslice([cx-480,cy-480,cx+480,cy+480],-60,-20,fill=(20,70,50))
for x,y in [(150,-300),(190,-260),(230,-310),(260,-240),(120,-230),(300,-280),(210,-200)]: d.ellipse([cx+x-9,cy+y-9,cx+x+9,cy+y+9],fill=(90,255,150))
d.text((cx+330,cy-360),'7 TRACKS · 170 km/h',font=F(30,m=True),fill=(90,255,150)); save('radar',im)
# map route (schematic)
im,d=base('Launch to target','SCHEMATIC · NOT TO SCALE')
d.rounded_rectangle([220,520,820,900],40,outline=AC,width=5); ctext(d,(520,710),'UKRAINE',F(54),AC)
d.ellipse([1380,250,1420,290],fill=WA); d.text((1440,240),'MOSCOW',font=F(54),fill=WA)
dashed(d,[(700,600),(1000,480),(1390,280)],TX,6); ctext(d,(1080,420),'500+ km',F(64),TX); save('map_route',im)
# airport board
im,d=base('DEPARTURES','ILLUSTRATIVE · GENERIC AIRPORT')
for i,(fl,de) in enumerate([('XA 101','NORTH CITY'),('XA 204','SEASIDE'),('XB 318','CAPITAL WEST'),('XC 422','LAKE PORT'),('XA 530','HIGHLANDS'),('XD 611','SOUTH BAY')]):
    y=260+i*110; d.rectangle([120,y,1800,y+90],fill=(18,22,26))
    d.text((150,y+18),fl,font=F(48,m=True),fill=TX); d.text((520,y+18),de,font=F(48,m=True),fill=TX); d.text((1350,y+18),'SUSPENDED',font=F(48,m=True),fill=WA)
save('airport',im)
# title
im,d=base(); ctext(d,(W//2,440),'DRONE WAR DECODED',F(120),TX); d.line([(660,540),(1260,540)],fill=AC,width=8)
ctext(d,(W//2,630),'EP01 · REACHING MOSCOW',F(64),AC); save('title',im)
# strike gap
im,d=base('2022: the strike gap')
d.rounded_rectangle([160,280,900,840],30,outline=WA,width=5); ctext(d,(530,350),'RUSSIA',F(52),WA)
for i,t in enumerate(['Cruise missiles','Ballistic missiles','Long-range aviation']): d.text((220,450+i*110),'• '+t,font=F(44,False),fill=TX)
d.rounded_rectangle([1020,280,1760,840],30,outline=AC,width=5); ctext(d,(1390,350),'UKRAINE',F(52),AC)
for i,t in enumerate(['Few long-range weapons','Usage restrictions','Need: build it at home']): d.text((1080,450+i*110),'• '+t,font=F(44,False),fill=TX)
save('strike_gap',im)
# types
im,d=base('Ukraine\'s long-range family','FIGURES: REPORTED / MANUFACTURER CLAIMS · VERIFY BEFORE PUBLISHING')
for i,n in enumerate(['Liutyi','UJ-22 Airborne','Bober','FP-1']):
    x=140+i*430; d.rounded_rectangle([x,300,x+390,820],24,fill=GR); plane(d,x+195+30,520,0.55,TX); ctext(d,(x+195,700),n,F(44),AC)
save('types',im)
# targets
im,d=base('Typical targets')
for i,t in enumerate(['Oil refineries','Airbases','Ammunition depots','Command sites']):
    y=300+i*150; d.ellipse([160,y,240,y+80],outline=AC,width=6); d.text((290,y+8),t,font=F(56,False),fill=TX)
d.text((1100,420),'hundreds to',font=F(56,False),fill=MU); d.text((1100,500),'1,000+ km',font=F(110),fill=WA); d.text((1100,640),'from the front',font=F(56,False),fill=MU); save('targets',im)
# triangle
im,d=base('The engineering triangle')
p=[(W//2,260),(560,900),(1360,900)]; d.polygon(p,outline=AC,width=8)
ctext(d,(W//2,210),'FLY FAR',F(60),TX); ctext(d,(420,960),'CARRY ENOUGH',F(60),TX); ctext(d,(1500,960),'COST LITTLE',F(60),TX)
ctext(d,(W//2,700),'improve one →',F(40,False),MU); ctext(d,(W//2,760),'the other two suffer',F(40,False),MU); save('triangle',im)
# aspect ratio
im,d=base('Aspect ratio = span² / wing area')
d.rectangle([300,330,900,450],fill=MU); ctext(d,(600,520),'LOW AR  · short & wide',F(40,False),TX)
d.rectangle([1000,360,1800,410],fill=AC); ctext(d,(1400,520),'HIGH AR · long & slender',F(40,False),AC)
ctext(d,(W//2,760),'Gliders and long-range drones use high aspect ratio wings',F(44,False),TX); save('aspect',im)
# vortex
im,d=base('Induced drag: wingtip vortices')
for cx,span,rad,lab,c in [(560,360,110,'short wing → strong vortex',WA),(1380,560,55,'long wing → weaker vortex',AC)]:
    d.rectangle([cx-span//2,480,cx+span//2,520],fill=TX)
    for sx in (cx-span//2,cx+span//2):
        for k in range(4): r=rad-k*rad//4; d.arc([sx-r,500-r,sx+r,500+r],0,300,fill=c,width=5)
    ctext(d,(cx,760),lab,F(42,False),c)
save('vortex',im)
# pusher vs tractor
im,d=base('Tractor vs pusher')
plane(d,600,420,1.0,MU,pusher=False); ctext(d,(560,560),'TRACTOR: wing sits in propeller wash',F(36,False),MU)
for y in (380,420,460): dashed(d,[(900,y+260),(300,y+260)],MU,3,14)
plane(d,1300,420,1.0,TX,pusher=True); ctext(d,(1340,560),'PUSHER: clean air over wing, free nose',F(36,False),AC)
for y in (380,420,460): d.line([(1620,y+260),(1060,y+260)],fill=AC,width=3)
save('pusher',im)
# materials
im,d=base('Cheap, light, fast to build')
for i,t in enumerate(['Composites','Foam cores','Simple tubing']): d.text((180,320+i*120),'■ '+t,font=F(56,False),fill=AC)
d.text((1000,320),'Still metal:',font=F(52),fill=WA)
for i,t in enumerate(['Engine','Fuel system','Payload']): d.text((1000,420+i*100),'• '+t,font=F(50,False),fill=TX)
ctext(d,(W//2,880),'Lower radar reflection — not "stealth"',F(46),TX); save('materials',im)
# cg
im,d=base('Centre of gravity')
d.rounded_rectangle([360,480,1560,600],60,outline=TX,width=6); d.rectangle([760,490,960,590],fill=AC); d.rectangle([980,490,1140,590],fill=WA)
ctext(d,(860,660),'FUEL',F(40),AC); ctext(d,(1060,660),'PAYLOAD',F(40),WA)
d.polygon([(960,380),(990,440),(930,440)],fill=TX); ctext(d,(960,340),'CG',F(44),TX)
ctext(d,(W//2,820),'Heavy items near CG → stable as fuel burns off',F(44,False),TX); save('cg',im)
# efficiency curves
im,d=base('Fuel efficiency vs speed','CONCEPTUAL')
d.line([(260,900),(1700,900)],fill=MU,width=4); d.line([(260,900),(260,300)],fill=MU,width=4)
d.text((1500,930),'speed →',font=F(36,False),fill=MU); d.text((120,250),'efficiency',font=F(36,False),fill=MU)
pp=[(260+i*14,900-520*math.exp(-((i-35)/30)**2)) for i in range(0,101)]; d.line(pp,fill=AC,width=7)
jp=[(260+i*14,900-520*math.exp(-((i-90)/30)**2)) for i in range(0,101)]; d.line(jp,fill=WA,width=7)
d.text((600,330),'piston + propeller',font=F(40),fill=AC); d.text((1300,330),'jet',font=F(40),fill=WA)
d.rectangle([520,380,760,900],outline=TX,width=2); d.text((470,960),'150–200 km/h',font=F(32,False),fill=TX); save('effcurve',im)
# breguet
im,d=base('Breguet range equation')
ctext(d,(W//2,460),'R  =  (η / c) · (L / D) · ln(W₀ / W₁)',F(84,False),TX)
for x,t,c in [(560,'engine +\npropeller',AC),(980,'aerodynamics',AC),(1420,'fuel fraction',WA)]:
    for k,l in enumerate(t.split('\n')): ctext(d,(x,640+k*60),l,F(44),c)
save('breguet',im)
# log curve
im,d=base('Diminishing returns','CONCEPTUAL')
d.line([(260,900),(1700,900)],fill=MU,width=4); d.line([(260,900),(260,300)],fill=MU,width=4)
d.text((1300,930),'fuel added →',font=F(36,False),fill=MU); d.text((120,250),'range',font=F(36,False),fill=MU)
pts=[(260+i*14,900-150*math.log(1+i/8)) for i in range(0,101)]; d.line(pts,fill=AC,width=7)
d.text((900,450),'each extra litre buys less',font=F(44),fill=TX); save('logcurve',im)
# tradeoff
im,d=base('Payload vs range','REPORTED RANGES ACROSS TYPES · ILLUSTRATIVE')
d.line([(260,900),(1700,900)],fill=MU,width=4); d.line([(260,900),(260,300)],fill=MU,width=4)
d.text((1400,930),'range →',font=F(36,False),fill=MU); d.text((120,250),'payload',font=F(36,False),fill=MU)
d.line([(320,360),(1640,840)],fill=AC,width=7)
d.text((360,300),'~70+ kg',font=F(40),fill=WA); d.text((1420,780),'~20 kg',font=F(40),fill=WA)
d.text((300,940),'several hundred km',font=F(32,False),fill=TX); d.text((1380,980),'1,500+ km',font=F(32,False),fill=TX); save('tradeoff',im)
# hours
im,d=base(); ctext(d,(W//2,420),'1,000 km  ÷  150–200 km/h',F(90),TX); ctext(d,(W//2,600),'≈ 5–7 hours in the air',F(90),AC); save('hours',im)
# radio horizon
im,d=base('Radio horizon')
d.ellipse([-400,620,2320,2400],outline=AC,width=6)
d.rectangle([380,560,400,640],fill=TX); d.text((300,500),'operator',font=F(34,False),fill=TX)
d.line([(390,560),(1500,330)],fill=WA,width=4); d.text((1200,280),'line of sight',font=F(34,False),fill=WA)
plane(d,1500,600,0.35,TX); d.text((1350,660),'drone below horizon',font=F(34,False),fill=TX)
ctext(d,(W//2,930),'Low flyers vanish from radio contact within a few dozen km',F(40,False),TX); save('horizon',im)
# INS drift
im,d=base('Inertial navigation drift','CONCEPTUAL')
d.line([(260,700),(1700,700)],fill=AC,width=6); d.text((1500,720),'true path',font=F(34,False),fill=AC)
pts=[(260+i*14,700-0.012*(i**2)) for i in range(0,101)]; d.line(pts,fill=WA,width=6); d.text((1350,500),'estimated',font=F(34,False),fill=WA)
for i,r in [(30,20),(60,50),(90,90)]: x=260+i*14; d.ellipse([x-r,700-r,x+r,700+r],outline=MU,width=3)
ctext(d,(W//2,900),'Accelerometers + gyros: unjammable, but errors grow every hour',F(40,False),TX); save('ins',im)
# jam vs spoof
im,d=base('Two ways to attack satellite navigation')
d.rounded_rectangle([160,280,900,860],30,outline=WA,width=5); ctext(d,(530,340),'JAMMING',F(56),WA)
random.seed(3)
for i in range(400): x=random.randint(220,840); y=random.randint(420,700); d.point((x,y),fill=TX); d.ellipse([x-2,y-2,x+2,y+2],fill=MU)
ctext(d,(530,790),'drown the signal in noise',F(38,False),TX)
d.rounded_rectangle([1020,280,1760,860],30,outline=WA,width=5); ctext(d,(1390,340),'SPOOFING',F(56),WA)
d.ellipse([1150,560,1190,600],fill=AC); d.ellipse([1560,460,1600,500],outline=WA,width=5); dashed(d,[(1190,580),(1560,480)],TX,4)
ctext(d,(1390,790),'fake signal, false position',F(38,False),TX); save('jam',im)
# CRPA
im,d=base('Anti-jam antenna array (CRPA)')
cx,cy=W//2,600
for a in range(0,360,60): x=cx+120*math.cos(math.radians(a)); y=cy+120*math.sin(math.radians(a)); d.ellipse([x-22,y-22,x+22,y+22],fill=AC)
d.ellipse([cx-22,cy-22,cx+22,cy+22],fill=AC)
arrow(d,(260,600),(560,600),WA); d.text((180,520),'jammer',font=F(40),fill=WA); d.text((380,650),'NULL',font=F(40),fill=WA)
for a in (-60,-90,-120): arrow(d,(cx+380*math.cos(math.radians(a)),cy+380*math.sin(math.radians(a))),(cx+180*math.cos(math.radians(a)),cy+180*math.sin(math.radians(a))),TX,4)
d.text((cx+200,240),'satellites',font=F(40),fill=TX); save('crpa',im)
# layers
im,d=base('Three navigation layers')
for i,(t,s) in enumerate([('INERTIAL','cannot be jammed · drifts'),('SATELLITE','precise · jammable'),('VISUAL','camera vs stored maps')]):
    y=300+i*200; d.rounded_rectangle([360,y,1560,y+160],24,fill=GR,outline=AC,width=4); d.text((420,y+40),t,font=F(60),fill=AC); d.text((1000,y+56),s,font=F(40,False),fill=TX)
save('layers',im)
# AD route
im,d=base('Routing through the gaps','SCHEMATIC · NOT REAL POSITIONS')
for x,y,r in [(700,420,180),(1100,700,200),(1350,350,170),(900,860,140)]: d.ellipse([x-r,y-r,x+r,y+r],outline=WA,width=4); d.ellipse([x-10,y-10,x+10,y+10],fill=WA)
dashed(d,[(200,600),(560,620),(900,560),(1180,470),(1600,560),(1760,300)],AC,6); save('ad_route',im)
# saturation
im,d=base('Saturation')
cx,cy=700,600
for r in (150,300,420): d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(20,90,60),width=3)
random.seed(7)
for i in range(28): a=random.uniform(0,6.28); r=random.uniform(60,400); x=cx+r*math.cos(a); y=cy+r*math.sin(a); d.ellipse([x-9,y-9,x+9,y+9],fill=(90,255,150))
d.text((1180,420),'targets: 28',font=F(52,m=True),fill=TX); d.text((1180,520),'track limit: reached',font=F(52,m=True),fill=WA)
d.text((1180,640),'+ cheap decoys',font=F(52,False),fill=TX); save('saturation',im)
# cost bars
im,d=base('The cost equation','RELATIVE · ESTIMATE · NOT TO SCALE')
d.rectangle([500,700,800,880],fill=AC); ctext(d,(650,930),'DRONE',F(44),AC)
d.rectangle([1120,300,1420,880],fill=WA); ctext(d,(1270,930),'INTERCEPTOR',F(44),WA)
ctext(d,(1270,250),'several × more',F(44),TX); save('cost',im)
# field
im,d=base('In the field','PUBLIC REPORTING · VERIFY FIGURES')
for i,t in enumerate(['Refineries: capacity offline at times','Airbases: hundreds of km deep','Moscow region: airport suspensions']):
    d.text((180,320+i*160),'▶ '+t,font=F(54,False),fill=TX)
save('field',im)
# weaknesses
im,d=base('Weaknesses')
for i,t in enumerate(['Slow','Loud','Visible on radar','Small warhead']):
    y=300+i*150; d.rectangle([180,y,250,y+70],outline=WA,width=6); d.text((300,y+4),t,font=F(60),fill=TX)
save('weak',im)
# question
im,d=base(); ctext(d,(W//2,H//2),'What if it were fast?',F(120),WA); save('question',im)
# end card
im,d=base(); ctext(d,(W//2,360),'NEXT EPISODE',F(50,False),MU); ctext(d,(W//2,470),'EP02 · FASTER THAN DEFENSE',F(90),AC)
ctext(d,(W//2,650),'Jet-powered missile-drones',F(56,False),TX); ctext(d,(W//2,850),'SUBSCRIBE',F(64),WA); save('end',im)
print('ok')
