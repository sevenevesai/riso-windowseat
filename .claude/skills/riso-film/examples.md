# Worked examples: where to look

Every shipped work is one `index.html` with the whole engine inline. These tables point at
named functions and constants; search for the name (`grep -n "function compose"`,
`grep -n "const VK"`) rather than trusting line numbers. Each film's `FILM.md` explains why
the design went the way it did; read it before borrowing from that film.

The common engine is in every file under the same names: `rngFor`, `buildScreen`/`screenOf`
(halftone screens), `bakePaper`, `bakeScene`, `print`/`plane`/`shade`/`carve`/`hatch`/`spray`
(plate marks), `nib` (tapered stroke), `makeWob`/`wobbler` (seamless wobble).

## films/window-seat — fixed-frame journey, 78 s

One window, a world that travels past it, and every content switch hidden under full cover.
Its own plate compositor lets live elements be drawn per frame without baked scenes.

| Technique | Where | Why copy it |
|---|---|---|
| Analytic speed profile | `VK`, `VSEG`, `S`, `accel`, `speed`, `invS` | Distance is a closed-form integral of smoothstep speed keys, so every position is pure in `t` and parallax, vibration and sound can all read `S(t)`. |
| Shot list for tools | `SHOTS`, `shot`, `window.__riso.shots` | Named shots with `readAt` and transition give the harness and score one timing source. |
| Live-plate compositor | `compose`, `resetPlates`, `put`, `add`, `knock`, `putM`, `smear`, `mixCov` | Per-plate coverage canvases screened by threshold at compose time; `put` occludes exactly, `knock` returns plates to paper, `smear` blurs along travel. |
| Parallax layers | `fields`, `bridge`, `forest`, `towers`, `mountains`, `ridgePath` | Each layer is placed by `S(t)` times its depth factor. |
| Reflections | `reflectPlates` (option `squash`), `canal`, `lakeside`, `mirrorAt` | Mirrors the plate stack below a waterline in rippled slices; `mirrorAt` turns the glass into a mirror in the dark. |
| Covered switches | `veil`, `fogD`, `hazeD`, `tunnel`, `passingTrain` | A content switch happens only while the view is a uniform field (D = 1) or fully occluded. |
| Sky keying | `SKYK`, `skyAt` | Palette keys over time; the one hard jump sits under a covered moment. |
| Seeded drops | `DROPS`, `dropPos`, `drops` | Seeded birth, stick time and radius; horizontal run follows `S(t)`, so drops stream at speed and fall straight once stopped. |
| Ballistic sparks | `BURSTS`, `ballistic`, `fwPos`, `fireworks` | Closed-form trajectories with drag; each burst is pure in its age. |
| Long exposure | `stars`, `STARS`, `POLE` | Trail arc length is a function of `t − T0`, not accumulated across frames. |
| Rainbow over reflection | `rainbow`, `lakeside` | Draw order fix: the arc drawn after the reflection so it does not mirror into an eye shape. |
| Sloshing glass | `SLOSH`, `slosh`, `glass` | A damped oscillator driven by `accel(t)` is integrated once at load into a table; `slosh(t)` interpolates it, so physics stays pure in `t`. |
| Level crossing | `crossing`, `X_LC` | A world event placed at a distance (`S(26.4)`), not a time. |

## films/roost — one continuous take, 70 s

A starling murmuration from sunset to nightfall in one fixed view. Eleven thousand birds are
the halftone: each is a solid 2–3 px indigo dot, and where the sheet turns edge-on they pile
into printed dark bands. Its compositor is window-seat's, copied.

