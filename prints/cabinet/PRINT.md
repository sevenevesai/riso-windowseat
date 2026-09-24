# Cabinet

Request (2026-09-23): "a collection of interesting artistic stills, originals, as high detail or
locked in unique style as you come to." Art-directed as five plates from an imaginary
natural-history cabinet. One style holds the series together: each specimen is centred on bare
stock and built from its own growth geometry. Colour is laid as screened fields, form is cut as
fine line in the plate's key ink, and each plate carries an engraved roman plate number.

Source: `index.html`; plate index = `floor(t)`: 0 nautilus, 1 diatoms, 2 luna, 3 agate,
4 sunflower. Native size is 2160 × 2160 (`OUT=2160`). Screen pitch is 3.4 at 1080, or 6.8
device px, finer than Sceneries because the subjects are small and dense. Registration is
`REG × K × 0.6`. Delivered PNGs (native 2160², not in git) come from
`node still.mjs ../prints/cabinet/index.html --at <index> --out ../out/cabinet-<plate>.png`;
`sheet.jpg` is a reduced contact sheet.
`verify.mjs --times 0,1,2,3,4` passes in Chromium and Firefox. `still.mjs` (Firefox) repeats
each plate byte-identically.

## Changes to this print's engine copy

- Screen dot centres sit on pixel centres (`+0.5` in `buildScreen`). The 45° lattice otherwise
  lands on pixel corners, so the smallest dots jump 0 → 4 → 12 px and gentle ramps contour into
  visible rings. That contouring was seen on the luna wing.
- A fixed 256² dither, ±4.5% at mid-tones only, breaks the remaining dot-size steps.
- Coverage ≥ 1 prints solid. Otherwise the threshold tile leaves the interstices open, and the
  engraved line breaks up.
- `?only=<ink>` bakes a single plate, and plates bake lazily on first seek.

## Plates, references and decisions

- **I. Nautilus, cut.** References: Commons `Nautilus Pompilius Section cut.jpg`,
  `Inside Nautilus Pompilius.jpg` and the MN exterior photos. One logarithmic spiral with whorl
  expansion 3.1, growing clockwise. Septa are self-similar in whorl coordinates and sag gently
  toward the apex, with necks pointing back along the siphuncle. The first attempt used septa
  that were far too curved, and a construction-line debug view (`?debug=lines`) compared against
  the section diagram caught it. The cut runs along two growth lines, so its edges curve as the
  shell grew. The exterior is lit as a whorl cross-section: growth lines are engraved with a
  width set by Lambert shade, flame stripes fork toward the umbilicus and withdraw near the
  aperture, and there is a black film at the aperture. A dotted pink line carries the spiral on
  past the aperture, as the growth that did not happen.
- **II. Arranged diatoms, dark-field.** References: Commons *Arachnoidiscus*, *Actinoptychus*
  and *Triceratium* micrographs. Structures are drawn additively as light into a three-hue
  buffer, then glowed with a deterministic box blur. Ink is derived from light: the ground is an
  indigo+yellow overprint (dark, not black), halos take their hue's ink, and the brightest cores
  go to paper. The layout is a six-fold Victorian rosette with small hand-placement jitter.
- **III. Luna moth, set.** Reference: Commons `Actias luna (luna moth) (17257003162).jpg`. The
  outline, costa, veins and eyespot positions were measured in that photo's pixel frame and
  mirrored, with a slight setting asymmetry. Scale rows are interpolated between neighbouring
  veins. The eyespots are almond-shaped with a dark lune and a pale window, as in the photo
  crops. Fig. 2 shows the same eyespot model rendered as overlapping toothed scales, drawn
  distal rows first so each proximal tip laps the one before.
- **IV. Agate, cut.** References: Commons blue-lace and banded agate photos, used for band
  character only. Bands are exact Euclidean distance transforms (Felzenszwalb–Huttenlocher) from
  the cavity wall. The depositional order is lining, then a level onyx floor (gravity), then a
  second lining, then a druzy hollow. Crystals are ordered by depth, their lit facets fall to
  paper, and amethyst deepens toward the heart.
- **V. Sunflower, late August.** Vogel's model with 1300 florets gives the 34/55 parastichies
  directly. The rim has set seed, a middle ring is open and shedding pollen, and the centre is
  still in bud. A bird has worked the lower-right seed ring, leaving empty sockets and chaff.
  Florets are ~20 px across, below the screen's resolving power, so they are modelled with solid
  overprints and shape rather than dot size.

## Inspected

The 1000 px view, 1:1 crops of each plate's hardest area (septa and necks, the diatom web,
the eyespot and scale inset, the crystal hollow, floret zones), a construction-line view of the
nautilus, and a Firefox contact sheet plus 1:1 crops of the delivered PNGs.

## Remaining weaknesses

- Nautilus: the umbilical callus reads as a pale boss rather than a clearly raised plug. At 1:1,
  the lightest engraved lines on the exterior break into dashes.
- Diatoms: the specimens are stylised to their diagnostic features. The border ring's small
  valves are simple.
- Luna: the body fur and antennae are schematic next to the wings. Fig. 2's scales are larger
  than a true ×4 view would show, so that they read at print size.
- Agate: the cavity outline is an authored polygon, and the fortification creases are gentle
  rather than sharply angular. The level floor is short.
- Sunflower: the ray petals are similar to one another. The seed ring reads as dark texture at
  viewing size; its stripes only show at 1:1.
