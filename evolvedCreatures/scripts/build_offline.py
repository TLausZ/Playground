#!/usr/bin/env python3
"""Erzeugt «Evolved Creatures offline.html»: index.html mit allen Abhängigkeiten eingebettet.

Die Datei läuft per Doppelklick, ohne Server und ohne Internet. Quelle bleibt index.html;
die Versionen der Abhängigkeiten kommen aus dessen Importmap. Nach jeder Änderung an
index.html neu laufen lassen:

    python3 scripts/build_offline.py

Die heruntergeladenen Dateien liegen danach in scripts/.cache, ein zweiter Lauf braucht
kein Internet.
"""
import base64
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path(__file__).resolve().parent / ".cache"
OUT = ROOT / "Evolved Creatures offline.html"

html = (ROOT / "index.html").read_text(encoding="utf-8")
importmap = re.search(r'<script type="importmap">(.*?)</script>', html, re.S)
imports = json.loads(importmap.group(1))["imports"]

# Bare Specifier im Code -> URL. Der Addon-Präfix wird für die eine benutzte Datei aufgelöst.
ORBIT = "three/addons/controls/OrbitControls.js"
assert f"from '{ORBIT}'" in html, "index.html importiert OrbitControls nicht mehr wie erwartet"
sources = {
    "three": imports["three"],
    ORBIT: imports["three/addons/"] + "controls/OrbitControls.js",
    "mujoco": imports["mujoco"],
}
wasm_url = imports["mujoco"].rsplit("/", 1)[0] + "/mujoco.wasm"


def fetch(url):
    """Lädt url einmal und legt sie unter einem aus der URL abgeleiteten Namen in den Cache."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / re.sub(r"[^A-Za-z0-9.@-]+", "_", url.split("://", 1)[1])
    if not path.exists():
        print("lade", url)
        with urllib.request.urlopen(url) as response:
            path.write_bytes(response.read())
    return path.read_bytes()


def embed(name, data):
    # Base64, damit kein "</script" im eingebetteten Code das Tag beendet.
    return f'<script type="application/octet-stream" data-lib="{name}">{base64.b64encode(data).decode()}</script>'


blocks = [embed(name, fetch(url)) for name, url in sources.items()]
blocks.append(embed("wasm", fetch(wasm_url)))

# Startskript: aus den eingebetteten Modulen Blob-URLs machen und als Importmap eintragen,
# bevor das Modulskript der Seite lädt. Das WASM geht ohne fetch direkt an MuJoCo.
bootstrap = """<script>
  const bytes = name => {
    const text = atob(document.querySelector(`[data-lib="${name}"]`).textContent);
    const out = new Uint8Array(text.length);
    for (let i = 0; i < text.length; i++) out[i] = text.charCodeAt(i);
    return out;
  };
  const imports = {};
  for (const name of %s) imports[name] = URL.createObjectURL(new Blob([bytes(name)], { type: 'text/javascript' }));
  window.MUJOCO_WASM = bytes('wasm');
  const map = document.createElement('script');
  map.type = 'importmap';
  map.textContent = JSON.stringify({ imports });
  document.currentScript.after(map);
</script>""" % json.dumps(list(sources))

out = html.replace(importmap.group(0), "\n".join(blocks) + "\n" + bootstrap)
assert "window.MUJOCO_WASM" in html, "index.html übergibt MUJOCO_WASM nicht mehr an loadMujoco"
leftover = re.findall(r'https?://[^\s"\'`<>)]+', re.sub(r"<script type=\"application/octet-stream\".*?</script>", "", out, flags=re.S))
assert not leftover, f"noch externe URLs in der Seite: {leftover}"

OUT.write_text(out, encoding="utf-8")
print(f"{OUT.name}: {OUT.stat().st_size / 1e6:.1f} MB")
