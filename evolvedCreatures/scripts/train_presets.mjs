#!/usr/bin/env node
// Vortraining der Vorlagen: Der Körper ist von Hand gebaut und bleibt fest, die Evolution sucht nur den Gang
// (Frequenz, Gelenkbereich, Amplitude, Phasen, zweite Achse, Wellenform, Gelenkachsen). Fitness wie in
// index.html auf freier Fläche: Strecke in 6 s mal upright. Ein Prozess pro Vorlage.
//
//   node scripts/train_presets.mjs 25m
//   node scripts/train_presets.mjs 10m --only spider
//
// Schreibt presets/<key>.js nach jeder Runde: ein Aufruf PRESET({...}) mit Stand, bestem Genom und dessen
// Bewegung als Aufzeichnung (Lage und Drehung jedes Glieds, 25 Bilder pro Sekunde). creatures.html lädt diese
// Dateien als Skript nach, das geht auch unter file://, und spielt die Aufzeichnung ohne Physik ab.
import { readFileSync, writeFileSync, mkdirSync, renameSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url)), ROOT = path.dirname(HERE), OUT = path.join(ROOT, 'presets');
const args = process.argv.slice(2);
const flag = (name, def) => { const i = args.indexOf(name); return i < 0 ? def : args.splice(i, 2)[1]; };
const only = flag('--only', null), key = flag('--worker', null);
const dur = args.find(a => /^\d+(\.\d+)?[mh]$/.test(a)) ?? '25m';
const ms = parseFloat(dur) * (dur.endsWith('h') ? 3600000 : 60000);

// Körper. Gene in [0,1] wie im Kern: Knoten v = [Länge, Breite, Höhe, Gelenkbereich, Amplitude],
// Verbindung v = [Versatz am Elternglied, Yaw, Pitch, Skalierung, Phase, Phase des gespiegelten Kinds].
// Yaw 0,5 zeigt nach vorn, 0,75 zur Seite; Pitch über 0,5 zeigt nach unten. Form: 0 Quader, 2 Kapsel, 4 Ellipsoid.
const W = [...Array(21).fill(0.5), 0.5, 0.5, 0.5];   // Netz stumm
const node = (shape, size, o = {}) => ({ v: [...size, o.range ?? 0.5, o.amp ?? 0.6], w: [...W], axis: o.axis ?? 2, recur: o.recur ?? 1, shape,
  hip: o.hip ?? 0, hv: [0.4, 0.5, 0.25], sk: [0.5], conns: [] });
