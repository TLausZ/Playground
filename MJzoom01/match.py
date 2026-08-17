"""Findet fuer jedes Bildpaar (innen, aussen) Skala und Zentrum per NCC-Template-Matching."""
import sys, glob, re, json
import numpy as np
from PIL import Image

def load(path, n):
    im = Image.open(path).convert("L").resize((n, n), Image.LANCZOS)
    return np.asarray(im, dtype=np.float64)

def ncc_map(img, tpl):
    N, m = img.shape[0], tpl.shape[0]
    t = tpl - tpl.mean()
    nt = np.sqrt((t * t).sum())
    if nt == 0:
        return None
    F = np.fft.rfft2(img)
    T = np.fft.rfft2(t[::-1, ::-1], s=img.shape)
    corr = np.fft.irfft2(F * T, s=img.shape)[m - 1:N, m - 1:N]
    ii = np.cumsum(np.cumsum(np.pad(img, ((1, 0), (1, 0))), 0), 1)
    ii2 = np.cumsum(np.cumsum(np.pad(img * img, ((1, 0), (1, 0))), 0), 1)
    def win(a):
        return a[m:, m:] - a[:-m, m:] - a[m:, :-m] + a[:-m, :-m]
    s1, s2 = win(ii), win(ii2)
    var = s2 - s1 * s1 / (m * m)
    den = np.sqrt(np.maximum(var, 1e-9)) * nt
    return corr / den

def best_fit(inner_path, outer_path, n=384, smin=1.05, smax=5.0, steps=90):
    outer = load(outer_path, n)
    best = None
    for s in np.exp(np.linspace(np.log(smin), np.log(smax), steps)):
        m = int(round(n / s))
        if m < 40 or m > n - 4:
            continue
        tpl = np.asarray(Image.open(inner_path).convert("L").resize((m, m), Image.LANCZOS), dtype=np.float64)
        r = ncc_map(outer, tpl)
        if r is None:
            continue
        idx = np.unravel_index(np.argmax(r), r.shape)
        score = r[idx]
        if best is None or score > best[0]:
            # Position/Groesse normiert auf 0..1 des aeusseren Bildes
            best = (score, n / m, idx[1] / n, idx[0] / n, m / n)
    return best

files = sorted(glob.glob(sys.argv[1] + "/*.png"), key=lambda p: int(re.search(r"_(\d+)\.png$", p).group(1)))
out = []
for a, b in zip(files, files[1:]):
    score, s, x, y, w = best_fit(a, b)
    ka = re.search(r"_(\d+)\.png$", a).group(1)
    kb = re.search(r"_(\d+)\.png$", b).group(1)
    cx, cy = x + w / 2, y + w / 2
    out.append(dict(inner=a, outer=b, pair=f"{ka}->{kb}", scale=round(s, 4),
                    cx=round(cx, 4), cy=round(cy, 4), score=round(float(score), 3)))
    print(f"{ka}->{kb}  scale={s:.3f}  center=({cx:.3f},{cy:.3f})  ncc={score:.3f}", flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