| Technique | Where | Why copy it |
|---|---|---|
| Analytic crowd | `flockState`, `birdPos`, `BU`/`BV`/`BW`, `flockC` | Each bird owns a slot on a thin 3-D sheet that twists, bends and yaws by sums of slow sines; no simulation, so any `t` is exact and thousands of agents stay pure. |
| Crowd as tone | `drawFlock`, `birdGlyph` | Distant birds are dots whose density makes the value; only close birds get flapping glyphs. |
| Predator through a crowd | `falconWorld`, `TS`, `PS` | Birds are pushed from the falcon's current and two lagged positions, so the hollow trails it; the strike adds a travelling twist pulse. |
| Tilt as a horizon shift | `lookUp`, `horizon` | The only camera move is the horizon; every layer hangs off `horizon(t)`. |
| Draining into a point | `TR`, `XR`/`ZR` | Per-bird roost times are ordered along the sheet, so the flock pours in from one end rather than fading. |
| Reflections without glitter over them | `drawWater`, `GLIT`, `BK`, `BR` | Birds drawn to `BK` are mirrored into `BR` with the water's ripple, then cut from the glint mask so glints never print over reflected birds. |
| Stable glitter | `GLIT`, `drawWater` | Glints grow and shrink over about 2 s at full ink on a page-fixed column; see `FILM.md` for the flashing version this replaced. |
| Seeded reedbed | `REEDS`, `drawReeds`, `PLUMEC` | 210 stems with ribbon leaves; plumes on their own lighter plate mask; per-stem sway plus a shared gust. |

## films/held — cut narrative with physical rope, 70 s

A kite's line parts, it tumbles across a town, is snagged by a vane and caught by a sloop. Five
shots on window-seat's live plates; camera moves are vector reprojections before screening.

| Technique | Where | Why copy it |
|---|---|---|
| Rope and tail physics | `simChain`, `breeze`, `drawTail` | Verlet chain integrated once at load on a 1/240 s step, recorded at 60 Hz and interpolated, so `seek(t)` stays pure. Head node rides the attachment; bows orient from nodes ±2. |
| Line running through a snag | `gripAt`, `C_GRIP` | Pulls the rope point at arc length s onto a moving point, so line slides through a vane or up a forestay instead of pinning. |
| Velocity-matched handoff | `hk`, `C_KEYS`, `C_HAND`, `catchKite` | Hermite keys with explicit velocities; after the catch the kite is keyed relative to the masthead from its current position and velocity. |
| Events derived from simulation | `C_RING` | Where the simulated tail first meets the water, so the splash and its pan follow the physics. |
| Jitter metric | `chainsAt` (`__riso.chains`), `jitter.mjs` | Screen-space chain points for measuring frame-to-frame jumps; nothing draws them. |

## films/nonpareil — one overhead take, 70 s

Paper marbling from above: drops, stones, rake, comb and a pulled flower, then a sheet rolled on,
peeled back toward the lens like a page and landed face up, mirrored, beside the tray. The
compositor is window-seat's; the camera stays overhead and reprojects vectors.

| Technique | Where | Why copy it |
|---|---|---|
| Closed-form marbling | `opMap`, `applyOp`, `mapPoly`, `refine`, `stateAt`, `PREFIX` | Drops and tine passes are bijections of the plane (Jaffer & Lu), so every boundary stays a simple closed curve; stretched edges refine through the map; prefix checkpoints keep `seek(t)` pure. |
| One list for picture and score | `OPS`, `buildOps`, `beat` | Every drop lands on the 96 BPM grid; the picture, ripples, tools and score all read the same ops. |
| Bending sheet in perspective | `sheetAt`, `drawSheet`, `CURL`, `LOOP`, `PAT` | A curve across the fold drawn as runs of a baked coverage map, one affine map per run; heights scale by `HCAM/(HCAM − Z)`; screening stays in `compose()`. |
| Page-turn transfer | `peelAt`, `LOOP`, `PX` | A loop rolling without slipping puts the flap at x = 2a + λ − s, so the print is face up and mirrored by construction and lands exactly at `PX − s`. |
| Shadow of a rising surface | `castShadow` | Laid on the ground before any of the sheet is drawn; laid again only where the flap overhangs the part still lying down. |
| Lagging follow camera | `camTail`, `follow`, `sheetMid` | The camera tracks the carried sheet's mean x averaged over the last 0.6 s: a late, smooth follow that stays pure in `t`. |
| Water on a print | `drawRinse`, `frontV`, `wetRim`, `drawPool`, `RIVULETS` | A wavy front with a glossy band, flow streaks and the window reflected where it is wet; rivulets start on beats and are also score notes. |

## films/eclosion — one macro take, 36 s

A monarch leaves its chrysalis, pumps its crumpled wings full, shows them once and flies; the
camera returns to the empty case. Window-seat's compositor; the butterfly is a planar 3D model.

