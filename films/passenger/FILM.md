# Passenger

36 seconds, 1080 × 1080, 30 fps, scored (procedural, D major, 6/8). Authoritative source:
`index.html`. Delivery: the MP4 is attached to [the v1.0 release](https://github.com/sevenevesai/riso-windowseat/releases/tag/v1.0)
as `passenger.mp4`, the Firefox render (`render.mjs`) of `index.html` with its score muxed.

A child of two repos: `sevenevesai/riso-windowseat` (Window Seat: one train window, the world
passing, a glass of water on the sill; Eclosion: a butterfly's first morning) and
`alexgreensh/anidoodle` (Mechanical Lepidoptera: a drawing makes itself in the order a hand
would, then comes alive and leaves a butterfly-shaped blank on the sheet it came from).

## Premise

Before dawn a train window has fogged over. A butterfly draws itself in the condensation the way
a finger would: head, body, the four wing outlines, antennae, then each wing coloured in cell by
cell, and finally border dots tapped in. The fog the finger never touched is left as the veins.
The clear lines are windows, so the drawing is made of the passing view. Village lamps slide
through it, and the dawn fills its wings, blue at the tips and orange at the base. When the sun
clears the ridge, its warmth does two things. It starts lifting the fog, and it lets the drawing
fly (a butterfly cannot fly until the sun has warmed it). Ink runs out along the veins from the
body, the wings shiver twice, and it peels off the glass on its first upstroke. It keeps the dawn
it was filled with as its colour. The camera, released by the take-off, pulls back from the pane
to the seat as it crosses the carriage. It lands on the far rim of the glass of water and drinks,
and rings cross the water. Then it opens its wings once in the sun. Up in the last of the fog,
the butterfly-shaped hole it left is still there.

Transformation: drawn → alive. Turn: sunrise at 17.2 s, caused inside the world (light and
warmth). Token: the drawing, which returns as its own blank. Window Seat's token, the glass of
water, gets a passenger.

## Inheritance

| From | Kept |
|---|---|
| Window Seat | A carriage window with a rounded aperture and a glass of water on the sill. The world is at infinity and slides by on a distance clock. Four inks (yellow, pink, blue, indigo) and the live-plate compositor. The water trembles at the rail joints, and the score hears the same joints. |
| Eclosion | Warmth before flight. A planar 3D wing model with fold, sweep and body frame, so one set of wings reads from above, in flight and in profile. Fluid pumped into the veins becomes the ink running out from the body. |
| Mechanical Lepidoptera | Marks are made in hand order: long strokes fast, fiddly ones slow, and the colouring-in speeds up. It draws itself, then lives, and the turn has a physical cause (their drop of water, our sunrise). A continuous move from macro to wide is released by the take-off. The blank left where the drawing was. No dead air. Music by recipe: major key, plucked, I–IV–V–I, a question answered. |

## Mapping, drawing → creature (literal positions)

| On the glass | Alive |
|---|---|
| Cell scribbled clear, showing the dawn | Dorsal cell pigment: the outside at T.lift, baked once (`bakeTexture`), deepening over 0.6 s (`TEX_GAIN`) |
| Fog left between cells | Dark veins (indigo over pink), inked from the body outward (17.7–18.85 s) |
| Fog band inside the outline | Dark border |
| Finger-tip dots in the band | White marginal spots (paper) |
| Finger outline | Dark edge; its outer half stays clear and becomes the hole's rim |
| Body stroke | Dark furred body with paper dots and eye glints |
| The fog itself | The underside colour (`UNDER`) |

## Construction

- One timeline `T` (touch, sunrise, wake, shivers, lift, pull-back, land, sips, open). The
  drawing schedule `STROKES` is built from stroke lengths and speeds at load (`T.drawEnd` 13.45 s).
  Shots, marks and the score all read these.
- Camera: a perspective dolly with lens rise. `proj(X,Y,z) = [540 + (X−ex)·k, hy + (Y−ey)·k]`,
  k = 700/(D−z), S = 700/D. Macro S 4.0 → 3.45 creep (hy 800, so the doodle's cells see only
  sky). The pull-back runs 20.0–27.2 s to S 1.62, then creeps back in to 1.76. Everything outside
  is at infinity and depends only on `hy` and the distance clock.
- Carriage in 3D: the pane at z 0, reveal to the wall at z 88, and the sill out to z 118. The
  glass of water (brim-full) stands at z 55, so the pull-back has real parallax.
- Fog: world-anchored density noise evaluated on a 270² grid per frame and smoothed up.
  Strokes, drips and (after lift-off) the silhouette are cut at full resolution. Where fog lies,
  each plate becomes a heavily blurred copy of the outside mixed 84 % toward a near-paper tint.
  Lamp halos and the sun's glow scatter into it on a 135² layer. After sunrise a ragged
  evaporation front sweeps in from the sunny right and stalls short of the hole.
- Drips: beads run from where strokes pool (abdomen tip, both hindwings) and two background
  drips were already running. Each bead has a paper glint and a dark lower rim.
- Butterfly: the doodle's own outlines and cells, folded about the body axis, forewing sweeping
  back to close. The body frame comes from head and dorsal vectors blended rest → flight → perch.
  Everything is projected per vertex; the wings are depth-sorted and the dorsal/ventral face is
  chosen per wing. Before lift-off its cells are windows (the hindwing is clipped under its
  forewing). The fog cut switches to the full silhouette only once the ink covers it (18.85 s),
  and the colour freezes at lift-off (19.6 s), as the second shiver returns the wings to within
  3° of flat.
- Flight keys are authored as screen position and depth, then converted through the camera of
  that moment. Wingbeat 4.4 Hz, two glides, a bob on each downstroke, erratic bank.
- Perch: far rim, head left, wings closed with the forewing swept back. The proboscis uncoils
  to the water, and five sips ring the surface. To bask it rolls its back toward the room and
  opens wide (full open 32.5 s).

## Score

D major, 6/8, drawn from both parents: Window Seat's felt piano (FM) and anidoodle's plucked,
major-key recipe (Karplus-Strong). The kit is copied from `studies/sound.html`, with `paper` →
`paperFx` and `tick` → `tickFx` because the engine owns those names.

- Bed: room tone, a low carriage rumble, rail joints as a muffled double knock (the same joints
  that tremble the water).
- Drawing (0.8–13.45 s): every mark is a note. Head, body and first wing ask the motif A4–D4–E4.
  The outlines and antennae restate it and leave it hanging on A. The colouring-in arpeggiates
  I–IV–V–I, one chord per wing and a pluck per cell. The border dots are falling music-box
  twinkles, and soft glass whispers follow the strokes.
- Dawn: Bm then G pads and chords, with a deliberate hush 1.5 s before the turn (valley at 15.65 s,
  −10.1 dB).
- Sunrise (17.2): glass swell peaking on the limb, Asus4, low A. Ink (17.7–18.85): a rising
  arpeggio that resolves the sus. Shivers: two soft mallet tremolos.
- Flight (19.6–27.6): four 2-second bars of 6/8 (D, G, Em, A) under a felt-piano tune built from
  the motif. The fifth downbeat is the landing. Wing flutter grows as the butterfly nears the
  lens; foreground is panned by screen x.
- Perch: a small ting on the rim, G then Em, water drops on each sip. The answer (A–D–E–F♯)
  lands its F♯ on full open (32.5) over D major, and the motif returns softly as the tail.
- Room: the kit's `impulse` is the hot one `docs/sound.md` warns about. Measured with a single
  note, send .3 returned about 13 dB over the dry signal (send 0 → −42.8 dB RMS, send .3 →
  −29.2 dB) and the mix's stereo correlation was −0.06. As Held did, the wet gain is cut (to .032)
  for a close, dry sound, and correlation rose to 0.48. Copying Window Seat's `impulse` is the
  documented alternative.

Marks (`__riso.marks`): touch 0.8, sunrise 17.2, lift 19.6, land 27.6, full open 32.5.

Measured (Firefox, `audio.mjs --twice --ffmpeg`):
`I −16.5 LUFS, LRA 5.4 LU, TP −1.0 dBTP, clipped 0, firefox byte-identical`. Onsets land at
+15, —, −10, +5 and −5 ms from the marks (the sunrise is a swell; its peak is at +220 ms).
Bands: 6.6 % sub, 30 % low, 46 % low-mid, 17 % mid, 0.7 % high, 0.07 % air. That is dark by
intent, with very little air. The three listed discontinuities (0.82, 3.07, 5.75 s) are pluck
attacks on stroke onsets. Nothing has been heard.

## References inspected (Wikimedia Commons, 2026-09-25; downloads in `out/passenger-refs/`, git-ignored)

| File | Establishes |
|---|---|
| `Angry-face-window-condensation-2021-Apr.jpg` | Finger lines in window fog at night: dark (outside) lines on pale lit fog, rounded ends, near-constant width, soft edges, fine grainy fog. |
| `Condensation_on_a_window_at_sunset.jpg` | Backlit condensation glows around the light; droplets are lenses with bright cores, bigger low on the pane. |
| `Monarchbutterflysdrinking.JPG` | Perched on a flat surface with wings open, the forelegs are tucked and the proboscis goes down to the liquid. |
| `Taking_a_drink.jpg` (monarch, lateral) | Closed wings upright with the ventral hindwing outermost and the forewing apex showing above it. The body is under the wings, antennae forward, and the proboscis curves down. |

The wing is an authored doodle, not a specimen trace. The monarch-like pattern of dark veins, a
dark border and white spots follows from the mapping above.

## Evidence

| Check | Result |
|---|---|
| Delivery decode (`passenger.mp4`) | 36.00 s, 1080 frames, 1080² H.264 High yuv420p, 30 fps, AAC 48 kHz stereo 196 kb/s; muxed I −16.5 LUFS, peak −1.0 dBFS; 72.7 MB |
| `review.mjs --mp4` (delivery) | median 4.67 % of pixels change per frame; 0 runs under 0.1 % for ≥ 0.5 s |
| `verify.mjs` (Chromium and Firefox, 29 times incl. every shot boundary) | seek is pure in t; contract holds |
| Pop scan of the delivery MP4 (360 px, blurred; [quality-bar](../../docs/quality-bar.md)) | 0 flags in 1080 frames. Per-second mean change: 0.2–0.4 through the drawing and dawn, 2.9–11.8 at lift-off and the close pass, 1–4 on the pull-back and landing, about 1.0 through the perch |
| Hand-offs, adjacent frames (Firefox, 270² luma, mean change) | wake 17.667→17.7→17.733: 0.39, 0.37; ink/silhouette switch 18.833→18.867: 0.50; colour freeze 19.567→19.6: 2.27 during the shiver's last frames. A 1:1 crop pair matched except for a saturation step, since replaced by a 0.6 s ramp (`TEX_GAIN`; the pair was not re-shot after that change). The first wingbeat that follows is 7–9 |
| `review.mjs --mp4` (a rough cut) | median 4.2 % of pixels change per frame; 0 runs under 0.1 % for ≥ 0.5 s |
| Strips read | lift-off 19.5–19.8 at 1/30 s, landing 26.9–27.9 at 0.1 s, flight 19.6–28 at 5 fps, whole film at 1 fps |
| Score | as above |

## User constraints

"Make a baby from these 2 repos", about 30–40 s. The score was added because both parents'
films are scored; it is optional in the contract (`renderAudio`).

## Remaining weaknesses

- Nobody has watched it at speed or listened to it. Judgement comes from strips, sheets and
  meters. Worth watching first: 19.6–21.5 (lift-off and the close pass), 26.5–28 (landing),
  31.5–33.4 (the opening).
- The first upstroke at macro distance throws one wing toward the lens as a long sliver for about
  two frames (≈19.7–19.75).
- Remnant fog during the pull-back can read as low cloud over the fields rather than
  condensation on the glass.
- The dorsal colours are pastel next to Eclosion's orange. The pigment is the sky it kept, lifted
  by a gain.
- The perched butterfly is about 110 px tall in the last frames. The window's frame is out of
  shot at the end; only the sill line and the glass carry the Window Seat composition.
- Score: nothing above 4 kHz to speak of. The cell plucks (a note per cell, 6.8–11.3 s) may
  read as busy.
