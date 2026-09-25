"""
Inline SVG diagrams for the Technical Note (docs/technical_notes.html).

Built on the same DSN-palette primitives as the slide deck
(scripts/build_dsn_presentation.py) so both documents share one visual language.
"""

import math
import random

from build_dsn_presentation import G, GD, GL, GT, R, RL, RT, INK, MUTE, COLD, _svg, _arrow

FONT = "Inter, Poppins, sans-serif"


def _text(x, y, txt, size=13, weight=600, fill=INK, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{txt}</text>')


def fig_decay():
    x0, y0, w, h = 70, 200, 560, 160
    body = (f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{MUTE}" stroke-width="1.5"/>'
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h - 10}" stroke="{MUTE}" stroke-width="1.5"/>')
    pts = " ".join(f"{x0 + t:.1f},{y0 - h * math.exp(-t / 110):.1f}" for t in range(0, w + 1, 8))
    body += f'<polyline points="{pts}" fill="none" stroke="{G}" stroke-width="3.5" stroke-linecap="round"/>'
    body += f'<circle cx="{x0 + 30}" cy="{y0 - h * math.exp(-30 / 110):.1f}" r="7" fill="{R}"/>'
    body += f'<circle cx="{x0 + 420}" cy="{y0 - h * math.exp(-420 / 110):.1f}" r="7" fill="{MUTE}"/>'
    body += _text(x0 + 44, y0 - h * math.exp(-30 / 110) - 12, "near: high covariance", 13, 600, R, "start")
    body += _text(x0 + 420, y0 - 30, "far: covariance &#8776; 0", 13, 600, MUTE)
    body += _text(x0 + w / 2, y0 + 30, "distance between two places", 13, 600, MUTE)
    body += (f'<text transform="translate({x0 - 24},{y0 - h / 2}) rotate(-90)" text-anchor="middle" '
             f'font-family="{FONT}" font-size="13" font-weight="600" fill="{MUTE}">covariance</text>')
    return _svg(700, 240, body)


def _grid3(ox, oy, fills, cell=40, gap=4):
    body = ""
    for i in range(3):
        for j in range(3):
            body += (f'<rect x="{ox + j * (cell + gap)}" y="{oy + i * (cell + gap)}" width="{cell}" '
                     f'height="{cell}" rx="5" fill="{fills[i][j]}"/>')
    return body


def fig_neighbours():
    N = "#f1f5f3"
    rook = [[N, G, N], [G, R, G], [N, G, N]]
    queen = [[GL, G, GL], [G, R, G], [GL, G, GL]]
    body = _grid3(20, 20, rook) + _grid3(200, 20, queen)
    body += _text(86, 170, "Rook: shared edge") + _text(266, 170, "Queen: edge or corner")
    # k-NN
    pts = [(470, 80), (452, 58), (494, 64), (462, 104), (492, 100), (430, 80), (512, 84), (474, 36),
           (446, 128), (520, 124), (410, 44), (538, 44), (405, 120), (545, 110)]
    c = pts[0]
    near = sorted(pts[1:], key=lambda p: math.dist(p, c))[:4]
    for p in near:
        body += f'<line x1="{c[0]}" y1="{c[1]}" x2="{p[0]}" y2="{p[1]}" stroke="{G}" stroke-width="2.5"/>'
    for p in pts[1:]:
        body += f'<circle cx="{p[0]}" cy="{p[1]}" r="6" fill="{G if p in near else MUTE}"/>'
    body += f'<circle cx="{c[0]}" cy="{c[1]}" r="8" fill="{R}"/>'
    body += _text(475, 170, "k-NN (k = 4)")
    # distance band
    cx, cy = 660, 80
    body += f'<circle cx="{cx}" cy="{cy}" r="52" fill="{GT}" stroke="{G}" stroke-width="2" stroke-dasharray="6 5"/>'
    for ang, d in ((20, 30), (100, 40), (170, 24), (240, 46), (300, 34), (60, 70), (200, 72), (330, 66)):
        x = cx + d * math.cos(math.radians(ang))
        y = cy + d * math.sin(math.radians(ang))
        body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{G if d <= 52 else MUTE}"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="8" fill="{R}"/>'
    body += _text(cx, 170, "Distance band")
    return _svg(760, 185, body)


def fig_wmatrix():
    nodes = {1: (70, 70), 2: (180, 44), 3: (126, 150), 4: (244, 138), 5: (310, 56)}
    edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5), (2, 5)]
    body = ""
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        body += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GL}" stroke-width="3.5"/>'
    for k, (x, y) in nodes.items():
        body += f'<circle cx="{x}" cy="{y}" r="20" fill="{G}"/>' + _text(x, y + 5, k, 15, 700, "#ffffff")
    body += _arrow(360, 100, 430)
    adj = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    ox, oy, c = 492, 22, 30
    for i in range(1, 6):
        body += _text(ox - 16, oy + (i - 1) * c + 20, i, 13, 600, MUTE)
        body += _text(ox + (i - 1) * c + 14, oy + 5 * c + 18, i, 13, 600, MUTE)
        for j in range(1, 6):
            x, y = ox + (j - 1) * c, oy + (i - 1) * c
            if i == j:
                fill, txt, tc = RT, "0", R
            elif (i, j) in adj:
                fill, txt, tc = G, "1", "#ffffff"
            else:
                fill, txt, tc = "#ffffff", "0", "#cbd5e1"
            body += (f'<rect x="{x}" y="{y}" width="{c - 2}" height="{c - 2}" rx="4" fill="{fill}" stroke="#e2e8f0"/>'
                     + _text(x + 14, y + 19, txt, 13, 600, tc))
    body += _text(ox + 72, oy + 5 * c + 40, "W (5 &#215; 5)", 13, 700, INK)
    return _svg(700, 225, body)


