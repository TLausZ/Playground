# DESIGN.md: WFC Planet

```yaml
color:
  space:
    background: "#04060b"        # page and GL clear, near-black blue
    star: "rgb(217, 227, 255)"   # star points, cold white
    halo: "rgb(77, 133, 217)"    # atmosphere band, additive
  ui:
    bg: "rgba(10, 14, 22, 0.78)" # panel, blurred
    border: "rgba(159, 216, 255, 0.22)"
    text: "rgba(226, 234, 244, 0.94)"
    text-muted: "rgba(226, 234, 244, 0.62)"
    accent: "#9fd8ff"            # titles, active button
  terrain:                       # fragment shader ramp, by height
    sea-deep: [0.03, 0.14, 0.24]
    sea-shallow: [0.12, 0.45, 0.50]
    sand: [0.66, 0.60, 0.44]
    grass: [0.22, 0.40, 0.20]
    forest: [0.12, 0.28, 0.15]
    rock: [0.42, 0.39, 0.34]
    snow: [0.93, 0.95, 0.97]
  light:
    ambient: [0.30, 0.36, 0.47]  # sky fill, faintly blue, all a shadow gets
    key: [0.98, 0.92, 0.80]      # warm white sun
type:
  family: system sans (ui-sans-serif stack)
  panel-title: 13px, uppercase, letter-spacing 0.12em, accent
  panel-body: 12-13px, line-height 1.45
layout:
  panel: fixed top-left, 250px, radius 14px, backdrop blur 12px
  canvas: fullscreen, planet centered
motion:
  terrain-morph: shownH -> targetH at 8% per frame
  idle-spin: 0.0016 rad per frame, pauses 3s after a drag
  ocean-swirl: slow sine field in model space, amplitude 6%
```

Die Bühne ist Weltraum: fast schwarzer Hintergrund, kaltweisse Sterne, ein
additiver blauer Atmosphärenring. Alles Helle und Warme gehört dem Planeten.

Das Terrain wird nicht durch Materialfarben dramatisiert, sondern durch Licht:
bläuliches Himmels-Ambient füllt die Schattenseiten, warmweisses Hauptlicht
die Sonnenseite, zusammen fast neutral. Die Rampe folgt der Höhe wie eine
hypsometrische Karte: Tiefsee, Schelf, Sandsaum, Gras, Wald, Fels, Schnee.
Steilhänge brechen unabhängig von der Höhe zu Fels.

Das UI bleibt ein einzelnes ruhiges Panel oben links, Akzentfarbe nur für den
Titel und den aktiven Auto-Knopf. Keine weiteren Farben im UI: die Show ist
der Planet.
