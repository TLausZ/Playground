# Sliced Portrait

A portrait mirrored into a 2x2 grid, cut into vertical strips, each strip turned 90 degrees and stacked into a new image. Done twice, the face dissolves into a symmetric tile pattern. Inspired by the paper-and-scalpel version by tete.au.carre on Instagram. One HTML file, Canvas 2D, no dependencies.

- Upload your own image or start with the default portrait.
- Strips: how many cuts per pass (10 to 60). Two passes, always.
- Click the Original step to flip the source, so the faces look outward in the mirrored grid.
- Black & white toggle and a view of the intermediate steps.
- Export: pick or type the long edge in pixels, WebP, JPEG or PNG. The image is recomputed at that size from the upload, never upscaled from the preview.

Needs an http server for the default image (`python3 -m http.server` from the repo root), uploads work anywhere.

Live: <https://tlausz.github.io/Playground/sliced-Portrait/>
