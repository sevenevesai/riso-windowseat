# Eclosion audio sources

The notes and arrangement are original to this film. Every recording is CC0 and embedded as
Ogg Vorbis in the page's `#sample-bank` JSON script (3.57 MiB including base64). There is no
runtime network access.

| Library | Pinned commit | License |
|---|---|---|
| [VCSL](https://github.com/sgossner/VCSL) (Versilian Community Sample Library), Versilian Studios / Sam Gossner | `c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e` | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) |
| [VSCO 2 Community Edition](https://github.com/sgossner/VSCO-2-CE), Versilian Studios; recordings Sam Gossner and Simon Dalzell, sample cutting Elan Hickler / Soundemote | `440300901dfe9275fd84e0b7763af1f8443ae62e` | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), text in `VSCO-LICENSE.txt` |

CC0 does not require attribution. Credits are kept for provenance, below the player and here.

## Instruments

| Instrument | Upstream files | Sounding roots (MIDI) | Role |
|---|---|---|---|
| Vibraphone, soft mallets, `v1` | VCSL `Idiophones/Struck Idiophones/Vibraphone/Soft Mallets/Vibes_soft_<p>_v1_rr1_Main.wav` (`rr2` for C3, E3); `<p>` = F2 A2 C3 E3 G3 B3 D4 F4 A4 C5 E5 | 53 57 60 64 67 71 74 77 81 84 88 | the motif, chords rolled on each pump, the flight arpeggio |
| Clarinet, long sustain, `v1` | VSCO `Woodwinds/Clarinet/susLong/DCClar_susLong_<p>_v1_rr1_sum.wav`; `<p>` = D2 F2 A#2 D3 F3 A#3 D4 F4 A#4 | 50 53 58 62 65 70 74 77 82 | the line that climbs as the wings lengthen |
| French horn, sustain, `v1` | VSCO `Brass/F Horn/sus/MOHorn_sus_<p>_v1_1.wav`; `<p>` = C1 D#1 G1 A#1 D2 F2 A2 C3 | 36 39 43 46 50 53 57 60 | the warm floor; one swell per pump |

Both libraries name these pitches an octave below scientific pitch. The builder measures the
vibraphone and clarinet roots from their partials. The soft low horn notes have almost no
fundamental: the C1 file measures 0.00 at f and 0.71 at 4f, relative to its strongest
harmonic. The partial scorer therefore took their second harmonic for the note, so horn roots
are pinned to the naming (+12) and only their tuning is measured, from the strongest harmonic.
Tuning corrections run from −5.3 to +6.1 cents. Every note in the score is within two
semitones of the recording it is played from.

## Preparation

`build-sample-bank.py` downloads the files once into `out/eclosion-samples/` (git-ignored). It
removes DC, trims leading silence (25 ms of safety for sustains, 4 ms for strikes), and keeps
vibraphone strikes until they fall 50 dB under their peak (at most 7 s) and sustains for 7 s.
It narrows stereo width (side at 50 % for vibes, 25 % clarinet, 30 % horn) and fades both ends.
Sustained body RMS is matched to 0.085 and the first 300 ms of each strike to 0.16. It then
resamples 44.1 → 48 kHz and encodes Vorbis quality 5. `sample-bank-manifest.json` keeps every
source URL, source and encoded SHA-256, trim, gain, measured root and tuning, without the
payload.

Rebuild from the project root:

```
python films/eclosion/build-sample-bank.py --embed
```

Requires Python with `numpy`, `scipy`, `soundfile` and `imageio-ffmpeg`. Re-run the audio gates
after rebuilding, because a different Vorbis encoder changes the decoded samples.

## Not sampled

The only other sound is the kit's `air`, a very quiet procedural room tone that keeps the
quietest moments from reading as a dropout. There are no sound effects: the split, the drop,
the pumps and the push-off are all voiced by the three instruments.
