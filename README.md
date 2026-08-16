# Playground

Small self-contained web experiments. No dependencies, no build step — open the
HTML file in a browser and it runs.

## Pool Caustics

[`Pool Caustics/index.html`](Pool%20Caustics/index.html) — an animated recreation
of the light reflections that drift across the surface of a swimming pool: thin
cyan loops on deep blue, shifting quickly while the background colors wander.

Inspired by a post from Peter Todd:
<https://primal.net/e/nevent1qvzqqqqqqypzpn92tr3hexwgt0z7w4qz3fcch4ryshja8jeng453aj4c83646jxvqqs29tzjn5xpsrprp2kegk55n2c4zprh2wzdtqrxqffas7thx20l45g3xhz4n>

### How it works

A wave field is built from about nineteen directional sine waves using
deep-water dispersion (ω ≈ √(g·k)), plus domain warping to keep the shapes
organic rather than striped. That field is evaluated on a grid laid out in
perspective, then marching squares extracts its contour lines.

The look comes from how those lines are drawn: **line width follows 1/|∇h|**.
Where the wave field is steep the line is hairline thin; where it flattens out
the same contour widens into a filled blob. That is the mechanism behind the
mix of fine loops and bright specks on real water.

Two details keep it from looking synthetic. Contour levels are derived each
frame from the field's own mean and spread, so the amount of visible line stays
stable whatever the settings. And neighbouring contour cells are grouped into
connected components, so a reflection is either drawn whole or left out
entirely — never sliced through at the edge of the lit band.

It runs on Canvas 2D rather than WebGL, with a fast sine approximation, a
downscaled offscreen buffer for the glow, and a grid resolution that adapts to
the measured frame time. That keeps it smooth on phones.

### Controls

Press `H` or the ☰ button to open the panel; `Space` pauses, `F` goes
fullscreen, and mouse or touch moves the light source. **Copy values** hands the
current slider settings over as one line of JSON, which can be pasted back into
the source as new defaults.

| Control | What it does |
| --- | --- |
| Wave speed | How fast the reflections shift |
| Wave scale | Size of the wave pattern |
| Line density | How much of the surface lights up |
| Line width | Thickness of the contour lines |
| Fill | How readily flat zones become filled blobs |
| Glow | Strength of the bloom |
| Color drift | Speed of the background color cycle |
| Roundness | Smooths the field, curving the shapes |
| Stretch | Elongates reflections along a diagonal axis |
| Light band | Height of the lit region |
| Edge falloff | 0 cuts the band hard; higher softens it |
| Tilt | Rotates the whole scene |
| Perspective | Grazing view across the water, or near top-down |