def fig_lag():
    cell = 60
    vals = {(0, 1): 4, (1, 0): 6, (1, 2): 8, (2, 1): 2}
    body = ""
    for i in range(3):
        for j in range(3):
            x, y = 40 + j * (cell + 5), 20 + i * (cell + 5)
            if (i, j) == (1, 1):
                body += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="{R}"/>' + _text(x + 30, y + 37, "i", 18, 700, "#ffffff")
            elif (i, j) in vals:
                body += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="{G}"/>' + _text(x + 30, y + 38, vals[(i, j)], 20, 700, "#ffffff")
            else:
                body += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="#f1f5f3"/>'
    body += _arrow(260, 117, 330)
    body += _text(470, 110, "[Wy]&#7522; = (4 + 6 + 8 + 2) / 4", 18, 600, INK)
    body += _text(470, 142, "= 5", 22, 800, GD)
    return _svg(640, 230, body)


def fig_moran_scatter():
    rnd = random.Random(7)
    cx, cy, sc = 300, 150, 52
    body = (f'<rect x="{cx}" y="{cy - 2.6 * sc}" width="{2.6 * sc}" height="{2.6 * sc}" fill="{RT}"/>'
            f'<rect x="{cx - 2.6 * sc}" y="{cy}" width="{2.6 * sc}" height="{2.6 * sc}" fill="#e7f0f8"/>')
    body += (f'<line x1="{cx - 2.7 * sc}" y1="{cy}" x2="{cx + 2.7 * sc}" y2="{cy}" stroke="{MUTE}" stroke-dasharray="5 4"/>'
             f'<line x1="{cx}" y1="{cy - 2.7 * sc}" x2="{cx}" y2="{cy + 2.7 * sc}" stroke="{MUTE}" stroke-dasharray="5 4"/>')
    for _ in range(90):
        z = rnd.gauss(0, 0.9)
        lag = 0.55 * z + rnd.gauss(0, 0.5)
        z, lag = max(-2.4, min(2.4, z)), max(-2.4, min(2.4, lag))
        col = R if z > 0 and lag > 0 else (COLD if z < 0 and lag < 0 else ("#f98400" if z > 0 else "#7fc4dd"))
        body += f'<circle cx="{cx + z * sc:.1f}" cy="{cy - lag * sc:.1f}" r="4.5" fill="{col}" opacity="0.85"/>'
    body += (f'<line x1="{cx - 2.5 * sc}" y1="{cy + 0.55 * 2.5 * sc}" x2="{cx + 2.5 * sc}" y2="{cy - 0.55 * 2.5 * sc}" '
             f'stroke="{INK}" stroke-width="2.5"/>')
    body += _text(cx + 2.0 * sc, cy - 2.3 * sc, "High-High", 14, 700, R)
    body += _text(cx - 2.0 * sc, cy + 2.45 * sc, "Low-Low", 14, 700, COLD)
    body += _text(cx - 2.0 * sc, cy - 2.3 * sc, "Low-High", 14, 700, "#3aa6c9")
    body += _text(cx + 2.0 * sc, cy + 2.45 * sc, "High-Low", 14, 700, "#f98400")
    body += _text(cx + 2.9 * sc, cy - 1.5 * sc, "slope = Moran's I", 14, 700, INK, "start")
    body += _text(cx, cy + 3.05 * sc, "own value z&#7522;", 13, 600, MUTE)
    body += (f'<text transform="translate({cx - 3.0 * sc},{cy}) rotate(-90)" text-anchor="middle" '
             f'font-family="{FONT}" font-size="13" font-weight="600" fill="{MUTE}">neighbours\' average [Wz]&#7522;</text>')
    return _svg(640, 320, body)


