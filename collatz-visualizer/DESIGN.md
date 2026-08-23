# DESIGN.md — Collatz Visualizer

Visual identity of the Collatz visualizer in this folder. Format after
github.com/google-labs-code/design.md: YAML tokens plus prose. The tokens are
inherited unchanged from an existing wiki-map identity and serve as the
reference. Tokens take precedence over ad hoc choices.

## Idea

The visualizer shows the Collatz trajectories of the start values 1 to N and
looks like an old topographic survey map: sepia paper, thin brown lines,
restrained labelling. The thousand faint sequence paths lie over each other
like contour lines and form a calm mesh; only the selected path stands out in
the warmer red-brown. A single colour family (warm brown and beige tones), no
pure black, no pure white, no second accent besides the red-brown for the
active sequence and its peak. Surfaces are matte and opaque; depth comes from
the density of the paths themselves, not from drop shadows or gradients.
Interface elements (number line, axes, tooltip) use the same palette as the
chart, so they read like a map border and legend, not like an overlaid UI.

## Tokens

```yaml
color:
  paper:        "#ece2cd"   # page background, map body, panels
  paper-bright: "#f2ead6"   # text on dark surfaces
  ink:          "#5c4a34"   # headings, active elements, buttons
  ink-soft:     "#6b5a42"   # list text, secondary text
  ink-faint:    "#8a7a5e"   # body text, subtitles, hints
  line:         "rgba(74,58,40,0.68)"    # contour lines, outlines
  line-shadow:  "rgba(110,92,64,0.07)"   # faint ground shadow of the contours
  border:       "rgba(110,92,64,0.25)"   # dividers panel/title bar
  border-strong: "rgba(110,92,64,0.4)"   # button borders
  bar:          "rgba(110,92,64,0.18)"   # weight bar in the list
  accent:       "rgba(150,90,50,0.95)"   # hover/selection: peak point
  accent-line:  "rgba(120,70,40,0.85)"   # hover/selection: connecting line
  accent-box:   "rgba(92,74,52,0.97)"    # hover/selection: label box

font:
  family: "ui-sans-serif, system-ui, sans-serif"
  size:
    title:    15px   # h1 title bar, weight 600
    base:     13px   # body font, line height 1.4
    ui:       12px   # list, subtitle, buttons, markers, link
    label:    11px   # map labels (canvas)
  weight:
    normal:   400
    strong:   600    # title and name prefixes only

radius:
  button: 4px
  pill:   3px        # link chip in the map area

space:
  page:   16px       # outer spacing title bar, link
  panel:  12px       # inner padding panel and buttons
  row:    3px        # vertical padding list rows

layout:
  topbar-height: 61px
  panel-width:   276px

stroke:
  contour: 0.85px    # contour lines (times devicePixelRatio)
  shadow:  1px
  leader:  1px       # label connecting lines, 1.2px when highlighted
```

## Colour

All colours come from one family. `paper` is the only surface colour; panel,
title bar and map body do not differ in tone, only through dividers (`border`).
Text steps through three brown levels from `ink` (important) to `ink-faint`
(incidental). Highlighting flips the scheme: dark box (`accent-box`), light text
(`paper-bright`). The warmer red-brown (`accent`) marks only the active peak and
its line, nothing else.

Transparencies are part of the palette: lines and borders are never fully
opaque, only surfaces are. New elements should reuse an existing alpha level
rather than introduce a new one.

**Exception — the "all" overview.** When all nine quick-pick sequences are
shown at once, a single brown family can no longer tell nine overlapping paths
apart. That view breaks from the one-family rule and colours each path with
its own hue from a validated nine-colour categorical set. It is scoped to that
overview only; every other state (single selection, axes, chrome) stays in the
brown family above.

**Exception — the arc view.** The circles view fills each half-circle with the
mean of a red-to-blue gradient across the run (red for the first hops, blue for
the last), taken from the same categorical set as the overview, at a low alpha
so the stacked fills stay legible. The outlines are a single dark brown (`ink`),
dotted like the guides. Scoped to that view; the line view stays brown.

## Typography

System font without exception, no web fonts. Four sizes are enough; nothing
below 11px, nothing above 15px. Bold only for the title and name prefixes.
No italics, no all-caps headings. Labels on the map are lowercase with spaces
instead of hyphens.

## Components

- **Number line** (start values 1 to N): narrow scale on the left edge, fine
  ticks in `line`, labels in `ink-faint`. The position under the cursor selects
  the start value; a leader in `accent-line` runs from there into the chart.
- **Sequence paths**: all thousand trajectories as thin lines in a very low
  alpha level (`line-shadow`), stacked over each other. The selected path sits
  above them in `accent-line`, its peak as a filled dot in `accent`.
- **Arc view** (circles): reached by the Circles/Steps toggle beside the scale
  button; the button names the view you switch to. Values sit on the horizontal
  axis, each hop is a filled half-circle rising from it, revealed in sequence as
  the animation runs. The half-circles never exceed the plot height. In the
  linear scale the axis fits the selected run's peak, so small start values fill
  the width; the log scale keeps the global maximum.
- **Axes**: base lines and ticks in `line`, numbers in `ink-faint`. The Y axis
  is fixed at the global maximum and can be switched to a logarithmic scale by
  button; the labels come from the data and are not maintained by hand.
- **Buttons** (Circles/Steps, log scale): 1px border `border-strong`, text
  `ink`, transparent ground. Active state inverts: ground `ink`, text
  `paper-bright`. The view toggle names the view you switch to.
- **Animation speed slider**: sets the draw duration of the selected run, from
  0s (instant) to 10s, default 3s. Endpoints labelled left and right, the
  caption sits below.
- **Tooltip**: dark box (`accent-box`) with light text (`paper-bright`), no
  border. Shows start value, steps, current value, highest value and end value.
  Disappears completely when nothing is selected.

## Motion

Used sparingly. The interface itself does not move: scale changes, selection
and button state changes jump without a transition. One content animation is
allowed: on each new start value the selected run is revealed in order, drawn
left to right in the line view and hop by hop as the half-circles fill in the
arc view, so the run reads as movement. Its duration is set by the animation
speed slider (default 3s). The load shows a spinner while the static views are
precomputed. No other transitions.

## Interface language

English, terse, lowercase in hints. Numbers in the subtitle come from the data
and are not maintained by hand.
