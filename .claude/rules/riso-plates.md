---
paths:
  - "films/**/*.html"
  - "studies/**/*.html"
  - "prints/**/*.html"
---

# Ink plates and canvas traps

A scene is drawn once per ink into a coverage layer, screened into halftone dots, tinted, and
multiplied onto the paper; alpha is tone, so `tone(g, 0.4)` means a 40% dot screen.
Plate correctness does not fix drawing, perspective or pacing; see `docs/visual-development.md`.

## Knockouts

- A bright element over a dark ground must clear that ground first with `destination-out`, or it
  prints muddy. This is the most common fault by far — it made fireworks olive and a hummingbird
  read as a leaf. Clear at full coverage: a knockout at a tone leaves the screen's own gaps and
  the plate below shows through the holes.
- Clear the subject out of every overlay plate, not just the ground. Light shafts crossing a
  whale turned it brown.
- A fringe or halo under a mark must be cleared where the top plate covers it. A whole disc left
  underneath works while the top ink is dark, but pink over yellow goes orange across the mark.
- Draw a subject into the ground's plate *before* knocking the ground out, or it stripes across the hole.

## Order within a plate

- Anything drawn after a knockout survives it. Order is the whole mechanism.
- A shape drawn after another buries it. Use `destination-over` to slot something behind.
- Tones add where two shapes overlap on one plate. A shape that must own its value clears first
  and prints second; ridges stacked back to front otherwise print solid at the bottom of frame.
- A shape used by two plates must be built from the shared `sr` rng *before* any
  `if (ink === …)` branch: `sr` is re-seeded identically per ink and must be consumed in the same
  order every time, or a knockout lands somewhere other than the shape it should clear. The
  per-ink `rng` is fine for anything only one plate draws.

## Canvas traps

- Increasing angle sweeps **clockwise** on screen, because y grows downward. Sweeping an arc the
  wrong way turned an `n` glyph into a `u`.
- Scaling a bitmap to reveal it drags the halftone along with it and the texture swims. Grow a
  clip and leave the artwork pinned; transform only when the movement itself is the effect.
- `multiply` lets white through. A scene inside a window must repaint paper before it multiplies,
  or the previous scene reads through all its light areas.
- An `inkPass` is a full-canvas operation screened at one flat coverage. Batch every shape of
  one ink into a single pass. Spatial tone on a live element needs `bandPass`, and a bright one
  over a dark ground needs `relight` first (`docs/motion.md`); moving frames use `docs/live-plates.md`.
- `coverage` is the dot screen, `alpha` is plate opacity. Fade line work on alpha and width:
  punching a screen through a 5px stroke breaks it into dashes rather than lightening it. A knock
  narrower than the screen pitch (~4.6 px) or under ~0.4 barely prints (Nonpareil's water
  streaks): count changed pixels against a render without it.