const conn = (to, offset, yaw, pitch, phase, o = {}) => ({ to, v: [offset, yaw, pitch, o.scale ?? 0.8, phase, o.side ?? 0.5], mirror: o.mirror ?? true, terminal: false });
const body = (kind, freq, nodes, links) => { for (const [from, c] of links) nodes[from].conns.push(c); return { v: [freq], nodes, kind }; };
const BODIES = {
  quadruped: body('Quadruped', 0.4,
    [node(0, [0.8, 0.3, 0.15]), node(2, [0.35, 0.03, 0.03], { hip: 2 }), node(2, [0.35, 0.02, 0.02], { axis: 1, amp: 0.4 })],
    [[0, conn(1, 0.9, 0.75, 0.8, 0)], [0, conn(1, 0.1, 0.75, 0.8, 0.5)], [1, conn(2, 1, 0.5, 0.62, 0.25, { mirror: false })]]),
  worm: body('Worm', 0.4,
    [node(2, [0.35, 0.15, 0.15], { axis: 1, recur: 5, hip: 1 })],
    [[0, conn(0, 1, 0.5, 0.5, 0.2, { mirror: false })]]),
  spider: body('Spider', 0.5,
    [node(4, [0.35, 0.5, 0.3]), node(2, [0.5, 0.02, 0.02], { hip: 2 })],
    [[0, conn(1, 0.9, 0.667, 0.69, 0)], [0, conn(1, 0.63, 0.722, 0.69, 0.5)], [0, conn(1, 0.37, 0.778, 0.69, 0)], [0, conn(1, 0.1, 0.833, 0.69, 0.5)]]),
  grasshopper: body('Grasshopper', 0.4,
    [node(2, [0.7, 0.15, 0.15]), node(2, [0.6, 0.1, 0.1], { axis: 1 }), node(2, [0.8, 0.03, 0.03], { axis: 1, range: 0.8 }), node(2, [0.2, 0.02, 0.02], { hip: 2, amp: 0.3 })],
    [[0, conn(1, 0.2, 0.917, 0.28, 0, { side: 0 })], [1, conn(2, 1, 0.5, 1, 0.25, { mirror: false })], [0, conn(3, 0.9, 0.72, 0.78, 0.5)]]),
  centipede: body('Centipede', 0.5,
    [node(0, [0.25, 0.25, 0.1], { recur: 3, amp: 0.2 }), node(2, [0.45, 0.02, 0.02], { hip: 2 })],
    [[0, conn(1, 0.5, 0.75, 0.7, 0)], [0, conn(0, 1, 0.5, 0.5, 0.33, { mirror: false })]]),
  biped: body('Biped', 0.3,
    [node(0, [0.1, 0.5, 0.5]), node(2, [0.25, 0.1, 0.1], { hip: 2, amp: 0.4 }), node(2, [0.25, 0.06, 0.06], { amp: 0.3 }), node(0, [0.35, 0.3, 0], { axis: 1, amp: 0.2 })],
    [[0, conn(1, 0.5, 0.75, 0.92, 0)], [1, conn(2, 1, 0.5, 0.5, 0.25, { mirror: false })], [2, conn(3, 1, 0.25, 0.5, 0, { mirror: false })]]),
};

// Ohne --worker: ein Prozess pro Vorlage, auf dem Mac bleibt das System wach.
if (key === null) {
  if (process.platform === 'darwin') spawn('caffeinate', ['-i', '-w', String(process.pid)], { stdio: 'ignore' });
  const keys = only ? [only] : Object.keys(BODIES);
  console.log(`${keys.join(', ')}: ${dur}, files in presets/`);
  const kids = keys.map(k => spawn(process.execPath, [fileURLToPath(import.meta.url), dur, '--worker', k], { stdio: 'inherit' }));
  await Promise.all(kids.map(k => new Promise(r => k.on('exit', r))));
  process.exit(0);
}

const CACHE = path.join(HERE, '.cache', 'mujoco-node');   // night_run.mjs lädt MuJoCo dorthin
const loadMujoco = (await import(pathToFileURL(path.join(CACHE, 'mujoco.js')).href)).default;
const mujoco = await loadMujoco({ wasmBinary: readFileSync(path.join(CACHE, 'mujoco.wasm')) });
const core = '//' + readFileSync(path.join(ROOT, 'index.html'), 'utf8').split('//<core>')[1].split('//</core>')[0];
const A = new Function('mujoco', 'SETTINGS_RAW', core + '; return { evaluate, hatch, advance, free, importGenome, nameOf, N, DT };')(mujoco, { course: 0, hip: 1, wave: 1 });

const rnd = n => Math.floor(Math.random() * n), pick = a => a[rnd(a.length)];
const clamp01 = v => Math.min(1, Math.max(0, v));
// Nur Gene der Steuerung. Grössen, Winkel und Ansatzpunkte der Glieder bleiben, wie sie gebaut sind.
function mutate(G) {
  const g = structuredClone(G), conns = g.nodes.flatMap(n => n.conns);
  for (let k = 1 + rnd(3); k > 0; k--) {
    if (Math.random() < 0.15) { const n = pick(g.nodes); if (Math.random() < 0.5) n.axis = rnd(3); else n.hip = rnd(3); continue; }
    const [a, i] = pick([[g.v, 0], ...g.nodes.flatMap(n => [[n.v, 3], [n.v, 4], [n.hv, 0], [n.hv, 1], [n.hv, 2], [n.sk, 0]]), ...conns.flatMap(c => [[c.v, 4], [c.v, 5]])]);
    a[i] = clamp01(a[i] + (Math.random() + Math.random() + Math.random() - 1.5) * 0.4);
  }
  return g;
}

