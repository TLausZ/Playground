"""Rendert aus den MJ-Zoom-Out-Stufen einen Pingpong-Kamerazoom und pipet ihn nach ffmpeg.

Aufruf: zoomvid.py fits.json out.mp4 [end.png] [sek_pro_oktave]
Der Zoom laeuft raus bis zum weitesten Bild und wieder rein; auf dem Rueckweg
ersetzt end.png die innerste Stufe. Geschwindigkeit ist an beiden Enden und am
Umkehrpunkt praktisch null, dazwischen konstant.
"""
import bisect, json, math, subprocess, sys
from PIL import Image

FITS, OUT = sys.argv[1], sys.argv[2]
END = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
SEC_PER_OCTAVE = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
SIZE, FPS = 720, 30
EASE = 0.3      # Anteil des Halbwegs, ueber den an- und abgebremst wird
VMIN = 0.02     # Restgeschwindigkeit an den Umkehrpunkten
HOLD = 0.5      # Standzeit ganz am Anfang und ganz am Ende
PAD = 384       # Rand, damit das Sichtfenster ueber die Bildkante hinausragen darf
FADE = (0.25, 0.85)   # Crossfade-Fenster innerhalb eines Segments

fits = json.load(open(FITS))
paths = [fits[0]["inner"]] + [f["outer"] for f in fits]

def pad(im):
    p = Image.new("RGB", (im.size[0] + 2 * PAD, im.size[1] + 2 * PAD), im.getpixel((4, 4)))
    p.paste(im, (PAD, PAD))
    return p

imgs = [Image.open(p).convert("RGB") for p in paths]
pads = [pad(im) for im in imgs]
img_end = Image.open(END).convert("RGB") if END else None

# Weltkoordinaten: innerstes Bild hat Groesse 1 und Zentrum (0,0).
# end.png teilt die Stufe mit dem innersten Bild (gemessen: gleicher Faktor, zentriert).
w = [1.0]
c = [(0.0, 0.0)]
for f in fits:
    wj = f["scale"] * w[-1]
    w.append(wj)
    c.append((c[-1][0] - (f["cx"] - 0.5) * wj, c[-1][1] - (f["cy"] - 0.5) * wj))

cum = [0.0]
for f in fits:
    cum.append(cum[-1] + math.log2(f["scale"]))
U = cum[-1]

def ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3 - 2 * t)

def box(m, vx, vy, vs):
    """Sichtfenster (Zentrum vx,vy, Kante vs) in Pixelkoordinaten von Bild m."""
    px = imgs[m].size[0]
    x0 = (vx - vs / 2 - (c[m][0] - w[m] / 2)) / w[m] * px + PAD
    y0 = (vy - vs / 2 - (c[m][1] - w[m] / 2)) / w[m] * px + PAD
    d = vs / w[m] * px
    return (x0, y0, x0 + d, y0 + d)

def frame(u, back):
    k = min(max(bisect.bisect_right(cum, u) - 1, 0), len(fits) - 1)
    t = (u - cum[k]) / (cum[k + 1] - cum[k])
    vs = w[k] * (w[k + 1] / w[k]) ** t
    vx = c[k][0] + (c[k + 1][0] - c[k][0]) * t
    vy = c[k][1] + (c[k + 1][1] - c[k][1]) * t
    base = pads[k + 1].resize((SIZE, SIZE), Image.LANCZOS, box=box(k + 1, vx, vy, vs))
    alpha = 1.0 - ss(FADE[0], FADE[1], t)
    if alpha <= 0.002:
        return base
    inner = img_end if (back and k == 0 and img_end) else imgs[k]
    n = max(1, round(w[k] / vs * SIZE))
    top = base.copy()
    top.paste(inner.resize((n, n), Image.LANCZOS),
              (round((c[k][0] - w[k] / 2 - (vx - vs / 2)) / vs * SIZE),
               round((c[k][1] - w[k] / 2 - (vy - vs / 2)) / vs * SIZE)))
    return Image.blend(base, top, alpha)

# Geschwindigkeitsprofil ueber einen Halbweg: null an den Raendern, konstant dazwischen
def speed(h):
    return VMIN + (1 - VMIN) * ss(0, EASE, h) * ss(0, EASE, 1 - h)

mean_v = sum(speed(i / 999) for i in range(1000)) / 1000
nf = max(2, round(U * SEC_PER_OCTAVE * FPS / mean_v))
vs_ = [speed(i / (nf - 1)) for i in range(nf)]
tot = sum(vs_)
leg, acc = [], 0.0
for v in vs_:
    leg.append(U * acc / tot)
    acc += v
leg.append(U)

plan = [(0.0, False)] * round(HOLD * FPS)
plan += [(u, False) for u in leg]
plan += [(u, True) for u in reversed(leg[:-1])]
plan += [(0.0, True)] * round(HOLD * FPS)

ff = subprocess.Popen([
    "ffmpeg", "-v", "error", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SIZE}x{SIZE}", "-r", str(FPS), "-i", "-",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", OUT],
    stdin=subprocess.PIPE)
print(f"{len(plan)} Frames = {len(plan)/FPS:.1f} s", flush=True)
for i, (u, back) in enumerate(plan):
    ff.stdin.write(frame(u, back).tobytes())
    if i % 120 == 0:
        print(f"{i}/{len(plan)}", flush=True)
ff.stdin.close()
sys.exit(ff.wait())
