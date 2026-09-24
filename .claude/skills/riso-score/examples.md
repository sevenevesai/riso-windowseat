# Worked scores: where to look

Each score lives inside its film's `index.html` and is built offline by `renderAudio()`.
Search for the names below (`grep -n "function windowRain"`); line numbers drift. The film's
`FILM.md` holds the cue table and measured results for each score.

## studies/sound.html — the kit

The canonical `── sound kit ──` block that films copy, proved as A/B pairs (A procedural
default, B the craft) on one timeline.

| Technique | Where | Why copy it |
|---|---|---|
| Score object | `Score` (`s.ac`, `s.env`, `s.render`) | Offline context, buses, room and mastering to a loudness target in one place. |
| Pitch helpers | `NOTE_INDEX`, `MODES` | Note names and scale degrees to MIDI. |
| Struck voices | `struck`, `mallet`, `glass`, `bell`, `musicBox` | One modal model; presets are partial tables. |
| Sustained voices | `organ`, `pad`, `sub`, `pluck`, `fm` | Every envelope starts and ends at silence. |
| Foley | `contact`, `MATERIALS`, `rain`, `wind`, `drop`, `riser`, `air`, `breath`, `tick` | Seeded noise buffers; material exciters and modes. |
| Room | `impulse` | Seeded convolution impulse. See the window-seat normalisation note below. |
| Meters and export | `integratedLufs`, `truePeakLinear`, `wavBase64` | What `audio.mjs` measures is computed the same way in page. |
| A/B studies | `STUDIES`, `STUDY_MARKS` | Contact, material, timbre menu, handoff and more, each with marks. |

## films/window-seat — sampled piano, 78 s

A written 6/8 piano piece on an embedded Salamander Grand bank, with bar times derived from
the picture and procedural effects under it.

| Technique | Where | Why copy it |
|---|---|---|
| Embedded sample bank | `<script id="piano-bank" type="application/json">`, `preparePiano` | Base64 Ogg keys decoded locally; no network. Rebuilt by `build-piano-bank.py`; attribution in `AUDIO-SOURCES.md`. |
| Sampler voice | `grand`, `pianoAnswer`, `pianoColour` | Nearest root per velocity layer, transposed by playback rate. |
| Bars from picture | `SCORE_BARS`, `musicTime`, `shot` | Bar groups span picture anchors (`T_DARK`, `SHOTS`, `T_DAWN`, `T_STOP`) with rubato weights, so cuts land inside continuing bars. |
| Written music | `HARMONY`, `MELODY`, `scoreForeground` | Chords and melody as data; the answering line in the foreground pass. |
| Layers | `scoreBed`, `scoreForeground`, `scoreWorld`, `buildScore` | Bed, music and world effects built separately, then mastered. |
| Picture-driven effects | `scoreWorld` (`S(t)`, `X_LC`, `BURSTS`, `trainX`), `windowRain` (`DROPS`) | Rail joints, crossing signal, fireworks, the passing train and drop taps read the picture's own consts. |
| Through-the-glass rain | `windowRain` | Aperiodic filtered contacts, 1350 Hz low-pass, no reverb: taps heard from inside, not an outdoor wash. |
| Room normalisation | `impulse` | Normalises by discrete sample energy. The kit's `sqrt(energy / rate)` added a `sqrt(48000)` gain to the wet signal and masked attacks. Keep this film's version. |
| Sync marks | `SCORE_MARKS`, `window.__riso.marks` | Tunnel dark, fireworks, dawn, stop: what `audio.mjs --marks` checks. |
| Attribution in exports | `AUDIO_CREDIT`, `wavBase64` | Credit written into WAV `LIST/INFO` metadata. |

## films/roost — recorded strings, 70 s

Cello section, bowed bass and solo violin from an embedded CC0 bank, on a compound pulse whose
tempo, cues and pan are measured from the projected flock.

