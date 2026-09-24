# Scene space and controlled motion

How to construct perspective, attach details, order occlusion and give motion explicit units and
clocks; read it when a scene needs perspective, camera changes or precise effect speeds.

`tools/lib/visual-kit.mjs` is the authoritative pure geometry/timing kit; `tools/new-riso.mjs`
embeds it as `Space`. It is not a 3D renderer: no anatomy, visibility, physics or judgment.

## Construct space once

World coordinates are +Y up. A camera looks from `eye` to `target`; positive depth points
forward and image Y points down. `focal` is in pixels, not degrees. Libraries using negative
camera Z differ: don't mix sign conventions. The default frame is 1080 square.

```js
const cam = Space.camera({eye:[900,850,1400], target:[0,300,0], focal:1400});
const desk = Space.plane([-400,250,-240], [800,0,0], [0,0,480]);
const border = cam.polygon([desk(0,0),desk(1,0),desk(1,1),desk(0,1)]);
const key = cam.polygon([desk(.2,.2),desk(.24,.2),desk(.24,.24),desk(.2,.24)]);
```

- `plane(origin,uAxis,vAxis)` maps local UV to world. `camera.project(point)` returns XY, or null
  behind the near plane. `polygon(points)` and `line(a,b)` clip before projecting.
- Interpolating in screen space across four projected corners gives wrong spacing. Build an
  ellipse, repeated slat or handle in the host surface first, then project every point.
- Block dimensions with a few solid masses, then draw the real shell, joints, recesses and
  silhouette; a box with many lines is still a box. Projection supports observed form; it doesn't
  impose a geometric style. Organic contours and deliberate graphic flattening remain valid.
