"""Rebuild the embedded CC0 instrument bank. Requires numpy, scipy, soundfile, imageio-ffmpeg.

Run from any directory: python films/eclosion/build-sample-bank.py --embed
Vibraphone (soft mallets) from VCSL; clarinet (long sustains) and French horn
(sustains) from VSCO 2 Community Edition. Both libraries are CC0 and pinned to one
commit. Downloads and prepared Oggs go in out/eclosion-samples/. The manifest keeps
source and encoded hashes, the measured root of every recording and its tuning
correction. --embed changes only the JSON bank in index.html.
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
CACHE = ROOT / 'out' / 'eclosion-samples'
VSCO = 'https://raw.githubusercontent.com/sgossner/VSCO-2-CE/440300901dfe9275fd84e0b7763af1f8443ae62e/'
VCSL = 'https://raw.githubusercontent.com/sgossner/VCSL/c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e/'
RATE = 48000
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi_of(name):
    """Filename pitch in scientific numbering (C4 = 60); the builder measures the real octave."""
    m = re.match(r'([A-G])(#?)(-?\d)$', name)
    return 12 * (int(m[3]) + 1) + NAMES[m[1]] + (1 if m[2] else 0)


# (instrument, filename pitch, library, path, seconds kept)
SOURCES = []
for p in ['F2', 'A2', 'C3', 'E3', 'G3', 'B3', 'D4', 'F4', 'A4', 'C5', 'E5']:
    rr = 'rr2' if p in ('C3', 'E3') else 'rr1'
    SOURCES.append(('vibes', p, 'vcsl', f'Idiophones/Struck Idiophones/Vibraphone/Soft Mallets/Vibes_soft_{p}_v1_{rr}_Main.wav', 7.0))
for p in ['D2', 'F2', 'A#2', 'D3', 'F3', 'A#3', 'D4', 'F4', 'A#4']:
    SOURCES.append(('clarinet', p, 'vsco', f'Woodwinds/Clarinet/susLong/DCClar_susLong_{p}_v1_rr1_sum.wav', 7.0))
for p in ['C1', 'D#1', 'G1', 'A#1', 'D2', 'F2', 'A2', 'C3']:
    SOURCES.append(('horn', p, 'vsco', f'Brass/F Horn/sus/MOHorn_sus_{p}_v1_1.wav', 7.0))
SUSTAINED = {'clarinet', 'horn'}
SIDE = {'vibes': .5, 'clarinet': .25, 'horn': .3}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(url, dst):
    if not dst.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'riso-eclosion'})
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


def measure_root(y, sr, nominal, sustained):
    """The sounding fundamental of the nominal pitch class, octaves -2..+3. A candidate is
    scored by its harmonics f, 3f, 5f (a vibraphone bar has no 3f, so its own f carries it);
    an octave too low finds none of them, and the lowest candidate that scores is the note.
    VSCO names pitches an octave low for some instruments, so the octave is always measured."""
    mono = y.mean(axis=1)
    start = int((0.6 if sustained else 0.12) * sr)
    seg = mono[start:start + int(1.2 * sr)]
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
        score = sum(peak_near(spectrum, f, hz * h, 30)[0] for h in (1, 3, 5) if hz * h < 12000)
        cands.append((m, score, at, mag))
    top = max(c[1] for c in cands)
    for m, score, at, mag in cands:
        if score > 0.3 * top and mag > 0.1 * max(c[3] for c in cands):
            hz = 440 * 2 ** ((m - 69) / 12)
            return m, 1200 * np.log2(at / hz)
    raise ValueError('no fundamental')


def measure_tuning(y, sr, root):
    """Tuning of a pinned root, read from its strongest harmonic: the soft low horn notes
    have almost no fundamental (C1's file measures 0.00 at f, 0.71 at 4f), so the scorer
    above takes their second harmonic for the note. The series spacing gives the octave."""
    mono = y.mean(axis=1)
    seg = mono[int(.6 * sr):int(1.8 * sr)]
    n = 1 << 19
    spectrum = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    f = np.fft.rfftfreq(n, 1 / sr)
    hz = 440 * 2 ** ((root - 69) / 12)
    k, (mag, at) = max(((k, peak_near(spectrum, f, hz * k, 30)) for k in range(1, 9)), key=lambda c: c[1][0])
    return 1200 * np.log2(at / (hz * k))


def build():
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest_path = FILM / 'sample-bank-manifest.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    expected = {s['source']: s['sourceSha256'] for s in previous.get('samples', [])}
    (FILM / 'VSCO-LICENSE.txt').write_bytes(get(VSCO + 'LICENSE', CACHE / 'VSCO-LICENSE').read_bytes())
    bank = dict(format='audio/ogg; codecs=vorbis', sampleRate=RATE, license='CC0-1.0', libraries=[
        dict(name='Versilian Community Sample Library (VCSL)', author='Versilian Studios (Sam Gossner)', license='CC0-1.0',
             source='https://github.com/sgossner/VCSL', commit='c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e'),
        dict(name='VSCO 2 Community Edition', author='Versilian Studios', license='CC0-1.0',
             source='https://github.com/sgossner/VSCO-2-CE', commit='440300901dfe9275fd84e0b7763af1f8443ae62e',
             recordings='Sam Gossner and Simon Dalzell; sample cutting Elan Hickler / Soundemote')], samples=[])
    for instrument, pitch, lib, rel, keep in SOURCES:
        base = VSCO if lib == 'vsco' else VCSL
        url = base + rel
        path = get(base + urllib.parse.quote(rel), CACHE / Path(rel).name)
        digest = sha(path.read_bytes())
        if url in expected and expected[url] != digest:
            raise ValueError(f'Source hash changed: {url}')
        y, sr = sf.read(path, always_2d=True)
        if y.shape[1] == 1:
            y = np.column_stack((y[:, 0], y[:, 0]))
        y = y[:, :2] - y[:, :2].mean(axis=0)
        sustained = instrument in SUSTAINED
        step = max(1, int(.005 * sr))
        energy = np.array([np.sqrt(np.mean(y[i:i + step] ** 2)) for i in range(0, len(y) - step, step)])
        audible = np.flatnonzero(energy > energy.max() * (.035 if sustained else .02))
        trim = max(0, int(audible[0] * step - (.025 if sustained else .004) * sr))
        y = y[trim:]
        if instrument == 'horn':            # VSCO names horn pitches an octave low
            root = midi_of(pitch) + 12
            cents = measure_tuning(y, sr, root)
        else:
            root, cents = measure_root(y, sr, midi_of(pitch), sustained)
        if not sustained:
            env = np.array([np.sqrt(np.mean(y[i:i + step] ** 2)) for i in range(0, len(y) - step, step)])
            quiet = np.flatnonzero(env > env.max() * 10 ** (-50 / 20))
            keep = min(keep, (quiet[-1] + 1) * step / sr + .05)
        y = y[:int(keep * sr)]
        mid, side = y.mean(axis=1), (y[:, 0] - y[:, 1]) * .5 * SIDE[instrument]
        y = np.column_stack((mid + side, mid - side))
        if sustained:
            body = y[int(.5 * sr):int(min(4.5, len(y) / sr - .3) * sr)]
            gain = min(.085 / float(np.sqrt(np.mean(body ** 2))), .82 / max(abs(y).max(), 1e-9))
        else:
            body = y[:int(.3 * sr)]
            gain = min(.16 / float(np.sqrt(np.mean(body ** 2))), .85 / max(abs(y).max(), 1e-9))
        y = y * gain
        fade_in = int((.012 if sustained else .0015) * sr)
        y[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
        fade_out = int(min(.25, len(y) / sr * .2) * sr)
        y[-fade_out:] *= (np.linspace(1, 0, fade_out) ** 2)[:, None]
        if sr != RATE:
            g = gcd(RATE, sr)
            y = resample_poly(y, RATE // g, sr // g, axis=0)
        stem = f'{instrument}-{root}'
        wav, ogg = CACHE / (stem + '.prep.wav'), CACHE / (stem + '.ogg')
        sf.write(wav, y, RATE, subtype='PCM_24')
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(wav), '-map_metadata', '-1',
                        '-c:a', 'libvorbis', '-q:a', '5', str(ogg)], check=True)
        encoded = ogg.read_bytes()
        bank['samples'].append(dict(instrument=instrument, root=root, filePitch=pitch, source=url, sourceSha256=digest,
                                    encodedSha256=sha(encoded), sourceRate=sr, trimSeconds=round(trim / sr, 4),
                                    gain=round(gain, 4), tuneCents=round(-cents, 2), seconds=round(len(y) / RATE, 3),
                                    audio=base64.b64encode(encoded).decode()))
        print(f'{stem:12s} file {pitch:4s} {len(y) / RATE:5.2f}s  tuning {-cents:+6.1f} c  sr {sr}  '
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
