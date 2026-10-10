"""EP01 edit plan -> jobs.json (ffmpeg commands per shot) + audio/narr.wav

Inputs (relative to this folder):
  audio/vo0.wav .. vo8.wav   narration per script section (Higgsfield seed_audio)
  img/NN.png                 AI keyframes (see assets.md for NN -> prompt)
  vid/NN.mp4                 AI 5s clips (Kling 3.0 std)
  gfx/*.png                  from graphics.py
Each section's visuals are stretched to its narration length (+GAP).
"""
import subprocess, os, json
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('seg',exist_ok=True)
FPS=30; GAP=0.7; FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
# (type, src, weight)  type: g=graphic, i=AI image, v=AI video(5s)
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
jobs=[]; n=0
for si,shots in enumerate(S):
    total=dur(f'audio/vo{si}.wav')+GAP
    vids=sum(5.0 for t,_,_ in shots if t=='v'); W=sum(w for t,_,w in shots if t!='v')
    for k,(t,src,w) in enumerate(shots):
        d=5.0 if t=='v' else (total-vids)*w/W
        fr=round(d*FPS); out=f'seg/{n:03d}.mp4'; n+=1
        label="drawtext=fontfile=%s:text='AI VISUALIZATION':fontsize=18:fontcolor=white@0.55:x=24:y=h-40,"%FONT if t in 'iv' else ''
        fade=f"fade=t=in:st=0:d=0.25,fade=t=out:st={fr/FPS-0.25:.3f}:d=0.25"
        if t=='v':
            cmd=['ffmpeg','-v','error','-y','-i',f'vid/{src}.mp4','-vf',f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps={FPS},trim=end_frame={fr},{label}{fade}",'-an']
        else:
            f=f'gfx/{src}.png' if t=='g' else f'img/{src}.png'
            zmax=1.04 if t=='g' else 1.12; step=(zmax-1)/max(fr,1)
            zin = (n%2==0)
            z=f"'1+{step:.6f}*on'" if zin else f"'{zmax}-{step:.6f}*on'"
            px="'iw/2-(iw/zoom/2)'" if t=='g' else ("'(iw-iw/zoom)*on/%d'"%fr if n%3==0 else "'iw/2-(iw/zoom/2)'")
            cmd=['ffmpeg','-v','error','-y','-loop','1','-i',f,'-vf',f"scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z={z}:x={px}:y='ih/2-(ih/zoom/2)':d={fr}:s=1280x720:fps={FPS},trim=end_frame={fr},{label}{fade}",'-frames:v',str(fr)]
        cmd+=['-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-r',str(FPS),out]
        jobs.append(cmd)
json.dump(jobs,open('jobs.json','w'))
# narration track
parts=[]
for si in range(len(S)):
    o=f'audio/p{si}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'audio/vo{si}.wav','-af',f'aresample=48000,apad=pad_dur={GAP}','-ac','2',o],check=True); parts.append(o)
open('audio/list.txt','w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','audio/list.txt','-c','pcm_s16le','audio/narr.wav'],check=True)
print('segments',len(jobs),'narr',dur('audio/narr.wav'))
