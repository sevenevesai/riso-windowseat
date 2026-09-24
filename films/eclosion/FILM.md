# Eclosion

36 seconds, 1080 × 1080, 30 fps, scored for vibraphone, clarinet and French horn. The title is
the word for an insect leaving its pupal case. Authoritative source: `index.html`. Sound sources:
`AUDIO-SOURCES.md`.

## Premise

One monarch butterfly's first morning, in one continuous take. A jade chrysalis hangs under a
milkweed stem before dawn. As the light comes up the case turns clear and dark and the folded
orange wing shows through it. The case splits at the bottom. The butterfly comes out head-down,
then swings down about its thorax to hang from the empty shell, with a swollen striped abdomen
and small, crumpled wings. In six slow pulses it pumps the abdomen's fluid into the wings: they
lengthen and lose their creases while the abdomen shrinks. The wings hang to dry. It turns and
opens them twice, the film's one full display of dorsal orange, then lets go and flies out of
frame. The camera returns to the empty case, framed as the chrysalis was in the first second:
clear now, still wearing its gold crown, swinging where the push-off left it.

Why it ends this way: what an eclosion leaves behind is the empty case. The opening image, a
green jewel with a gold crown, comes back in the same framing as a clear husk with the same
crown. The turn (the split) is the subject's own act, and so is the expansion: the abdomen
visibly gives up what the wings gain.

Treatments already made in this kit are a fixed-frame journey (Window Seat), wide continuous
takes (Roost, Nonpareil), a cut narrative (Held) and the Resonance montage. The obvious pitch for
"butterfly" is one flitting among flowers. This film is a continuous take because its wonder is
continuity: the same creature goes from crumpled to full with no cut to hide the change. What is
new is the macro scale, a single creature transforming, and a subject that grows inside the
frame.

## Passages

All times come from `T` in the source. Shots, marks and score read it.

| t (s) | Passage | Action | Eye / camera |
|---|---|---|---|
| 0–2.6 | jade | The green chrysalis swings gently in a dying breeze; pre-dawn indigo haze starts to burn off; three dots of the gold crown catch the first light in turn (0.9, 1.6, 2.3). | Case at centre; zoom 1.42. |
| 2.6–6.95 | clearing | Green drains bottom-up. A near-black body and a folded orange forewing with white-dotted margin show through the glossy case. | The reveal travels up the case. |
| 6.95–7.75 | twitch, split | Two shivers (driven pendulum), then the bottom seam cracks and the flaps part. | The crack. |
| 7.75–9.35 | emergence | Head and legs come out head-down and hold the lip. The contents drain down the case with a rounded tip; the striped abdomen swings out left and down about the thorax (8.4–9.35). The case jolts. | Eye drops with the body; camera pulls back 6.6–14.2 to zoom 1.0. |
| 9.35–12.2 | hang | Pendulum settle; head up below the shell, legs climb to a hanging grip; antennae lift from limp (9.8–12.2). | Read the new creature. |
| 12.2–22.1 | pumping | Six pulses 1.8 s apart, each 0.9 s. At each, the abdomen squeezes, the body rocks, the wings part slightly and lengthen and flatten one step (scale 0.42 → 1, creases fade). | Down the lengthening wings. |
| 22.1–25.0 | drying | Full wings hang: ventral buff hindwing with paper-edged black veins, forewing apex below it. | A breath. |
| 25.0–28.8 | display | The body turns toward camera (yaw 14° → 48°). Wings open to show the dorsal orange (full at 26.3), close part way (27.6), open again (28.35), then rise to 40° as a wind-up. | The colour peak. |
| 28.8–31.6 | flight | Push-off from the raised wings; the beat accelerates to 3 Hz within about 0.3 s. Wingbeats carry 7-sample motion blur; it rises and exits top right. | Eye exits top right. |
| 31.6–36 | empty | The case, kicked by the push-off and no longer loaded, swings and settles. The camera pushes back in (30.4–35.0) to the opening's framing. | Ends on the planted image, changed. |

## Construction

- Live plates: yellow, green, orange, indigo, using the compositor copied from Window Seat.
  Green's screen moved to 63.4° so it no longer shares indigo's 45°. `withM()` sets one affine
  map on every plate, so each surface is drawn in its own coordinates (world, case, wing).
  `layer()` draws the jade shell into sprite plates and lays it over the case through a
  bottom-up ramp mask. `blurred()` averages 7 shutter samples of the flying butterfly through
  its averaged silhouette.
