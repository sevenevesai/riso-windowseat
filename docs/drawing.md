# Drawing and composition

How to draw a frame that reads (contour, value, tone, depth, texture) and what it spends (ink
budget, focus, lettering); read it when drawing scenes, after
[visual-development.md](visual-development.md).

Plate mechanics are in [riso-plates.md](../.claude/rules/riso-plates.md), perspective in
[scene-space.md](scene-space.md), live elements in [motion.md](motion.md). Numbers belong to the
specific study renders. The original diagnosis: weak scenes were ellipses, rings, straight
polylines and arc fans, flat-filled on flat grounds, one subject size, no dark, not one coverage
gradient: exactly what the helper vocabulary offered.

## The craft kit

[studies/index.html](../studies/index.html) carries a `── craft kit ──` block after `starve()`;
copy it whole to the same place in a film. It depends only on `clamp`, `makeWob`, `tone`, `W`,
`CX`, `CY`. Shapes are `Path2D`, so one shape can be filled on one plate, knocked out of another
and hatched on a third, and a knockout can't miss its target.

| Builds a shape | |
|---|---|
| `curve(pts, closed, per)` | Catmull-Rom through points, as a dense polyline |
| `cut(pts, rng, {amp, tear})` | closed hand-cut contour: the silhouette builder |
| `nib(pts, wfn, {per, raw})` | variable-width ribbon, the tapered stroke Canvas lacks |
| `wTip / wSwell / wLeaf / wNib` | width profiles for `nib`; `wNib` is a held calligraphic nib |
| `ringPts(x, y, rx, ry, n, rot)` | points round an ellipse, to feed `cut` |
| `ridgeAt(y, o)` / `peaksAt(y, o)` | skylines: smooth hills or triangular mountains |
| `ridge(yOrFn, o)` | skyline closed to frame bottom; `ridgeU(x)` maps x to its parameter |

| Puts ink down | |
|---|---|
| `print(g, path, a)` | fill at a tone |
| `carve(g, path)` | knock out at full coverage |
| `plane(g, path, a)` | clear, then print: a shape that owns its value |
| `keyline(g, path, w, a)` | outline |
| `shade(g, path, {stops, …})` | coverage ramp in a shape; `cut: true` ramps a knockout |
| `hatch(g, path, rng, o)` | clipped hatching; `gap` 4–6 with `cut` is dry-brush |
| `spray(g, path, rng, o)` | stipple by density function: a gradient of grain |
| `bed(g, x, y, rx, ry, rng, a)` | contact shadow, so a subject isn't a decal |

## Value first

Decide the value hierarchy before inks. Paper, a mid and a dark anchor is a good start;
high-key works too. Add a dark for separation or depth, not by quota.

A dark must be an overprint, mechanically: one orange plate at coverage 1.0 bottoms at luminance
129, one indigo at 52, orange over indigo at 7. The threshold tile clamps at 1, so gaps between
dots never take ink; one plate can't print a true solid, two can.

Model form by removing ink toward the light: `print` solid, then `shade(…, {cut: true})` a ramp
centred on the light. The hue stays pure, every value one plate at different dot sizes. A foreign
ink over the shaded half turned an orange ball olive-brown; keep foreign ink for the smallest,
darkest accent (core shadow, contact shadow, inside an opening). Highlights are paper, cleared
with `carve`, not a light ink.

## Silhouette and contour

An ellipse body, circle head and triangle beak carry their parts' curvature: one machine radius
everywhere, joins reading as bumps, an outline that says nothing about action. Draw one contour
through deliberate points and let `cut` waver it (study 0).

- Double a control point for a corner: Catmull-Rom cusps there, keeping a beak or tail tip sharp.
- Vary curvature: a flat, a long slow curve, one tight turn. A wobbled ellipse is still an ellipse.
- `cut` smooths its displacement twice; an unsmoothed tear on one sample reads as damage, not a
  bay in the edge.
- Constant `lineWidth` marks a machine; stems, branches, legs, rigging, whiskers and petals want
  `nib` with a profile.
- Tight concavities can overshoot or self-intersect in `curve`; inspect. If a notch fills in, use
  explicit Bézier control or print the mass and `carve` the bite.
