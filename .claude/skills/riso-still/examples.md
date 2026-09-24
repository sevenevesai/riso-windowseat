# Worked prints: where to look

Each print series is one `index.html` with the whole engine inline; integer times select prints
(`PRINTS`, `drawArt`). Search for the names below rather than trusting line numbers, and read the
series' `PRINT.md` before borrowing: it records references, decisions and remaining weaknesses.
Borrowing rules are in [riso-film/examples.md](../riso-film/examples.md#how-to-borrow).

## prints/cabinet — five natural-history plates, 2160²

One locked style across five subjects: a specimen centred on bare stock, colour as screened
fields, form as fine line in the plate's key ink, an engraved roman numeral. Every mark is placed
by the specimen's own growth geometry.

| Technique | Where | Why copy it |
|---|---|---|
| Dots centred on pixels | `buildScreen` (`+ 0.5` on lattice positions) | Small dots grow 1 → 5 → 9 px instead of 4 → 12, so gentle ramps stop contouring into rings. |
| Mid-tone dither and solid line | `DITHER`, `screenCoverage` | A fixed ±4.5% dither on mid-tones breaks dot-size steps; coverage 1 closes up solid so engraved line doesn't break into dots. |
| Debug views | `ONLY` (`?only=<ink>`), `?debug=lines` in the nautilus layer | Plate isolation, and construction lines alone against the reference section diagram. |
| Growth spiral | `nautilus` | One logarithmic spiral owns walls, septa, growth lines and the dotted future path. |
| Light as ink | `diatoms`, `boxBlur` | Structures drawn additively as light, glowed, then converted to ink: dark ground as overprint, brightest cores to paper. |
| Measured from a photo | `luna` | Outline, veins and eyespots measured in the reference photo's pixel frame, then mirrored. |
| Distance-transform bands | `agate`, `edt` | Exact Euclidean distance from the cavity wall gives every deposition band. |
| Phyllotaxis | `sunflower` | Vogel's model (θ = n·137.508°) produces the 34/55 parastichies by itself. |
| Key ink per plate | `KEY_INK`, `numeral` | One ink carries line and numeral per specimen. |

## prints/sceneries — three landscapes, 2160²

Each print shows a different strength: constructed perspective with fog, lights with mirrored
reflection, stepped strata with layered haze.

| Technique | Where | Why copy it |
|---|---|---|
| World-space camera | `VIA` (`Space.camera`, metres) | A curved viaduct in true plan: R 120 m, seven 24 m arches, Lambert shade along the curve. |
| Stacked fog | `fogCut`, `below` | Partial knockouts stacked under a wavering top thin the dots as (1 − a)ⁿ into the bank: fog as dissipation, not a hard edge or a flat overlay. |
| Owned values | `own` | Clear, then print: a face keeps its value where planes overlap. |
| Reflection by re-projection | `HARB`, `HARB_SEA` | Houses re-projected through y = 0, then broken by sea-coloured ripple lenses and light streaks. |
| Strata profiles | `STRATA`, `CANYON`, `paintPlane`, `hazed` | Skylines from erosion depth through the rock column, so every profile steps; haze per plane. |

## prints/workings — the print kit's donor

A series of stills where every mark is on a baked plate, so `shade` coverage ramps are used
everywhere a film would settle for a flat pass. `tools/new-riso.mjs` copies its print kit.

| Technique | Where | Why copy it |
|---|---|---|
| Native bake size | `OUT`, `K`, `PITCH` | Pitch scales with the bake size so a larger print re-rasterises instead of resizing a screen. |
| Stills driven like a film | `PRINTS`, `window.__riso` (`seek: render`) | Each integer time is one print; the tools shoot it unchanged. |
| Baked coverage ramps | `shade` | Gradient stops screened at bake time. |
| Structure helpers | `towerPath`, `hangPoints`, `span` | Seeded architecture and sagging cables. |
