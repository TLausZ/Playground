# Sliced Portrait

Nachbau einer Papierarbeit von tete.au.carre (Instagram): Porträt spiegeln, in Streifen schneiden, umlegen, wiederholen.

## Struktur

`index.html` plus `warhol.jpg` als Vorlage. Farben, Schrift und Panel-Masse in `DESIGN.md`, übernommen von Contour Drawing im Plotter-Projekt; vor visueller Arbeit lesen. Kein Build. Braucht den Python-HTTP-Server aus dem Repo-Root, per `file://` ist das Canvas mit dem Vorlagebild tainted (kein Download, kein `getImageData`). Uploads laufen auch per `file://`.

## Wie es funktioniert

Der ganze Algorithmus ist eine Funktion `pass()`, die mehrfach angewendet wird:

1. `prepare(img, max)`: Bild auf höchstens `max` px längste Seite skalieren, optional Graustufen. Vorschau 1400 px, Export die halbe gewünschte Kantenlänge.
2. `mirror()`: Bild an beiden Achsen spiegeln, 2x2-Raster. Das Original liegt oben rechts, die x-gespiegelte Kopie oben links, so schauen die Gesichter nach aussen (beim Vorlagebild, das nach rechts schaut). Unten dasselbe kopfüber.
3. `pass(src, n)`: in n vertikale Streifen schneiden, jeden Streifen um 90 Grad im Uhrzeigersinn drehen und als horizontales Band von oben nach unten stapeln. Reihenfolge: abwechselnd links und rechts der Mittelachse nach aussen (L1, R1, L2, R2 …). Breite und Höhe tauschen dabei.
4. Schritt 3 ein zweites Mal, fix zwei Durchgänge wie im Vorbild.
5. Endbild um 180 Grad drehen: zwei Vierteldrehungen stellen es auf den Kopf, der Künstler dreht am Schluss das Blatt. Die Schritt-Ansicht zeigt Original, Mirrored und Pass 1 rechts neben dem Endbild, Pass 2 ist das Endbild selbst.

Warum das Bild symmetrisch wird: nach der Spiegelung ist jeder Streifen in sich oben/unten symmetrisch, gedreht ergibt das ein links/rechts symmetrisches Band. L1 und R1 sind Spiegelbilder, ihre Bänder sind zueinander vertikal gespiegelt, daher die Rauten zwischen benachbarten Bändern im zweiten Durchgang.

Export: `build(size / 2)` rechnet die Pipeline neu mit der Vorlage in halber Zielgrösse, weil das 2x2-Spiegeln die Kante verdoppelt. Kein Hochskalieren des Vorschaubilds. Zielgrösse ist ein Zahlenfeld ohne Spinner plus Preset-Buttons 1280, 2048, 4000, Standard 1280, Maximum 4000 (Eingabe wird geklemmt). Keine Datalist: Chrome filtert sie nach dem Feldinhalt und zeigt dann nur den aktuellen Wert. Format WebP (Standard), JPEG oder PNG, Qualität 0.92. Die Dateiendung folgt dem Typ des erzeugten Blobs, weil Safari kein WebP encodiert und dann PNG liefert. Über die Auflösung der Vorlage hinaus wird nicht vergrössert, `prepare()` skaliert nur runter.

Streifenbreite ist `floor(width / n)`, ein Rest am rechten Rand fällt weg. Bei ungerader Streifenzahl kommt der Mittelstreifen zuerst.

## Regeln

- Alle Streifen in dieselbe Richtung drehen. Der Künstler macht das so, und die Symmetrie hängt daran.
- Reihenfolge von der Mitte nach aussen beibehalten, nicht einfach links nach rechts.
- Layout wie Contour Drawing: Titelleiste 61 px, Panel 276 px rechts mit Lasche, Bildfläche dazwischen. «show steps» zeigt links das Endbild gross, rechts original, mirrored und pass 1 kleiner. Die geplante Animation (Deluxe-Version) soll hier andocken: die Stufen liegen als Canvas-Liste `stages` in `render()` bereit.
- Das Pass-1-Bild nicht ins Hochformat drehen. Ausprobiert: die Bänder werden zu Spalten, Pass 2 schneidet dann längs statt quer, und die Kacheln verschwinden. Das Querformat nach Pass 1 ist korrekt. In der Schritt-Vorschau wird es nur für die Anzeige hochkant gedreht, die Daten bleiben quer.
- Klick auf «original» in der Schritt-Ansicht oder der Button «flip» im Panel spiegelt die Vorlage an der vertikalen Achse (`flip`), damit ein Upload, der nach links schaut, nicht von Hand gespiegelt werden muss. Ein neuer Upload setzt `flip` zurück.
- Ein Umschalter für horizontalen Schnitt war drin (Blatt drehen, vertikal schneiden, zurückdrehen) und ist bewusst wieder raus. Die Variation kommt über den Spiegel-Klick auf «Original».
- Single File bleibt, nur das Vorlagebild liegt daneben.
