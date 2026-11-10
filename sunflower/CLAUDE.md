# Sunflower

Video über die Platzverteilung von Sonnenblumenkernen: Titelfrage, dann läuft der Drehwinkel von 0° bis 360° in 0.1°-Schritten, links die Blume im gelben Umkreis, rechts der Graph «Winkel gegen Kernenanzahl». Erstes Teilprojekt im Playground, das kein Browser-Code ist, sondern ein ManimGX-Video.

## Struktur

- `sunflower.py`: die Szene `Sunflower` für [ManimGX](https://github.com/academa-labs/manimgx) 0.1.1 (Manim-CE-API, `import manimgx as m`). Kein ManimGL, kein ManimCE. `Preview` rendert zwei Standbilder (130° und 137.5°) zum Prüfen, bevor die ganze Animation läuft.
- `sunflower.mp4`: 1920×1080, 60 fps, 84.2 s, 30.5 MB.
- `index.html`: zeigt nur das Video, damit der «live:»-Link der Landingpage etwas öffnet.
- `preview.webp`: 72 Frames à 250 ms, 480×270, aus Sekunde 28.5 bis 46.5 des Videos (Verlangsamung und Halt beim goldenen Winkel).

Installation: `uv tool install --python 3.14 manimgx`. Rendern:

```
manimgx render sunflower.py Sunflower -r 1920x1080 --fps 60 -o sunflower.mp4
manimgx render sunflower.py Preview -o preview.mp4
```

Selbsttest: `python sunflower.py` mit dem Python aus dem manimgx-Tool-Env (`$(dirname $(readlink -f $(which manimgx)))/python`) prüft vier Zählwerte und das Maximum. Der Import rechnet alle 3'603 Winkel durch und dauert rund 55 s, jeder Render also auch. Der Render selbst braucht danach rund 20 s.

## Wie es funktioniert

Vogel-Modell: Same n liegt bei Radius c·√n und Winkel n·θ. Umkreis (Radius 1) und Samendurchmesser `SEED = 0.04` sind fix. Kernenanzahl für θ ist das grösste N, bei dem N Samen ohne Überlappung hineinpassen: Das Muster wird mit c = (1 − SEED/2)/√N so skaliert, dass der äusserste Same am Umkreis anliegt, und N passt, wenn dann der kleinste Abstand zweier Samen mindestens `SEED` ist. Der kleinste Abstand unter den ersten N Samen kommt für alle N aus einer einzigen Distanzmatrix (2000×2000, `np.minimum.accumulate` über den Abstand jedes Samens zu seinem nächsten Vorgänger). Gezeichnet werden nur diese N Samen, von Braun innen nach Gelb aussen.

Werte: 0° 12, 90° 50, 130° 450, 137.5° 1'440, 99.5° 1'486, goldener Winkel 137.508° 1'540 (Maximum).

`ANGLES` ist das 0.1°-Raster plus der exakte goldene Winkel und sein Spiegel 222.492°, die das Raster um 0.008° verfehlt. Getrieben wird alles über einen `ValueTracker` mit dem Index in `ANGLES`, ein Index pro Frame bei voller Geschwindigkeit. Um den goldenen Winkel laufen je 15 Schritte über 6 s, dazwischen ein Halt von 3.3 s mit gestrichelter Linie und «golden angle».

## Regeln

- Zählung nicht auf «bis zur ersten Überlappung» oder «Überlappende grau markieren» zurückbauen. Beides hatte die erste Fassung, und es war falsch: Gefragt ist, wie viele Samen maximal ohne Überlappung in den fixen Umkreis passen (Korrektur vom 10. November 2026).
- 99.5° kommt nahe an den goldenen Winkel heran. Das ist echt, ein weiterer Winkel aus dem goldenen Schnitt, kein Rechenfehler.
- Tracker-Werte in einer Szene über `self.play(... run_time=1 / FPS)` setzen, nicht mit `set_value` zwischen zwei `wait`: ManimGX übernahm sonst den letzten Wert für die ganze Szene.
- Titel am Anfang: «What's the best angle to fit the most seeds into a sunflower?» mit «Nature figured it out.» darunter. Der zweite Satz steht auf Wunsch am Anfang, nicht als Auflösung am Schluss.
- Beschriftung im Video Englisch wie der Rest des Playgrounds.
- Video unter 50 MB halten (GitHub-Warnschwelle). Wird es grösser, mit ffmpeg neu kodieren (`-c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart`).
