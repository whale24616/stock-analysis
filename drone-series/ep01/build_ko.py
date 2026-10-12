# EP01 Korean version: smooth sub-pixel Ken Burns (PIL), 24fps, hard cuts, Korean narration + burned-in Korean subtitles
# Run in the Higgsfield sandbox next to img/ vid/ gfx/ (from graphics.py) and audio/raw0..8.wav (Korean TTS per section).
# Needs NanumGothic font in ~/.fonts (Google Fonts) and narration_ko_easy.json.
import subprocess, os, json, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('seg',exist_ok=True)
FPS=24; GAP=0.7; W,H=1280,720; TEMPO=0.94
LBLF=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
def sh(c): subprocess.run(c,check=True)
# 1) narration: slight slow-down for clarity
for i in range(9): sh(['ffmpeg','-v','error','-y','-i',f'audio/raw{i}.wav','-af',f'atempo={TEMPO},aresample=48000','-ac','2',f'audio/vo{i}.wav'])
D=[dur(f'audio/vo{i}.wav') for i in range(9)]
S=[
 [('g','radar',5),('i','01',6),('v','02',0),('g','map_route',6),('i','03',7),('g','airport',7),('g','title',6)],
 [('g','strike_gap',12),('i','04',10),('g','types',15),('g','targets',12),('i','09',8),('g','triangle',6)],
 [('g','triangle',8),('v','05',0),('i','05',6),('g','aspect',13),('g','vortex',15),('i','06',7),('i','07',7),('g','pusher',12),('g','materials',13),('g','cg',11)],
 [('i','08',8),('g','effcurve',12),('g','breguet',16),('g','logcurve',13),('g','tradeoff',15),('i','09',7),('g','hours',9)],
 [('g','horizon',14),('g','ins',14),('i','10',8),('g','jam',14),('i','11',8),('g','crpa',12),('i','12',9),('g','layers',9)],
 [('g','ad_route',11),('v','13',0),('i','13',5),('g','saturation',12),('g','cost',13)],
 [('i','14',10),('g','field',14),('i','03',5),('i','16',6)],
 [('g','weak',14),('i','16',8),('i','11',7),('i','01',6),('g','question',9)],
 [('v','17',0),('g','end',18)],
]
def ease(t): return t*t*(3-2*t)
def still(src,kind,fr,n,out):
    im=Image.open(src).convert('RGB')
    if kind=='i': im=im.resize((1920,int(1920*im.height/im.width)),Image.LANCZOS)
    sw,sh_=im.size; z0,z1=(1.0,1.03) if kind=='g' else (1.0,1.10)
    if n%2: z0,z1=z1,z0
    pan=0 if kind=='g' else [0,0.6,-0.6][n%3]
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for k in range(fr):
        e=ease(k/max(fr-1,1)); z=z0+(z1-z0)*e
        cw=sw/z; ch=cw*H/W
        if ch>sh_: ch=sh_; cw=ch*W/H
        cx=sw/2+pan*e*(sw-cw)/2; cy=sh_/2
        f=im.transform((W,H),Image.EXTENT,(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2),Image.BICUBIC)  # float crop box = sub-pixel smooth motion
        if kind=='i': ImageDraw.Draw(f).text((20,16),'AI VISUALIZATION',font=LBLF,fill=(230,230,230))
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
jobs=[]; n=0; starts=[]; t0=0
for si,shots in enumerate(S):
    total=D[si]+GAP; starts.append(t0); t0+=total
    vids=sum(5.0 for t,_,_ in shots if t=='v'); Wt=sum(w for t,_,w in shots if t!='v')
    for t,src,w in shots:
        d=5.0 if t=='v' else (total-vids)*w/Wt; fr=round(d*FPS); out=f'seg/{n:03d}.mp4'
        if t=='v':
            jobs.append(('cmd',['ffmpeg','-v','error','-y','-i',f'vid/{src}.mp4','-vf',f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},trim=end_frame={fr},drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='AI VISUALIZATION':fontsize=16:fontcolor=white@0.9:x=20:y=16",'-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r',str(FPS),out]))
        else: jobs.append(('still',(f'gfx/{src}.png' if t=='g' else f'img/{src}.png',t,fr,n,out)))
        n+=1
def run(j):
    if j[0]=='cmd': sh(j[1])
    else: still(*j[1])
with ThreadPoolExecutor(6) as ex: list(ex.map(run,jobs))
print('segments',n,flush=True)
# 2) narration track
open('audio/list.txt','w').write(''.join(f"file 'p{i}.wav'\n" for i in range(9)))
for i in range(9): sh(['ffmpeg','-v','error','-y','-i',f'audio/vo{i}.wav','-af',f'apad=pad_dur={GAP}','-ac','2',f'audio/p{i}.wav'])
sh(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','audio/list.txt','-c','pcm_s16le','audio/narr.wav'])
# 3) subtitles: script sentences aligned to whisper word timings (character-proportional mapping)
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
KO=json.load(open('narration_ko_easy.json'))['sections']
norm=lambda s: re.sub(r'[^0-9A-Za-z가-힣]','',s)
def chunks(sent,maxc=32):
    if len(sent)<=maxc: return [sent]
    parts=re.split(r'(?<=,)\s+',sent)
    out=[];cur=''
    for p in parts:
        if cur and len(cur)+1+len(p)>maxc: out.append(cur); cur=p
        else: cur=(cur+' '+p).strip()
    if cur: out.append(cur)
    res=[]
    for c in out:
        while len(c)>maxc+12:
            k=c.rfind(' ',0,len(c)//2+6); k=k if k>0 else len(c)//2
            res.append(c[:k]); c=c[k:].strip()
        res.append(c)
    return res
def ts(x): h=int(x//3600); m_=int(x%3600//60); s=x%60; return f'{h}:{m_:02d}:{s:05.2f}'
ev=[]
for si in range(9):
    segs,_=m.transcribe(f'audio/vo{si}.wav',language='ko',word_timestamps=True,beam_size=1)
    ct=[]
    for sg in segs:
        for wd in sg.words:
            cs=norm(wd.word)
            for j,_c in enumerate(cs): ct.append((wd.start+(wd.end-wd.start)*j/len(cs), wd.start+(wd.end-wd.start)*(j+1)/len(cs)))
    cks=[c for s in KO[si]['text'] for c in chunks(s)]
    Ns=sum(len(norm(c)) for c in cks); Nt=len(ct); cum=0; prev=ct[0][0] if ct else 0
    for c in cks:
        cum+=len(norm(c)); idx=min(Nt-1,max(0,round(cum/Ns*Nt)-1)); end=ct[idx][1]
        ev.append((starts[si]+prev,starts[si]+end,c)); prev=end
for i in range(len(ev)-1):  # no overlapping subtitle lines
    a,b,c=ev[i]; ev[i]=(a,min(b+0.15,ev[i+1][0]-0.04),c)
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,NanumGothic,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,2.6,1.2,2,60,60,34,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open('subs_ko.ass','w') as f:
    f.write(hdr)
    for a,b,c in ev: f.write(f'Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{c}\n')
# 4) assemble
open('seg/list.txt','w').write(''.join(f"file '{i:03d}.mp4'\n" for i in range(n)))
sh(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c','copy','video_only.mp4'])
T=dur('audio/narr.wav')
sh(['sox','-n','-r','48000','-c','2','audio/pad.wav','synth',str(T),'sine','55','sine','82.4','tremolo','0.08','40','fade','q','3',str(T),'4','vol','0.05'])
sh(['ffmpeg','-v','error','-y','-i','audio/narr.wav','-i','audio/pad.wav','-filter_complex','[1:a]volume=0.5[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','audio/mix.m4a'])
sh(['ffmpeg','-v','error','-y','-i','video_only.mp4','-i','audio/mix.m4a','-vf','subtitles=subs_ko.ass:fontsdir='+os.path.expanduser('~/.fonts'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-shortest','ep01_ko_720p.mp4'])
print('DONE',dur('ep01_ko_720p.mp4'),flush=True)
