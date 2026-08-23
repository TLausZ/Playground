---
name: bitcoin-halving-animation
tokens:
  color:
    background: "#F4EEE0"
    line: "#6B4226"
    fill: "#E8892E"
    fill-opacity: 0.15
  typography:
    font-family: "Georgia, serif"
    size-heading: 18px
    size-body: 13px
    line-height-body: 1.6
  stroke:
    shapes: 1px
  motion:
    duration: 14s
    easing: ease-in-out
  base-layer:
    alpha-per-box: 0.15 # flach pro Box (Rotations-Sweep als Union), additiv zwischen Boxen
    static: true # einmalig gemalt, nicht animiert
    shape: swept-circles # jede Box ueberstreicht rotierend eine Kreisscheibe
---

## Grundidee
Cremefarbener Hintergrund, eine einzige braune Linienfarbe für die animierten Kontur-Quadrate, darunter ein statischer orangener Flächen-Unterbau: jede Box überstreicht in ihrer Rotation eine Kreisscheibe, die genesteten Scheiben bilden ein Bullseye aus Kreisen, das nach innen dunkler wird. Die Boxen rotieren als Konturen entlang dieser Kreisbahnen darüber.

## Komposition
Das Bullseye-Auge ist im Bildzentrum platziert (nicht oben rechts), die ganze Szene um 45° nach links gekippt. Die 50er-Box hängt als gekippte Kontur an einer Ecke des Auges und ist, wie alle kleineren Boxen, flach gefüllt — statisch (keine Rotation), aber sie übermalt die inneren Formen zusätzlich, dadurch etwas dunkler. Der Bildausschnitt ist quadratisch und symmetrisch um den Augen-Mittelpunkt.

## Farbe
`#F4EEE0` (Creme) als Hintergrund, `#6B4226` (dunkles Braun) für Quadrat-Umrisse und Text, `#E8892E` (Orange) als Flächenfüllung bei 15% Deckkraft pro Box — Überlappungen verdunkeln sich bewusst additiv, je mehr Boxen sich an einer Stelle stapeln.

## Typografie
Georgia (Serif) für die Legende oben links. Die Überschrift (18px) bleibt gewichtsneutral (`font-weight: normal`) statt fett — die Legende soll wie eine Bildunterschrift wirken, nicht wie ein UI-Element.

## Linienführung
Quadrat-Konturen: 1px, `vector-effect="non-scaling-stroke"` (bleiben bei jeder Skalierung exakt 1px).

## Bewegung
Ein einziger 14-Sekunden-Zyklus, `ease-in-out`, ohne Halt bei offen oder geschlossen — die Rotation läuft durchgehend zwischen ineinander verschachtelt (-180°/180°, visuell identisch) und voll ausgeklappt (0°).

## Flächen-Unterbau
Einmalig gemalt, nicht animiert. Statt jede Box nur an einer Position zu zeigen, wird ihre gesamte Rotation als Fläche gemalt: eine rotierende Box überstreicht um ihren Scharnierpunkt eine volle Kreisscheibe. Jede Box bleibt dabei flach bei 15% Deckkraft (`#E8892E`, keine Kontur) — die eigene Rotation verdunkelt sich nicht. Wo sich die Scheiben verschiedener Boxen überlappen, addiert sich die Deckkraft bewusst auf: nach innen (kleinere, stärker genestete Boxen) wird es dunkler, ein Bullseye aus Kreisen. Die animierten Kontur-Quadrate rotieren unabhängig davon endlos über diesem Unterbau, ihre Bahn deckt sich mit den Kreisrändern.