- Darks are overprints. Monarch black is indigo over orange; the pupa inside is indigo, orange
  and green. White spots and body dots are paper knockouts. The ventral hindwing's pale vein
  edging is a paper band knocked along each cell's edge, with the veins re-laid through an
  even-odd clip.
- The butterfly is a planar 3D model. Wings are outlines, orange cells, dusky apex cells and
  spots in specimen units. They were extracted by colour thresholding from the MHNT male dorsal
  photograph (Didier Descouens, CC BY-SA 4.0, credited in the source) and then smoothed.
  `measure-wings.py` rebuilds it from the hash-pinned 960 px rendition; its output matches the
  embedded `WING` exactly. The hindwing's hidden anterior edge and inner margin were drawn by
  hand (they are literals in the script). One affine
  per wing maps the pattern: sweep in the wing plane, then fold about the body axis, then body
  yaw, pitch and roll, then an orthographic camera. The visible face (dorsal or ventral) comes
  from the wing normal.
- Layering is by depth, not fixed rules, so the body agrees with whichever side we see. Legs
  (ventral) and antennae go first, then the wings far side first, then the abdomen and the
  thorax. The head is drawn before the thorax. After each body part, any wing surface nearer the
  camera than that part's near surface is laid again inside the part's silhouette. A wing is a
  plane and a body part is a cylinder along an axis, so "nearer" is a screen half-plane
  (`wingDepth`, `axisFront`, `halfPlane`). Closed wings wrap the abdomen, so their depth is
  biased by its radius toward their own side; that keeps the hanging look, with the ventral
  hindwing over the abdomen. In flight we are behind the butterfly, so its head tips away from
  the camera (pitch +24°).
- Crumpling is two pleat families plus a ripple, applied to specimen points before the affine.
  It prints as dark creases with paper ridges and fades with expansion.
- Legs are two-bone chains solved in screen space to feet on the case surface. Their grip
  moves from the split lip to a hanging hold after the swing.
- While the butterfly is still inside, it is clipped to below the split line and drawn under
  the case, so nothing pokes through the shell.
- The case swing is a damped pendulum integrated once at load (240 Hz) and interpolated. Its
  forcing: shivers, the tug of the body, a loaded rest while the butterfly hangs from it, and
  the push-off kick. Seeks stay pure.

## References inspected (Wikimedia Commons, 2026-09-24)

Downloads are in `out/eclosion-refs/` (git-ignored); nothing from them is embedded.

| Reference | Establishes |
|---|---|
| `Monarch_Butterfly_Danaus_plexippus_Chrysalis_2000px.jpg`, `Danaus_plexippus_chrysalis_2003-10-16.jpg` | Chrysalis shape: a domed top widening to the gold band at about ⅓, rounded bottom, length ≈ 1.65 × width. Black cremaster from a white silk pad. Gold band is a black line with gold dots; a few gold spots lower down; faint wing-pad seam. |
| `Monarch_butterfly_chrysalis_(53138332352).jpg` | Ready to eclose: case near-black and glossy, with orange forewing and white margin dots showing through the wing pad. |
| `Danaus_plexippus_emerging_from_chrysalis_02.jpg`, `_04.jpg` | Hanging pose: head up by the empty case, legs up to it; closed wings hang with the ventral hindwing outermost and the forewing apex below it. Crumpled wings are small and creased with the pattern crammed. Empty case is clear and keeps its gold line. |
| `Monarch_Butterfly_Emerging_from_Chrysalis.webm` (frames 24–49 s) | The case splits at the bottom; the swollen abdomen, grey-white between black bands, drops out below; the butterfly hangs head-up from the case bottom within about 1 s. |
| `Danaus_plexippus_MHNT_dos.jpg`, `_ventre.jpg` (male) | Wing outlines, cells and spots (`WING` in the source). Black margins with two rows of white dots; dorsal forewing apex black with pale subapical spots; pale buff ventral hindwing with thick, pale-edged veins. |

## Score

A slow, warm trio in F, with at most three voices and usually two. Details are in
`AUDIO-SOURCES.md`.

- Motif: vibraphone C–F–G, unresolved. Each note is one gold dot catching the first light (`T.glints`),
  it asks again while the wings dry, and over the empty case it comes back and resolves to A.
- Clearing: the clarinet's low line A–C–B♭–A over a horn walk F–D–B♭, with sparse vibraphone.
  Two damped vibraphone taps are the shivers.
- Split (7.52): open fifth C–G on vibraphone; horn C holds under the emergence.
- Swing: vibraphone G–E–C–A falls with the body, panned with it; it lands on low F at 9.35 as
  the horn returns to F. The clarinet's first long F is the first breath.
