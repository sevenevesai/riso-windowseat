# Sound

How to build, sync, bridge, mix and measure a film's score; read it when scoring.

The kit and A/B studies live in [studies/sound.html](../studies/sound.html); `tools/audio.mjs` is
the contact sheet for sound. First lessons came from [Lumen](../films/lumen/FILM.md). Named
subjects and timbres demonstrate techniques; they aren't required.

## The sound kit

Copy the `── sound kit ──` block after the motion kit; it depends on `rngFor`, `clamp`, `lerp`,
`W`. Instruments take the score, a time in film seconds, then options; `hit` puts the loudest
moment on that time by starting `attack` earlier.

| | |
|---|---|
| `Score({duration, key, room})` | context, buses `bed`/`fore`/`fx`, synthesised room, `place`, `noise`, `env`, `swell`, `render` |
| `s.place(node, {x, pan, send, bus})` | pan from screen x, reverb send; bass stays centred |
| `s.render({target: -16, ceiling: -1})` | render, then one static gain to the loudness target under a true-peak ceiling |
| `pad`, `organ`, `air`, `wind`, `rain` | sustained: chords, drawbars, room tone, weather from `at` to `end` |
| `mallet`, `glass`, `bell`, `musicBox`, `pluck`, `fm`, `sub`, `tick` | struck, plucked, FM, bass |
| `contact(s, at, {material})` | wood, metal, stone, felt, card: exciter through modal resonators |
| `paper(s, at, {kind})` | slide, turn, flick, tear |
| `drop`, `breath`, `riser` | water drop, band-swept whoosh, climb into a `hit` |
| `hz`, `note('F#3')`, `degree(root, mode, d)`, `grid(bpm)` | pitch and time helpers |
| `wavBase64(buffer)` | the `renderAudio()` return value |

## Determinism and engines

- The score is a pure function of film data: seeded noise buffers, envelopes starting and ending
  at silence, no clock reads. `audio.mjs --twice` renders twice and compares.
- Firefox is byte-identical. Chromium sums node inputs in unordered-set order, so renders differ
  by 1–2 16-bit steps in a few percent of samples at −90 dBFS, reported as jitter. A difference
  40 dB louder is unseeded state.
- Exactly `duration` at 48 kHz: `render.mjs` muxes with `-shortest`, so a longer score is cut
  (a 29 s score once met a 28 s film) and a shorter one leaves a silent ending.
- Set loudness by one static gain after render; `DynamicsCompressor` differs across engines and
  hides the balance the mix should already have.
- `ConvolverNode.normalize` off; scale the impulse yourself. The kit's `impulse` in
  `studies/sound.html` still divides energy by the sample rate, so its wet signal is about 77×
  hot: it masked Window Seat's attacks (fixed there) and forced Held down to wet .035. Copy
  Window Seat's `impulse`.
- Exponential ramps can't reach 0 (the kit floors at `1e-4`). `setValueCurveAtTime` owns its
  parameter for its span. Stop sources after release, never with gain open. Cache the render so
  `renderAudio()` and the player share it.
- An AudioParam sums its connected inputs with its automation, so modulation wired into an
  enveloped gain adds to the envelope instead of scaling it: in an explainer film a ±0.5 LFO on a
  0.04 envelope played about 12× too loud. Put tremolo and wobble on their own gain stage ahead of
  the envelope. The kit's `wind` adds its gusts this way; at its default depth the room tail masks
  the difference (its fall measured within 0.3 dB of a corrected version).

## Sound follows a visible event

Drive picture and score from the same event data so retiming a reveal moves its sound. Publish
claimed landing times as `window.__riso.marks`; `audio.mjs` reports each mark's onset and energy
peak.

- Sound lagging picture by up to ~40 ms fuses; leading by more than ~20 ms reads wrong.
- A fast attack lands at its start, a swell at its peak, so start swells early. Study 5: started
  on the mark it peaks 295 ms late; started early, 45 ms after.
- Early room reflections put the energy peak 50–150 ms behind onset even for a click; hence both
  are reported.
- Three to five true sync points per film (impact, reveal, snap into place); the rest breathes
  under the bed. Sound on every motion is a whole aesthetic, not a default.
- The cue start isn't always the accent: a sweep starts off-screen; a bloom's accent is peak
  expansion, which Lumen derives from projected area, not petal start. Lumen's act accents land
  125–225 ms after their marks, soft by design; check any accent the eye reads as a hit.
- Bowed or swelled cues have no onset to detect. Roost's detector found none at four of five
  marks; energy peaks sat −280 to +300 ms from them. That is not a passed 40 ms test: record the
  offsets and judge those cues with the picture.
- When the event is diffuse (a flock arriving, leaving frame), measure it from the picture's
  projection rather than choosing a time: Roost's `FLIGHT_SCORE` takes arrival and return from
  the visible fraction of projected birds and tempo from their density and speed.
