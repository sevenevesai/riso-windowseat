# Live plates

A per-pixel plate compositor for frames that are mostly in motion with tone; read it before
copying `compose()` or when a film's frames draw slower than playback. Tone on a single moving
element (`bandPass`, `relight`) is in [motion.md](motion.md#tone-on-a-moving-element).

For frames mostly in motion with tone (parallax landscapes, blurred foregrounds, moving sky
gradients) use per-pixel live plates, as in `compose()` in
[films/window-seat/index.html](../films/window-seat/index.html). Each frame draws continuous
coverage as alpha into one CPU canvas per ink (`willReadFrequently`), thresholds per pixel against
a page-pinned table, and multiplies onto paper: gradients print as dot size and the screen can't
swim. Four plates cost ~110 ms/frame at 1080 in Firefox: export is fine, playback well below 30 fps.

- Build each ink's threshold table once: screen distance field, low-frequency mottling,
  starvation flecks (255 = never prints), per-pixel jitter. Yellow's 5 px tile holds few levels;
  a smooth shift crossed them in hard blotches until jittered.
- Own a value with destination-out then `lighter` at the coverage: old·(1−α) + cov·α. With
  source-over second, soft and smeared edges printed lighter than both neighbours.
- Motion blur: n shutter samples into a mask with `lighter` at 1/n; full coverage survives where
  the shape stays, the smear fades. Shutter distance comes from the film's distance clock. Size
  n from on-screen travel, about one sample per 3 px (`smear`: `ceil(|d| / 3)`, capped at 10); a
  fixed 4 samples still strobed on fast camera swoops in another code-drawn film, which needed up
  to 24. Blur coverage before screening, never the screened frame.
- Draw the pinned interior (frame, wall, props) after the view through an evenodd aperture.
- Reflection (`reflectPlates`): copy coverage above the waterline, flipped, in 3 px slices with a
  sine x-offset; screened afterwards, so it can't swim.
- Hidden switch (`veil`): push every plate toward one colour; at D = 1 the view is uniform and the
  scene can change underneath (fog, rain haze), as can a passing object filling the window.
- Drops on glass: snapshot the plates, draw each drop's region inverted and minified in its clip.
  Drive runs by distance travelled, so drops stream at speed and fall straight when stopped. At
  4.6 px pitch, drops under ~8 px radius read as dirt.
- Fog on glass ([Passenger](../films/passenger/FILM.md), `fogLayer`): fog scatters, so where it
  lies each plate becomes a heavily blurred copy of the outside mixed toward a near-paper tint.
  Halve the plate step by step to 34², mix there, add lamp and sun glows at 135², upsample, and lay it through a density mask as old·(1 − m) + F·m. Cut the drawn clear
  marks from the mask at full resolution. Restore `fillStyle` on shared scratch contexts: a glow's
  gradient left on one turned the next plate's full-canvas `fillRect` into a partial clear, and
  the fog vanished from the frame the glow began.
- Fireworks: each spark analytic from burst age with drag and gravity, into a mask that knocks out
  the night before inking. Star trails are arcs of length ω·(t − t0).
- Sun glitter on water ([Roost](../films/roost/FILM.md)): glints switching on and off at
  5.3 rad/s were reported as flashing, and printed over the reflected flock. Keep glints at full
  ink and grow or shrink them over about 2 s; fading 1 px dashes by coverage drops them below the
  screen. Mirror the subject into its own mask with the water's ripple and cut that from the glint
  mask.

## Cost

A character film on five live plates ran 90–200 ms/frame in Firefox, of which screening was
only ~16 ms. Unbuffered in-page playback at that cost was reported as "choppy" before the art was
judged; the generated player now buffers slow films (tools/new-riso.mjs). Before optimising,
wrap the named draw functions and time a few sequential seeks per shot. What paid off:

- `ctx.filter = 'blur()'` processes the whole canvas. Blur each soft shape once into a scratch
  canvas limited to its padded bounding box, then stamp that mask on every plate at its coverage.
- Many similar strokes (strands, hairs): batch back-to-front groups into one path per pass;
  weaving survives between groups and a hundred strands cost a few dozen fills.
- A shot's static backdrop: draw it once, keep `getImageData` copies of the plates and
  `putImageData` them back on later frames of that shot. The copy is exact, so seeks stay pure.
