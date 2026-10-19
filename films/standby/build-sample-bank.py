"""Rebuild the embedded CC0 instrument bank for Standby. Requires numpy, scipy, soundfile, imageio-ffmpeg.

Run from any directory: python films/standby/build-sample-bank.py --embed
Everything comes from the Versilian Community Sample Library (VCSL, CC0), pinned to one commit:
Yamaha TX81Z FM piano (hardware samples), Knight upright piano, Kenya kalimba, bass drum, cajon,
closed hi-hat and small shaker. Downloads and prepared Oggs go in out/standby-samples/
(git-ignored). The manifest keeps source and encoded hashes, the measured root of every pitched
recording and its tuning correction. --embed changes only the JSON bank in index.html.
"""
import argparse
import base64
import hashlib
import json
from math import gcd
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request

import imageio_ffmpeg
import numpy as np
from scipy.signal import resample_poly
import soundfile as sf

FILM = Path(__file__).resolve().parent
ROOT = FILM.parents[1]
CACHE = ROOT / 'out' / 'standby-samples'
COMMIT = 'c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e'
VCSL = f'https://raw.githubusercontent.com/sgossner/VCSL/{COMMIT}/'
RATE = 48000
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi_of(name):
    """Filename pitch in scientific numbering (C4 = 60); the builder measures the real octave."""
    m = re.match(r'([A-G])(#?)(-?\d)$', name)
    return 12 * (int(m[3]) + 1) + NAMES[m[1]] + (1 if m[2] else 0)


# (instrument, label, filename pitch or None, path under VCSL, seconds kept)
SOURCES = []
FM = 'Electrophones/TX81Z/FM Piano/FMPiano_{}_vl2.wav'
for p in ['C1', 'E1', 'G#1', 'C2', 'E2', 'G#2', 'C3', 'E3', 'G#3', 'C4', 'E4', 'G#4', 'C5', 'E5']:
    SOURCES.append(('fmpiano', p, p, FM.format(p), 6.0))
UP = 'Chordophones/Zithers/Upright Piano, Knight/Sustains/Player_vl1_rr1_{}.wav'
for p in ['A2', 'C#3', 'F3', 'A3', 'C#4', 'F4', 'A4', 'C#5', 'F5', 'A5']:
    SOURCES.append(('upright', p, p, UP.format(p), 5.5))
KAL = 'Idiophones/Plucked Idiophones/Kalimba, Kenya/Mbira6_Normal_MainSpirit_{}_k{}_vl3_rr2.wav'
for p, k in [('D#3', 6), ('F#3', 5), ('G#3', 11), ('B3', 3), ('C#4', 2), ('D#4', 13), ('F#4', 14), ('A4', 1)]:
    SOURCES.append(('kalimba', p, p, KAL.format(p, k), 3.2))
PERC = 'Idiophones/Struck Idiophones/'
for label, rel, keep in [
    ('kick-soft', 'Membranophones/Struck Membranophones/Bass Drum 1/BDrumNew_hit_v2_rr1_Sum.wav', 1.2),
    ('kick-mid', 'Membranophones/Struck Membranophones/Bass Drum 1/BDrumNew_hit_v3_rr1_Sum.wav', 1.2),
    ('cajon-pp', PERC + 'Cajon/Cajon_hit2_pp_rr1.wav', 1.0),
    ('cajon-p', PERC + 'Cajon/Cajon_hit3_p_rr1.wav', 1.0),
    ('hat-closed', PERC + 'Hi-Hat Cymbal/HiHat_Close_rr1_Mid.wav', .5),
    ('hat-tip', PERC + 'Hi-Hat Cymbal/HiHat_HitC_v1_rr1_Mid.wav', .5),
    ('shaker-down', PERC + 'Shaker, Small/Mid_ShakerDouble_Down_rr1.wav', .5),
    ('shaker-up', PERC + 'Shaker, Small/Mid_ShakerDouble_Up_rr1.wav', .5),
]:
    SOURCES.append(('perc', label, None, rel, keep))
SIDE = {'fmpiano': .5, 'upright': .45, 'kalimba': .5, 'perc': .5}
BODY_RMS = {'fmpiano': .16, 'upright': .16, 'kalimba': .16}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(url, dst):
    if not dst.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'riso-standby'})
        with urllib.request.urlopen(req, timeout=90) as response:
            dst.write_bytes(response.read())
    return dst


def peak_near(spectrum, f, center, cents=45):
    lo, hi = center * 2 ** (-cents / 1200), center * 2 ** (cents / 1200)
    idx = np.flatnonzero((f > lo) & (f < hi))
    if len(idx) < 3:
        return 0.0, center
    i = idx[np.argmax(spectrum[idx])]
    a, b, c = np.log(spectrum[i - 1:i + 2] + 1e-12)
    delta = .5 * (a - c) / (a - 2 * b + c)
    return float(spectrum[i]), float((i + delta) * (f[1] - f[0]))


