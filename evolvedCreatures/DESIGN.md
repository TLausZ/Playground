# DESIGN.md: Evolved Creatures

```yaml
color:
  sky: "#5BB8F5"          # Himmelblau, oberer Himmel
  horizon: "#D9EEFB"      # Horizont, Nebel, Hintergrund vor dem ersten Frame
  floor-light: "#FBF8F0"  # helles Schachfeld
  floor-dark: "#E2DACA"   # dunkles Schachfeld
  surface: "#FCFBF7"      # Dashboard, Schildchen
  rule: "#E3DFD3"         # Trennlinien, Raster in Diagrammen
  ink: "#26251F"          # Text, Pfeile im Genotyp-Graphen
  ink-2: "#5E5B52"        # Nebentext, Achsenbeschriftung
  node-0: "#2a78d6"       # Genom-Knoten 0 (Wurzel), blau
  node-1: "#eb6834"       # Knoten 1, orange
  node-2: "#1baf7a"       # Knoten 2, aqua
  node-3: "#eda100"       # Knoten 3, gelb
  best: "#6250d6"         # Diagramm: beste Fitness
  mean: "#8f8c84"         # Diagramm: mittlere Fitness, Sollwinkel, Rhythmus im Netz
  w-pos: "#26251F"        # Netz: positive Gewichte und Aktivierungen
  w-neg: "#d55181"        # Netz: negative Gewichte (gestrichelt) und Aktivierungen
  highlight: "#e34948"    # roter Umriss der Kreatur beim Hover über ihren Namen; in stats.html der pulsierende Punkt vor «live»
  coral-side: "#E2614D"   # Parcours: Streifen der Slalomstangen
  bumps: ["#B79BFF", "#FF8A6B"]      # Parcours, je Hindernis [Lauffläche, Seite]
  bars: ["#FF77B4", "#B79BFF"]
  balls: ["#C9F25A", "#FF77B4"]      # lose Kugeln: [leicht, schwer]
  wedges: ["#5EE3E8", "#C9F25A"]
  staircase: ["#FF8A6B", "#5EE3E8"]
typography:
  body: system-ui, -apple-system, sans-serif
  mono: ui-monospace, "SF Mono", Menlo, monospace  # alle Zahlen
floor:
  square: 1 m
ghost:
  fade-to-white: [0.35, 0.5, 0.65]   # jüngster bis ältester
  opacity: [0.42, 0.32, 0.24]
```

Die Tokens stehen als CSS-Variablen in `:root` von `index.html`. Three.js und die Canvas-Diagramme lesen sie von dort.

Die Szene ist ein heller Tag: himmelblauer Himmel, der zum Horizont hin ausbleicht, und ein Schachboden in zwei Papiertönen. Der Boden bleibt blass, damit die Kreaturen die einzigen kräftigen Farben im Bild sind. Ein Feld ist 1 m gross, so kann man Strecken am Boden ablesen.

Die vier Knotenfarben tragen Bedeutung: Ein Glied hat die Farbe des Genom-Knotens, aus dem es gebaut wurde. Dieselbe Farbe hat der Knoten im Genotyp-Graphen und die Kurve des Gelenks im Dashboard. Die Reihenfolge blau, orange, aqua, gelb ist fest und auf Unterscheidbarkeit bei Farbsehschwäche geprüft. Aqua und Gelb haben auf der hellen Fläche weniger als 3:1 Kontrast, darum steht im Graphen unter jedem Knoten eine Beschriftung. Ein fünfter Knoten bekäme keine neue Farbe; das Genom ist auf vier begrenzt.

Ghosts tragen dieselben Knotenfarben, zu Weiss hin aufgehellt und halbtransparent, je älter desto blasser. Sie werfen keinen Schatten.

Im Dashboard ist Farbe den Daten vorbehalten. Text ist immer `ink` oder `ink-2`, nie eine Datenfarbe. Die beste Fitness ist violett, weil Violett keine Knotenfarbe ist; die mittlere Fitness und der Sollwinkel sind grau, weil sie Vergleichslinien sind. Flach: keine Schatten und keine Verläufe im UI (einzige Ausnahme: der leuchtende «live»-Punkt in `stats.html`, wie ein «On air»-Zeichen), 1px-Linien in `rule`. Überschriften der Abschnitte klein, in Versalien und `ink-2`.

Im Parcours (`course.html`) hat jedes Hindernis seine Farbe im Grundkörper: Koralle, Lavendel, Pink, Limette, Türkis. Die Laufflächen, also wo die Kreatur das Hindernis berührt, tragen die Grundfarbe eines anderen Hindernisses (ursprünglich des nächsten; seit dem Tausch von Slalom und letzter Treppe stimmt die Reihenfolge nicht mehr, die Farben blieben) und leuchten leicht von selbst (`emissive`); so unterscheiden sie sich in der Farbe vom Grundkörper, nicht nur in der Helligkeit (Wunsch von TLausZ). Keine der Farben ist eine Knotenfarbe, so heben sich die Glieder ab. Teile eines Hindernisses leuchten abwechselnd stärker und schwächer, sonst verschmelzen gleich hohe Stufen von oben zu einer Fläche. Die Slalomstangen sind gestreift, `coral-side` und `surface` im 10-cm-Takt. Start, Bahnränder und Ziel sind `ink`, das Ziel als Schachmuster. In den Übersichten von oben (Dashboard, `stats.html`) trägt jedes Hindernis die Farbe seiner Lauffläche, weil man von oben nur sie sieht.