// Aufzeichnung: pro Bild und Glied Lage (3) und Drehung als Quaternion x, y, z, w (4), ab Sekunde 0 samt Settling.
const EVERY = 8, r3 = v => Math.round(v * 1000) / 1000;
function quat(m, o) {   // Rotationsmatrix (zeilenweise ab o) zu Quaternion
  const [a, b, c, d, e, f, g, h, i] = m.subarray(o, o + 9), t = a + e + i;
  if (t > 0) { const s = 2 * Math.sqrt(t + 1); return [(h - f) / s, (c - g) / s, (d - b) / s, s / 4]; }
  if (a > e && a > i) { const s = 2 * Math.sqrt(1 + a - e - i); return [s / 4, (b + d) / s, (c + g) / s, (h - f) / s]; }
  if (e > i) { const s = 2 * Math.sqrt(1 + e - a - i); return [(b + d) / s, s / 4, (f + h) / s, (c - g) / s]; }
  const s = 2 * Math.sqrt(1 + i - a - e); return [(c + g) / s, (f + h) / s, s / 4, (d - b) / s];
}
function record(g) {
  const c = A.hatch(g), frames = [];
  const geoms = c.nodes.map((n, k) => ({ t: c.model.geom_type[k + 1], s: Array.from(c.model.geom_size.subarray((k + 1) * 3, (k + 1) * 3 + 3), r3), n }));
  for (;;) {
    const f = [];
    for (let k = 1; k <= c.limbs; k++) f.push(...Array.from(c.data.geom_xpos.subarray(k * 3, k * 3 + 3), r3), ...quat(c.data.geom_xmat, k * 9).map(r3));
    frames.push(f);
    if (c.step >= A.N) break;
    A.advance(c, Math.min(EVERY, A.N - c.step));
  }
  A.free(c);
  return { geoms, frames, fps: 1 / (EVERY * A.DT) };
}

const ISLANDS = 3, POP = 20, KEEP = 5;
const start = A.importGenome(BODIES[key]);
if (!start) throw new Error(key + ': body is not a valid genome');
const score = g => ({ g, ...A.evaluate(g) });
const islands = Array.from({ length: ISLANDS }, () => [score(start), ...Array.from({ length: POP - 1 }, () => score(mutate(mutate(start))))]);
const t0 = Date.now(), history = [], file = path.join(OUT, key + '.js');
let best = null, replay = null, rounds = 0, evals = ISLANDS * POP;
mkdirSync(OUT, { recursive: true });
function save(done) {
  const text = `PRESET(${JSON.stringify({ key, kind: start.kind, name: A.nameOf(best.g), rounds, evals, done, fit: r3(best.fit), dist: r3(best.dist), heading: r3(best.heading),
    foundAt: best.round, history, minutes: Math.round((Date.now() - t0) / 6000) / 10, of: ms / 60000, genome: best.g, ...replay })})\n`;
  writeFileSync(file + '.tmp', text); renameSync(file + '.tmp', file);   // nie eine halbe Datei für die Seite
}
for (;;) {
  for (const isl of islands) isl.sort((a, b) => b.fit - a.fit);
  const top = islands.map(i => i[0]).sort((a, b) => b.fit - a.fit)[0];
  if (top !== best) { best = top; best.round = rounds; replay = record(best.g); }
  history.push(Math.round(best.fit * 100) / 100);
  const done = Date.now() - t0 >= ms;
  save(done);
  if (done) break;
  for (const isl of islands) { isl.length = KEEP; while (isl.length < POP) isl.push(score(mutate(isl[rnd(KEEP)].g))); evals += POP - KEEP; }
  rounds++;
}
console.log(`${key}: done, ${rounds} rounds, best ${best.fit.toFixed(2)}, ${A.nameOf(best.g)}`);
process.exit(0);
