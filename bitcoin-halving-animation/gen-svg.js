// Erzeugt die Flaechen-SVGs (Quadrate + Kreise) mit exakt derselben Geometrie
// wie index.html / buildFillSVG. Reine Mathematik, kein DOM.
const fs = require('fs');

const SIZES = [500, 250, 125, 62.5, 31.25, 15.625, 7.8125, 3.90625];
const R = SIZES.map((s) => s / Math.SQRT2);
const UNFOLD = [[0, -180], [50, 0], [100, 180]];
const SWEEP_STEPS = 360;
const dir = (k) => (k % 2 === 0 ? -1 : 1);

function angleAt(pct) {
  for (let i = 0; i < UNFOLD.length - 1; i++) {
    const [p0, v0] = UNFOLD[i], [p1, v1] = UNFOLD[i + 1];
    if (pct >= p0 && pct <= p1) return v0 + (v1 - v0) * (pct - p0) / (p1 - p0);
  }
  return UNFOLD[UNFOLD.length - 1][1];
}
const translate = (tx, ty) => [1, 0, 0, 1, tx, ty];
const rotate = (deg) => { const r = deg * Math.PI / 180, c = Math.cos(r), s = Math.sin(r); return [c, -s, s, c, 0, 0]; };
const mul = (A, B) => [
  A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3],
  A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3],
  A[0] * B[4] + A[1] * B[5] + A[4], A[2] * B[4] + A[3] * B[5] + A[5],
];
const apply = (M, x, y) => [M[0] * x + M[1] * y + M[4], M[2] * x + M[3] * y + M[5]];

function quadsFromAngle(a) {
  let M = translate(100, 1000);
  const quads = [];
  for (let i = 0; i < SIZES.length; i++) {
    if (i > 0) { M = mul(M, translate(SIZES[i - 1], -SIZES[i - 1])); M = mul(M, rotate(a)); }
    const s = SIZES[i];
    quads.push([[0, 0], [s, 0], [s, -s], [0, -s]].map(([x, y]) => apply(M, x, y)));
  }
  return quads;
}
const C0 = [600, 500 + R[0]];
function circlesFromAngle(a) {
  let M = translate(C0[0], C0[1]);
  const out = [{ c: apply(M, 0, 0), r: R[0] }];
  M = mul(M, translate(0, dir(0) * R[0]));
  for (let i = 1; i < SIZES.length; i++) {
    M = mul(M, rotate(a));
    out.push({ c: apply(M, 0, -dir(i - 1) * R[i]), r: R[i] });
    M = mul(M, translate(0, -2 * dir(i - 1) * R[i]));
  }
  return out;
}

const sweeps = SIZES.map(() => []);
const cSweeps = SIZES.map(() => []);
for (let k = 0; k <= SWEEP_STEPS; k++) {
  const pct = (k / SWEEP_STEPS) * 100;
  quadsFromAngle(angleAt(pct)).forEach((q, i) => sweeps[i].push(q));
  circlesFromAngle(angleAt(pct)).forEach((o, i) => cSweeps[i].push(o));
}

const PIVOT = [600, 500], TILT = -45;
const rotP = mul(translate(PIVOT[0], PIVOT[1]), mul(rotate(TILT), translate(-PIVOT[0], -PIVOT[1])));

function hull(pts) {
  const p = pts.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo = [];
  for (const q of p) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q); }
  const up = [];
  for (let k = p.length - 1; k >= 0; k--) { const q = p[k]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q); }
  lo.pop(); up.pop();
  return lo.concat(up);
}

const EXPORT_PAD = 2;
function buildFillSVG(circles) {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  const ext = (x, y) => { if (x < minX) minX = x; if (x > maxX) maxX = x; if (y < minY) minY = y; if (y > maxY) maxY = y; };
  let body;
  if (!circles) {
    let paths = '';
    for (let i = 0; i < sweeps.length; i++) {
      const s = sweeps[i]; let d = '';
      for (let k = 0; k < s.length - 1; k++) {
        const h = hull(s[k].concat(s[k + 1])).map((p) => apply(rotP, p[0], p[1]));
        for (const p of h) ext(p[0], p[1]);
        d += 'M' + h.map((p) => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join('L') + 'Z';
      }
      paths += `<path d="${d}"/>`;
    }
    body = `<g fill="#E8892E" fill-opacity="0.15" fill-rule="nonzero">${paths}</g>`;
  } else {
    let paths = '';
    {
      // Kreis 0 statisch -> gefuellte Scheibe statt Bahn-Stroke (siehe index.html).
      const [cx, cy] = C0;
      ext(cx - R[0], cy - R[0]); ext(cx + R[0], cy + R[0]);
      paths += `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${R[0].toFixed(1)}" fill="#E8892E" fill-opacity="0.15" stroke="none"/>`;
    }
    for (let i = 1; i < SIZES.length; i++) {
      const N = 32 * i, pts = [];
      for (let k = 0; k < N; k++) pts.push(circlesFromAngle(angleAt((k / N) * 100))[i].c);
      for (let k = 0; k < 360; k++) { const c = circlesFromAngle(angleAt((k / 360) * 100))[i].c; ext(c[0] - R[i], c[1] - R[i]); ext(c[0] + R[i], c[1] + R[i]); }
      let d = 'M' + pts[0][0].toFixed(1) + ',' + pts[0][1].toFixed(1);
      for (let k = 0; k < N; k++) {
        const p0 = pts[(k - 1 + N) % N], p1 = pts[k], p2 = pts[(k + 1) % N], p3 = pts[(k + 2) % N];
        const c1x = p1[0] + (p2[0] - p0[0]) / 6, c1y = p1[1] + (p2[1] - p0[1]) / 6;
        const c2x = p2[0] - (p3[0] - p1[0]) / 6, c2y = p2[1] - (p3[1] - p1[1]) / 6;
        d += 'C' + c1x.toFixed(1) + ',' + c1y.toFixed(1) + ' ' + c2x.toFixed(1) + ',' + c2y.toFixed(1) + ' ' + p2[0].toFixed(1) + ',' + p2[1].toFixed(1);
      }
      d += 'Z';
      // Jeder Kreis eigene Gruppe: opacity flacht die opake, sich selbst
      // kreuzende Bahn zu EINER Flaeche ab (sonst addieren sich Ueberkreuzungen
      // auf). Zwischen den Gruppen bleibt die additive Verdunkelung.
      paths += `<g opacity="0.15"><path d="${d}" stroke-width="${(2 * R[i]).toFixed(1)}"/></g>`;
    }
    body = `<g fill="none" stroke="#E8892E" stroke-linecap="round" stroke-linejoin="round">${paths}</g>`;
  }
  minX -= EXPORT_PAD; minY -= EXPORT_PAD; maxX += EXPORT_PAD; maxY += EXPORT_PAD;
  const vb = `${minX.toFixed(1)} ${minY.toFixed(1)} ${(maxX - minX).toFixed(1)} ${(maxY - minY).toFixed(1)}`;
  return { svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${body}</svg>`, vb };
}

const dir_out = process.argv[2];
const q = buildFillSVG(false), c = buildFillSVG(true);
fs.writeFileSync(dir_out + '/flaeche-quadrate.svg', q.svg);
fs.writeFileSync(dir_out + '/flaeche-kreise.svg', c.svg);
console.log('geschrieben: flaeche-quadrate.svg (' + fs.statSync(dir_out + '/flaeche-quadrate.svg').size + ' B), viewBox ' + q.vb);
console.log('           : flaeche-kreise.svg (' + fs.statSync(dir_out + '/flaeche-kreise.svg').size + ' B), viewBox ' + c.vb);