- Edges follow the world: diffusive ones (fog, glow, a crack's far end, steam) break into dots;
  structural ones (window, rooftop, bell rim) stay hard. A softened structural edge reads as a
  registration fault, not atmosphere.

## Tone that prints

`screenCoverage` thresholds per pixel, so a canvas gradient in a plate becomes a dot-size ramp:
the signature riso gesture. `shade` wraps it.

- Baked plates only. `inkPass` screens live elements at one flat coverage, so a gradient there
  prints smooth; moving elements use `bandPass` ([motion.md](motion.md#tone-on-a-moving-element)).
- Tones add on a plate: ridges at 0.14, 0.3 and 0.62 drawn back to front print 0.79 at frame
  bottom, a colour band, not land. Use `plane()`.
- Start a ramp from a visible point. Twice a dark end sat under a later knockout and the opening
  printed as a bright patch.
- A feature smaller than a few screen cells can't carry a dot-size ramp: model it with shape and
  solid overprints. Roost's starlings are solid 2–3 px dots; a sunflower's ~20 px florets at a
  6.8 px pitch were shaped, not shaded.
- The kit's `buildScreen` puts dot centres on pixel corners for several angles, so dots grow
  0 → 4 → 12 px and a gentle ramp contours into rings. Computed from the kit at 1080, yellow,
  orange and violet get one tone step below 25% coverage (two when centres are shifted half a
  pixel, `+ 0.5` on the lattice positions); at 2160 yellow gets three (five). A large print can
  shift its own copy, as [Cabinet](../prints/cabinet/PRINT.md) did; the kit keeps the films' look
  until the change is judged in motion.
- Open a dark ground with a soft knockout (`shade(…, {cut: true})`) before a light ink lands:
  yellow over green prints lime, on opened paper it prints as light. A soft knockout also lets a
  halo fade instead of ending on a cut circle.

## Depth

Four planes at falling coverage, one occluder and haze at each skyline turn a sticker on a
backdrop into a place (study 5).

- The furthest plane must not clear the sky: printed over it, it inherits the sky's value, which
  is haze. Give it its own ramp so its base sinks into the horizon. Nearer planes clear what they
  stand in front of.
- Haze each plane before drawing the next; one knockout at the end eats them all.
- A silhouette at its plane's tone vanishes: a treeline needed 0.52 on a 0.3 hill; telescope
  dishes vanished until the sky behind was lightened and they moved onto the skyline.
- A cropped dark foreground silhouette is one depth cue; it needn't be darkest or detail-free.

## Texture, last

Added last, cut first. At 340 px contact-sheet size the texture A/B is hardest to tell apart while
silhouette, tone and depth A/Bs are obvious; at montage speed outline and value beat interior
marks. Spray over a whole form eats the silhouette; keep it where the light is.

- No extra ink needed: a ramp for a turning form, `hatch` for a shaded flank, `spray` for an edge
  catching light, fine-gap `hatch` with `cut` for a dry pass. Carved line (grout, foam, veins,
  pleats, steam) is ink removed, not pale ink added.
- Dots thin outward (fog, glow, something to nothing); hatching thickens inward (deep water,
  shadow under a mass, the nearest plane's weight). Sprayed depth reads as evaporating, hatched
  dissipation as a screen door. One gradient is dots or lines; if a frame uses both, they belong
  to different surfaces.

## Composition and focus

- Compose around the focus and eye path, which may move. If a concept needs a fixed anchor,
  decide what it represents first; retrofitting the Resonance (540, 540) dot into a wave study
  cost five iterations.
- Vary shot size: cropped by two edges, or a tenth of the frame in empty sky, not everything
  middling and centred.
- One area of high detail; simplify the rest. Three things the same size always compete.
- Reserve the subject's zone at its hero moment before placing clutter, particles, glints or
  foreground occluders, and check that frame, not the establishing one. Roost's sun glints printed
  over the reflected flock; in another code-drawn film a prop placed early covered the hero's
  entrance.
- Ground objects through contact, occlusion and the receiving surface's light; `bed` is a
  shortcut for a soft contact shadow, not a substitute for that surface.
- Originality is mostly viewpoint and moment: the instant the kettle whistles, a wave as an
  opening, what the dish is listening to. A second scale of life (one gull, one figure) gives the
  main mass its size.
- A hue outside the scene's working pair must be earned by meaning. Test by removal: if meaning
  survives, it was decoration, and decoration turns a third overprint brown. One such element is
  a default, not a limit.
- Repeats of one event (lanterns, lit windows, flowers on a stem) can carry focus. Equal repeats
  read as several subjects; decreasing emphasis (nearest full, each next lower, furthest nearly
  paper, far ones losing their overprint dark first) reads as one event across distance.
  (Adapted from an external poster-prompting skill; unproven in a film here.)

## The frame budget

Measured from a community recreation of Kevin Ngo's riso animation, 112 frames at 4 fps.
**Occupancy** (share with readable ink) and **mass** (share reading dark or solid) move
independently.

| Occupancy | 0–20% | 20–40% | 40–60% | 60–80% | 80–100% |
|---|---|---|---|---|---|
| Frames | 32.1% | 12.5% | 7.1% | 6.2% | 42.0% |

Quartiles 6.5% and 94.5%; the 53.8% median is a value almost no frame holds. The 15 middle frames
(40–80%) are two passages in transit, not compositions. That is this piece's rhythm, not a rule:
a middle-density scene works with clear value groups and negative space; marks without hierarchy
are clutter.

**Covered is not heavy.** As the rings close in, occupancy climbs 42% → 69% while mass stays
under 3%; at t=22.0, two open-screen fields each with a keyline ring and solid dot give 65%
occupancy, 2.0% mass. Screen and line fill a frame almost free; mass is the expensive budget,
spent on full-bleed scenes and the indigo night (up to 90%). Open screen makes atmosphere without
another dark but can't replace a missing subject, space or action.

[studies/composition.html](../studies/composition.html) draws these rules: `budget` at 54%
occupancy, 0.4% mass; `deepen`, `window`, `lanterns` at 78–96% occupancy, 20–44% mass. Measure
your own from stills (cleaner than h264):

```
node shoot.mjs ../films/<name>/index.html --range 0:27.75:0.25 --out <dir>
```

```python
import numpy as np, glob
from PIL import Image
B = 12                                   # ~2.6 screen cells at pitch 4.6; averages the dots away
for p in sorted(glob.glob('<dir>/t_*.png')):
    a = np.asarray(Image.open(p).convert('L'), np.float32)
    a = a.reshape(a.shape[0] // B, B, a.shape[1] // B, B).mean(axis=(1, 3))
    paper = np.percentile(a, 97)         # bare stock is the brightest thing in frame
    d = np.clip((paper - a) / paper, 0, 1)
    print(p, f'occupancy {(d > .04).mean() * 100:5.1f}%  mass {(d > .35).mean() * 100:5.1f}%')
```

Paper is the frame's own 97th-percentile block, so a full-bleed dark frame reads ~96% occupancy
by definition; read the two numbers together.

## Text in the frame

Optional. Text is ink, with screen, registration and knockout; choose its layer (conventions from
the same external skill, unproven here):

- **Sunken:** in the ground's plate before its haze and knockouts; atmosphere rolls over it.
- **Same layer:** a `Path2D` on the subject's plate at its coverage and screen; part of the impression.
- **Overprinted:** own plate and offset, printed last; the newest thing on the sheet.

A word meant to be read stays legible for at least 0.5 s plus one second per three words after
its write-on ends, and lands about 0.6 s after a camera move begins (caption timing from an
explainer kit; unproven here).

Rather starved than bold. Fade on alpha and width, never coverage (a screen breaks a thin stroke
into dashes). Text follows the scene's physics (dissipation, light, current); a square line in
the corner of a moving frame reads as a label added later. At most one starved or broken word per
frame; two is a filter. Captions stay lighter than the subject; posters compose their own hierarchy.

## Judging a frame

A halftoned 1080 frame shown scaled down beats against the sampling grid and invents banding. A
sky showing three hard bands measured 99, 99, 100, 99, 100, 104, 106, 108 in 80 px rows: a smooth
ramp. Confirm banding, moiré or a weak silhouette at 1:1 before acting:

```
python -c "from PIL import Image; im=Image.open('frame.png').convert('L'); w,h=im.size; px=im.load(); print([round(sum(px[x,y] for y in range(b,b+90) for x in range(0,w,3))/(90*len(range(0,w,3)))) for b in range(0,h,90)])"
python -c "from PIL import Image; Image.open('frame.png').crop((40,800,700,1060)).save('crop.png')"
```

Block means answer tone; a 1:1 crop answers small shapes and is the only way to know a
thumbnail-sized silhouette reads (it found dishes buried in their own ridge).

## The studies

`node shoot.mjs ../studies/index.html --times 0,1,2,3,4,5,6,7,8,9,10,11 --sheet --cols 4 --cell 300`
(composition: `../studies/composition.html --times 0,1,2,3 --sheet --cols 2 --cell 520`).
0–5 are A/B (old way left); 6–8 whole pictures.

| t | Study | Proves |
|---|---|---|
| 0 | silhouette | assembled primitives vs one cut contour |
| 1 | stroke | constant `lineWidth` vs `nib` ribbons |
| 2 | ramp | flat screens vs coverage gradients; sun knocked out of its sky |
| 3 | form | flat vs modelling by subtraction, bedded, one overprint dark |
| 4 | texture | flat screen vs ramp, hatch, spray, dry pass |
| 5 | depth | flat ground vs four planes, haze, occluder |
| 6 | kettle | the moment it whistles; the dot is the sound's source |
| 7 | wave | a barrel is an opening; the dot is the tube's throat |
| 8 | telescope | scale instead of detail; the dot is the galaxy core |
| 9–11 | motion | see [motion.md](motion.md); shoot as strips |