| Technique | Where | Why copy it |
|---|---|---|
| Embedded string bank | `<script id="string-bank" type="application/json">`, `prepareStrings` | 21 Ogg recordings decoded locally. Rebuilt by `build-string-bank.py`; hashes, roots and tuning in `string-bank-manifest.json`; attribution in `AUDIO-SOURCES.md`. |
| Bowed voice | `bowed`, `bowSpan` | Long notes change bow across overlapping recordings; no sustain loops or artificial vibrato. |
| Score measured from picture | `FLIGHT_SCORE` (`rows`, `at`, `cue`) | Samples `birdPos` and `flockC` at 30 Hz: visible fraction, screen pan, presence and speed. Arrival, crest, exit and return cues are found in that data, not typed in. |
| Tempo from picture | `FLIGHT_SCORE.pulses`, `beat` | Dotted-quarter pulse integrated from flock density and speed (48–62 per minute), so phrasing follows the flock and retiming the picture retimes the music. |
| Layers | `scoreStringsBed`, `scoreFlightMelody`, `scoreRoostEnding`, `buildScore` | Bed, the four-note idea and the ending built separately, then mastered. |
| Marks | `SCORE_MARKS` | Five cues from `FLIGHT_SCORE.cue`, exposed as `__riso.marks`. |
| Attribution in exports | `AUDIO_CREDIT`, `wavBase64` | Same WAV `LIST/INFO` credit as window-seat. |

## films/held — found CC0 instruments, 70 s

Mbira, glockenspiel, hand chimes, harp, cello, violin pizzicato and flute from VCSL and
VSCO-2-CE, in B pentatonic, with kit synthesis only for weather and contact.

| Technique | Where | Why copy it |
|---|---|---|
| Embedded FLAC samples | `SAMPLES`, `loadSamples` | 16-bit mono 32 kHz FLAC, lossless, so both browsers decode the same samples. Rebuilt by `build-samples.py`; sources in `AUDIO-SOURCES.md`. |
| Sampler voices | `samp`, `bowed` | Nearest root repitched by rate; `bowed` crossfades retriggers past the bow attack for notes longer than a sample. |
| Cues from picture constants | `buildScore` (`spins`), `K_SNAP`, `L_SNAG`, `C_TAUT`, `E_LAMP` | Every cue reads the picture's event constants; tumble runs sit on the keyed spin times. |
| Dry room for recorded samples | `room.wet` in `buildScore`, `samp` (`send * .4`) | Samples carry their own rooms. With the kit's reverb at wet .3, stereo correlation fell to 0.02; at .035 it is 0.72. |

## films/nonpareil — sampled handpan, 70 s

A D Celtic minor handpan (Freesound CC0 previews, embedded as Ogg) over VSCO 2 cello and
contrabass. Nearly every note is a picture event: a drop, a pin crossing, an edge.

| Technique | Where | Why copy it |
|---|---|---|
| Drops are notes | `scoreGround`, `scoreStones`, `panOf`, `pan1` | Each landing plays a handpan tone panned by its x; brush taps are rolls with muted ghost taps. |
| Runs clocked by a moving edge | `crossings` (tool ops), `crossAt` (any `pos(t)`) | Times at which a pin, contact line or water front crosses evenly spaced lines: one tone per band, in the order it meets them. |
| Tuned transition swell | `edgeGesture`, `edges`, `reversedOf` | A lead-instrument recording played backwards into the edge's mid-frame crossing, its decay undone so the rise starts with the edge, then forwards out. It replaced noise-grain paper slides the user heard as static; `GESTURE = 'resonance'` keeps the measured alternative. |
| Cue from picture geometry | `flowerFlip`, `flipBeat` | The mirrored motif lands when the sheet sample under the flower turns face up, snapped to the half-beat grid. |
| Bass line as data | `bassLine`, `scoreBass`, `bowSpan` | Roots change on picture events; a note longer than a recording is overlapping bows, so moving the next entry re-cuts the held note before it. |

## films/eclosion — CC0 trio, 36 s

Vibraphone (VCSL), clarinet and French horn (VSCO 2) in F, never more than three voices; every
cue reads the picture's `T`.

