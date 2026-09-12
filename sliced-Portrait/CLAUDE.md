# Sliced Portrait

Nachbau einer Papierarbeit von tete.au.carre (Instagram): Porträt spiegeln, in Streifen schneiden, umlegen, wiederholen.

## Struktur

`index.html` plus `warhol.jpg` als Vorlage. Kein Build. Braucht den Python-HTTP-Server aus dem Repo-Root, per `file://` ist das Canvas mit dem Vorlagebild tainted (kein Download, kein `getImageData`). Uploads laufen auch per `file://`.

## Wie es funktioniert

Der ganze Algorithmus ist eine Funktion `pass()`, die mehrfach angewendet wird:

1. `prepare()`: Bild auf höchstens 1400 px längste Seite skalieren, optional Graustufen.
2. `mirror()`: Bild an beiden Achsen spiegeln, 2x2-Raster. Das Original liegt oben rechts, die x-gespiegelte Kopie oben links, so schauen die Gesichter nach aussen (beim Vorlagebild, das nach rechts schaut). Unten dasselbe kopfüber.
3. `pass(src, n)`: in n vertikale Streifen schneiden, jeden Streifen um 90 Grad im Uhrzeigersinn drehen und als horizontales Band von oben nach unten stapeln. Reihenfolge: abwechselnd links und rechts der Mittelachse nach aussen (L1, R1, L2, R2 …). Breite und Höhe tauschen dabei.
4. Schritt 3 ein zweites Mal, fix zwei Durchgänge wie im Vorbild.
5. Endbild um 180 Grad drehen: zwei Vierteldrehungen stellen es auf den Kopf, der Künstler dreht am Schluss das Blatt. Die Schritt-Ansicht zeigt Original, Mirrored und Pass 1 rechts neben dem Endbild, Pass 2 ist das Endbild selbst.

Warum das Bild symmetrisch wird: nach der Spiegelung ist jeder Streifen in sich oben/unten symmetrisch, gedreht ergibt das ein links/rechts symmetrisches Band. L1 und R1 sind Spiegelbilder, ihre Bänder sind zueinander vertikal gespiegelt, daher die Rauten zwischen benachbarten Bändern im zweiten Durchgang.

Streifenbreite ist `floor(width / n)`, ein Rest am rechten Rand fällt weg. Bei ungerader Streifenzahl kommt der Mittelstreifen zuerst.

## Regeln

- Alle Streifen in dieselbe Richtung drehen. Der Künstler macht das so, und die Symmetrie hängt daran.
- Reihenfolge von der Mitte nach aussen beibehalten, nicht einfach links nach rechts.
- «Show steps» zeigt links das Endbild gross, rechts Original, Spiegelung und Pass 1 kleiner. Die geplante Animation (Deluxe-Version) soll hier andocken: die Stufen liegen als Canvas-Liste `stages` in `render()` bereit.
- Das Pass-1-Bild nicht ins Hochformat drehen. Ausprobiert: die Bänder werden zu Spalten, Pass 2 schneidet dann längs statt quer, und die Kacheln verschwinden. Das Querformat nach Pass 1 ist korrekt. In der Schritt-Vorschau wird es nur für die Anzeige hochkant gedreht, die Daten bleiben quer.
- Klick auf «Original» in der Schritt-Ansicht spiegelt die Vorlage an der vertikalen Achse (`flip`), damit ein Upload, der nach links schaut, nicht von Hand gespiegelt werden muss. Ein neuer Upload setzt `flip` zurück.
- Ein Umschalter für horizontalen Schnitt war drin (Blatt drehen, vertikal schneiden, zurückdrehen) und ist bewusst wieder raus. Die Variation kommt über den Spiegel-Klick auf «Original».
- Single File bleibt, nur das Vorlagebild liegt daneben.