| Technique | Where | Why copy it |
|---|---|---|
| Planar 3D wings | `WING`, `wingFrame`, `bodyR`, `drawWingPattern` | Pattern in specimen units under one affine per wing (sweep, fold, body yaw/pitch/roll, orthographic camera); the wing normal picks the dorsal or ventral pattern. |
| Depth layering | `drawButterfly`, `wingDepth`, `axisFront`, `halfPlane` | Legs and far wings first; after each body part, wing surface nearer than it is redrawn through a screen half-plane clip. Holds from the side, from behind and in flight. |
| Crumple that unfolds | `PLEAT`, `deformer`, `drawCreases`, `expansion` | In-plane pleat displacement before the affine; creases print dark with paper ridges and fade as the wings pump full. |
| Layer through a ramp mask | `layer` | Draws a modelled surface into sprite plates and lays it over the frame as old·(1 − m) + new·m: the jade shell clearing bottom-up. |
| Motion blur for one subject | `blurred`, `TG`, `SIL` | Shutter samples drawn into sprite plates, averaged through the averaged silhouette. |
| Pendulum driven by events | `SWING`, `caseSwing` | Damped pendulum integrated once at load (240 Hz) and interpolated: shivers, the body's tug, a loaded rest, the push-off kick. |
| Still inside a container | `drawArt` (`inside`), `caseOutline` | The emerging body is clipped to below the split line and drawn under the case, so nothing pokes through the shell. |
| Measured specimen geometry | `measure-wings.py` | Rebuilds `WING` from a hash-pinned Commons photo; credit and license in `FILM.md`. |

## films/passenger — macro to wide in one take, 36 s

A butterfly draws itself in window fog, is warmed alive at sunrise and lands on the glass of
water; a child of Window Seat and anidoodle. Window-seat's compositor; a perspective dolly over a
3D carriage.

| Technique | Where | Why copy it |
|---|---|---|
| Fog as a scatter layer | `fogField`, `fogLayer`, `fogTint`, `fogGlow`, `fogLamps` | World-anchored density on a 270² grid; each plate halved to 34², mixed toward a near-paper tint, glows added at 135², laid through the mask as old·(1 − m) + F·m. Clear marks are cut from the mask at full resolution. |
| A drawing made in hand order | `STROKES`, `sched`, `tapAt`, `strokeHead`, `drawStrokes` | The schedule is built from stroke lengths and speeds at load, so the colouring-in can speed up; the score reads the same list. |
| Cells from a fan of veins | `makeWing`, `rayExit`, `scribble` | The outline is ray-cast from the wing base; cells are angular bands inset by the vein width; a boustrophedon scribble clears each one. |
| Drips on glass | `DRIPS`, `dripState`, `dripsOn`, `beads` | Beads at a stroke's low points run on an eased clock with a seeded meander; glint and dark rim are drawn after the fog. |
| Dolly with lens rise | `camAt`, `proj`, `planeT`, `kAt` | The horizon row is its own parameter, so everything outside reads only `hy` and the distance clock. |
| 3D carriage | `carriage`, `rrectPts`, `glassOfWater`, `ripples` | Pane, reveal, sill and tumbler projected per vertex, so the pull-back has parallax. |
| Planar 3D creature from 2D art | `basis`, `wingPt`, `drawWing`, `drawBody`, `drawButterfly` | The doodle's own geometry folds about the body axis; the frame comes from head and dorsal vectors blended rest → flight → perch; face chosen by the wing normal. |
| A view kept as pigment | `bakeTexture`, `TEX`, `TEX_GAIN`, `drawWing` (`look.tex`) | The outside at lift-off, baked once and mapped into the wing cells by an affine; the colour freezes as the wings return flat. |
| Flight keyed where it is seen | `FLIGHT`, `PATH`, `pathAt`, `poseAt` | Keys are screen position and depth, converted through the camera of that moment. |

## films/lumen — resonance form, 28 s

A centre dot opens eight worlds through irises and sweeps, recollects them through one
closing lens, then releases a flower. The template for cue-driven abstract shorts.

