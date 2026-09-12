---
version: alpha
name: Sliced Portrait
description: >
  Corporate Identity der Sliced-Portrait-App. Format nach
  github.com/google-labs-code/design.md, übernommen von Contour Drawing
  (Plotter-Projekt) und auf diese App angepasst. Tokens haben Vorrang vor
  eigenen Annahmen.
omitted:
  - Elevation & Depth
colors:
  primary: "{colors.ink}"
  paper: "#ece2cd"                      # Seitenhintergrund, Bildfläche, Panel
  paper-bright: "#f2ead6"               # Text auf dunklen Flächen
  ink: "#5c4a34"                        # Überschriften, aktive Elemente, Buttons, Slider
  ink-soft: "#6b5a42"                   # Regler-Beschriftung, Checkbox-Text
  ink-faint: "#8a7a5e"                  # Grundtext, Hinweise, Status, Bildunterschriften
  border: "rgba(110,92,64,0.25)"        # Trennlinien Panel/Titelleiste, Bildrahmen
  border-strong: "rgba(110,92,64,0.4)"  # Button-, Select- und Eingabefeld-Rahmen
typography:
  title:                                # h1 Titelleiste
    fontFamily: "ui-sans-serif, system-ui, sans-serif"
    fontSize: 15px
    fontWeight: 600
  base:                                 # Grundschrift
    fontFamily: "ui-sans-serif, system-ui, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
  ui:                                   # Regler, Buttons, Hinweise, Status, Bildunterschriften
    fontFamily: "ui-sans-serif, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 400
rounded:
  button: 4px
spacing:
  page: 16px                            # Aussenabstand Titelleiste und Bildfläche
  panel: 12px                           # Innenabstand Panel, Abstand zwischen Panel-Blöcken
  control: 8px                          # Abstand benachbarter Buttons in einer Reihe
components:
  button:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.ui}"
    rounded: "{rounded.button}"
    border: "1px solid {colors.border-strong}"
  frame:                                # Rahmen um Endbild und Schrittbilder
    border: "1px solid {colors.border}"
---

## Overview

Die App sieht aus wie ein Blatt auf einem Schneidetisch: Sepia-Papier,
braune Beschriftung, das Werk in der Mitte mit einem dünnen Rahmen. Eine
einzige Farbfamilie (warme Braun- und Beigetöne), kein reines Schwarz,
kein reines Weiss, keine Akzentfarbe. Das Endbild ist neutral grau oder
farbig wie die Vorlage und wird nicht sepia getönt; das Papier drumherum
ist die Tönung.

## Colors

Alle Farben stammen aus einer Familie. `paper` ist die einzige Flächenfarbe;
Panel, Titelleiste und Bildfläche unterscheiden sich nur durch Trennlinien
(`border`). Text staffelt sich über drei Braunstufen von `ink` (wichtig) bis
`ink-faint` (beiläufig). Aktive Buttons invertieren: Grund `ink`, Text
`paper-bright`. Linien und Rahmen sind nie voll deckend, nur Flächen sind
es. Keine neuen Alpha-Stufen.

## Typography

Systemschrift ohne Ausnahme, keine Webfonts. Drei Grössen genügen; nichts
unter 12px, nichts über 15px. Fett (600) nur für den Titel. Titel,
Buttons, Hinweise und Bildunterschriften in Kleinschreibung («click to
flip»).

## Layout

Feste Masse ausserhalb des Token-Schemas:

- Titelleiste: 61px hoch, links der Titel, rechts Dateiname und Pixelmasse
  der Vorlage
- Panel: 276px breit, rechts, mit Lasche zum Einklappen
- Bildfläche: Endbild zentriert; bei «show steps» das Endbild links, rechts
  die drei Schrittbilder (original, mirrored, pass 1) als Spalte, höchstens
  220px breit und zusammen nie höher als die Bildfläche, damit nichts
  scrollt

## Components

- **Buttons**: 1px-Rahmen `border-strong`, Text `ink`, transparenter Grund.
  Aktiver Zustand invertiert (Grund `ink`, Text `paper-bright`), benutzt
  für «flip». Kein Hover-Effekt.
- **Regler**: native range-Inputs mit `accent-color: ink`, Beschriftung
  links in `ink-soft`, aktueller Wert rechts in `ink`.
- **Checkboxen**: native, `accent-color: ink`, Text in `ink-soft`.
- **Eingabefeld und Select**: gleicher Rahmen wie Buttons, Grund `paper`.
- **Bildrahmen**: 1px `border` um Endbild und Schrittbilder, keine
  Passepartouts, keine Schatten.
- **Status**: eine Zeile unter dem Download-Button in `ink-faint`,
  Pixelmasse, Format und Dateigrösse des letzten Exports.

## Do's and Don'ts

- Keine Animationen und keine Übergänge. Zustandswechsel springen.
  Einzige Ausnahme: das Panel gleitet beim Ein-/Ausklappen mit 0.2s
  heraus, die Lasche wandert mit.
- Keine Schatten, keine Verläufe.
- Interface-Sprache: Englisch, knapp, Kleinschreibung.
- Keine Emojis, keine Icons. Die Lasche benutzt ein Textzeichen (›/‹).
