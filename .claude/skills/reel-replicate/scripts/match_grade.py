#!/usr/bin/env python3
"""Fix a colour/contrast jump inside a Seedance start->end clip (end frame graded differently).
Usage: python3 match_grade.py IN.mp4 OUT.mp4   (480x854 @24fps; edit W,H,FPS and the frame ranges below)
Takes the look of frames 40-45 (before the jump) as reference, measures frames 72-89 (after it) on the static
regions (sky rows 0-200, table/shoes rows 640-854), and maps the after-part onto the reference per channel
(mean/std), top and bottom separately with a vertical blend, ramped in over 2.05-2.45 s. Check with per-frame
means of the sky region before/after.
"""
import sys, subprocess, numpy as np
src, out = sys.argv[1], sys.argv[2]
W,H,FPS=480,854,24
raw=subprocess.run(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
v=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.float32)
pre=v[40:46].mean(0); post=v[72:90].mean(0)
def tr(r):
    a=pre[r].reshape(-1,3).std(0)/post[r].reshape(-1,3).std(0); b=pre[r].reshape(-1,3).mean(0)-a*post[r].reshape(-1,3).mean(0); return a,b
aT,bT=tr(slice(0,200)); aB,bB=tr(slice(640,854))
print('top',aT.round(3),bT.round(1),'bot',aB.round(3),bB.round(1))
y=np.arange(H,dtype=np.float32)[:,None,None]; k=np.clip((y-200)/(640-200),0,1)
A=aT*(1-k)+aB*k; B=bT*(1-k)+bB*k
res=[]
for i,f in enumerate(v):
    t=i/FPS
    w=0 if t<2.05 else (1 if t>2.45 else (t-2.05)/0.4)
    if w>0: f=f*(1-w)+(f*A+B)*w
    res.append(np.clip(f,0,255).astype(np.uint8))
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",src,"-map","0:v","-map","1:a","-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-c:a","copy",out],stdin=subprocess.PIPE)
p.stdin.write(np.stack(res).tobytes());p.stdin.close();p.wait()
