# Figures: people, hands, arms and contact

How to make a body read as a particular someone doing a particular thing; read it when a film or
still has a person, an animal or a hand at work, after [visual-development.md](visual-development.md).

Most rules here come from eight revisions of a remake of a person eating (not shipped in this
repo). Each records a failure the user saw or a measurement caught. Its motion traps are in
[motion.md](motion.md#traps-that-pass-verify).

## Gesture, support and staging

- Gesture and weight-bearing contacts come before contour: place shoulders, pelvis, joints and
  attachments, and check limb proportions in the chosen view. Hands reach and grasp; seated
  figures meet seat and controls. A generic head-and-limbs stamp repeated at a desk does not
  improve when shrunk. If an essential figure fails, study and redraw it or choose a truthful,
  readable viewpoint; don't hide it.
- Stage the body for its action. A seated eater's table sits at elbow height, over a head-height
  below the shoulders; a table just under the shoulders forces every reach level across the
  chest. A turned head needs a turned torso: with a frontal torso under a ¾ head, a correctly
  solved arm still read as "a flat dark slab across the chest".
- Limbs that leave frame are geometry continuing off-canvas, never cut ends.
- A close shot needs the close camera's strong perspective; drawn with the medium shot's weak
  perspective, a face flattens.

## Likeness of a real person

Judge at recognition scale first. Seven passes that matched landmark positions still read as a
generic well-drawn man; the eighth, measured on the coarse value pattern, moved it. Familiar faces
are named from about 7×10 px (Sinha et al. 2006, "Face recognition by humans: nineteen results");
pigmentation weighs about as much as shape, and eyebrows about as much as eyes.

1. Vet every reference. A name search on Wikimedia Commons returns other people with the name;
   two sat in a reference set until a review caught them.
2. Squint test: align photo and render on the two eye centres (near eye and mouth for a turned
   head), blur both until the face is about 20 px wide, and compare mean luminance by region
   (forehead, brow, socket, under-eye, nose, both cheeks, moustache, chin). Fix the largest
   differences first. It found a pale under-eye band (+74), a lit nose-bridge stripe (+40), brows
   too light (+27) and a lit/shadow split that halved the face; each reads as a mask.
3. Landmark grid on a frontal photo, head units from crown −0.5 to chin +0.5: hairline, brows,
   eye spacing, nose width and base, mouth, chin, ear span, skull and jaw width. Author features
   in those units on a surface-wrapped head (rings of half-width and depth per height) so a turn
   foreshortens them together. Each pass names a measured difference ("nose too narrow, brows too
   high"). Study the photo; never trace or embed it.
4. Form is a relief heightfield (brow shelf, sockets, cheekbones, nose bulb and alae, muzzle,
   chin) lit from the mesh, not painted plane blobs: Lambert wrapped past the terminator, a cast
   shadow marched toward the light, concavity. Keep the relief smooth at the midline (a smoothed
   |x|, not `abs`), or gloss prints a seam down the forehead. Skin takes a tight specular lobe
   limited to its oily planes (forehead centre, nose tip, cheekbone crest, chin), printed as a
   warm knockout rather than paper white. Build the silhouette from front-facing quads so a
   turned contour breaks at nose, lips and chin.
5. Compare at the film's actual yaws and pitches against ¾, down-angle and profile photos, and
   every shot's head old beside new, so a fix for one angle doesn't break another.

Details that each cost a revision: ears sit about 35° off the skull and from the front show only
a thin lit rim; a closed eye is a lit lid and a lash line, not a dark slit; bright whites round a
small iris stare; the ala groove is an open C (closed, it reads as a ball on the cheek); a beard
filled up to the nostrils reads as a block. Untried: a caricature pass that exaggerates the
subject's measured departures from an average head (Rhodes, Brennan and Carey 1987).

## Hands

- A hand is a posable 3D joint chain with one solved pose per grip, never one 2D stamp: a fork
  grip reused for pinching and holding read wrong everywhere. Size it at about 0.8 head heights.
- Solve contact numerically (thumb pad onto the handle line, a small residual minimisation in a
  scratch script), then anchor the hand on the contact point. Some targets are unreachable without
  passing through a finger; check a photo for where the thumb really goes.
- Depth-sort phalanges with what they hold. A flat object at the mouth sits between the fingers
  on its near face and the thumb behind, so the back of the hand faces the camera; thumb-forward
  points the fingers at the face.
- To wrap a hand round an object, anchor on a point inside the fingers' curl and turn the hand so
  that line lies along the object.
- Compare one large hand beside a photograph of the same grip before placing it in shots. A
  debug-sheet match does not carry to the shot: sweep roll and pitch in the shot itself as a 3×3
  grid at 1:1 and pick the one that reads (at shot scale the palm side reads as an open hand).
  When a part can't be identified in a sweep, tint it a flat ink while choosing.
- Capsule fingers read as sausages. Profile each phalanx with the joint wider than the shaft and
  a palmar pad, nails on the distal half of the last phalanx, fingers lying together in a hold.
  Curled fingers separate only with a knuckle head, a crease inside each bend and a small shadow
  each phalanx casts on what lies behind it. On dark skin the palm side is paler as a gradient
  toward the side it faces, not a flat pale shape.
- A grip is held by working fingers: blend toward an in-grip extreme over time. The pinch parts to
  take and release, thumb and index roll a twirling handle, the fist squeezes and the held thing
  deforms. Check 1/30 s strips around every blend and loop wrap for pops.

## Arms

- Solve arms as two-bone IK in 3D: upper arm 1.5 and forearm 1.15 head heights, about 0.2 wide at
  the biceps and 0.12 at the wrist. Outline the side edges only, so the elbow reads as one form.
- A hand at the face sits under a head-height in front of the shoulder; pushing the wrist further
  aims the upper arm at the lens and balloons the sleeve. The shoulder joint sits a deltoid's
  radius below the shoulder line, or sleeves read as pads.
- After restaging, log the elbow angle per frame to confirm the solve never flips.

## Contact with held and eaten things

- Loose parts on a moving holder (strands, cords, tails) trail by the holder's past motion, with
  the holder's position a pure function of `t`
  ([motion.md](motion.md#anticipation-and-follow-through)).
- Things wound onto a tool spool: each turn winds over those already there, with a growing
  radius, and is drawn in stacking order with its own edge, or they merge into one mass. Tails
  pull taut to their source before unwinding; threads stretch, neck and snap.
- A bite scallops the cut edge, drags the near edge toward the lips, stretches a few strands to
  snap and tugs the head. Anything leaving the mouth starts between the lips and passes under the
  upper lip (redraw the lip over it). Lip strands go taut just before the whip; taut for a whole
  slurp reads as a comb.
- Consequences accumulate and stay: each scoop empties the plate (strands taken, a hollow opened,
  the wall slumping in) and sauce stays on the face at the bite that caused it. Chewing moves the
  jaw and the mouthful between the cheeks; a cheek bulge is a broad, low swell eased in with the
  food. A compact lump that popped out fast was called "little golf balls" though single frames
  looked better.
- Contact shadows come from depth: each finger and tool part shadows the face or plate by its
  real gap along the light. Fixed offsets threw shadows onto the face where the lamp throws them
  off it.

## Acting

Unproven in a riso film; these come from a hand-drawn explainer kit whose films read as alive:

- Eyes lead every reaction: the look moves a beat before the head, the head before the body, and a
  look toward the next point of interest motivates the cut there.
- Blink for about 0.11 s every 3.3 s or so, offset per character, where the eye reads at 1:1.
- Symmetric poses look stiff: tilt the head a few hundredths of a radian and offset the hands.
- Write a figure's pose as a pure function of `t`, one block per beat, each setting hands, look,
  mouth and brows from the film's event data.

## Inspection

Give the work debug views selected by query string (a hero head beside its photo, the form
passes alone, one hand on a pose grid, heads at every shot angle) and prove each change there,
then in its shot, then in 1/30 s strips around the action. Confirm a suspected pop at 1:1, since
reduced sheets exaggerate differences. Keep each revision's source and MP4 in `out/` for old
beside new. A figure film costs 90–200 ms a frame, so judge pace from the MP4
([live-plates.md](live-plates.md#cost)).