| Technique | Where | Why copy it |
|---|---|---|
| One clock for picture and score | `T`, `T.glints`, `SCORE_MARKS` | The motif's three notes are the three gold dots catching light; pumps, display and push-off are `T` times too. |
| Struck and held voices | `vib`, `roll`, `sus`, `clar`, `horn`, `hornSpan` | One sampler for strikes (ring or damp), one enveloped sustain under a low-pass; a horn note longer than a take overlaps takes. |
| Pan with the subject | `butterflyX`, `panX` | Pans read the butterfly's projected x from `poseAt`, so the flight arpeggio follows it out of frame. |
| Pinned roots | `build-sample-bank.py` (`measure_tuning`) | Soft low horn notes lack a fundamental: roots pinned from the naming, tuning read from the strongest harmonic. |

## films/lumen — procedural score, 28 s

A self-contained score that does not use the shared kit: its voices are nested inside
`buildScore`.

| Technique | Where | Why copy it |
|---|---|---|
| Offline build, cached | `buildScore`, `scorePromise`, `renderAudio` | One promise serves both player and export. |
| Nested voices | `glass`, `bass`, `continuousAir` inside `buildScore` | A continuous reed and air bed keeps 16–18 s from falling silent. |
| Accents from picture | `expansionPeak` inside `buildScore`, `BLOOM` | Bloom accents are computed from peak petal expansion, not typed-in times. |
| Cue-driven tones | `CUES`, `FLOW`, `ANSWER_PULSES` | Foreground follows the same data as the picture. |

## films/emergence — two candidates, 28 s

Two complete arrangements share one event list; the page picks one.

| Technique | Where | Why copy it |
|---|---|---|
| Candidate selection | `SCORE_NAMES`, `DEFAULT_SCORE`, `selectedScore` (`?score=pulse`) | Default `warm` (Gravity); `pulse` (Orbit) by query or player selector; `__riso.score` reports the choice. |
| Events from picture | `scoreEvents` reading `CUES`, `FLOW`, `ANSWER_PULSES`, `RELEASE`, `MEMORY_ABSORB` | Retiming the picture retimes the score. |
| Marks | `scoreMarks` | Derived from `scoreEvents`, exposed as `__riso.marks`. |
| Organ voices | `organ`, `organLead`, `lowPulse` | Additive drawbar organ; low pulse carries continuity through the memory cut. |
| Per-kind build | `buildScore(kind)`, `renderAudio` | Both candidates from one builder with a `warm` flag. |

## Player audio wiring

Every film renders the whole score offline once, then plays that buffer from the playhead in
a live `AudioContext`. Seeking or pausing stops the source; playing restarts it at the new
time. Nothing is scheduled live, so the player cannot drift from `renderAudio()`.

| Film | Build / cache | Start and stop at playhead | Called from |
|---|---|---|---|
| window-seat | `ensureScore` | `syncAudio` | `play`, `pause` (and `seek` via `pause`), the Sound button |
| roost | `ensureScore` | `syncAudio` | Same as window-seat; its Record control also records the score while the monitor is muted |
| lumen | `buildScore` (`scorePromise`) | `startSound`, `stopSound` | `setPlaying` (frame loop `tick` only moves the picture) |
| emergence | `buildScore(kind)` via `refreshAudio` | `startSound`, `stopSound` | `setPlaying` (frame loop `advancePlayback`); `refreshAudio` on sound toggle or score change |

`refreshAudio` guards against a stale build with a request counter (`audioLoad`), so switching
scores mid-build never plays the wrong buffer.

## How to borrow

- Copy the kit block from `studies/sound.html`, then check its top-level names against the
  film before pasting; the block's header lists them.
- Derive times from the picture's consts (`SHOTS`, `CUES`, `FLOW`, `S(t)`), never retype them.
- Seed every noise buffer through `rngFor(key)`; `audio.mjs --twice` proves it.
- Borrow the window-seat `impulse` normalisation if a room masks attacks.
