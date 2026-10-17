# Standby

52 seconds, 1080 × 1080, 30 fps, scored (procedural, D major with a lydian II, 96 BPM).
Authoritative source: `index.html`. Delivery: `out/standby.mp4`, the Firefox render
(`render.mjs`) of `index.html` with its score muxed.

## Premise

A kid's bedroom around 2001, long after everyone should be asleep. The DVD player has idled so
long that its logo bounces round the dark CRT, taking the next ink each time it touches an edge,
and every ink floods the room: the glass, the bezel's recess, the carpet, the duvet's crests, the
walls. We watch from the bed, waiting for the thing everybody waited for: the logo landing
exactly in a corner. It nearly does three times, each miss closer (30, 20, 10 screen units), and
after each one the camera leans in. At 36 s it lands, top left, and flares pink. Three seconds
later the TV's sleep timer switches it off: the raster collapses to a line, the line to a dot,
the dot fades, and the standby light comes on red. In the dark the things the screen had
drowned come up: glow-in-the-dark stars on the wall, and the DVD/VCR's clock blinking 12:00
because nobody ever set it. The camera eases back to the bed; a car passes in the street and
sweeps the blind-slat stripes across the wall and the stars.

Turn: the corner hit, caused by the logo's own path. Its x and y wall rhythms run at nearly 3:2
(5.000 s and 3.372 s), so they drift into phase: each near miss is one step of the drift
(the y touch arrives 0.346, 0.231, then 0.115 s before the x touch), the hit is phase lock. The
score plays the same two rhythms. Ending: the CRT's own way of dying, then the room's dark
state. Planted early and returned changed: the stars (pale plastic in the screen's light, the
brightest things at the end) and the 12:00 (green on the silver box throughout, then one of
three lights left in the room with the red standby LED).

## Why this concept

Treatments the kit already made: a fixed-frame journey (Window Seat), one continuous take of an
event (Roost, Nonpareil, Eclosion, Passenger), a cut narrative (Held), the Resonance montage
(Lumen, Emergence). The first pitch for "late 90s / early 2000s" is a collage: wallpaper hills, a
vaporwave grid, VHS glitch bars, a dial-up screech. A list of nouns has no action, turn or
ending. Weighed instead:

- Dial-up: a modem handshake, then a photo loading in coarse-to-fine interlaced passes, cut off
  when someone picks up the phone. A strong turn, but the frame is a flat browser window.
- 3D pipes escaping the monitor. Charming, but fantasy without a cause.
- The bouncing DVD-player logo and the corner. Chosen: a real, shared ritual of the era with
  built-in suspense; its motion is a closed-form billiard (pure in `t`); every bounce is a printed
  ink change; its coloured light gives the plates a reason to change. The room around it (a black
  CRT, a silver DVD/VCR combo blinking 12:00, mini blinds under a sodium lamp, a wallpaper
  border, glow stars) carries the period without a collage.

## Construction

- One timeline: `T` (hit 36.0, off 39.25), the billiard (`logoXY`, `BOUNCES`, `MISSES`), the
  camera (`LEANS`, `CAM_OUT`), `CRT` phases and `CAR`. Shots, marks and the score all read these.
- The billiard: the picture is 640 × 480 screen units, the logo's box 160 × 88 bounces in a
  600 × 450 area at 88 and 107.4 units/s, solved backwards from the hit so `x = tri(VX·(t − T.hit))`.
  `logoInk` cycles pink, yellow, green, violet, orange, blue per wall; the ink before the hit is
  blue, the dimmest light, so the room darkens into the corner and floods pink at it.
