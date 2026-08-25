# WFC Planet

[`index.html`](index.html), a planet grown from a wave function collapse.
Open it in a browser; no dependencies, nothing to build.

The same pipe-tile collapse as the [Wave Function Collapse](../Wave%20Function%20Collapse/)
sketch runs on a coarse icosphere, but here its output becomes terrain.
Distance to the nearest pipe is height: the pipe network turns into mountain
ranges, junctions into peaks, the first ring of cells around them into
lowlands, and everything further out into the sea. The continents are the
pattern, not decoration on top of it.

The planet starts as an empty ocean. **Grow** advances the collapse one chunk
and the new land rises out of the water; **Auto** keeps growing; **Finish**
jumps to the settled world; **New** reseeds. One seed always grows the same
planet, because the solver and the noise share it. Drag to turn, wheel to
zoom.

## How it works

Two lattices subdivide the same icosahedron. The solver runs on the coarse
one (492 cells); a much finer mesh (23k vertices) samples the resulting
height field, each vertex blending its three nearest cells. Seeded value
noise adds what the coarse field cannot: coastline wiggle and rock roughness
that only shows on high ground.

The sea level is not a constant but a percentile of the settled cells'
heights. The pipes always win the collapse, so absolute heights alone would
drown almost nothing; pinning the level keeps the land fraction earth-like
whatever the tile weights do, and leaves the pattern to decide where the land
sits rather than how much of it there is.

Rendering is raw WebGL, three programs: the planet with two tinted lights
(a faintly blue sky fill that is all a shadowed slope gets, and a warm white
key), a fixed star field, and an additive atmosphere halo. The ocean stays a
geometrically smooth sphere so the water reads as a surface; land rises up to
seven percent of the radius, and normals come from the actual triangles, so
slopes shade as slopes. While the terrain morphs the buffers re-upload; once
it settles a frame is three draw calls.

## Origin

Grown out of the Wave Function Collapse sketch next door, whose lifted-shapes
view kept hinting that the collapse wanted to be geography.