- Frame by numbers, not by eye: take the projected bounds of the subject plus everything attached
  to it at its hero moment (rope, rider, reflection, wake, the flock's spread), then scale so that
  span fits the safe area and place it. A pinhole camera shows world height H at depth z as
  `focal × H / z` px. In another code-drawn film, framing set by eye took five rounds of fixes.

## Occlusion and light

Projection does not solve visibility. Define what covers what: background, support, object
shell, attached details, foreground occluders.

- An average-depth painter sort can put a wall or table over its own details. In the
  drawing-machine study it did exactly that; explicit background/support/object/detail order fixed
  it (the lamp draws behind the plotter; the desk top occludes the leg tops). Sort only suitable
  disjoint surfaces or use explicit order; split intersecting geometry at the overlap. There is
  no depth buffer.
- A subject that turns to show its other side needs layering by depth, not fixed rules.
  Eclosion drew legs over the body, the head over the thorax and the body over the wings: right
  in profile, but once the butterfly turned its back to the camera the body read as facing us
  while the wings showed their backs. The user caught it at the flight, where the pitch also
  tipped the head toward the lens. Draw what lies beyond first (legs, antennae, far wings), then
  each body part, then redraw inside that part's silhouette only the wing surface nearer than the
  part's near surface. A plane's depth is affine in screen space and a cylinder's near surface
  nearly so, so "nearer" is one half-plane clip (`drawButterfly`, `wingDepth`, `axisFront`,
  `halfPlane`). A surface that wraps a part (closed wings round the abdomen) is biased toward its
  own side by the part's radius.
- Use the same projected shape for the subject and all its plate knockouts.
- A contact shadow lies on the receiving plane; a cast shadow follows a chosen light direction.
  Don't offset a generic ellipse under everything. Highlights, hatching and seam spacing turn
  with the surface.
- A flexible sheet (curl, page turn, peel) is one curve across its fold. Bake its face once as
  coverage, then draw runs of samples that one affine map can carry, far to near; a point at height
  Z scales by H/(H − Z) about the frame centre. The face turns over where the projected order along
  the curve reverses, which also mirrors it. Screening stays in `compose()`, so no screened bitmap
  is resized (Nonpareil's `sheetAt`, `drawSheet`).
- A rigid flap (kite panel, box lid, page of a stiff book) rotates about a persistent crease axis
  with shared vertices that cannot separate. Flip its ink by projected polygon facing at the
  edge-on pose, and fade crease accents with hinge angle so they don't vanish abruptly at rest;
  both removed visible pops in a folding kite.
- A surface rising from the ground casts its shadow on the ground before any of the surface is
  drawn. Laid between its grounded and raised parts, the shadow printed a 1 px crease where the
  sheet left the bath; lay it again only where an overhang covers a part still lying down, clipped
  to that side.
- Moving camera: transform vector geometry, then screen at final pixel size; never scale a
  screened bitmap to fake a dolly. Cache static coverage per fixed camera and redraw only
  changing geometry. Arbitrary camera motion may exceed the frame budget: measure on the real
  scene before committing a sequence to it.
- Interpolate a zoom in `1/z` or `log z`, not `z`, or a big pull-out rushes at one end.
- Stroke weight under a zoom is a choice. Scaling it with the full zoom gives a 3× close-up a 3×
  nib, heavier than the mark would be redrawn at that size; holding it in pixels makes the
  close-up spindly. `w * zoom ** 0.35` (about 1.5× at 3×) is an unmeasured starting point: judge
  it on 1:1 crops at the closest and widest framing. Screen pitch never scales.

## Speed units and an owner

Decide whether a request changes an action's duration, a material's speed, the cut rhythm or the
whole film; they are different changes. Record action clocks in seconds. Tie masks and sound to
meaningful arrivals rather than duplicating time constants.

```js
const route = Space.pathByLength(sampledWorldPoints);
const stroke = Space.travel(route,{start:1.2,speed:180}); // world units / second
// Alternatively: {start:1.2,duration:2.4}; never both.
const {point,distance,u} = stroke.at(t);
drawLine(route.prefix(distance));
drawPenAt(point); // same sample, so the tool cannot run ahead of the mark
```

- `pathByLength` approximates length along the supplied polyline; sample curves finely enough
  for their size and inspect fast motion. A linear curve parameter is not constant speed (it
  speeds up through long segments).
- World-speed travel changes screen speed with depth. For deliberately uniform graphic travel,
  measure the path in screen pixels and rebuild the table when the camera changes.
- `travel` clamps before/after and exposes start/end/duration. Its default is constant distance
  per second; an optional `ease(u)` changes that deliberately.
- Inspect an arrival at 0.5×, 1× and 2× before claiming robust retiming. Retiming changes
  duration, cut times and action clock together. When the action no longer fits, lengthen the
  shot; never truncate it at the old end time.
- A drawn-on mark matches its static drawing only once progress is exactly 1. `travel` clamps and
  `prefix(route.length)` returns the whole route; a hand-rolled reveal (a glyph write-on, a custom
  arc-length walk) must clamp the same way, or it stops at 0.999 with the last sliver undrawn. A
  cue ending at the film's duration never completes: the last frame is `duration - 1/fps`.
- `hermite(a,b,va,vb,seconds,u)` uses endpoint velocities in units/second; share them at a joint
  for a continuous handoff.
- `ballistic(origin,velocity,acceleration,age)` evaluates particles analytically; seed birth
  times and attributes once. Collisions need an explicit piecewise trajectory or deterministic
  precomputation. No universal ease models every material.
- Keep coupled mechanics on one clock: pen and trace, hand and handle, boat and wake, loaded
  branch and launch must agree on contact and release. A new camera shot must not restart that
  clock. Independent atmosphere may use its own stable phase. Loops and live tone: [motion.md](motion.md).

## Effect design card

For a requested effect, record the smallest useful spec beside the work:

| Field | Example |
|---|---|
| Cause and consequence | Pen contacts paper, deposits ink, lifts before transfer. |
| Coordinates and clock | Sheet UV mapped to world; passage time survives the cut. |
| Parameters with units | Travel in world units/s; lift height in world units; delay in s. |
| Phases | Prepare, act, settle/hold; name any instantaneous cut. |
| Geometry and plate policy | Shared endpoint; full silhouette knockout; fixed page screen. |
| Limits and inspection | No collision simulation; test slow/normal/fast and the transfer seams. |

Don't build a universal catalogue of fancy effects. Develop one relevant signature action, test
its geometry and timing, and keep the reusable mechanism. Actions may share a solver without
sharing an appearance or speed.

## Executable example: the drawing machine

[studies/scene-space.html](../studies/scene-space.html): a 12 s silent construction and motion
study plus native still; a scoped demonstration, not a long film or house style. An invented
flatbed plotter lays seven nested survey contours, lifting between them, then parks. Wide view,
closer working-surface view, wide again for the lift and result; cuts at 3.6 s and 8.6 s keep
action time. Construction draws on the inspected CalComp brochure
([research sources](visual-development.md#research-sources)), not a named model. One camera
projects desk, inset sheet, controls, rails, case chamfers and supports; paper coordinates own
both lines and pen endpoint; separate axes drive bridge and carriage. Blue, orange, indigo, with
overprinted darks; lamp, panel, cable and loose sheet give scale. Static plates cache per camera;
moving geometry redraws before screening; the two views are distinct vector projections, never an
enlarged bitmap.

Corrections found by inspection: mean-depth sorting covered attached details (above); thin
screened lines broke into dashes, so lines use solid coverage with opacity for tone while fills
keep dot-size tone; travel uses cumulative distance with pen and trace on one sample, and
transfers lift the pen in their own phase; retiming scales duration, cuts and clock together
without truncating a slow stroke.

Controls: play, scrubber, frame-step arrows, and selectors that reload the page. `?view=wide` /
`?view=detail` hold a camera; `?debug=structure` shows the grid; `?debug=value` shows luminance;
`?rate=0.5` retimes (12 s normal, 24 s half, 6 s double were checked; 0.25–4 parses but extremes
are unvalidated). Its geometry is an embedded copy of `tools/lib/visual-kit.mjs`; edit the study's
art directly, don't regenerate it with `new-riso.mjs`. From `tools/`:

```
node visual-kit.test.mjs
node scene-space.test.mjs
node verify.mjs ../studies/scene-space.html
node review.mjs ../studies/scene-space.html
node still.mjs ../studies/scene-space.html --at 6 --out <png>
node shoot.mjs ../studies/scene-space.html --times 6 --query "debug=structure" --engine firefox
node render.mjs ../studies/scene-space.html --engine firefox
```

`visual-kit.test.mjs` covers projection, clipping, distance travel, retiming, velocity continuity
and analytic flight: mechanics, not art.

**Verified:** repeat and seek-history checks at 14 times in Chromium and Firefox (rasterization
differs by browser); seven times spanning a cut identical across 0.5×, 1×, 2× in Firefox; warm
draw median 12 ms, p95 13 ms, max 14 ms over 120 frames (one machine, no encoding); repeatable
1080² PNG; silent MP4 12.000 s, 30 fps, 360 frames, full error-gated decode; UI selectors work.
Sheets, close view, construction/value views and encoded strips through contact, first cut and
parking were inspected; continuous normal-speed playback was not.

**Limits:** stylized materials, idealized motor motion (no acceleration/jerk limits), small contact
lift in the wide view, no arbitrary camera motion or depth buffer. It proves nothing about
anatomy, natural fluid motion, minute-long pacing or better aesthetics across fresh sessions;
those stay [review cases](quality-bar.md#review-cases).
