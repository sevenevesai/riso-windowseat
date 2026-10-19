# Standby audio sources

The notes, arrangement and groove are original to this film. Every recording is CC0 and
embedded as Ogg Vorbis in the page's `#sample-bank` JSON script (2.72 MiB including base64,
40 recordings). There is no runtime network access.

| Library | Pinned commit | License |
|---|---|---|
| [VCSL](https://github.com/sgossner/VCSL) (Versilian Community Sample Library), Versilian Studios / Sam Gossner | `c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e` | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), text in `VCSL-LICENSE.txt` |

CC0 does not require attribution. Credits are kept for provenance, below the player and here.
The library README states that the collection is CC0 "essentially public domain", free for
commercial use with no credit. The TX81Z folder's `Origin.txt` says its patches are
user-created in TX81Z Programmer and sampled from the hardware; no patch author is named
upstream, and the folder sits under the same repository-wide CC0 `LICENSE`.

## Instruments

| Instrument | Upstream files (`<VCSL>/` + path) | Sounding roots (MIDI) | Role |
|---|---|---|---|
| Yamaha TX81Z FM piano, `vl2` | `Electrophones/TX81Z/FM Piano/FMPiano_<p>_vl2.wav`; `<p>` = C1 E1 G#1 C2 E2 G#2 C3 E3 G#3 C4 E4 G#4 C5 E5 | 24 28 32 36 40 44 48 52 56 60 64 68 72 76 | rolled chords on each x wall, comping, the bass (low-passed at 240 Hz) |
| Upright piano, Knight (Simon Dalzell, Ivy Audio), soft `vl1` | `Chordophones/Zithers/Upright Piano, Knight/Sustains/Player_vl1_rr1_<p>.wav`; `<p>` = A2 C#3 F3 A3 C#4 F4 A4 C#5 F5 A5 | 57 61 65 69 73 77 81 85 89 93 | the y-wall melody |
| Kalimba, Kenya | `Idiophones/Plucked Idiophones/Kalimba, Kenya/Mbira6_Normal_MainSpirit_<p>_k<n>_vl3_rr2.wav`; `<p>_k<n>` = D#3_k6 F#3_k5 G#3_k11 B3_k3 C#4_k2 D#4_k13 F#4_k14 A4_k1 | 63 66 68 71 73 75 78 81 | near-miss and corner sparkle, the last approach's pulse, the lullaby |
| Bass drum 1 | `Membranophones/Struck Membranophones/Bass Drum 1/BDrumNew_hit_v2_rr1_Sum.wav` (soft), `..._v3_rr1_Sum.wav` (mid) | unpitched | the groove's kick; the corner's body |
| Cajon | `Idiophones/Struck Idiophones/Cajon/Cajon_hit3_p_rr1.wav`, `Cajon_hit2_pp_rr1.wav` | unpitched | the half-time backbeat and a ghost note |
| Hi-hat, closed | `Idiophones/Struck Idiophones/Hi-Hat Cymbal/HiHat_Close_rr1_Mid.wav`, `HiHat_HitC_v1_rr1_Mid.wav` | unpitched | swung ghost eighths |
| Small shaker | `Idiophones/Struck Idiophones/Shaker, Small/Mid_ShakerDouble_Down_rr1.wav`, `..._Up_rr1.wav` | unpitched | the brush-like off-beat wash |

VCSL names pitches an octave below scientific pitch for the upright and the kalimba (the
upright file `A2` sounds A3). The builder measures every pitched root from the recorded partials
and the table lists the measured value. The kalimba's tines are not tuned to equal temperament:
corrections run from −44 to +36 cents and are applied at playback. Two kalimba files were left
out: `B4_k15`, whose strongest partial sits an octave under its name, and any tine whose root
could not be told apart from a 499 Hz resonance shared by several files.

## Preparation

`build-sample-bank.py` downloads the files once into `out/standby-samples/` (git-ignored). It
removes DC, trims leading silence to 3 ms, and keeps pitched notes for 3.2 to 6 s and drums
until they fall 55 dB under their peak. It narrows stereo width (side at 45 to 50 %), matches
the first 400 ms of each pitched note to RMS 0.16 and peak-normalises drums, fades both ends,
resamples 44.1 → 48 kHz and encodes Vorbis quality 4. `sample-bank-manifest.json` keeps every
source URL, source and encoded SHA-256, trim, gain, measured root and tuning, without the
payload.

Rebuild from the project root:

```
python films/standby/build-sample-bank.py --embed
```

Requires Python with `numpy`, `scipy`, `soundfile` and `imageio-ffmpeg`. Re-run the audio gates
after rebuilding, because a different Vorbis encoder changes the decoded samples.

## Not sampled

Mains hum, the 15.734 kHz line whine, crickets, the switch-off's relay click, thump and static,
the car, a quiet kit pad, a sub-bass sine and a triangle riser are synthesised by the sound kit.
The tape (a slow wow and a faster flutter of 7 and 2.2 cents on every pitched sample, a soft
saturation, a rolled-off top) and the vinyl pops and hiss are seeded noise generated in the
page. None of them is a recording.
