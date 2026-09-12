# Sliced Portrait

Nachbau einer Papierarbeit von tete.au.carre (Instagram): Porträt spiegeln, in Streifen schneiden, umlegen, wiederholen.

## Struktur

`index.html` plus `warhol.jpg` als Vorlage. Farben, Schrift und Panel-Masse in `DESIGN.md`, übernommen von Contour Drawing im Plotter-Projekt; vor visueller Arbeit lesen. Kein Build. Braucht den Python-HTTP-Server aus dem Repo-Root, per `file://` ist das Canvas mit dem Vorlagebild tainted (kein Download, kein `getImageData`). Uploads laufen auch per `file://`.

## Wie es funktioniert

Der ganze Algorithmus ist eine Funktion `pass()`, die mehrfach angewendet wird:

1. `prepare(img, max)`: Bild auf höchstens `max` px längste Seite skalieren, optional Graustufen. Vorschau 1400 px, Export die halbe gewünschte Kantenlänge.
2. `mirror()`: Bild an beiden Achsen spiegeln, 2x2-Raster. Das Original liegt oben rechts, die x-gespiegelte Kopie oben links, so schauen die Gesichter nach aussen (beim Vorlagebild, das nach rechts schaut). Unten dasselbe kopfüber.
3. `pass(src, n)`: in n vertikale Streifen schneiden, jeden Streifen um 90 Grad im Uhrzeigersinn drehen und als horizontales Band von oben nach unten stapeln. Reihenfolge: abwechselnd von aussen nach innen, erst der linke Rand, dann der rechte, dann der zweite von links und so weiter (0, n-1, 1, n-2 …). Breite und Höhe tauschen dabei.
4. Schritt 3 ein zweites Mal, fix zwei Durchgänge wie im Vorbild.
5. Keine Drehung am Schluss. Das gab es (zwei Vierteldrehungen stellen das Blatt auf den Kopf, der Künstler dreht es zurück), ist auf Wunsch wieder raus: das Endbild bleibt, wie es nach Durchgang 2 liegt.

Warum das Bild symmetrisch wird: nach der Spiegelung ist jeder Streifen in sich oben/unten symmetrisch, gedreht ergibt das ein links/rechts symmetrisches Band. Der linke und der rechte Randstreifen sind Spiegelbilder, ihre Bänder sind zueinander vertikal gespiegelt, daher die Rauten zwischen benachbarten Bändern im zweiten Durchgang.

Export: `build(size / 2)` rechnet die Pipeline neu mit der Vorlage in halber Zielgrösse, weil das 2x2-Spiegeln die Kante verdoppelt. Kein Hochskalieren des Vorschaubilds. Zielgrösse ist ein Zahlenfeld ohne Spinner plus Preset-Buttons 1280, 2048, 4000, Standard 1280, Maximum 4000 (Eingabe wird geklemmt). Keine Datalist: Chrome filtert sie nach dem Feldinhalt und zeigt dann nur den aktuellen Wert. Format WebP (Standard), JPEG oder PNG, Qualität 0.92. Die Dateiendung folgt dem Typ des erzeugten Blobs, weil Safari kein WebP encodiert und dann PNG liefert. Über die Auflösung der Vorlage hinaus wird nicht vergrössert, `prepare()` skaliert nur runter.

Streifenbreite ist `floor(width / n)`, ein Rest am rechten Rand fällt weg. Bei ungerader Streifenzahl kommt der Mittelstreifen zuletzt.

## Regeln

- Alle Streifen in dieselbe Richtung drehen. Der Künstler macht das so, und die Symmetrie hängt daran.
- Reihenfolge von aussen nach innen beibehalten, nicht einfach links nach rechts und nicht von der Mitte aus. Von der Mitte aus war die erste Fassung, das Reel zeigt aussen zuerst.
- Animation («animate» im Panel): dieselben Stufen aus `build()`, gezeichnet in ein 1000x1000-Canvas `#anim`, das während der Animation das Endbild ersetzt. `planAnim()` legt die Zeitachse fest: Spiegelkopien blenden ein (bis 1.3 s), dann fliegt pro Durchgang jeder Streifen von seiner Quellposition zur Bandposition, Position, Drehung (0 bis 90 Grad) und Massstab interpoliert, 700 ms pro Streifen, Versatz höchstens 60 ms. Jede Stufe wird per `fit()` ins Quadrat eingepasst, weil Breite und Höhe pro Durchgang tauschen. Zeichenreihenfolge: fertige Streifen unten, wartende darüber, fliegende zuoberst. «loop animation» wiederholt. Während der Animation ist das Panel gesperrt (`busy`), «animate» wird zu «stop».
- Hover-Overlays, nur ohne «show steps»: dann steht das Spiegelblatt (`#sheet`, Kopie von «mirrored») in gleicher Grösse neben dem Endbild. Hover über eines der beiden nummeriert auf beiden alle n·n Zellen: auf dem Blatt in Lesereihenfolge 1 bis n·n, auf dem Endbild die Nummer der Herkunftszelle. Zuordnung: Blattzelle (Spalte i1, Zeile von unten i2) ist Pass-1-Streifen i1 und Pass-2-Streifen i2, weil die x-Achse von Pass 2 der y-Achse des Blatts entgegenläuft. Endbildzelle (Zeile r2, Spalte c) hat i1 = order[n-1-c], i2 = order[r2]. Geprüft: Mittelwerte aller 400 Zellpaare sind identisch. Overlay zeichnet auf die Display-Canvases und stellt beim Verlassen per `putImageData` wieder her; Pipeline und Export bleiben unberührt. Bei «show steps» ist das Blatt ausgeblendet, die Zahlen wären zu klein.
- Layout wie Contour Drawing: Titelleiste 61 px, Panel 276 px rechts mit Lasche, Bildfläche dazwischen. «show steps» zeigt links das Endbild gross, rechts original, mirrored und pass 1 kleiner. Die geplante Animation (Deluxe-Version) soll hier andocken: die Stufen liegen als Canvas-Liste `stages` in `render()` bereit.
- Das Pass-1-Bild nicht ins Hochformat drehen. Ausprobiert: die Bänder werden zu Spalten, Pass 2 schneidet dann längs statt quer, und die Kacheln verschwinden. Das Querformat nach Pass 1 ist korrekt. In der Schritt-Vorschau wird es nur für die Anzeige hochkant gedreht, die Daten bleiben quer.
- Klick auf «original» in der Schritt-Ansicht oder der Button «flip» im Panel spiegelt die Vorlage an der vertikalen Achse (`flip`), damit ein Upload, der nach links schaut, nicht von Hand gespiegelt werden muss. Ein neuer Upload setzt `flip` zurück.
- Ein Umschalter für horizontalen Schnitt war drin (Blatt drehen, vertikal schneiden, zurückdrehen) und ist bewusst wieder raus. Die Variation kommt über den Spiegel-Klick auf «Original».
- Single File bleibt, nur das Vorlagebild liegt daneben.
