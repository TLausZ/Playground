# CLAUDE.md — Block-Cloud

3D-Visualisierung eines Bitcoin-Blocks in einer Three.js-Szene, zwei umschaltbare Ansichten (Select im Header): «Würfel» (Würfelstadt in Blockreihenfolge) und «Ringe» (radialer Treemap als extrudierte Donut-Stücke, Zikkurat-Form). Jede Transaktion ein Würfel bzw. Ringsegment, Grösse/Fläche aus vsize, Farbe aus Feerate (grün = günstig, rot = teuer, Skala wie mempool.space). Blockhöhe eingeben, Block wird von der mempool.space-API geladen.

## Struktur

Ein einziges File: `index.html`. Kein Build, keine Dependencies ausser Three.js via CDN-Importmap (v0.166.0). Öffnen im Browser genügt; wegen fetch auf mempool.space via `python3 -m http.server` serven (kein PHP auf dieser Maschine).

## Wie es funktioniert

- **API**: `mempool.space/api` — Blockhöhe → Hash → Blockdaten → Tx-Summary (`fee`, `vsize` pro Tx). Beim Start wird der Tip-Block geladen.
- **Packing**: `BlockLayout`/`Row`/`Slot` sind ein Port des Packing-Algorithmus aus der mempool-2D-Blockansicht (block-scene.ts, AGPL): 86er-Grid, jede Tx ein Quadrat, platziert in der tiefsten passenden Lücke. Nicht umschreiben — das Layout soll der mempool-Ansicht entsprechen.
- **3D**: Das 2D-Packing wird nach oben extrudiert (Höhe = Kantenlänge, vsize bestimmt alle drei Dimensionen). Eine `InstancedMesh` für alle Würfel, ein `LineSegments` für alle Kanten. Aufbau-Animation ~1s von vorne nach hinten, OrbitControls mit Auto-Rotate.
- **Ringe**: eigener Layout-Algorithmus (`ringLayout`), kein d3. Konzentrische Ringe von innen nach aussen nach Feerate-Rang sortiert (hohe Feerate im Zentrum), Segmentfläche exakt proportional zur vsize: die d-Heuristik (√ der grössten Tx, gedeckelt, mit Lookahead) gruppiert nur, die Endgeometrie rechnet Ringdicke aus der tatsächlichen Ringfläche und Winkel als Flächenanteile. 3D via `ExtrudeGeometry` aus `Shape.absarc`-Donut-Stücken, Höhe = Ringdicke, pro Ring eine gemergte Geometrie (`buildRings`), Aufbau-Animation skaliert Ringe von innen nach aussen (~1 s). Default ist eine explodierte Darstellung: Ringe radial auseinandergezogen (1.2 Welteinheiten pro Ring), deutliche Fugen zwischen den Segmenten. Umschalten via `show()` (Group-Visibility, gleiche Szene/Kamera).
- **Farbe**: rohe Feerate `fee/vsize` (bewusst nicht das effektive `rate`-Feld), log-skaliert, pro Block auf 5.–95. Perzentil normalisiert (`feeTints`, von beiden Ansichten genutzt).
- **Selbsttest**: `console.assert` in `buildCubes` prüft die ersten 300 Quadrate auf Überlappung.

## Regeln

- `DESIGN.md` vor visueller Arbeit lesen: Papier-Creme/Braun-Palette, flaches UI, einzige Farbausnahme ist die Feerate-Skala der Würfel.
- UI-Sprache Deutsch, Zahlen in de-CH (Tausendertrennzeichen, Komma).
- Single-File-Charakter beibehalten: kein Build-Setup, kein Splitting ohne Auftrag.
