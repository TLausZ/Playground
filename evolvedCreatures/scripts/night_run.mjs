#!/usr/bin/env node
// Lange Läufe ohne Browser: dieselbe Evolution wie index.html (der <core>-Block wird ausgeschnitten),
// headless in Node, mehrere Läufe parallel. Jeder Lauf schreibt alle 1000 Generationen, alle 10 Minuten und am Ende
// eine Datei im Format von «Export run», die stats.html unter «Compare runs» lädt.
//
//   node scripts/night_run.mjs 8h
//   node scripts/night_run.mjs 3h --runs 4 --name tuned mutations=3 islands=4 net=1
//
// Dauer: 30m, 3h oder 1.5h. Einstellungen wie in der URL der Seite (Schlüssel aus SPEC), alles
// andere bleibt Standard. --runs: parallele Läufe (Standard 1), --name: Teil des Dateinamens,
// --dir: Ordner, relativ zum Projekt oder absolut (Standard runs).
// Ergebnis: <dir>/Evolved Creatures night <name> <n>.json. Auf dem Mac bleibt das System wach, solange
// das Skript läuft; der Bildschirm darf ausgehen.
// Braucht Node 18 oder neuer. MuJoCo kommt aus scripts/.cache (beim ersten Lauf von jsDelivr geladen).
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url)), ROOT = path.dirname(HERE);
const args = process.argv.slice(2);
const flag = (name, def) => { const i = args.indexOf(name); return i < 0 ? def : args.splice(i, 2)[1]; };
const runs = Math.max(1, +flag('--runs', 1) || 1), name = flag('--name', 'run'), worker = flag('--worker', null), dir = flag('--dir', 'runs');
const dur = args.find(a => /^\d+(\.\d+)?[mh]$/.test(a)) ?? '8h';
const settings = Object.fromEntries(args.filter(a => a.includes('=')).map(a => a.split('=')));
const ms = parseFloat(dur) * (dur.endsWith('h') ? 3600000 : 60000);

// Mehrere Läufe: dieses Skript startet sich selbst je einmal pro Lauf.
if (worker === null && runs > 1) {
  if (process.platform === 'darwin') spawn('caffeinate', ['-i', '-w', String(process.pid)], { stdio: 'ignore' });
  console.log(`${runs} runs, ${dur}, ${JSON.stringify(settings)}, files in ${dir}/`);
  const kids = Array.from({ length: runs }, (_, i) =>
    spawn(process.execPath, [fileURLToPath(import.meta.url), ...process.argv.slice(2).filter((a, k, all) => a !== '--runs' && all[k - 1] !== '--runs'), '--worker', String(i + 1)], { stdio: 'inherit' }));
  await Promise.all(kids.map(k => new Promise(r => k.on('exit', r))));
  process.exit(0);
}
if (worker === null && process.platform === 'darwin') spawn('caffeinate', ['-i', '-w', String(process.pid)], { stdio: 'ignore' });

// MuJoCo einmal laden und neben das Skript in den Cache legen.
const CACHE = path.join(HERE, '.cache', 'mujoco-node'), BASE = 'https://cdn.jsdelivr.net/npm/@mujoco/mujoco@4.0.1/';
mkdirSync(CACHE, { recursive: true });
for (const f of ['mujoco.js', 'mujoco.wasm']) {
  if (!existsSync(path.join(CACHE, f))) writeFileSync(path.join(CACHE, f), Buffer.from(await (await fetch(BASE + f)).arrayBuffer()));
}
const loadMujoco = (await import(pathToFileURL(path.join(CACHE, 'mujoco.js')).href)).default;
const mujoco = await loadMujoco({ wasmBinary: readFileSync(path.join(CACHE, 'mujoco.wasm')) });

const core = '//' + readFileSync(path.join(ROOT, 'index.html'), 'utf8').split('//<core>')[1].split('//</core>')[0];
const A = new Function('mujoco', 'SETTINGS_RAW', core + `; return { evolveStep, S, COLUMNS,
  get generation(){return generation}, get history(){return history}, get events(){return events}, get reseeds(){return reseeds}, ends: ENDS };`)(mujoco, settings);

const n = worker ?? 1, out = path.resolve(ROOT, dir, `Evolved Creatures night ${name} ${n}.json`), t0 = Date.now(), startedAt = new Date().toISOString();
mkdirSync(path.dirname(out), { recursive: true });
const save = () => writeFileSync(out, JSON.stringify({ format: 'evolvedCreaturesRun', version: 1, exportedAt: new Date().toISOString(), startedAt,
  settings: A.S, columns: A.COLUMNS, generation: A.generation, reseeds: A.reseeds, history: A.history, events: A.events,
  ends: A.ends.map(([x, y, k]) => [Math.round(x * 100) / 100, Math.round(y * 100) / 100, k]) }));
let next = 1000, saved = Date.now();
while (Date.now() - t0 < ms) {
  A.evolveStep(200);
  if (Date.now() - saved > 600000) { save(); saved = Date.now(); }   // auch alle 10 min, falls ein Lauf früh abbricht
  if (A.generation >= next) {
    save();
    console.log(`${name} ${n}: generation ${next}, best ${A.history[next - 1][0]}, ${Math.round((Date.now() - t0) / 60000)} min`);
    next += 1000;
  }
}
save();
console.log(`${name} ${n}: done, ${A.generation} generations, best ${A.history.at(-1)?.[0]}, ${out}`);
process.exit(0);
