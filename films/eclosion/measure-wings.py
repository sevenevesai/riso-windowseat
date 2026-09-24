"""Rebuild the WING geometry embedded in index.html. Requires numpy, scipy, opencv-python.

Run from the project root: python films/eclosion/measure-wings.py
Prints the WING JSON; paste it over `const WING = …` in index.html. The source is a
photograph of a male monarch specimen, dorsal side: "Danaus plexippus MHNT dos.jpg" by
Didier Descouens, Wikimedia Commons, CC BY-SA 4.0. The 960 px rendition is downloaded once
into out/eclosion-refs/ and checked by hash; nothing from it is embedded but this data.

Outlines, orange cells, dusky apex cells, white spots and pale subapical spots are found
by colour thresholds on the right wings, then resampled and smoothed. Units: 1000 = the
forewing from base to apex; u runs out from the body, v toward the tail. The hindwing's
front edge (under the forewing) and its pale inner margin are drawn by hand below.
"""
import hashlib
import json
from pathlib import Path
import urllib.request

import cv2
import numpy as np
from scipy.ndimage import gaussian_filter1d

ROOT = Path(__file__).resolve().parents[2]
SRC = ('https://thumb.wikimedia.org/wikipedia/commons/thumb/5/57/Danaus_plexippus_MHNT_dos.jpg/'
       '960px-Danaus_plexippus_MHNT_dos.jpg')
SHA = 'ea4eb62e6b035014f0621e2b21272acaf09f701b4f1205f45e51fce2d526361b'
BASE, APEX = np.array([505.0, 335.0]), np.array([870.0, 80.0])   # forewing base and apex, px
L = float(np.linalg.norm(APEX - BASE))


def image():
    path = ROOT / 'out' / 'eclosion-refs' / '52118554.jpg'
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(SRC, headers={'User-Agent': 'riso-eclosion'})
        path.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA:
        raise ValueError(f'{path} is not the measured photograph')
    return cv2.imread(str(path))


def nm(p):
    return [int(round(v)) for v in (np.array(p, float) - BASE) / L * 1000]


def px(q):
    return np.array(q, float) / 1000 * L + BASE


def smooth(poly, sig, eps):
    """Resample a closed polygon at ~1 px, Gaussian-smooth it, and simplify."""
    p = np.array([px(q) for q in poly])
    closed = np.r_[p, p[:1]]
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(closed, axis=0), axis=1))]
    u = np.linspace(0, s[-1], max(24, int(s[-1])), endpoint=False)
    x = gaussian_filter1d(np.interp(u, s, closed[:, 0]), sig, mode='wrap')
    y = gaussian_filter1d(np.interp(u, s, closed[:, 1]), sig, mode='wrap')
    a = cv2.approxPolyDP(np.stack([x, y], 1).astype(np.float32).reshape(-1, 1, 2), eps, True)[:, 0, :]
    return [nm(q) for q in a]


def main():
    im = image()
    H, W = im.shape[:2]
    b, g, r = [im[:, :, i].astype(int) for i in range(3)]
    bg = (r + g + b > 690) & (np.abs(r - b) < 40)                        # white backdrop
    wing = (~bg).astype(np.uint8)
    wing[:, :508] = 0                                                   # body and left wings
    wing = cv2.morphologyEx(wing, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))   # antenna
    n, lab, st, _ = cv2.connectedComponentsWithStats(wing)
    wing = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    ff, m = wing.copy(), np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(ff, m, (W - 1, 0), 1)
    filled = wing | (ff == 0).astype(np.uint8)                          # white spots belong to the wing
    yy, xx = np.mgrid[0:H, 0:W]
    fore_side = yy < 345 + (xx - 505) * 0.028                           # forewing inner margin, read by eye
    foreM, hindM = (filled == 1) & fore_side, (filled == 1) & ~fore_side

    def outline(mask):
        cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return [nm(p) for p in cv2.approxPolyDP(max(cs, key=cv2.contourArea), 1.6, True)[:, 0, :]]

    def spots(mask, region, min_area):
        n, lab, st, cen = cv2.connectedComponentsWithStats((mask & region).astype(np.uint8))
        out = []
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] < min_area:
                continue
            ys, xs = np.where(lab == i)
            pts = np.stack([xs, ys], 1).astype(np.float32)
            (cx, cy), (w, h), ang = cv2.minAreaRect(pts) if len(pts) >= 5 else ((cen[i][0], cen[i][1]), (2, 2), 0)
            out.append(nm((cx, cy)) + [int(round(w / L * 1000)), int(round(h / L * 1000)), int(round(ang))])
        return out

    def cells(mask, region, min_area, erode):
        m = cv2.morphologyEx((mask & region).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        m = (cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.3) > 0.5).astype(np.uint8)
        if erode:
            m = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode + 1, 2 * erode + 1)))
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return [smooth([nm(q) for q in c[:, 0, :]], 1.8, 0.9)
                for c in sorted(cs, key=lambda c: -cv2.contourArea(c)) if cv2.contourArea(c) >= min_area]

    orange = (r > 170) & (g > 60) & (g < 175) & (b < 90) & (r - b > 120)
    pale = (r > 200) & (g > 150) & (b > 90) & (b < 200) & (r - b > 40)
    white = (r > 205) & (g > 200) & (b > 185)
    dusky = (r > 95) & (r - b > 55) & (r - g > 40) & (g < 120)

    # Outlines: drop the antenna's bite in the costa, add a point on the straight split line,
    # and give the hindwing the front edge and inner margin the photo cannot show.
    fore = [p for p in outline(foreM) if p not in ([218, -296], [202, -281], [186, -281])]
    i = fore.index([7, 22])
    fore = fore[:i + 1] + [[300, 42]] + fore[i + 1:]
    hm = outline(hindM)
    tail = hm[hm.index([254, 640]):hm.index([620, 299]) + 1]
    hind = ([[7, 25], [12, 130], [24, 250], [46, 380], [80, 490], [118, 568], [160, 620], [211, 642]] + tail
            + [[622, 240], [606, 185], [566, 128], [498, 78], [400, 42], [262, 20], [120, 16]])

    def mask_of(poly):
        mk = np.zeros((H, W), np.uint8)
        cv2.fillPoly(mk, [np.round(np.array([px(q) for q in poly])).astype(np.int32)], 1)
        return mk

    fM = mask_of(fore)
    hM = mask_of(hind) & (1 - fM)
    wing_json = {
        'fore': smooth(fore, 1.2, 0.8), 'hind': smooth(hind, 1.2, 0.8),
        'foreCells': cells(orange, fM, 50, 0), 'hindCells': cells(orange, hM, 50, 0),
        'foreDusk': cells(dusky & ~orange, fM, 60, 1),
        'foreWhite': spots(white, foreM, 6), 'hindWhite': spots(white, hindM, 6),
        'forePale': spots(pale & ~white, foreM, 25),
    }
    print(json.dumps(wing_json, separators=(',', ':')))


if __name__ == '__main__':
    main()