- `audio.mjs` takes the steepest 10 ms rise within ±300 ms of a mark as its onset. Under a held
  bed it can lock onto beating: Eclosion's split read −55 to −105 ms wherever the note was
  placed, while the WAV's 10 ms RMS showed it rising where it was put. Before moving a note, print
  that envelope around the mark. A soft-mallet vibraphone builds over about 50 ms, so place it on
  the mark, not after it.
## Material is the timbre

A struck sound is exciter → resonator → body. Exciter speed is hardness: 0.5 ms of noise is a
click, 20 ms low-passed is felt. Partial ratios and decays are material: near-harmonic and short
for wood, inharmonic and long for metal, low-Q and brief for stone. Study 1: the same notes as a
sine ping and as strike noise plus modal partials; only the second reads as contact.

- Take the palette from the screen: paper slides and tears, ink rolls, plates thunk, drops, wind,
  rain, a ticking clock. `contact`/`paper` cover print; `drop`/`rain`/`wind`/`breath` weather;
  `mallet`, `glass`, `bell`, `pluck`, `fm`, `organ`, `pad` music.
- Heavier is lower and longer, smaller higher and shorter, closer brighter with faster attack,
  farther low-passed, softer and wetter.
- Felt piano, music box and mallets are the paper world's habitual palette; tape hiss and chimes
  are one texture, not the whole voice. A passage spends one focal timbre, as a frame spends one
  focal hue.

## Structure in a minute

- Spot first: list every boundary and event in `FILM.md` and decide whether the music notices it.
  Lock tempo to a cut only at a structural turn; re-syncing at every edit sounds stitched.
- Sixty seconds holds one motif (2–4 notes), at most one secondary idea and one harmonic device.
  Transform the motif by register, rhythm or harmony instead of a new tune per scene.
- Arc: establish, develop, turn, release. A drone changes harmonic colour without moving; an
  ostinato changes chords under a fixed rhythm; one bass-note change against either is a legible
  event, so spend it at the turn.
- Modes: lydian open, dorian bittersweet, mixolydian pastoral, pentatonic without tension,
  whole-tone without ground.
- Endings declare themselves: a button for a punchline, a tail for anything open, a hard out on
  the last cut for an abrupt one. Anything else sounds unfinished.

## Transitions carry the ear

Fading the mix to silence at a cut reads as a restart. Study 4: the naive handoff drops 4.3 LU
with a 200 ms hole 30 dB down; the crafted one moves 1.7 LU with no valley. Bridge by what the eye
follows:

- **Pre-lap:** incoming bed or a breath starts before the picture changes.
- **Post-lap:** outgoing tail rings under the new image; leave headroom in the overlap.
- **Pedal:** one held note or room tone spans the cut, claiming one place.
- **Pivot:** chords either side share a note.
- **Texture handoff:** one voice thins as another enters, not a crossfade through silence.

Save audible tools (riser, stinger, hush before impact) for the one or two real turns; at every
cut they cancel. An unbridged hard cut is a choice only when one of them marks it. Check summed
envelopes: a long release that's inaudible before the next attack bridges nothing.

A transition sound in a tonal score comes from the score's own instrument. The kit's `paper`
grains read as static and ripping under Nonpareil's handpan and were replaced: a handpan
recording played backwards into the moment the edge crosses mid-frame, then forwards out, in key
and panned with the edge. Undo the recording's decay (kept to −50 dB, so about 50/length dB per
second) or the reversed swell arrives only in its last second; soften the strike with a 30 ms
crossfade at the peak; pick long-ringing recordings for long run-ups
([Nonpareil](../films/nonpareil/FILM.md) `edgeGesture`).

## Density, silence, climax

- The ear tracks about two and a half simultaneous layers of one kind; a third reads as mass.
  Plan bed and foreground separately, each under that.
- Wall-to-wall music becomes wallpaper and leaves statements nowhere to land (study 9: full bed
  with a note every quarter beat vs room tone and three accents). Sparse frames want one voice or none.
- Digital silence between cuts reads as a dropout; `air` keeps room tone so a quiet picture is
  still a place. Real silence is a deliberate beat with a considered return, recorded in `FILM.md`.
- Louder and brighter is compensation, not climax. Study 6: that version jumps 8.4 LU and, with
  its true peak at the ceiling, pulls the whole reel down 3.5 dB; the prepared one rises 1.9 LU
  with a riser, low body and staggered accents. A soft release wants rising preparation, a rounded
  low-mid body, restrained upper partials and a tail into the next passage; a hard impact can suit
  another material. Judge the lift against what precedes it: more voices, brighter filters and
  gain compound.

## Mix and master