def fig_moran_patterns():
    vals = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95] * 4
    vals = sorted(vals)[:36]

    def colour(v):
        return R if v > 0.66 else (RL if v > 0.5 else (GL if v > 0.33 else G))

    clustered = sorted(vals)
    rnd = random.Random(3)
    shuffled = vals[:]
    rnd.shuffle(shuffled)
    lo, hi = sorted(vals)[:18], sorted(vals)[18:]
    checker = [hi.pop() if (i // 6 + i % 6) % 2 else lo.pop(0) for i in range(36)]
    body = ""
    for p, (grid, label) in enumerate(((clustered, "Clustered: I &#8776; +0.8"),
                                       (shuffled, "Random: I &#8776; 0"),
                                       (checker, "Checkerboard: I &#8776; &#8722;0.9"))):
        ox = 30 + p * 240
        for k, v in enumerate(grid):
            i, j = divmod(k, 6)
            if grid is clustered:
                i, j = k % 6, k // 6
            body += f'<rect x="{ox + j * 30}" y="{14 + i * 30}" width="27" height="27" rx="4" fill="{colour(v)}"/>'
        body += _text(ox + 88, 216, label, 14, 700, INK)
    return _svg(740, 230, body)


def fig_permutation():
    rnd = random.Random(11)
    sims = [rnd.gauss(-0.002, 0.012) for _ in range(999)]
    bins = [0] * 30
    lo, hi = -0.045, 0.045
    for v in sims:
        k = int((v - lo) / (hi - lo) * 30)
        if 0 <= k < 30:
            bins[k] += 1
    x0, y0, w, h = 60, 190, 460, 150
    top = max(bins)
    body = f'<line x1="{x0}" y1="{y0}" x2="{x0 + w + 150}" y2="{y0}" stroke="{MUTE}" stroke-width="1.5"/>'
    for k, c in enumerate(bins):
        bh = h * c / top
        body += f'<rect x="{x0 + k * w / 30:.1f}" y="{y0 - bh:.1f}" width="{w / 30 - 2:.1f}" height="{bh:.1f}" fill="{MUTE}" opacity="0.8"/>'
    ex = x0 + (0 - lo) / (hi - lo) * w
    body += f'<line x1="{ex:.1f}" y1="{y0}" x2="{ex:.1f}" y2="{y0 - h - 10}" stroke="{INK}" stroke-dasharray="4 4"/>'
    body += _text(ex, y0 - h - 16, "E[I]", 13, 700, INK)
    ox = x0 + w + 120
    body += f'<line x1="{ox}" y1="{y0}" x2="{ox}" y2="{y0 - h - 10}" stroke="{R}" stroke-width="3.5"/>'
    body += _text(ox, y0 - h - 16, "observed I", 13, 700, R)
    body += _arrow(x0 + w + 10, y0 - 70, ox - 8, R)
    body += _text(x0 + w / 2, y0 + 26, "Moran's I from 999 random shuffles of the map", 13, 600, MUTE)
    return _svg(720, 230, body)


def fig_gi_bins():
    bins = [("99%", "z > 2.58", "#b2182b"), ("95%", "z > 1.96", "#ef8a62"), ("90%", "z > 1.65", "#fddbc7"),
            ("Not significant", "", "#f1f5f3"),
            ("90%", "z < &#8722;1.65", "#d1e5f0"), ("95%", "z < &#8722;1.96", "#67a9cf"), ("99%", "z < &#8722;2.58", "#2166ac")]
    body = _text(160, 20, "Hot spot confidence", 14, 700, R) + _text(620, 20, "Cold spot confidence", 14, 700, COLD)
    for k, (lab, z, col) in enumerate(bins):
        x = 20 + k * 108
        body += f'<rect x="{x}" y="34" width="100" height="44" rx="6" fill="{col}"/>'
        tc = "#ffffff" if col in ("#b2182b", "#2166ac", "#67a9cf", "#ef8a62") else INK
        body += _text(x + 50, 61, lab, 13, 700, tc)
        if z:
            body += _text(x + 50, 100, z, 12, 600, MUTE)
    return _svg(780, 112, body)


def fig_residuals():
    rnd = random.Random(5)
    body = ""
    for p in range(2):
        ox = 40 + p * 380
        for i in range(8):
            for j in range(8):
                if p == 0:
                    v = rnd.random()
                else:
                    v = min(1, max(0, 0.9 - 0.11 * (i + j) + rnd.gauss(0, 0.08)))
                col = R if v > 0.75 else (RL if v > 0.5 else (GL if v > 0.25 else G))
                body += f'<rect x="{ox + j * 32}" y="{14 + i * 32}" width="29" height="29" rx="4" fill="{col}"/>'
        body += _text(ox + 126, 294, "Random residuals: OLS OK" if p == 0 else "Clustered residuals: OLS invalid",
                      14, 700, GD if p == 0 else R)
    return _svg(720, 310, body)


NOTE_FIGURES = {
    "decay": fig_decay(),
    "neighbours": fig_neighbours(),
    "wmatrix": fig_wmatrix(),
    "lag": fig_lag(),
    "moran_scatter": fig_moran_scatter(),
    "moran_patterns": fig_moran_patterns(),
    "permutation": fig_permutation(),
    "gi_bins": fig_gi_bins(),
    "residuals": fig_residuals(),
}
