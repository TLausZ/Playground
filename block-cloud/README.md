# Block-Cloud

A Bitcoin block as a 3D city. Every transaction is one cube: its footprint comes
from the transaction's vsize, its colour from the fee rate, on the same green to
red scale mempool.space uses. Type a block height or pick one of the presets, and
the block is fetched from the mempool.space API and built up front to back.

![Three blocks loaded one after another, each building front to back](preview.webp)

Live: https://tlausz.github.io/Playground/block-cloud/

The select in the header switches to a second view, where the same block becomes
a radial treemap: concentric rings of extruded segments, sorted by fee rate with
the highest rates in the centre, pulled apart so the rings stay readable.

The 2D packing is a port of the algorithm behind mempool.space's own block view,
extruded upwards so the cube height matches its footprint. All cubes live in a
single instanced mesh, so a full block stays interactive.

## Running it

Double-click `index.html`. What the page does need is a network connection: it
loads Three.js from a CDN import map and the block data from the mempool.space
API. Both are served with permissive CORS headers, so they also load from a
`file://` page (checked in Chrome).

The interface is in German, with Swiss number formatting.

## Files

- `index.html` — the whole thing, no build step.
- `DESIGN.md` — the paper-cream palette and the one exception to it, the fee-rate scale.