- The room is a raycast, one ray per device pixel (`renderRoom`): axis-aligned boxes in cm (TV
  housing with rounded front corners, stand, combo, tapes) inside the room box. Each hit
  gets its material's unlit plate values, then light: the logo as a moving point source plus the
  screen's glow (Lambert at both ends), a bounce term that opens the dark more than it inks (so a
  yellow light reads as a pale wash, not olive), the sodium lamp through the mini blinds, and the
  car. Blind stripes are the slat phase where the ray to the lamp crosses the window plane,
  softened by the lamp's footprint and shadowed by the boxes. A 90s wallpaper border (rules, a
  zigzag, dots; `borderInk`) runs round the back wall at picture-rail height and shows mostly
  where light falls. Surfaces inside the stand are darkened as occluded. Values go straight into
  each plate's alpha; vector details (bezel strip, combo front, VFD, logo, stars, collapse, LED,
  duvet) are drawn on top, and `compose()` screens per pixel (Window Seat's compositor). A frame
  costs 250–440 ms in Firefox and Chromium; the full render took 479 s.
- The glass: rounded picture corners, a dark recess round the tube lit by the logo's own box as
  it nears an edge (`lip`), so a near miss lights the bezel it almost touches, a pale sheen where the convex glass mirrors the window, and a bloom of the
  logo's ink. A dead tube is darker than a live one showing black.
- Camera: a perspective dolly in log distance to the glass. A slow creep plus one eased lean per
  near miss (6.3, 16.4, 26.5 s) brings the screen from about 380 px to about 990 px wide; it
  settles by 38 s, then eases back to the bed and up to the stars (41.2–48.4 s).
- The hit flares: logo light, bloom and lip jump 2.5× and decay over about 0.5 s. The bloom opens
  the dark more than it inks, so the logo stays legible inside its own flare.
- Switch-off (`CRT`): 0.09 s vertical collapse with the logo squashed in the band, 0.19 s to a
  dot, 3.1 s afterglow; the room light dies with the raster. The standby LED is pink over orange,
  which prints red.
- Stars: 14 stars, a moon and a ringed planet on the wall above the TV; their glow rises over
  3.2 s after the switch-off. The car is a lamp moving along the street at window height; its
  stripes sweep the wall left to right (45.0–49.6 s).
- The duvet: three ridges over the feet at the bed's foot, filled down past the frame; only the
  crests catch the screen, so every bounce recolours them.

## Plates and palette

Seven plates: indigo, blue and violet carry the night (darks are overprints of all three);
orange is the street lamp; the logo cycles pink, yellow, green, violet, orange and blue; green is
the VFD; yellow and green the stars. Most frames use four or five.

## Score

D major with a lydian II, 96 BPM, bars counted from the first x wall (1.0 s), so every x wall is
a downbeat two bars after the last. Kit-only (`studies/sound.html`, `paper` and `tick` renamed
`paperFx` and `tickFx`; Window Seat's `impulse`, room wet .2).

- The two wall rhythms are the two voices: x walls play a low FM e-piano on the chord root and
  change the chord (Dmaj7, E/D, Bm9, Gmaj7#11, F#m7, Gmaj9, A7sus4, D add9 at the corner); y walls
  play a high FM bell melody that climbs to D6. A near miss is a y note landing early, the next
  chord's note as an anticipation; the flam closes 0.35 → 0.23 → 0.12 s and at the corner both
  voices land together (the bass 20 ms behind so their attacks don't stack). Pans follow the
  logo's projected x.
- Bed: pads per chord in a crescendo across the seven chords; the set's mains hum (60/120/180 Hz)
  and line-output whine (15.734 kHz, very quiet), both cut at the switch-off; three crickets
  through the closed window, louder in the dark.
- Last approach: a soft eighth-note music-box pulse on the chord tones from 26.2 s, growing, and
  a triangle riser into the corner.
- Corner: low body, a staggered bell chord (D F# A E), then music-box sparkles falling.
- Switch-off: relay click, the high voltage letting go (a falling thump), static crackle on the
  glass, and the music stops. A deliberate hush (about −15 dB at 40.9 s) returns with the
  crickets and a music box playing the melody's first notes under the stars, ending on D with a
  low drone; the car passes (tyres, engine, a doppler band sweep) panned left.

Marks (`__riso.marks`, from `MISSES`, `T` and `CAR`): near misses 5.654, 15.769, 25.885; hit 36.0;
switch-off 39.25; car 47.3.

Measured (Firefox, `audio.mjs --twice --engine firefox --ffmpeg`):
`I −16.8 LUFS, LRA 10.0 LU, TP −1.0 dBTP, clipped 0, firefox byte-identical`. Onsets: −4, −4 and
−20 ms at the near misses, none detected at the hit (peak +30 ms), −60 ms at the switch-off; the
car is a swell (peak −15 ms). The −20 and −60 ms readings lock onto beating in the pad bed (10 ms
RMS printed around both); those notes start on their marks by construction. Bands: 2.2 % sub,
65 % low, 28 % low-mid, 4.3 % mid, 0.5 % high, 0.3 % air: dark by intent. Valleys: 39.7 s
(−22.8 dB, the deliberate hush after the switch-off), 40.8 s (−10.7 dB) and 51.65 s (the
ending's fade). Nothing has been heard.

## References inspected (Wikimedia Commons, 2026-10-17; downloads in `out/standby-refs/`, git-ignored)

| File | Establishes |
|---|---|
| `Sony Trinitron KV-27FS100.jpg` (Roboat06, CC BY-SA 4.0) | Early-2000s CRT: speaker grilles both sides, a control door, on-screen display in green-cyan blocky type. |
| `1990s Television Set.jpg` (ProtoKiwi, CC BY 4.0) | A black 90s CRT with rounded picture corners on a stand, the VCR on the shelf under it. |
| `19" Sylvania CRT television …jpg` (Norfolk757man, CC BY-SA 4.0) | Thick black bezel, rounded picture corners, a control strip with small buttons under the screen; the dead screen is grey-green glass. |
| `JVC HR-XV31.jpg` (Alex long, CC BY-SA 4.0), `Videoregistratore Daewoo.jpg` (Antonio Mette, CC BY-SA 4.0) | DVD/VCR combos: low silver box, cassette flap left, disc tray right, a smoked display window in the centre, round buttons, RCA jacks front left. |
| `Living Room 1998 NOLA.jpg` (Infrogmation, CC BY 2.0) | A CRT on a shelf among VHS tapes; venetian blinds. |

Facts used: the blinking 12:00 of unset VCR clocks ([Wikipedia: Blinking twelve
problem](https://en.wikipedia.org/wiki/Blinking_twelve_problem)); VFDs, usually green, on VCRs
([Wikipedia: Vacuum fluorescent display](https://en.wikipedia.org/wiki/Vacuum_fluorescent_display));
an old CRT's raster collapsing to a spot that fades when switched off, and modern sets flashing
as the raster collapses ([repairfaq.org, TV FAQ](https://repairfaq.org/samnew/tvfaq/tvslolatva.htm));
corner hits happen when both wall rhythms coincide
([Mental Floss](https://www.mentalfloss.com/technology/did-the-bouncing-dvd-logo-ever-hit-the-corner-of-the-screen)).
The 15.734 kHz whine is the NTSC line rate. The logo is an invented wordmark, not the DVD Video
mark; no brand appears in frame.

## Evidence

| Check | Result |
|---|---|
| Delivery decode (`out/standby.mp4`) | 52.00 s, 1560 frames, 1080² H.264 High yuv420p, 30 fps, AAC 48 kHz stereo 194 kb/s; no decode errors; muxed I −16.8 LUFS, LRA 10.0 LU, peak −1.0 dBFS; 95.5 MB |
| `review.mjs --mp4` (delivery) | median 3.24 % of pixels change per frame; 0 runs under 0.1 % for ≥ 0.5 s |
| `verify.mjs` (Chromium and Firefox, 26 times incl. every shot boundary) | seek is pure in t; contract holds |
| Pop scan of the delivery MP4 (360 px, blurred; [quality-bar](../../docs/quality-bar.md)) | 5 flags, all designed: 36.00 s (the hit's flare, 15.4 vs local 0.7) and 39.27–39.37 s (the raster collapse). Per-second mean change 0.2–0.9 through the approach, 1.3 at the hit, 2.6 at the collapse, 0.0–0.3 in the afterglow and final hold, 3.7 at the car |
| Strips read | near misses 5.2–6.3, 15.3–16.4 and 25.4–26.5 at 0.1 s; the hit 35.9–36.6 at 1/30 s; the switch-off 39.15–39.65 at 1/30 s (pink logo, a one-frame flash, the band, the line, the dot, the standby light coming on); the car 44.6–50.2 at 0.4 s; the whole film at 1.5 s |
| 1:1 crops | the hit's corner (logo legible in the flare), the third near miss (lip lit), the VFD, encoded MP4 frames at 20, 36.03, 44.5 and 47.6 s (from a rough render before the last value changes) |
| Score | as above |

Previews (`preview.webp` 540 px at 12 fps, `preview-thumb.webp` 300 px at 10 fps) are four beats of
the delivery MP4: the third near miss, the hit, the collapse, the headlight sweep.

## User constraints

"Make a new riso using the riso/riso-windowseat project, something that feels especially
nostalgic to the late 90s early 2000s." Subject, concept, duration and score were chosen here;
the score follows the scored films before it.

## Remaining weaknesses

- Nobody has watched it at speed or listened to it; judgement comes from strips, sheets, crops
  and meters. Worth watching and hearing first: 5.4–6.3 s (the first near miss is small: the
  logo about 90 px wide, the gap about 17 px), 25.7–26.2 s (the third near miss's double flash and
  flam), 35.8–36.6 s (the hit), 39.2–40 s (the switch-off and the hush), 45–50 s (the car).
- The 12:00 is legible mid-film only; in the final framing it is a small green blink beside the
  red standby light.
- The TV and stand are mostly dark silhouettes; their form comes from the glass, the bezel's
  recess and the stripes behind them, not from modelling.
- The score is dark (65 % low band). The 15.734 kHz whine is very quiet and many listeners will
  not hear it; whether it survives every player's AAC decoder is unchecked.
- Raycast edges are unantialiased; at 1080 the screen hides the 1 px steps, but a downscaled
  preview shows some stair-stepping and moiré, as all halftone previews do.
- The MP4 is not uploaded to the v1.0 release.