- `bed`, `fore`, `fx` feed the master, each with a post-fader send to one synthesised room
  (pre-delay, a few early taps, a darkening noise tail). The send is high-passed so bass stays dry,
  the return low-passed so a long film doesn't accumulate hiss.
- Pan foreground by screen `x`; centre sub bass and bed so a phone speaker gets everything. Put
  bed and accents in different registers; where they must overlap, duck the bed with automation.
- Balance voices relatively; `render` measures integrated loudness, applies one gain to −16 LUFS,
  pulls back if true peak would pass −1 dBTP, and records both in `s.stats`. Don't peak-normalise:
  a sparse score can pass a peak target far below platform loudness. When the ceiling wins, fix
  the peak, not the target. Platforms turn loud deliveries down and leave quiet ones quiet. A film
  may choose its dynamics; the tool warns beyond 1 LU and never enforces.
- Kit levels aren't comparable across instruments. In [Window Seat](../films/window-seat/FILM.md)
  a four-note `pad` at .03 sums eight oscillators, sat ~8 dB over everything and buried the
  foreground until cut to ~.012. A `contact` under ~150 Hz is a narrow band of a 3–6 ms burst and
  measured as nothing under a bed; a rail click needed f0 300–400 Hz plus a brighter `contact`
  4 ms later. If a voice seems missing, stub the others and compare raw RMS before touching levels.
- Three finished films put 40–75% of energy at 250 Hz–1 kHz and under 6% above 2 kHz (dark);
  nothing above 4 kHz means no air.
- A click at a note start is a gain jump instead of a ramp; the tool lists discontinuities (one at
  a designed tick is expected). The full-film list keeps the 12 largest; `--around`
  lists every one in its window.

## Judging sound

```
node audio.mjs ../films/<name>/index.html --twice --marks 6,13.9,22.14
node audio.mjs ../films/<name>/index.html --around 13.9 --window 1
node audio.mjs ../films/<name>/index.html --engine firefox --ffmpeg
```

- The sheet, top down: waveform lanes (balance, clipping); log spectrogram (register, air, voice
  placement); momentary and short-term loudness against the target band, with silences shaded,
  valleys marked, discontinuities ticked; green lines are marks. The table gives per mark: onset,
  peak, loudness change, quietest 200 ms nearby. A valley 10 dB under its surroundings at a
  handoff is the fade-to-silence failure.
- Console: same data, `FAIL` for a contract break, `WARN` for level outside the band. `--ffmpeg`
  adds ffmpeg's ebur128 reading (within 0.1 on films measured).
- Measurements support listening, not replace it. Listen to quiet passages, handoffs and the
  climax with picture in the full muxed export (section renders are silent). `render.mjs` prints
  the muxed loudness and true peak, since AAC can raise true peak. If the muxed peak passes
  −1 dBTP while the WAV doesn't, fix the source, not the target: zero-attack onsets ring in the
  codec (an explainer's overshoot fell from 4.3 to 0.7 dB with ~1.5 ms onset ramps and a 16.5 kHz
  low-pass on the master). If you can't listen, report the measured checks, leave perceptual
  quality unclaimed and name three to five times for the user to hear (first hit, the turn, the
  loudest moment, a handoff, the ending). Record direction, sync events, silences and what was
  measured or heard in `FILM.md`.
- A local revision can change approved audio without touching its notes. Moving Nonpareil's
  next bass entry re-cut the held note before it (`bowSpan` spreads its hops over the span),
  leaving a residual only 8 dB down inside the approved section. Check a revision against the
  previous WAV: fit one gain over the approved span, then measure the residual every few seconds;
  about −80 dB is identical up to loudness re-normalisation.

## Studies and gaps

7.8 s per study, A for 3.6 s then B; `node audio.mjs ../studies/sound.html` measures the reel.

| | Study | A vs B |
|---|---|---|
| 1 | contact | sine ping vs strike noise with modal partials |
| 2 | material | one noise burst vs wood, metal, stone, felt |
| 3 | timbre menu | plain sines vs glass, pluck, FM piano, bell, music box over organ |
| 4 | handoff | fade to silence vs carried tail under a pre-lap on a shared note |
| 5 | accent | swell started on the mark vs peaking on it |
| 6 | climax | louder and brighter vs riser, low body, staggered accents |
| 7 | weather | filtered white noise vs gusting wind, rain over a wash, two drops |
| 8 | paper | a burst per event vs slide, turn, flick, tear |
| 9 | density | full bed and constant notes vs room tone and three accents |
| 10 | space | centred and dry vs screen panning, a room, centred bass |

- Studies were measured, not listened to; perceptual quality is unreviewed.
- Presets are starting points, none tuned to an on-screen material; `card` and `felt` unproved
  against a picture.
- No study covers a looping bed's seam or a tempo change.
- `AudioWorklet` is unused; nodes plus per-sample buffers suffice so far.
