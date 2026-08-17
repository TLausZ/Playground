# Whackaddodle MJ zoom

![Whackaddodle MJ zoom](TLausZ_isometric_Bitcoin_B_--sref_3879714017_--stylize_0_--v__4c34480c-7778-472c-b259-6f000b9bfd81_2.png)

Twelve Midjourney frames, each one zoomed out from the last, stitched back
together into a single continuous camera move. The film runs out to the widest
frame and back in, slowing to a near stop at both ends and at the turning
point.

Prompt: `isometric Bitcoin B --sref 3879714017`

[zoom_pingpong_720.mp4](zoom_pingpong_720.mp4) — 720x720, 37 seconds.

`match.py` measures how far each frame is zoomed out from the previous one and
writes `fits.json`; `zoomvid.py` reads that and renders the film. Needs ffmpeg,
numpy and pillow.