def measure_root(y, sr, nominal):
    """The sounding fundamental of the nominal pitch class, octaves -2..+3. A candidate is
    scored by its harmonics f, 2f, 3f; the lowest candidate that scores is the note."""
    mono = y.mean(axis=1)
    seg = mono[int(.08 * sr):int(1.3 * sr)]
    n = 1 << 19
    spectrum = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    f = np.fft.rfftfreq(n, 1 / sr)
    cands = []
    for k in range(-2, 4):
        m = nominal + 12 * k
        hz = 440 * 2 ** ((m - 69) / 12)
        if hz < 25 or hz > 9000:
            continue
        mag, at = peak_near(spectrum, f, hz)
        score = sum(peak_near(spectrum, f, hz * h, 30)[0] for h in (1, 2, 3) if hz * h < 12000)
        cands.append((m, score, at, mag))
    top = max(c[1] for c in cands)
    for m, score, at, mag in cands:
        if score > 0.3 * top and mag > 0.1 * max(c[3] for c in cands):
            hz = 440 * 2 ** ((m - 69) / 12)
            return m, 1200 * np.log2(at / hz)
    raise ValueError('no fundamental')


def build():
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest_path = FILM / 'sample-bank-manifest.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    expected = {s['source']: s['sourceSha256'] for s in previous.get('samples', [])}
    (FILM / 'VCSL-LICENSE.txt').write_bytes(get(VCSL + 'LICENSE', CACHE / 'VCSL-LICENSE').read_bytes())
    bank = dict(format='audio/ogg; codecs=vorbis', sampleRate=RATE, license='CC0-1.0', libraries=[
        dict(name='Versilian Community Sample Library (VCSL)', author='Versilian Studios (Sam Gossner)', license='CC0-1.0',
             source='https://github.com/sgossner/VCSL', commit=COMMIT)], samples=[])
    for instrument, label, pitch, rel, keep in SOURCES:
        url = VCSL + rel
        path = get(VCSL + urllib.parse.quote(rel), CACHE / Path(rel).name)
        digest = sha(path.read_bytes())
        if url in expected and expected[url] != digest:
            raise ValueError(f'Source hash changed: {url}')
        y, sr = sf.read(path, always_2d=True)
        if y.shape[1] == 1:
            y = np.column_stack((y[:, 0], y[:, 0]))
        y = y[:, :2] - y[:, :2].mean(axis=0)
        step = max(1, int(.002 * sr))
        energy = np.array([np.sqrt(np.mean(y[i:i + step] ** 2)) for i in range(0, len(y) - step, step)])
        audible = np.flatnonzero(energy > energy.max() * .03)
        trim = max(0, int(audible[0] * step - .003 * sr))
        y = y[trim:]
        root, cents = (None, 0.0) if pitch is None else measure_root(y, sr, midi_of(pitch))
        if pitch is None:
            env = np.array([np.sqrt(np.mean(y[i:i + step] ** 2)) for i in range(0, len(y) - step, step)])
            quiet = np.flatnonzero(env > env.max() * 10 ** (-55 / 20))
            keep = min(keep, (quiet[-1] + 1) * step / sr + .04)
        y = y[:int(keep * sr)]
        mid, side = y.mean(axis=1), (y[:, 0] - y[:, 1]) * .5 * SIDE[instrument]
        y = np.column_stack((mid + side, mid - side))
        if pitch is None:
            gain = .8 / max(abs(y).max(), 1e-9)
        else:
            body = y[:int(.4 * sr)]
            gain = min(BODY_RMS[instrument] / float(np.sqrt(np.mean(body ** 2))), .85 / max(abs(y).max(), 1e-9))
        y = y * gain
        fade_in = int(.0015 * sr)
        y[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
        fade_out = int(min(.4, len(y) / sr * .25) * sr)
        y[-fade_out:] *= (np.linspace(1, 0, fade_out) ** 2)[:, None]
        if sr != RATE:
            g = gcd(RATE, sr)
            y = resample_poly(y, RATE // g, sr // g, axis=0)
        stem = f'{instrument}-{label}'.replace('#', 's')
        wav, ogg = CACHE / (stem + '.prep.wav'), CACHE / (stem + '.ogg')
        sf.write(wav, y, RATE, subtype='PCM_24')
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(wav), '-map_metadata', '-1',
                        '-c:a', 'libvorbis', '-q:a', '4', str(ogg)], check=True)
        encoded = ogg.read_bytes()
        bank['samples'].append(dict(instrument=instrument, label=label, root=root, filePitch=pitch, source=url,
                                    sourceSha256=digest, encodedSha256=sha(encoded), sourceRate=sr,
                                    trimSeconds=round(trim / sr, 4), gain=round(gain, 4),
                                    tuneCents=round(-cents, 2), seconds=round(len(y) / RATE, 3),
                                    audio=base64.b64encode(encoded).decode()))
        print(f'{stem:20s} file {str(pitch):4s} root {root}  {len(y) / RATE:5.2f}s  tuning {-cents:+6.1f} c  sr {sr}  '
              f'{len(encoded) // 1024} KiB', flush=True)
    manifest = {**bank, 'samples': [{k: v for k, v in s.items() if k != 'audio'} for s in bank['samples']]}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    payload = json.dumps(bank, separators=(',', ':'))
    (CACHE / 'sample-bank.json').write_text(payload, encoding='utf-8')
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--embed', action='store_true')
    args = parser.parse_args()
    payload = build()
    if args.embed:
        html = FILM / 'index.html'
        text = html.read_text(encoding='utf-8')
        block = '<script id="sample-bank" type="application/json">\n' + payload + '\n</script>'
        pattern = r'<script id="sample-bank" type="application/json">[\s\S]*?</script>'
        if re.search(pattern, text):
            text = re.sub(pattern, lambda _: block, text)
        else:
            text = text.replace('</html>', block + '\n</html>')
        html.write_text(text, encoding='utf-8')
    print(f'PASS: {len(SOURCES)} CC0 recordings; bank {len(payload) / 1048576:.2f} MiB')