| Technique | Where | Why copy it |
|---|---|---|
| Cue list and dispatch | `CUES`, `DRAW`, `render` | Each cue is `{start, dur, kind}`; `render` runs every active cue's `DRAW[kind]`. |
| Overlapping reveals | `FLOW`, `drawWindow` | Each outgoing world stays until the next reveal (`reveal: 'iris'` or `'sweep'`) covers it; no empty beats. |
| One closing lens | `memoryRadius`, `drawRecollection`, `drawMemoryLens` | One continuous radius across four recollections; per-shot radii jumped. |
| Colourway swaps | `SWAPS`, `bakeScene(id, size, swap)` | Remaps plates for the recollection without redrawing scenes. |
| Scene registry | `scene('tide', {...})` with `live(ctx,u)` | Baked plates per world plus one live element. |
| Loop-safe live element | tide's `live` | Envelope value and slope reach zero before a filament wraps; recycling a visible carrier teleports a curve. |
| Release | `BLOOM`, `flowerGeometry`, `petal`, `drawRelease`, `drawNightGarden` | Staggered petal timings in one const that the score also reads. |
| Answer and attraction | `ANSWER_PULSES`, `drawAnswerRipples`, `drawAttraction` | Two voices approach; pulse times shared with the score. |
| Signature | `SCRIPT`, `letterStrokes`, `writeLetters`, `drawSignature` | Handwritten title drawn stroke by stroke with a progress parameter. |

## films/emergence — resonance form, sibling of lumen

Same machinery as lumen with new worlds; adds interference, a branch generator and screen
supercells.

| Technique | Where | Why copy it |
|---|---|---|
| Iris and sweep transitions | `FLOW`, `drawWindow` (`reveal`, `angle`) | Same contract as lumen; the sweep angle is per cue. |
| Branch generator | `arbor`, `arborPaths`, `drawArbor`, `ARBOR`, `NEURON_ARBOR` | One seeded generator grows both dendrites and the release; branches carry spawn times so any age replays purely. |
| Interference | `interference`, `drawAnswer` | Nodal lines drawn analytically from the two voices' positions. |
| Loop-safe fades | `life`, `smooth01`, `fract` | `life(v, edge)` is zero with zero slope at both ends of a wrap (web pluck, bubbles, network dashes). |
| Memory absorption | `MEMORY_ABSORB`, `drawMemory` | One const drives both picture and score. |
| Network ending | `NET`, `NET_EDGES`, `drawNetwork` | The arbor shrinks to one node; pulses travel edges. |
| Screen supercells | `SCREEN` (header comment), `buildScreen` | Non-reduced tangents (3/3, 2/0) keep the angle but add sub-pixel phases, so slow ramps stop banding into plateaus. Compare lumen's reduced `SCREEN`. |
| Knockouts | `carve`, `print`, `shade` with `cut` | A knockout at full coverage clears the screen gaps; highlights return to bare paper. |
| Drawn year digits | `YEAR`, `yearPath` | Small numerals as paths, sunk into or carved from the ground plate. |

## prints/

The print series, including `prints/workings` (whose print kit `tools/new-riso.mjs` copies),
are mapped in [riso-still/examples.md](../riso-still/examples.md).

## studies/

| File | Demonstrates | Look at |
|---|---|---|
| `studies/index.html` | Drawing-craft A/B pairs: silhouette, stroke, ramp, form, texture, depth, exemplars, motion weight and launch, live flame | `STUDIES` (ids and captions), `flame`, `FAMILY` |
| `studies/composition.html` | Frame budget, edge hierarchy, one event at several distances | `STUDIES`, `word` |
| `studies/scene-space.html` | 3D camera, path travel, cuts that preserve action time | `camera`, `pathByLength`, `travel`, `hermite`, `ballistic`, `staticObjects`, `motionObjects`, `SHOTS`; notes in `docs/scene-space.md` |
| `studies/sound.html` | The sound kit; see `riso-score/examples.md` | `Score`, `STUDIES` |

## How to borrow

- Copy routines, not scenes. A scene is tuned to its film's palette, timing and framing;
  the function underneath (`reflectPlates`, `arbor`, `life`) is what transfers.
- Check for collisions before pasting: every file defines `render`, `SCENES`, `INK`,
  `SCREEN`. Rename the borrowed routine or its constants when a name exists.
- Keep seeds keyed: take randomness from `rngFor('<film>:<thing>:<index>')`, never
  `Math.random()`, so the borrowed routine stays pure in `t`.
- Bring the timing contract with the routine: if it reads `S(t)`, `FLOW` or `CUES`, supply
  an equivalent in the new film rather than hard-coding times.
- Rerun `verify.mjs` after the paste; seek purity breaks quietly.
