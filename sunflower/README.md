# Sunflower seeds

Live: <https://tlausz.github.io/Playground/sunflower/>

![Seeds arranged in spirals, the turning angle sweeping past 137.5 degrees](preview.webp)

How many seeds fit on a sunflower head before two of them collide? Each seed sits one fixed turning angle further round than the one before and a little further out (Vogel's model: radius grows with the square root of the seed number). The video sweeps that angle from 0 to 360 degrees in steps of 0.1 degree. Seeds are laid down from the centre outwards until the first one overlaps another; the graph on the right records how many made it.

Almost every angle fails within a handful of seeds, because the seeds line up in spokes or tight spirals with gaps between. At 137.5 degrees 465 seeds fit. At the golden angle, 137.508 degrees, all 1,500 seeds fill the disk without a single overlap. The second spike at 222.492 degrees is the same angle turned the other way.

The seed size decides how sharp the peak is. With slightly smaller seeds, 99.5 degrees (another angle related to the golden ratio) also fills the disk; at the size used here only the golden angle does.

Made with [ManimGX](https://github.com/academa-labs/manimgx). `sunflower.py` is the whole scene, `sunflower.mp4` the 1080p60 render.
