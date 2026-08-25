# CLAUDE.md: Wave Function Collapse

Eine Kachelkarte, die sich selbst baut. Jede Zelle startet als jede Kachel gleichzeitig, die unsicherste entscheidet sich, die Einschränkung wandert zu den Nachbarn, das Ganze setzt sich. Drei Lattices mit demselben Solver: Quadrat, Hexagon und eine Kugel, die man drehen kann.

## Struktur

Ein einziges File: `index.html`, Canvas 2D, keine Dependencies, kein Build. Für `file://` reicht es nicht mehr, seit die Auswahl im Fragment steht; zum Testen den Python-HTTP-Server nehmen.

Das gewählte Lattice steht im Hash (`index.html#sphere`), damit ein Lesezeichen darauf zeigen kann.

## Wie es funktioniert

- **Kachelsatz**: Eine Kachel ist nur ein Muster von Rohren, die durch die Kanten austreten. Zwei Zellen passen zusammen, wenn die geteilte Kante beidseitig gleich liest. Daraus entsteht der Satz von selbst: jede Kombination von Kanten ist eine Kachel, ohne die mit genau einem Rohr. Vier Kanten geben 12 Kacheln, fünf 27, sechs 58.
- **Solver**: Beobachten, kollabieren, propagieren, mit Trail für jede Entfernung und Stack für jede Vermutung, also mit Backtracking. Er erfährt nie, auf welchem Lattice er läuft: eine Zelle kennt nur ihre Nachbarn und für jede Kante den Slot, über den sie beim Nachbarn ankommt.
- **Kugel**: Die Zellen sind die Ecken eines unterteilten Ikosaeders, 10f²+2 Stück. Die unterste Slider-Stufe (`FOOTBALL`) ist ein Sonderfall: der abgestumpfte statt unterteilte Ikosaeder, also 12 Ecken plus 20 Flächenmittelpunkte, die 32 Zellen eines echten Fussballs.
- **Zellecken**: Eine Ecke ist der Punkt, der von den drei dort zusammentreffenden Zellen gleich weit entfernt ist, also die Normale des Dreiecks ihrer Mittelpunkte. Nicht durch den Schwerpunkt ersetzen, sonst kommen die Fünfecke des Fussballs so gross heraus wie die Sechsecke.
- **Formen**: Die Rohre zerschneiden die Oberfläche in geschlossene Formen, gefunden per Union-Find über Keile, einer pro Zellecke. Ein Rohr trennt die Keile links und rechts von sich, aber die Zellkante selbst ist nie eine Wand: ein Rohr reicht nur bis zur Kantenmitte, beide Kantenhälften bleiben offen. Genau deshalb läuft eine Form um Ecken herum in die Nachbarzelle.
- **Lift**: Grosse Formen sinken ein, kleine steigen auf, über fünf Stufen. Die Grössen werden vorher logarithmisch verteilt, weil eine Form den halben Globus bedecken kann, während zwei Dutzend andere einzelne Eckdreiecke sind.
- **Extrusion**: Eine Wand ist die Stufe zwischen zwei Formen und wird nur von der höheren gezeichnet. Beide bis zur Kugel hinunterzuziehen stapelt zwei Wände in zwei Farben, wo eine Fläche hingehört.
- **Shading**: Farbrampe nach Höhe in `DEEP` und `HIGH` (dunkler Schiefer bis fast weisser Stein). Das Licht in `SUN` sind zwei getönte Quellen: bläuliches Ambient als Himmelslicht, das allein die Schattenseiten füllt, und warmweisses Hauptlicht; voll beleuchtet summieren sie sich fast neutral. Nicht auf einen grauen Faktor zurückbauen, die kühlen Schatten sind der Tageslicht-Look. Konturlinien gibt es bei aktivem Lift keine: die Kante einer Form ist die Stufe selbst, Wand plus Helligkeitswechsel. Die Deckflächen bekommen einen Verlauf, keinen eigenen Lambert-Wert. Eine Zelle hat nur eine Normale, also kämen alle ihre Keile gleich hell heraus und jede Zelle zeichnete sich als Sechseck ab. Nicht auf flächenweises Licht zurückbauen. Die Wände behalten es, sie sind echte Facetten.
- **Malreihenfolge**: Deckflächen und Wände liegen in einer Liste, gemalt von hinten nach vorne. Der Sortierschlüssel ist der Winkel der Flächenrichtung zur Blickachse (cos θ der Einheitsrichtung), nicht die Tiefe eines Punkts. Der Körper ist sternförmig um den Kugelmittelpunkt, und entlang jedes Sehstrahls wächst dieser Winkel streng monoton, darum ist die Winkelordnung exakt und nicht heuristisch. Nicht auf Tiefen-Schlüssel zurückbauen: die tragen den Radius mit, angehobene und eingesunkene Flächen überholen sich beim Drehen, und das Bild flackert (zweimal passiert). WebGL mit Z-Buffer wäre die Alternative, aber erst nötig, falls Formen je überhängen und der Körper nicht mehr sternförmig ist. Nichts wird wegen Blickrichtung oder Horizont verworfen, sonst blinken Flächen weg, sobald die Drehung sie über die Schwelle schiebt. Der Kern sitzt auf dem Radius der tiefsten Form, sonst schaut sein Rand als dunkles Band zwischen den eingesunkenen und den angehobenen Formen hervor.

## Regeln

- Single-File-Charakter beibehalten: kein Build, keine Dependencies, kein Splitting ohne Auftrag.
- README und UI sind englisch, die Codekommentare auch. Sie erklären das Warum, nicht das Was, in ganzen Sätzen. Bewusste Vereinfachungen mit `ponytail:` markieren, samt Obergrenze und Ausbaupfad.
- Der Solver darf nicht wissen, auf welchem Lattice er läuft. Neue Geometrie kommt als Topologie dazu, nicht als Sonderfall im Solver.
- Es gibt keine DESIGN.md. Die Palette steht in `HOT`, `COOL`, `SUN`, `DEEP` und `HIGH` im File; vor visueller Arbeit dort nachsehen.

## Im Browser testen

Zwei Fallen, beide schon zweimal zugeschnappt:

- `requestAnimationFrame` läuft in einem Hintergrund-Tab nicht. Die Uhr `now` friert ein, und ein Screenshot zeigt den letzten Frame von vor einer halben Minute. Statt zu warten `frame(t)` mit selbst hochgezählter Zeit takten.
- `ctx.getImageData` stellt den Canvas in Chrome auf Software-Rendering um. Danach gemessene Frame-Zeiten sind um ein Vielfaches zu hoch. Nach einem Pixeltest neu laden, bevor Performance gemessen wird.

Der Panel-Text hinkt dem Solver einen Frame hinterher. Wartschleifen gegen `count` prüfen, nicht gegen `ui.state.textContent`, sonst bricht die Schleife sofort mit dem Text des vorigen Durchlaufs ab.
