# Sceneries

Request (2026-09-23): "beautiful stills of detailed sceneries that utilise our skills and
strengths to their fullest." Art-directed as a series of three, each built on a different
strength: constructed perspective plus fog (viaduct), repeated lights plus mirrored reflection
(harbour), and stepped strata plus layered haze (canyon).

Source: `index.html`; print index = `floor(t)` (0 viaduct, 1 harbour, 2 canyon).
Native size is 2160 x 2160: `OUT=2160`, screen pitch 9.2 device px, and plate registration
scaled by `K`. Delivered PNGs (native 2160², not in git) come from
`node still.mjs ../prints/sceneries/index.html --at <index> --out ../out/sceneries-<print>.png`;
`sheet.jpg` is a reduced contact sheet.
`verify.mjs --times 0,1,2` passes: seek is pure, and still.mjs repeats byte-identically.

## References and observations

- Landwasser Viaduct (Commons: `CH_Landwasser_2.jpg`, `Allegra…Landwasser_viaduct….jpg`):
  tall piers that taper toward the top, semicircular arches, horizontal masonry courses, a thin
  deck above each crown, and the deck running straight into a tunnel portal in a limestone cliff.
  Drawn as an original curved viaduct, not a copy.
- Manarola at dusk (Commons: `Manarola_at_Dusk_(29757315375).jpg`): narrow 4–6 storey tower
  houses, window grids with green shutters, pastel walls, a dark rock plinth, terraced hill,
  and afterglow over the open sea.
- Canyon: stratigraphy from general knowledge, not an inspected photo (unverified detail):
  Kaibab, Toroweap, Coconino, Hermit, Supai, Redwall, Muav.

## Geometry and light

- Viaduct: one `Space.camera` in world metres. The curved plan is R=120 m with 7 arches of
  24 m span. Pier sides are backface-culled, and face tone follows Lambert shading along the
  curve (shade near, sun far). The train is boxes plus an octagonal boiler. Steam is puffs
  trailing back along the track. The landscape is screen-space planes keyed to the camera
  horizon. Fog uses `fogCut` stacked partial knockouts.
- Harbour: houses are world boxes on one hillside surface H(x,z). Reflections re-project the same
  geometry through y=0, then sea-coloured ripple lenses break them up. Light streaks sit under
  every lit window and lamp. Shutters and lit glass print at full coverage so they survive the
  screen.
- Canyon: each plane's skyline is an erosion depth e(x) mapped through the rock column (a cliff
  spends little run on a lot of drop), so every profile steps. Bands are horizontal per plane,
  east-facing flanks are violet, and the depths fill with violet shadow below the lit beds.

## Remaining weaknesses

- Viaduct: the loco is small and blocky; the near spruce rank is still somewhat regular.
- Harbour: the rock strata are a uniform diagonal hatch; one boat is half hidden by the
  foreground rocks; the houses read flat (front faces only, from a low eye).
- Canyon: the foreground slabs read a little like paving; shadowed middle depths lack
  structure; the juniper foliage is stylised clumps.
