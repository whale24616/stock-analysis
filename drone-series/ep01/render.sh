#!/usr/bin/env bash
# Full EP01 render: graphics -> shot segments -> concat -> narration + ambient pad -> ep01_test_720p.mp4
# Needs ffmpeg, sox, python3 + Pillow (all preinstalled in the Higgsfield sandbox).
set -e
cd "$(dirname "$0")"
python3 graphics.py
python3 build.py
python3 - <<'P'
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
jobs=json.load(open('jobs.json'))
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    return (c[-1],r.returncode,r.stderr[-300:])
with ThreadPoolExecutor(6) as ex:
    for out,rc,err in ex.map(run,jobs):
        if rc: print('FAIL',out,err)
print('segments done')
P
ls seg/*.mp4 | sed "s/^/file '/; s/$/'/" > seg/list.txt && sed -i "s#file 'seg/#file '#" seg/list.txt
ffmpeg -v error -y -f concat -safe 0 -i seg/list.txt -c copy video_only.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 audio/narr.wav)
sox -n -r 48000 -c 2 audio/pad.wav synth $D sine 55 sine 82.4 tremolo 0.08 40 fade q 3 $D 4 vol 0.05
ffmpeg -v error -y -i audio/narr.wav -i audio/pad.wav -filter_complex "[0:a]volume=1.0[a];[1:a]volume=0.5[b];[a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11" -c:a aac -b:a 160k audio/mix.m4a
ffmpeg -v error -y -i video_only.mp4 -i audio/mix.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest ep01_test_720p.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 ep01_test_720p.mp4
echo RENDER_DONE
