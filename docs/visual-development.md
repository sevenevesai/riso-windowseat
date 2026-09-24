# Visual development

How to turn a request into observed, constructed, staged pictures and actions; read it before
drawing any new film or still, especially a complex one.

The print engine supplies a medium, not observation, anatomy, staging or story. A deterministic
film can still fail every artistic criterion.

## Translate the request

Extract subject, feeling, deliverable, duration, audience and explicit inclusions/exclusions;
carry forward approved choices. Asked for ideas, pitch; asked to make it, choose and build. A
broad aesthetic request is permission to art-direct, not a missing brief.

| Request language | Decision to make and inspect |
|---|---|
| Detailed, beautiful assets | The object's distinctive proportions, construction and material; put detail where it explains them. |
| Serious, cinematic | Viewpoint, scale, light, consequence. No default cute proportions or decorative captions. |
| Snappy, good pace | Clear actions, short preparation, readable arrivals; shot length follows information. Cut in during an action and out on its last beat: a tail hold (chewing, settling) reads slow even when the action is fast. |
| Smooth | Direction, eye destination and velocity through handoffs and wraps. A cut can be smooth. |
| Magical, explosive | A transformation rule staged as preparation, release, aftermath. |
| Original | New viewpoint, action and progression for the subject; new palette or nouns isn't enough. |
| Like an earlier film | Which to keep: print, rhythm, structure or one effect. Don't silently inherit all four. |
| A remake of a known video or meme | Measure the actual file: cut times, shot list, what each shot does. Keep its identity (structure, cut rhythm, action) and drop its defects (low resolution, morphing, watermarks) unless asked for. Its cut length is a ceiling, not a slot: trim each shot to its action with a per-shot in/out/speed table, holding it fixed once pacing is approved. |
| Devouring, greedy, frantic | Overlapping actions: the next starts before the last consequence finishes, and consequences accumulate (the plate empties, sauce stays on the face). |

Lessons from real requests (the current request always overrides; assistant praise and old
completion reports are not evidence of satisfaction):

- Requests are usually aesthetic briefs with delegated choices, then precise perceptual
  corrections. Answer with observation, constructed assets and visible iteration, and report
  weaknesses candidly. "Ideas first" means proposals before production.
- Honour per-request exclusions of earlier outputs as references.
- Liked pictures were still rejected for white-clear flashes at transitions and a strip snapping
  on its loop: inspect handoffs and loop boundaries, not just attractive frames.
