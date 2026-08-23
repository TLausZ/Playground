# DESIGN.md: Block-Cloud

```yaml
color:
  cream: "#F7F1E3"      # Hintergrund, Seitenfläche
  beige: "#E8DCC4"      # Header, Panels
  sand: "#D9C7A0"       # Ränder, hellste Punkte
  brown: "#8C6B4F"      # Mittelton, Buttons, Akzente
  dark-brown: "#4E3B2A" # Text, dunkelste Punkte
typography:
  body: system-ui, -apple-system, sans-serif
  mono: ui-monospace, "SF Mono", Menlo, monospace  # Zahlen, Hashes, Blockhöhen
cubes:
  gradient: "#AED581 -> #FFF176 -> #FFB74D -> #EF5350"  # Feerate wie mempool.space: grün = günstig, rot = teuer, helle Töne
  edges: brown
  fog: cream  # Tiefenwirkung gegen Hintergrund
```

Farbwelt des UI angelehnt an das Bitcoin-Wiki: warmes Papier-Creme statt Weiss, Braun
statt Schwarz. Fehler und Status in Brauntönen, Unterscheidung über Text. Einzige
Ausnahme: Die Würfel der 3D-Ansicht tragen die Feerate-Skala von mempool.space
(grün bis rot), in helle Töne übersetzt, damit sie zur Papier-Optik passen.

Zahlen im UI in Mono und mit Schweizer Tausendertrennzeichen (de-CH).
Flaches Design: keine Schatten, keine Verläufe im UI (der Verlauf gehört den Punkten),
1px-Ränder in `sand`.
