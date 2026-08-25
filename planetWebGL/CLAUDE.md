# CLAUDE.md: WFC Planet

Ein Planet, der aus einem Wave Function Collapse wächst. Der Solver aus dem Nachbarprojekt «Wave Function Collapse» läuft auf einem groben Ikosaeder-Gitter; sein Rohrnetz wird Gelände: Distanz zum nächsten Rohr ist die Höhe, Rohre werden Gebirgskämme, Kreuzungen Gipfel, die leeren Zellen weitab die Tiefsee. Der User baut den Planeten klickweise auf (Grow), lässt ihn laufen (Auto) oder springt zum Endstand (Finish).

## Struktur

Ein einziges File: `index.html`. Rohes WebGL 1, keine Dependencies, kein Build. Zum Testen den Python-HTTP-Server nehmen.

## Wie es funktioniert

- **Zwei Gitter, eine Unterteilung**: `subdivide(freq)` baut beide aus demselben Ikosaeder, geteilte Punkte über ganzzahlige baryzentrische Schlüssel (keine Float-Nähte). `FREQ = 7` ist das Solver-Gitter (492 Zellen), `MESH_FREQ = 48` das Render-Mesh (23'042 Vertices). MESH_FREQ nicht über 80: die Indizes sind Uint16.
- **Solver**: Beobachten, kollabieren, propagieren, portiert und getrimmt. Kein Backtracking: ein Widerspruch säht neu (kommt bei diesen Grössen praktisch nie vor, `restarts` zählt mit). `settledFlag` beim Reset löschen, sonst zählt `settled` nach dem ersten Planeten nie wieder hoch.
- **Blank-Gewicht**: Ein einzelner Blank-Tile konkurriert gegen die Summe von ~57 Pipe-Tiles, sein Gewicht (48) muss in dieser Grössenordnung liegen, sonst füllt die Karte sich wandfüllend mit Rohren.
- **Meeresspiegel**: Kein fester Wert, sondern ein Perzentil (0.58) der Höhen aller gesetzten Zellen. Die Rohre gewinnen den Kollaps immer; absolute Höhen allein würden fast nichts ertränken. Das Perzentil hält den Landanteil erdähnlich (~40%), das Muster entscheidet nur noch, wo das Land liegt.
- **Höhenfeld**: BFS-Distanz zum nächsten Rohr über die gesetzten Zellen. Ungesetzte Zellen zählen als offenes Wasser, darum startet der Planet als Ozean und Land steigt beim Kollabieren auf. Grossskaliges fbm-Sway (±0.34) verhindert, dass alle Kämme gleich hoch sind.
- **Mesh-Sampling**: Jeder Mesh-Vertex mischt die drei nächsten Zellen invers distanzgewichtet, die Zuordnung ist einmalig vorberechnet (`nearCell`/`nearW`), weil das Gitter nie wandert. Darüber geseedetes Noise: Küstenzacken (`coastNoise`) und Fels-Rauheit (`roughNoise`, nur auf Land). Land wird nach dem Meeresspiegel-Abzug mit 1.6 gestreckt, damit Grate Fels und Schnee erreichen.
- **Morph**: `shownH` läuft jedem `targetH` mit 8% pro Frame nach; nur solange sich etwas bewegt, werden Positionen und Normalen neu gerechnet und hochgeladen. Ozean bleibt geometrisch eine glatte Kugel (Verschiebung nur für h > 0), darum liest sich das Wasser als Oberfläche und das Specular bleibt ruhig.
- **Rendering**: Drei Programme: Planet (Lambert mit zwei getönten Lichtquellen wie im WFC-Sketch: bläuliches Himmels-Ambient, warmweisses Hauptlicht), Sterne (fixe Punkte, himmelsfest statt planetenfest), Atmosphären-Halo (additiver Screen-Space-Ring). Wasserwirbel im Fragment-Shader in Modellkoordinaten, damit die Strömungen mit dem Planeten drehen.
- **Matrizen**: Von Hand, eine mat3-Rotation (Yaw um die Pole, dann Pitch) plus Distanz plus Perspektive. Kein Matrix-Stack nötig.

## Regeln

- Single-File-Charakter beibehalten: kein Build, keine Dependencies, kein Splitting ohne Auftrag.
- README und UI englisch, Codekommentare englisch, ganze Sätze, das Warum statt das Was.
- `DESIGN.md` vor visueller Arbeit lesen; Terrain-Rampe und Lichtfarben stehen dort und im Fragment-Shader.
- Ein Seed, ein Planet: Solver-RNG und Noise-Hash hängen beide am Planeten-Seed. Nichts einbauen, das unseeded `Math.random` in die Geometrie mischt.
- `preserveDrawingBuffer: true` bleibt an, solange Previews per `toDataURL` gezogen werden.

## Im Browser testen

Dieselben Fallen wie im WFC-Sketch: `requestAnimationFrame` steht in Hintergrund-Tabs still, also Animationen mit manuell getaktetem `frame(t)` treiben statt zu warten. `Finish` und `Grow` sind synchron und sofort messbar, aber der Morph braucht getaktete Frames, bis `shownH` die Targets erreicht hat.