- Long films the user liked were still corrected at playback speed: glints flashing, a rope tail
  glitching, a catch moving choppily, a transition sound jarring, a final passage dropping in pace
  and richness, shots opening on idle holds. Measure those symptoms
  ([quality-bar.md](quality-bar.md#defects-seen-at-playback-speed)) and judge pace from an MP4.
- Automatic pink/blue collisions and two-dot endings were rejected after several films: reuse the
  craft, not the Resonance story. A concept-specific motion doesn't carry to later films.
- A meme remake was corrected twice: away from imitating the source's poor quality, then back
  to its structure (ten 2-second shots, a new room and outfit at each cut) at a devouring pace,
  with no playing to camera. A recognisable reference has an identity and defects; decide which
  is which from the file, not from memory of it.
- Longer films raise the burden on drawing and within-shot action; a short motif can't be
  stretched. "Stills, not animations" means native PNG, with the effort spent on form, pose,
  contact and light.
- Short dot films mostly worked; long films read generic, goofy or badly paced, and detailed
  stills had perspective and positioning faults. An audit found repeated seated-figure builds,
  schematic contact and pose, a thin creature contour vocabulary, an unreadable person/tool
  relationship. More texture, linework or grain fixed none of it; the missing steps were an early
  reference/construction check and an action proof before expanding the timeline. Keep the short
  forms and sparse/dense contrast that worked; this is no ban on abstraction or dots.

## References that answer drawing questions

For unfamiliar recognizable subjects, inspect a few real references first: primary collections,
manufacturers, natural-history institutions, the artist's own work. Get construction/anatomy
evidence and a useful viewpoint, plus material or staging references when needed. A search
snippet is not an inspected picture. Keep links and observations beside the work; mark
inaccessible images and imagined mechanisms as such.

- Record what changes in the drawing: a handle's angle and attachment, a folded wing against the
  torso, a cast enclosure's thickness, the spacing of weight-bearing feet. No mood board without
  decisions. Study relationships; compose originally.
- Separate subject facts, composition/lighting and print finish. A riso poster can't show how a
  machine works. Generated imagery may suggest composition when requested but can't establish
  anatomy or historical accuracy.
- Wikimedia Commons serves photos by script: the API's `generator=search` with `prop=imageinfo`
  and `iiurlwidth` returns thumbnail URLs. Send a User-Agent; on HTTP 429 wait ~20 s and retry.
  Keep downloads in `out/`, never in the deliverable, and open every result: a name search also
  returns other people and things with that name.
- A flat specimen photograph can be measured, not only viewed. Eclosion's wing outlines, cells
  and spots came from colour thresholds on a Commons specimen photo, smoothed, with hidden edges
  drawn by hand (`films/eclosion/measure-wings.py`). Such geometry is data derived from that
  photo: pin the source by hash, record its license and credit it beside the work.

## Prove the hardest picture first

For an ambitious request, draw small alternatives differing in camera height, crop, depth and
value grouping (palette swaps don't count); pick the one where action and subject read most
easily. Then develop one representative difficult frame at delivery resolution before filling the
timeline: the hardest subject or interaction, not the title card. Keep construction, value and
final-ink views available. Order:

1. Horizon, projection, support, main masses and overlap ([scene-space.md](scene-space.md)).
2. Silhouette and pose: landmarks, weight and negative space identify the subject before interior
   marks. Primitive volumes are scaffolding; resolve the final contour.
3. Light, mid and dark grouped by form and light source. A high-key concept stays pale;
   hierarchy matters more than a near-black patch everywhere.
4. Details attached to the same geometry: joints, rim thickness, inset openings, supported weight,
   folds, plane changes, material boundaries.
5. Plate craft. Thumbnail: subject and hierarchy. 1:1: contours, tangencies, screen, registration.
   Texture is not evidence steps 1–4 worked.

People and animals: gesture and weight-bearing contacts before contour, then likeness, hands,
arms and contact as in [characters.md](characters.md). If an essential figure fails, study and
redraw it or pick a truthful readable viewpoint; don't just hide it.

A subject that recurs at several sizes or poses (a bird of the flock, a kite, a character) goes on
one sheet, printed on the real plates at its smallest and largest screen size and in each pose,
before any shot. At 4.6 px pitch small sizes fail first (drops under ~8 px read as dirt). In a
code-drawn explainer, a gallery of characters and props before any scene caught gray paper and
thin lines while each fix still cost one frame instead of fifty.

Objects: attach every detail to a host surface. Equal keys on a sloping keyboard foreshorten;
circles on a turned panel become ellipses. Use coherent perspective or a coherent
orthographic/graphic treatment; mixing them by accident disconnects parts.

## Build actions, then edit

- Describe what changes in the subject before coding a shot. "A whale crosses and turns its fin"
  is an action; "a whale appears through a mask" only an introduction. Reveals can carry abstract
  work but rarely every narrative shot.
- Separate subject, camera, transition and atmosphere; not all need move. Animate the main action
  with contacts and consequences, plus a subordinate material response. Add effects after the
  action works; a helper existing is no reason to use it.
- Plan long films as cause and consequence, not one captioned noun per equal interval. Reusing
  one set through establishing, action and detail shots deepens the event and saves drawing.
  Let complexity develop; constant maximum activity and repeated empty resets both flatten rhythm.
- Before polishing, play a silent timed rough cut at full duration to test density, anticipation,
  holds and transitions; a contact sheet can't show how long a hold feels. Don't reach a minute
  by stretching a 28-second montage's cues. Leave music out unless scoring was requested.
- Something that must cover the subject for a while (a sheet laid on a bath, a cloth over a
  table) covers least as a moving roll or curl. Held up by one edge it spans everything between
  contact and hands: Nonpareil's sheet printed the frame plain cream for about 2 s; unrolled from
  a loose curl it covered a third of the bath, moving.

## Evidence and stopping

- Use the relevant [review cases](quality-bar.md#review-cases). Fix failed silhouette,
  perspective, contact or action before adding texture or scenes. Record the defect and the
  artifact judged, never an invented beauty score.
- On large scope, prove the hard frame and a short motion sample first, then reuse their
  construction and materials. Cut secondary detail or scene count before duration or story, and
  surface any essential scope change: an attractive fragment is not a finished long film.
- Keep a short source-linked note of what changed and why. Promote a technique to shared craft
  only after inspecting its output, distinguishing mechanical tests, visual judgment and untested
  generality. Reuse the method, not the demo's subject or palette. Fix each correction in the
  smallest responsible mechanism with a comparable before/after; never derive universal style
  rules from one attractive frame.

## Research sources

Checked 2026-09-20. The right column is this project's adaptation, not the source's prescription.

| Source | Observation and application |
|---|---|
| [RISOTTO: advanced print setup](https://risottostudio.com/pages/advanced-print-setup) | Separates grayscale separations, ink density, gradients, registration, fine detail. Review print fidelity separately; paper texture doesn't fix bad form. Press opacity limits aren't imposed on digital pictures. |
| [Disney Animation: process](https://disneyanimation.com/process/) | Research, visual development, layout, animation, editorial. Adapted as observed subject, hero frame, action proof, full-duration rough edit; no feature-film staffing or timing. |
| [Scratchapixel: perspective projection](https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/building-basic-perspective-projection-matrix.html) | Perspective divides by depth. Map details in the object's plane, then project; screen-space guesses lose consistent foreshortening. The local kit uses positive forward depth. |
| [PBRT 4th ed.: projective cameras](https://www.pbr-book.org/4ed/Cameras_and_Film/Projective_Camera_Models) | View transform separate from projection. Keep object, world and page coordinates explicit; move geometry before the final screen. |
| [CHM: EAI 1140 Variplotter](https://www.computerhistory.org/revolution/input-output/14/356/1786) | A real X-Y drawing instrument and its dimensions. Text only; its photographs weren't retrieved, so they count as uninspected. |
| [CalComp 1984 brochure, CHM](https://archive.computerhistory.org/resources/text/CALCOMP/Calcomp.25Yrs.1984.10264634.pdf) | Pages 5–7 and 12 inspected: substantial enclosures, inset controls, paper-working areas, human work scale. The [drawing-machine study](../studies/scene-space.html) combines them into an invented mechanism, not a reconstruction. |

Lasseter's 1987 animation paper couldn't be retrieved; no rule here rests on it.

## Known gaps

The geometry/timing kit gives camera, mapped surfaces, near clipping, distance paths, Hermite
handoffs and analytic trajectories, not anatomy, visibility, physics or judgment. Minute-long
pacing now has production evidence: Window Seat, Roost, Held and Nonpareil (70–78 s) were built
with this kit and revised after playback review. Figure craft rests on one remake
([characters.md](characters.md)); character acting and consistent taste across fresh sessions
remain unevaluated.
