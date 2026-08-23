# Whackaddodle MJ zoom

[![The whole move at 3.5× speed](preview.webp)](https://tlausz.github.io/Playground/MJzoom01/)

Twelve Midjourney frames, each one zoomed out from the last, stitched back
together into a single continuous camera move. The film runs out to the widest
frame and back in, slowing to a near stop at both ends and at the turning
point.

Prompt: `isometric Bitcoin B --sref 3879714017`

The loop above is the whole move sped up. The film itself —
[zoom_pingpong_720.mp4](zoom_pingpong_720.mp4), 720×720, 37 seconds — plays in
the browser at <https://tlausz.github.io/Playground/MJzoom01/>. GitHub strips
`<video>` out of markdown, so a real player only exists on that page, not here.

`match.py` measures how far each frame is zoomed out from the previous one and
writes `fits.json`; `zoomvid.py` reads that and renders the film. Needs ffmpeg,
numpy and pillow.
