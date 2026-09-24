# riso-windowseat

Procedural risograph films and still art. Each work is one self-contained `index.html` that draws
every pixel in Canvas 2D: no libraries, fonts, images or network calls in the deliverable
(the exception: attributed instrument recordings embedded in the sampled films below).
External references may be viewed for research, never embedded.

Skills: `riso-film` for animation, `riso-still` for images, `riso-score` for sound. Before
drawing, read `.claude/rules/riso-plates.md` and `docs/visual-development.md`. Technical checks
do not certify artistic quality; say what was and was not looked at or heard.

## Setup and commands

`cd tools && npm install && npm run setup && npm test`, then run these in `tools/`:

```
node new-riso.mjs --kind film --duration 60 --out ../films/<name>/index.html
node verify.mjs ../films/<name>/index.html
node review.mjs ../films/<name>/index.html [--mp4 ../out/<name>.mp4]
node shoot.mjs ../films/<name>/index.html --range 6.6:6.9:0.0333333333 --sheet
node still.mjs ../prints/<name>/index.html --at 0 --out ../out/<name>.png
node render.mjs ../films/<name>/index.html --fps 30 --size 1080 --engine firefox
node audio.mjs ../films/<name>/index.html --twice --marks 6,13.9
```

Read every sheet you generate. Range renders are silent; full exports mux `renderAudio()`.
Firefox is the primary engine. `out/` is disposable and git-ignored.

## Invariants

- Expose `window.__riso = { duration, ready, seek(t), renderAudio?, marks?, shots? }`; every tool
  drives it.
- `seek(t)` is pure in time, independent of seek history. Never call `Math.random()` in a render
  path; stable keys through `rngFor(key)` prevent texture crawl. A hook flags violations in
  `films/`.
- `renderAudio()` is exactly `duration` long at 48 kHz stereo and seeded like the picture;
  `--twice` checks it.
- Bake scenes at displayed size. Never resize a screened bitmap: it causes moiré. Film backing
  stores are 1080, independent of DPR; screen pitch is in device pixels.
- No pure black ink. Darks are overprints; keep full knockouts for bright subjects.
- Changing a `Score({ key })` or any `rngFor` key reseeds that output; freeze keys once approved.
- Sampled films embed recordings as multi-MB single lines (Held near the top, others at the
  end): grep with `-o` or `cut -c1-200`, never print or full-read them.

## Map

| Path | Holds |
|---|---|
| `films/window-seat/` | Showcase: sampled piano, piano-bank rebuild. |
| `films/roost/`, `films/held/`, `films/nonpareil/` | 70 s films: murmuration, kite on a rope, marbling; sampled scores. |
| `films/lumen/`, `films/emergence/` | 28 s shorts in the Resonance form. |
| `prints/` | Cabinet, Sceneries and Workings; workings donates the print kit. |
| `docs/` | The brief and craft docs; `brief.md` tables which to read when. |
| `studies/` | Craft, composition, scene-space and sound kits with A/B studies. |
| `.claude/skills/*/examples.md` | Where techniques live in the shipped sources. |
| `tools/` | Scaffolding, inspection and export harness; `README.md` documents each tool. |