- Pumps: one horn swell per pump (roots F, B♭, G, D, C, A). The clarinet climbs a step per pump
  (A4 → A5), and the vibraphone rolls a chord as each pump settles.
- Display: D♭maj7 (the one borrowed chord) rolled to land on full open (26.3), then C, then
  home to F as the wings open again (28.35).
- Flight: low F at the push-off; a vibraphone arpeggio C5 → F6 panned with the butterfly's x;
  the clarinet rises to F5.
- Ending: a tail. Horn F pedal, clarinet low F, motif C–F–G–A; master fade over the last 1.2 s.

Marks (`__riso.marks`): split 7.5, landing 9.35, first pump swell 13.0, full open 26.3,
push-off 28.8.

## User constraints

Roughly 30–40 s on a subject of my choosing; slow, warm music; open-source recordings; at most
2–3 instruments for most of the score. All three instruments are CC0.

## Revisions

- v2 (user correction). In the display and flight the wings showed their backs, as seen from
  behind the butterfly. The body contradicted this: legs drawn over it, head over the thorax,
  the body always over the wings, and in flight a pitch that tipped the head toward the camera.
  The fixes are depth layering (above) and the flip of the flight pitch sign. In the hanging
  poses the only change is that the legs now come from behind the thorax. v1 is kept for
  comparison as `out/eclosion-v1.mp4`, `-v1.wav` and `eclosion-v1-index.html` (the maker's
  local, git-ignored evidence, like every `out/` path here). The score is
  unchanged.

## Evidence

Delivery: the MP4 is attached to [the v1.0 release](https://github.com/sevenevesai/riso-windowseat/releases/tag/v1.0)
as `eclosion.mp4`. It is the v2 Firefox render (`render.mjs`) of `index.html`, which is
authoritative, with credits added to its metadata. Decoded it is 36.00 s,
1080 frames, 1080² H.264 High, 30 fps, AAC 48 kHz stereo at 193 kb/s, with credits in its
comment metadata. Muxed: I −16.0 LUFS, LRA 5.0 LU, peak −2.9 dBFS.

| Check | Result |
|---|---|
| `verify.mjs` (Chromium and Firefox, every shot boundary) | seek is pure in t; contract holds (v1 and again on v2) |
| `audio.mjs --engine firefox --twice` | two cold renders byte-identical; 36.000 s at 48 kHz; I −16.0 LUFS; TP −2.86 dBTP; clipped 0 |
| Pop scan of the delivery MP4 (360 px, blurred) | no flags, v1 and v2 (v2 includes the turn from profile to back view). Earlier renders flagged the push-off (fixed by a wind-up and an eased-in wingbeat). |
| `review.mjs --mp4` | 0 runs under 0.1 % change for ≥ 0.5 s; median 2.35 % of pixels change per frame |
| Emergence strips at 0.1 s | Fixed wings poking through the shell, leg scribbles while head-down, and a flat "fill-level" drain. |
| Split sync | The onset detector reports −105 ms. It locks onto beating in the held clarinet and horn; the WAV's 10 ms RMS shows the note rising at +10 ms and full by +50 ms. |

Per-second mean frame change (360 px, blurred) shows the shape of the film: 0.04–0.2 through
the jade and clearing; 1.3–2.4 at the emergence; 0.13–0.24 through the pumping (it was
0.05–0.16 before the pump sway, wing stir and drifting light); 1.7–9 at the display and
flight; a settling tail.

## Not reviewed, and known weaknesses

- Nothing was heard. The score passes its meters, but whether the recordings sound warm,
  in tune and well balanced together is unjudged. Times worth listening to first: 0.9–2.3 (the
  motif against the glints), 7.5 (the split), 9.35 (the landing), 26.3 (D♭ on full open),
  28.8–31.6 (the flight arpeggio), 32–36 (the motif resolving to A). The spectrum is dark
  (92 % of energy at 250 Hz–1 kHz, none measured above 4 kHz). That is warm by intent, but no
  air has been added.
- Pacing was judged from measurements and 10 fps strips, not by watching at speed. The pumping
  (12.2–22.1) is the quietest stretch of motion and may still feel long.
- Legs and antennae are thin lines and can read as a tangle at the case bottom right after the
  drop. The head-down emergence is staged with a clip under the case rather than a modelled
  abdomen sliding out.
- The empty case's shadowed mouth can read as the opening of a jar.
- The wing geometry is data extracted from a CC BY-SA photograph (credited). Whether
  ShareAlike reaches measured outlines of a natural pattern has not been checked. If it matters,
  the fallback is to re-author the cells by hand from landmarks.
