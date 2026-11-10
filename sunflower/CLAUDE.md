# Sunflower

Video über die Platzverteilung von Sonnenblumenkernen: der Drehwinkel läuft von 0° bis 360° in 0.1°-Schritten, links die Blume, rechts der Graph «Winkel gegen Kernenanzahl». Erstes Teilprojekt im Playground, das kein Browser-Code ist, sondern ein ManimGX-Video.

## Struktur

- `sunflower.py`: die Szene `Sunflower` für [ManimGX](https://github.com/academa-labs/manimgx) 0.1.1 (Manim-CE-API, `import manimgx as m`). Kein ManimGL, kein ManimCE.
- `sunflower.mp4`: 1920×1080, 60 fps, 78.8 s.
- `index.html`: zeigt nur das Video, damit der «live:»-Link der Landingpage etwas öffnet.
- `preview.webp`: 72 Frames à 250 ms, 480×270, aus Sekunde 23 bis 41 des Videos (Verlangsamung und Halt beim goldenen Winkel).

Installation: `uv tool install --python 3.14 manimgx`. Rendern und neu kodieren:

```
manimgx render sunflower.py Sunflower -r 1920x1080 --fps 60 -o sunflower.mp4
ffmpeg -i sunflower.mp4 -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart out.mp4
```

Der Render dauert rund 40 s. Der ManimGX-Export ist 57.6 MB, mit crf 28 sind es 35 MB, ohne sichtbaren Verlust bei den Punkten. Selbsttest: `python sunflower.py` mit dem Python aus dem manimgx-Tool-Env (`$(dirname $(readlink -f $(which manimgx)))/python`) prüft vier Zählwerte. `manimgx inspect sunflower.py Sunflower` schreibt ein Storyboard und meldet Layout-Kollisionen.

## Wie es funktioniert

Vogel-Modell: Samen n (1 bis 1'500) liegt bei Radius √n und Winkel n·θ. Alle Samen haben denselben Durchmesser `SEED = 1.6` (Modelleinheiten). Kernenanzahl für θ: Samen werden von innen nach aussen gesetzt, bis der erste einen früheren überlappt; gezählt wird bis dorthin, also das kleinste J aller Paare (I, J) mit Abstand unter `SEED`. Deckel ist 1'500, die volle Scheibe. Die Rechnung ist Brute Force über alle rund 1.1 Mio. Paare pro Winkel und läuft beim Import für alle 3'603 Winkel, rund 12 s.

`ANGLES` ist das 0.1°-Raster plus der exakte goldene Winkel 137.508° und sein Spiegel 222.492°. Das Raster verfehlt ihn um 0.008°, und dort springt die Zahl von 465 (bei 137.5°) auf 1'500. Ohne die zwei Extrapunkte zeigt das Video den Effekt nicht. Getrieben wird alles über einen `ValueTracker` mit dem Index in `ANGLES`, ein Index pro Frame bei voller Geschwindigkeit. Um den goldenen Winkel herum laufen je 15 Schritte über 6 s, dazwischen ein Halt von 3.3 s mit gestrichelter Linie und «golden angle».

Die Blume ist ein `PMobject`. Ein Updater setzt Punkte und Farben pro Frame: Samen bis zur ersten Überlappung von Braun innen nach Gelb aussen, die übrigen grau. Die Kurve ist ein `VMobject` mit `set_points_as_corners` bis zum aktuellen Index.

## Regeln

- `SEED` nicht verkleinern: bei 1.5 füllt auch 99.5° die Scheibe (ebenfalls ein Winkel aus dem goldenen Schnitt), bei 1.4 weitere Winkel zwischen 80° und 105°. Dann ist die Aussage «137.5° ist der beste Winkel» im Graphen nicht mehr sichtbar. Bei 1.65 schafft kein Winkel mehr als 9 Samen.
- Beschriftung im Video Englisch wie der Rest des Playgrounds.
- Video unter 50 MB halten (GitHub-Warnschwelle), darum die Neukodierung.
