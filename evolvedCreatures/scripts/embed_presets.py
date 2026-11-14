#!/usr/bin/env python3
"""Übernimmt die trainierten Vorlagen aus presets/<key>.js in den Kern von index.html.

Schreibt die Zeilen zwischen //<presets> und //</presets> neu: pro Vorlage das beste Genom, am Start
in Laufrichtung gedreht (yaw), und seine Strecke in 6 s auf freier Fläche. Aufruf nach scripts/train_presets.mjs:

    python3 scripts/embed_presets.py && python3 scripts/build_offline.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYS = ['quadruped', 'worm', 'spider', 'grasshopper', 'centipede', 'biped']   # Reihenfolge = Wert der Einstellung preset, ab 1

lines = []
for key in KEYS:
    text = (ROOT / 'presets' / f'{key}.js').read_text(encoding='utf-8').strip()
    d = json.loads(text[len('PRESET('):-1])
    g = d['genome']   # ungerundet: schon vier Stellen ändern den Gang (Vierfüssler 3,6 statt 10,5 m)
    g['yaw'] = round(-d['heading'], 4)   # am Start so gedreht, dass der trainierte Gang nach +x führt
    lines.append('  ' + json.dumps({'g': g, 'dist': d['dist']}, separators=(',', ':')) + ',')
    print(f"{key}: {d['name']}, {d['dist']} m, {d['rounds']} rounds")

page = ROOT / 'index.html'
s = page.read_text(encoding='utf-8')
a, b = s.index('//<presets>'), s.index('//</presets>')
page.write_text(s[:a] + '//<presets>\nconst PRESETS = [\n' + '\n'.join(lines) + '\n];\n' + s[b:], encoding='utf-8')
