"""
DSN Spatial Statistics Masterclass Deck & Portal - Refined Minimalist Theme.

Strict Design Rules:
1. NO colored borders on shapes/cards/callouts. Clean 1px solid #e2e8f0 only.
2. NO tags or subheadings with background at the top of slides.
3. Smart, smaller fonts: h2 (21px), h4 (13.5px), body p/li (11.5px - 12px).
4. Generous whitespace: slides leave comfortable 45px+ breathing room above the DSN bottom line.
5. GitHub link with official GitHub icon in the sidebar pointing to:
   https://github.com/SammyGIS/dsn_advanced_spatial_stats
6. Base64 embedded logos and backgrounds for 100% path independence.
7. Embedded Technical Notes view with KaTeX equations (ZERO 404).
"""

import os
import re
import base64

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(path)[1].lower().replace(".", "")
        if ext == "jpg": ext = "jpeg"
        if ext == "svg": ext = "svg+xml"
        return f"data:image/{ext};base64,{data}"
    return ""


# =============================================================================
# SVG DIAGRAMS (DSN LOGO PALETTE) - pure visuals, no extra words on slides
# =============================================================================
G, GD, GL, GT = "#00a859", "#007f43", "#8fd6b0", "#e3f5ec"
R, RL, RT = "#ed3237", "#f6a3a5", "#fde9ea"
INK, MUTE = "#0f172a", "#94a3b8"


def _svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{body}</svg>')


def _arrow(x1, y, x2, color=MUTE):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y} {x2 - 10},{y - 6} {x2 - 10},{y + 6}" fill="{color}"/>')


def _hex(cx, cy, r, fill, stroke="#ffffff"):
    pts = " ".join(f"{cx + r * c:.1f},{cy + r * s_:.1f}" for c, s_ in
                   [(0, -1), (0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5)])
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'


def _hex_grid(w, h, r):
    """Yield (cx, cy, q, rr) for a pointy-top hex grid covering w x h."""
    dx, dy = r * 1.732, r * 1.5
    rows = int(h / dy) + 2
    cols = int(w / dx) + 2
    for row in range(rows):
        for col in range(cols):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            yield cx, cy, col, row


def _pin(x, y, color=G):
    return (f'<path d="M{x},{y} C{x - 3},{y - 7} {x - 8},{y - 10} {x - 8},{y - 16} '
            f'A8,8 0 1,1 {x + 8},{y - 16} C{x + 8},{y - 10} {x + 3},{y - 7} {x},{y}Z" fill="{color}"/>'
            f'<circle cx="{x}" cy="{y - 16}" r="3" fill="#ffffff"/>')


def _person(x, y, color=R):
    return (f'<circle cx="{x}" cy="{y - 7}" r="3.4" fill="{color}"/>'
            f'<path d="M{x - 5.5},{y + 4} a5.5,6.5 0 0,1 11,0 Z" fill="{color}"/>')


def svg_average():
    cols = [G, GL, R, GT, G, RL, GL, R, G, GT, RL, G, GT, R, GL, G, RL, GT, G, RL, GT, GL, R, G]
    body = ""
    for i, c in enumerate(cols):
        x, y = 34 + (i % 6) * 21, 14 + (i // 6) * 21
        body += f'<rect x="{x}" y="{y}" width="18" height="18" rx="3" fill="{c}"/>'
    body += _arrow(178, 55, 216)
    body += f'<rect x="228" y="14" width="81" height="81" rx="6" fill="#a9c7b5"/>'
    body += (f'<text x="268.5" y="66" text-anchor="middle" font-family="Poppins, sans-serif" '
             f'font-size="30" font-weight="700" fill="#ffffff">x&#772;</text>')
    return _svg(340, 110, body)


def svg_spillover():
    body = ""
    r, cx0, cy0 = 12, 170, 55
    for q in range(-9, 10):
        for rr in range(-4, 5):
            d = (abs(q) + abs(rr) + abs(q + rr)) // 2
            x = cx0 + r * 1.732 * (q + rr / 2)
            y = cy0 + r * 1.5 * rr
            if not (-15 < x < 355 and -15 < y < 125):
                continue
            fill = [R, G, GL, GT][d] if d < 4 else "#f3f8f5"
            body += _hex(x, y, r, fill)
    for rad, op in ((30, 0.55), (52, 0.35), (74, 0.2)):
        body += (f'<circle cx="{cx0}" cy="{cy0}" r="{rad}" fill="none" stroke="{R}" '
                 f'stroke-width="1.6" stroke-dasharray="4 4" opacity="{op}"/>')
    return _svg(340, 110, body)


def svg_misallocation():
    body = f'<circle cx="95" cy="60" r="44" fill="{GT}"/>'
    for x, y in ((80, 50), (97, 44), (113, 53), (86, 68), (104, 70), (72, 84), (120, 86), (95, 90)):
        body += _pin(x, y)
    body += (f'<circle cx="250" cy="60" r="44" fill="{RT}" stroke="{R}" stroke-width="2" '
             f'stroke-dasharray="5 5"/>')
    for x, y in ((230, 48), (250, 42), (270, 48), (222, 72), (242, 68), (262, 70), (280, 74), (250, 90)):
        body += _person(x, y)
    return _svg(340, 110, body)


def svg_aspatial():
    clustered = [G, G, GL, RL, R, G, G, GL, R, R, G, GL, RL, R, R, GL, GL, RL, RL, R]
    shuffled = [R, GL, G, RL, G, RL, G, R, GL, R, GL, R, G, RL, G, R, RL, GL, G, R]
    body = ""
    for ox, cells in ((34, clustered), (218, shuffled)):
        for i, c in enumerate(cells):
            body += f'<rect x="{ox + (i % 5) * 18}" y="{8 + (i // 5) * 15}" width="16" height="13" rx="2" fill="{c}"/>'
        for j, h in enumerate((8, 16, 26, 20, 12, 6)):
            body += f'<rect x="{ox + 2 + j * 14.5}" y="{104 - h}" width="11" height="{h}" rx="1.5" fill="{MUTE}"/>'
    body += _arrow(138, 36, 206)
    body += (f'<path d="M156,26 C166,26 172,46 186,46 M156,46 C166,46 172,26 186,26" '
             f'fill="none" stroke="{MUTE}" stroke-width="2"/>')
    body += (f'<text x="172" y="102" text-anchor="middle" font-family="Poppins, sans-serif" '
             f'font-size="24" font-weight="700" fill="{R}">=</text>')
    return _svg(340, 110, body)


def _slope(cx, cy, deg, color, L=7):
    import math
    a = math.radians(deg)
    return (f'<line x1="{cx - L * math.cos(a):.1f}" y1="{cy + L * math.sin(a):.1f}" '
            f'x2="{cx + L * math.cos(a):.1f}" y2="{cy - L * math.sin(a):.1f}" '
            f'stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>')


def svg_heterogeneous():
    body = ""
    for cx, cy, col, row in _hex_grid(520, 150, 16):
        t = min(max((cx + 0.35 * cy) / 560, 0), 1)       # 0 = west, 1 = east
        deg = 55 - 110 * t
        fill = [G, GL, GT, RT, RL][min(int(t * 5), 4)]
        stroke = GD if deg > 8 else (R if deg < -8 else MUTE)
        body += _hex(cx, cy, 16, fill) + _slope(cx, cy, deg, "#ffffff" if fill in (G,) else stroke)
    return _svg(520, 150, body)


def _hbars(rows, maxv, w=340, row_h=26, label_w=96):
    """Horizontal bar chart: rows = [(label, value, color, value_text)]."""
    h = len(rows) * row_h + 8
    span = w - label_w - 56
    body = ""
    for i, (label, v, color, vt) in enumerate(rows):
        y = 6 + i * row_h
        bw = max(4, span * v / maxv)
        body += (f'<text x="{label_w - 8}" y="{y + 15}" text-anchor="end" font-family="Poppins, sans-serif" '
                 f'font-size="12" font-weight="600" fill="{INK}">{label}</text>'
                 f'<rect x="{label_w}" y="{y + 2}" width="{bw:.1f}" height="{row_h - 8}" rx="4" fill="{color}"/>'
                 f'<text x="{label_w + bw + 6:.1f}" y="{y + 15}" font-family="Poppins, sans-serif" '
                 f'font-size="12" font-weight="700" fill="{INK}">{vt}</text>')
    return _svg(w, h, body)


def svg_multiplier():
    body = ""
    r, cx0, cy0 = 11, 70, 55
    for q in range(-3, 4):
        for rr in range(-3, 4):
            d = (abs(q) + abs(rr) + abs(q + rr)) // 2
            if d > 2:
                continue
            x = cx0 + r * 1.732 * (q + rr / 2)
            y = cy0 + r * 1.5 * rr
            body += _hex(x, y, r, [R, G, GL][d])
    body += _arrow(128, 55, 160)
    body += (f'<rect x="172" y="22" width="70" height="24" rx="4" fill="{MUTE}"/>'
             f'<text x="248" y="39" font-family="Poppins, sans-serif" font-size="13" font-weight="700" fill="{INK}">&#8358;1M</text>'
             f'<rect x="172" y="62" width="128" height="24" rx="4" fill="{G}"/>'
             f'<text x="306" y="79" font-family="Poppins, sans-serif" font-size="13" font-weight="700" fill="{GD}">&#8358;1.82M</text>')
    return _svg(360, 110, body)


def svg_shock():
    body = ""
    for cx, cy, col, row in _hex_grid(360, 120, 12):
        inside = ((cx - 180) / 110) ** 2 + ((cy - 62) / 42) ** 2 < 1
        body += _hex(cx, cy, 12, RL if inside else GT)
    body += (f'<ellipse cx="180" cy="62" rx="118" ry="48" fill="{R}" fill-opacity="0.10" '
             f'stroke="{R}" stroke-width="2" stroke-dasharray="6 5"/>')
    body += (f'<path d="M184,20 L170,58 L184,58 L174,98 L200,50 L186,50 L198,20 Z" fill="{R}" '
             f'stroke="#ffffff" stroke-width="2"/>')
    return _svg(360, 120, body)


def svg_effects():
    return _hbars([("OLS &#946;", 0.39, MUTE, "0.39"),
                   ("Direct", 0.42, G, "0.42"),
                   ("Indirect", 0.31, GL, "0.31"),
                   ("Total", 0.73, GD, "0.73")], 0.73, w=360, row_h=30)


def svg_gwr_coefs():
    return _hbars([("Rural NE", 0.74, G, "0.74"),
                   ("Urban Lagos", 0.09, RL, "0.09"),
                   ("Global OLS", 0.38, MUTE, "0.38")], 0.74, w=360, row_h=30, label_w=104)


def svg_bandwidth():
    return _hbars([("Open defecation", 31, R, "31"),
                   ("Facility density", 124, GL, "124"),
                   ("Climate", 820, G, "820")], 820, w=360, row_h=30, label_w=118)


COLD = "#2b83ba"

# Emerging Hot Spot patterns over 12 time steps: H = hot, C = cold, . = not significant.
# Digits 1-4 are hot bins of rising intensity (used for intensifying / diminishing).
EHSA_PATTERNS = {
    "new": "...........H",
    "consecutive": ".........HHH",
    "intensifying": "111222333444",
    "persistent": "HHHHHHHHHHHH",
    "diminishing": "444333222111",
    "sporadic": ".H..H.H...HH",
    "oscillating": "C.H.C.HC.H.H",
    "historical": "HHHHHHHHHHH.",
}


def svg_ehsa(pattern, cell=14, gap=3):
    body = ""
    for i, ch in enumerate(pattern):
        x = i * (cell + gap)
        if ch == ".":
            fill, op = "#e2e8f0", 1
        elif ch == "C":
            fill, op = COLD, 1
        elif ch in "1234":
            fill, op = R, 0.25 + 0.25 * int(ch)
        else:
            fill, op = R, 1
        body += f'<rect x="{x}" y="0" width="{cell}" height="{cell}" rx="3" fill="{fill}" opacity="{op:.2f}"/>'
    w = len(pattern) * (cell + gap) - gap
    return _svg(w, cell, body)


def svg_cube(layers=4, n=4):
    body = ""
    cw, chh, lh = 16, 9, 20
    ox, oy = 90, 26
    hot = {(3, 1, 1), (3, 1, 2), (3, 2, 1), (2, 1, 1), (3, 0, 3)}
    for t in range(layers):
        for s_ in range(2 * n - 1):
            for i in range(n):
                j = s_ - i
                if not 0 <= j < n:
                    continue
                x = ox + (i - j) * cw
                y = oy + (i + j) * chh + (layers - 1 - t) * lh
                fill = R if (t, i, j) in hot else (RL if t >= 2 and (i + j) in (2, 3) else GT)
                body += (f'<polygon points="{x},{y} {x + cw},{y + chh} {x},{y + 2 * chh} {x - cw},{y + chh}" '
                         f'fill="{fill}" stroke="#ffffff" stroke-width="1.2"/>')
    body += (f'<line x1="170" y1="{oy + 3 * lh + 70}" x2="170" y2="{oy + 8}" stroke="{MUTE}" stroke-width="2"/>'
             f'<polygon points="170,{oy} 164,{oy + 10} 176,{oy + 10}" fill="{MUTE}"/>'
             f'<text x="178" y="{oy + 40}" font-family="Poppins, sans-serif" font-size="12" font-weight="600" fill="{MUTE}">time</text>')
    return _svg(220, 170, body)


def svg_trend():
    import math
    zs = [0.4, 0.9, 0.6, 1.3, 1.1, 1.8, 1.6, 2.2, 2.5, 2.3, 2.9, 3.3]
    x0, y0, w, h = 20, 100, 200, 84
    body = (f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{MUTE}" stroke-width="1.5"/>'
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="{MUTE}" stroke-width="1.5"/>')
    thr = y0 - 1.96 / 3.5 * h
    body += (f'<line x1="{x0}" y1="{thr:.1f}" x2="{x0 + w}" y2="{thr:.1f}" stroke="{R}" stroke-width="1.5" stroke-dasharray="5 4"/>'
             f'<text x="{x0 + w + 4}" y="{thr + 4:.1f}" font-family="Poppins, sans-serif" font-size="11" font-weight="600" fill="{R}">1.96</text>')
    pts = [(x0 + 8 + k * (w - 16) / 11, y0 - z / 3.5 * h) for k, z in enumerate(zs)]
    body += '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{GD}" stroke-width="2.5"/>'
    for (x, y), z in zip(pts, zs):
        body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{R if z > 1.96 else G}"/>'
    return _svg(250, 108, body)


def svg_hot_bin():
    body = ""
    cell, gap = 22, 4
    for layer, (ox, oy, op) in enumerate(((20, 60, 0.55), (74, 34, 0.8), (128, 8, 1.0))):
        for i in range(3):
            for j in range(3):
                centre = (i, j) == (1, 1) and layer == 1
                fill = R if centre else (RL if layer >= 1 else GT)
                body += (f'<rect x="{ox + j * (cell + gap)}" y="{oy + i * (cell + gap)}" width="{cell}" height="{cell}" '
                         f'rx="3" fill="{fill}" opacity="{op}"/>')
    body += (f'<rect x="{74 + cell + gap - 3}" y="{34 + cell + gap - 3}" width="{cell + 6}" height="{cell + 6}" rx="5" '
             f'fill="none" stroke="{INK}" stroke-width="2"/>')
    body += (f'<text x="20" y="150" font-family="Poppins, sans-serif" font-size="11" font-weight="600" fill="{MUTE}">t-1</text>'
             f'<text x="96" y="150" font-family="Poppins, sans-serif" font-size="11" font-weight="600" fill="{MUTE}">t</text>'
             f'<text x="150" y="150" font-family="Poppins, sans-serif" font-size="11" font-weight="600" fill="{MUTE}">t+1</text>')
    return _svg(220, 156, body)


# Emerging Hot Spot legend styles (conventional ArcGIS colours, redrawn as SVG)
EHSA_STYLES = {
    "hot": {
        "new": ("mark", "#e8321e"), "consecutive": ("flat", "#d4805f"), "intensifying": ("glow", "#f03b20", "#e5957a"),
        "persistent": ("flat", "#a0280c"), "diminishing": ("fade", "#fff6ef", "#f4c09c"),
        "sporadic": ("speckle", "#f8cdb2", "#e9a07c"), "oscillating": ("speckle", "#c98f80", "#7f8fb8"),
        "historical": ("flat", "#e4c4a2"),
    },
    "cold": {
        "new": ("mark", "#0b4ea2"), "consecutive": ("flat", "#4a78b0"), "intensifying": ("glow", "#123f8c", "#7ea3d2"),
        "persistent": ("flat", "#0d3566"), "diminishing": ("fade", "#f6f9fd", "#b6cae4"),
        "sporadic": ("speckle", "#c8d8ee", "#8fb0da"), "oscillating": ("speckle", "#a996a4", "#d08a78"),
        "historical": ("flat", "#aec3dc"),
    },
}
EHSA_ORDER = ["new", "consecutive", "intensifying", "persistent", "diminishing", "sporadic", "oscillating", "historical"]


def _ehsa_defs(prefix):
    defs = ""
    for kind, styles in EHSA_STYLES.items():
        for cat, st in styles.items():
            pid = f"{prefix}-{kind}-{cat}"
            if st[0] == "glow":
                defs += (f'<radialGradient id="{pid}"><stop offset="0" stop-color="{st[1]}"/>'
                         f'<stop offset="1" stop-color="{st[2]}"/></radialGradient>')
            elif st[0] == "fade":
                defs += (f'<radialGradient id="{pid}"><stop offset="0.1" stop-color="{st[1]}"/>'
                         f'<stop offset="1" stop-color="{st[2]}"/></radialGradient>')
            elif st[0] == "speckle":
                defs += (f'<pattern id="{pid}" width="6" height="6" patternUnits="userSpaceOnUse">'
                         f'<rect width="6" height="6" fill="{st[1]}"/><circle cx="1.5" cy="1.5" r="1" fill="{st[2]}"/>'
                         f'<circle cx="4.5" cy="4" r="0.9" fill="{st[2]}"/></pattern>')
    return f"<defs>{defs}</defs>"


def _ehsa_fill(prefix, kind, cat):
    st = EHSA_STYLES[kind][cat]
    if st[0] in ("flat",):
        return st[1]
    if st[0] == "mark":
        return "#ffffff"
    return f"url(#{prefix}-{kind}-{cat})"


def svg_ehsa_legend():
    p = "lg"
    body = _ehsa_defs(p)
    names = {k: k.capitalize() for k in EHSA_ORDER}
    for col, kind in enumerate(("hot", "cold")):
        ox = 6 + col * 236
        body += (f'<text x="{ox}" y="14" font-family="Poppins, sans-serif" font-size="13" font-weight="700" '
                 f'fill="{R if kind == "hot" else COLD}">{"Hot" if kind == "hot" else "Cold"} spot patterns</text>')
        for r_, cat in enumerate(EHSA_ORDER):
            y = 26 + r_ * 29
            body += f'<rect x="{ox}" y="{y}" width="24" height="24" rx="3" fill="{_ehsa_fill(p, kind, cat)}" stroke="#cbd5e1"/>'
            if EHSA_STYLES[kind][cat][0] == "mark":
                body += f'<rect x="{ox + 6}" y="{y + 6}" width="12" height="12" fill="{EHSA_STYLES[kind][cat][1]}"/>'
            body += (f'<text x="{ox + 34}" y="{y + 17}" font-family="Poppins, sans-serif" font-size="13.5" '
                     f'font-weight="500" fill="{INK}">{names[cat]} {"Hot" if kind == "hot" else "Cold"} Spot</text>')
    y = 26 + 8 * 29 + 4
    body += (f'<rect x="6" y="{y}" width="24" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1"/>'
             f'<text x="40" y="{y + 17}" font-family="Poppins, sans-serif" font-size="13.5" font-weight="500" '
             f'fill="{MUTE}">No Pattern Detected</text>')
    return _svg(470, y + 30, body)


def svg_ehsa_map():
    p = "mp"
    body = _ehsa_defs(p)
    grid = [
        "   h.     ",
        "  Cc.hi.  ",
        " cCI.o.h  ",
        "iC.o.dHs  ",
        " c.D.s.dP ",
        "  .sHd..n ",
        "   sPhsd  ",
        "    nh.   ",
    ]
    key = {"h": ("hot", "historical"), "i": ("hot", "intensifying"), "c": ("hot", "consecutive"),
           "P": ("hot", "persistent"), "d": ("hot", "diminishing"), "s": ("hot", "sporadic"),
           "o": ("hot", "oscillating"), "n": ("hot", "new"), "H": ("hot", "consecutive"),
           "C": ("cold", "consecutive"), "I": ("cold", "intensifying"), "D": ("cold", "diminishing")}
    # override a few cells for cold variety
    cold_extra = {(3, 0): ("cold", "intensifying"), (4, 1): ("cold", "consecutive"), (2, 3): ("cold", "sporadic"),
                  (1, 2): ("cold", "persistent"), (3, 2): ("cold", "sporadic"), (4, 8): ("cold", "new"),
                  (2, 1): ("cold", "consecutive"), (5, 7): ("cold", "intensifying")}
    cw, chh = 34, 20
    ox, oy = 150, 10
    n = 10
    for s_ in range(2 * n):
        for i in range(n):
            j = s_ - i
            if not 0 <= j < n:
                continue
            row = grid[i] if i < len(grid) else ""
            ch = row[j] if j < len(row) else " "
            x = ox + (j - i) * cw
            y = oy + (i + j) * chh
            if ch == " ":
                continue
            cat = cold_extra.get((i, j)) or key.get(ch)
            fill = "#ffffff" if cat is None else _ehsa_fill(p, *cat)
            body += (f'<polygon points="{x},{y} {x + cw},{y + chh} {x},{y + 2 * chh} {x - cw},{y + chh}" '
                     f'fill="{fill}" stroke="#94a3b8" stroke-width="0.8"/>')
            if cat and EHSA_STYLES[cat[0]][cat[1]][0] == "mark":
                mc = EHSA_STYLES[cat[0]][cat[1]][1]
                body += (f'<polygon points="{x},{y + 8} {x + 14},{y + chh} {x},{y + 2 * chh - 8} {x - 14},{y + chh}" '
                         f'fill="{mc}"/>')
    return _svg(400, 320, body)


def svg_local_outlier():
    body = ""
    for i in range(25):
        x, y = 30 + (i % 5) * 20, 8 + (i // 5) * 19
        fill = G if i == 12 else (RL if i in (6, 7, 8, 11, 13, 16, 17, 18) else RT)
        body += f'<rect x="{x}" y="{y}" width="18" height="17" rx="3" fill="{fill}"/>'
    body += f'<rect x="67" y="44" width="26" height="25" rx="5" fill="none" stroke="{GD}" stroke-width="2.5"/>'
    body += _arrow(146, 55, 186)
    # global boxplot: the local outlier sits inside the box, so it is never flagged
    body += (f'<line x1="206" y1="55" x2="318" y2="55" stroke="{MUTE}" stroke-width="2"/>'
             f'<line x1="206" y1="45" x2="206" y2="65" stroke="{MUTE}" stroke-width="2"/>'
             f'<line x1="318" y1="45" x2="318" y2="65" stroke="{MUTE}" stroke-width="2"/>'
             f'<rect x="238" y="38" width="52" height="34" rx="3" fill="#ffffff" stroke="{MUTE}" stroke-width="2"/>'
             f'<line x1="262" y1="38" x2="262" y2="72" stroke="{MUTE}" stroke-width="2"/>'
             f'<circle cx="276" cy="55" r="6" fill="{G}" stroke="#ffffff" stroke-width="2"/>')
    return _svg(340, 110, body)


def svg_histogram():
    body = ""
    for j, h in enumerate((10, 22, 38, 52, 40, 24, 12)):
        body += f'<rect x="{8 + j * 16}" y="{70 - h}" width="13" height="{h}" rx="2" fill="{MUTE}"/>'
    return _svg(124, 76, body)


def svg_cluster_map():
    body = ""
    for cx, cy, col, row in _hex_grid(124, 76, 9):
        t = ((cx - 30) ** 2 + (cy - 25) ** 2) ** 0.5
        u = ((cx - 98) ** 2 + (cy - 58) ** 2) ** 0.5
        fill = R if t < 16 else (G if u < 16 else "#e2e8f0")
        body += _hex(cx, cy, 9, fill)
    return _svg(124, 76, body)


def svg_blind():
    return _svg(76, 76, f'<path d="M8,38 C22,14 54,14 68,38 C54,62 22,62 8,38Z" fill="none" stroke="{R}" stroke-width="4"/>'
                        f'<circle cx="38" cy="38" r="9" fill="{R}"/>'
                        f'<line x1="14" y1="64" x2="62" y2="12" stroke="{R}" stroke-width="5" stroke-linecap="round"/>')


def svg_unlock():
    return _svg(76, 76, f'<circle cx="32" cy="32" r="20" fill="none" stroke="{G}" stroke-width="5"/>'
                        f'<circle cx="26" cy="28" r="4" fill="{R}"/><circle cx="38" cy="36" r="4" fill="{G}"/>'
                        f'<line x1="47" y1="47" x2="66" y2="66" stroke="{G}" stroke-width="7" stroke-linecap="round"/>')


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dsn_theme_dir = os.path.join(base_dir, "docs", "figures", "dsn_theme")

    # Base64 assets
    logo_b64 = get_b64(os.path.join(dsn_theme_dir, "image7.png"))
    cover_logo_b64 = get_b64(os.path.join(dsn_theme_dir, "image3.png")) or logo_b64
    ending_logo_b64 = get_b64(os.path.join(dsn_theme_dir, "image5.png")) or logo_b64
    bg_content_b64 = get_b64(os.path.join(dsn_theme_dir, "image8.png"))
    bg_cover_b64 = get_b64(os.path.join(dsn_theme_dir, "image2.png"))
    bg_agenda_b64 = get_b64(os.path.join(dsn_theme_dir, "bg_agenda.png"))
    bg_ending_b64 = get_b64(os.path.join(dsn_theme_dir, "image11.png"))

    # Slide images cropped from the project's own analysis figures
    slides_img_dir = os.path.join(dsn_theme_dir, "slides")
    img_deserts = get_b64(os.path.join(slides_img_dir, "q1_health_deserts.jpg"))
    img_retail = get_b64(os.path.join(slides_img_dir, "q2_retail.jpg"))
    img_religious = get_b64(os.path.join(slides_img_dir, "q3_religious.jpg"))
    img_lorenz = get_b64(os.path.join(slides_img_dir, "q4_lorenz.jpg"))
    img_lisa = get_b64(os.path.join(slides_img_dir, "lisa_clusters.jpg"))
    img_moran = get_b64(os.path.join(slides_img_dir, "moran_scatter.jpg"))
    img_gwr_map = get_b64(os.path.join(dsn_theme_dir, "..", "gwr_slope_map.svg"))

    # Official tool logos (Wikimedia Commons, project GitHub repositories, Simple Icons)
    logos_dir = os.path.join(dsn_theme_dir, "logos")
    logo_python = get_b64(os.path.join(logos_dir, "python.svg"))
    logo_pysal = get_b64(os.path.join(logos_dir, "pysal.png"))
    logo_geopandas = get_b64(os.path.join(logos_dir, "geopandas.png"))
    logo_r = get_b64(os.path.join(logos_dir, "r.svg"))
    logo_geoda = get_b64(os.path.join(logos_dir, "geoda.png"))
    logo_arcgis = get_b64(os.path.join(logos_dir, "arcgis.svg"))

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    slide_1 = f"""
            <!-- SLIDE 1: COVER SLIDE -->
            <section class="dsn-cover-slide">
                <div class="dsn-cover-container">
                    <img src="{cover_logo_b64}" alt="Data Science Nigeria" class="dsn-cover-logo">
                    <h1 class="dsn-cover-title">Advanced Spatial Statistics</h1>
                    <h3 class="dsn-cover-subtitle">Theory, Intuition &amp; Spatial Statistics Modeling</h3>
                    <div class="dsn-cover-author">
                        <div class="author-name">Adedoyin S. Ajeyomi</div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 2: AGENDA SLIDE (MATCHING DSN NEW PRESENTATION SLIDES PPTX)
    # =========================================================================
    slide_agenda = f"""
            <!-- SLIDE 2: AGENDA -->
            <section class="dsn-agenda-slide">
                <div class="agenda-items-wrap">
                    <div class="agenda-item-row">
                        <div class="agenda-num-box">01</div>
                        <div class="agenda-text-box">Why Spatial Statistics in the Real World</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">02</div>
                        <div class="agenda-text-box">Exploring Space: ESDA, Moran's I &amp; LISA</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">03</div>
                        <div class="agenda-text-box">Testing &amp; Modelling Spatial Dependence</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">04</div>
                        <div class="agenda-text-box">Space-Time Pattern Mining: Emerging Hot Spots</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">05</div>
                        <div class="agenda-text-box">Tools, Software &amp; Hands-on Notebook Use Cases</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">06</div>
                        <div class="agenda-text-box">Q&amp;A / Open Discussion</div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 3: WHY SPATIAL STATISTICS IN THE REAL WORLD? (THREE MAJOR FALLACIES)
    # =========================================================================
    slide_2 = f"""
            <!-- SLIDE 3: WHY SPATIAL STATISTICS IN THE REAL WORLD? -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Why Spatial Statistics in the Real World?</h2>
                </header>
                <div class="slide-body why-body why-dense">
                    <div class="lead-callout why-lead">
                        <p>Traditional statistical methods and data science pipelines operate under the assumption of <em>independent and identically distributed</em> ($i.i.d.$) observations, the assumption that what happens in one village, ward, or neighborhood is completely independent of its neighbors. In reality, human settlements, economic commerce, disease vectors, and infrastructural access <strong>do not stop at administrative boundaries</strong>.</p>
                        <p>When public institutions and private corporations make strategic decisions based on state or national averages, they fall victim to three major fallacies:</p>
                    </div>

                    <div class="grid-3 why-grid">
                        <div class="card why-card">
                            <div class="viz viz-sm">{svg_average()}</div>
                            <div class="why-head"><div class="why-num">1</div><h4>The Fallacy of the Average</h4></div>
                            <p>A state or province can appear "moderately wealthy" or "well-served by healthcare" on paper, while masking extreme internal inequality, such as affluent metropolitan centers sitting beside vast rural "healthcare deserts" where hundreds of thousands of citizens have zero access to clinics.</p>
                        </div>

                        <div class="card why-card">
                            <div class="viz viz-sm">{svg_spillover()}</div>
                            <div class="why-head"><div class="why-num">2</div><h4>The Spillover Blindspot (Tobler's First Law)</h4></div>
                            <p><em>"Everything is related to everything else, but near things are more related than distant things"</em> (Waldo Tobler, 1970). Investing in a major regional hospital, agricultural market, or road corridor in one ward creates positive spatial externalities (spillovers) across neighboring wards. Standard regressions dismiss this as unexplainable noise; spatial econometrics explicitly models and quantifies it.</p>
                        </div>

                        <div class="card why-card">
                            <div class="viz viz-sm">{svg_misallocation()}</div>
                            <div class="why-head"><div class="why-num">3</div><h4>The Capital Misallocation Trap</h4></div>
                            <p>Deploying bank branches, supermarket retail stores, or drilling water boreholes without spatial intelligence leads to capital waste: saturating already competitive clusters while completely missing high-demand, underserved communities.</p>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 4: THE CORE OBJECTIVE
    # =========================================================================
    slide_objective = f"""
            <!-- SLIDE 4: THE CORE OBJECTIVE -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>The Core Objective</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="lead-callout why-lead">
                        <p>This curriculum bridges the gap between raw <strong>Earth Observation (EO) data</strong> (high-resolution satellite-derived purchasing power, gridded population rasters) and <strong>on-the-ground operational decisions</strong>. Using Nigeria's administrative wards as a worked example, students see how spatial statistics answers critical questions across diverse spheres of national life:</p>
                    </div>

                    <div class="grid-5 why-grid q-grid">
                        <div class="card why-card q-card">
                            <div class="q-img"><img src="{img_deserts}" alt="Healthcare deserts map"></div>
                            <div class="why-num">1</div>
                            <h5>Where are the most urgent healthcare deserts?</h5>
                            <p>(e.g. areas with $&gt;17{{,}}000$ residents and zero registered clinics).</p>
                        </div>
                        <div class="card why-card q-card">
                            <div class="q-img"><img src="{img_retail}" alt="Retail catchment map"></div>
                            <div class="why-num">2</div>
                            <h5>Where are prime, untapped consumer retail catchments?</h5>
                            <p>(e.g. areas with high purchasing power but low commercial market density).</p>
                        </div>
                        <div class="card why-card q-card">
                            <div class="q-img"><img src="{img_religious}" alt="Religious geography map"></div>
                            <div class="why-num">3</div>
                            <h5>How do religious and civic institutions sort geographically?</h5>
                            <p>(Mapping cultural cohesion and Shannon Entropy diversity zones).</p>
                        </div>
                        <div class="card why-card q-card">
                            <div class="q-img"><img src="{img_lorenz}" alt="Lorenz inequality curves"></div>
                            <div class="why-num">4</div>
                            <h5>How unequal is clean water infrastructure?</h5>
                            <p>(Lorenz inequality curves and Gini coefficients).</p>
                        </div>
                        <div class="card why-card q-card">
                            <div class="q-img q-svg">{svg_spillover()}</div>
                            <div class="why-num">5</div>
                            <h5>What is the true economic multiplier of public investments?</h5>
                            <p>(Spatial Lag SAR models decomposing direct vs. indirect spillover effects).</p>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 5: THE SUPERPOWER OF SPATIAL STATISTICS (ESDA)
    # =========================================================================
    slide_superpower = f"""
            <!-- SLIDE 5: THE SUPERPOWER OF SPATIAL STATISTICS -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>The Superpower of Spatial Statistics: Exploratory Spatial Data Analysis (ESDA) for Pattern Discovery</h2>
                </header>
                <div class="slide-body why-body body-2line">
                    <div class="lead-callout why-lead">
                        <p><strong>Why is spatial statistics so exceptionally powerful for exploratory analysis?</strong></p>
                        <p>Traditional non-spatial data exploration relies on summary metrics (mean, median, standard deviation), histograms, and correlation matrices. These tools operate in "feature space" and completely discard geographic coordinates and spatial relationships:</p>
                    </div>

                    <div class="flow">
                        <div class="flow-row">
                            <div class="flow-label">Traditional EDA</div>
                            <div class="flow-box"><span class="flow-chip">[Values]</span></div>
                            <div class="flow-arrow"></div>
                            <div class="flow-box"><div class="flow-viz">{svg_histogram()}</div><span>Summary Stats (Mean, SD)</span></div>
                            <div class="flow-arrow"></div>
                            <div class="flow-box flow-end flow-red"><div class="flow-icon">{svg_blind()}</div><span><strong>BLIND</strong> to geographic arrangement</span></div>
                        </div>
                        <div class="flow-row">
                            <div class="flow-label flow-label-g">Spatial EDA</div>
                            <div class="flow-box"><span class="flow-chip">[Values + Space]</span></div>
                            <div class="flow-arrow flow-arrow-g"></div>
                            <div class="flow-box"><div class="flow-viz">{svg_cluster_map()}</div><span>Moran's I + LISA Maps</span></div>
                            <div class="flow-arrow flow-arrow-g"></div>
                            <div class="flow-box flow-end flow-green"><div class="flow-icon">{svg_unlock()}</div><span><strong>UNLOCKS</strong> hidden clusters &amp; anomalies</span></div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 6: WHAT TRADITIONAL EDA MISSES
    # =========================================================================
    slide_misses = f"""
            <!-- SLIDE 6: WHAT TRADITIONAL EDA MISSES -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>What Traditional Exploratory Data Analysis (EDA) Misses</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="grid-3 why-grid">
                        <div class="card why-card">
                            <div class="viz">{svg_aspatial()}</div>
                            <div class="why-head"><div class="why-num">1</div><h4>Geographic Blindness</h4></div>
                            <p>You can shuffle the locations of 9,308 Nigerian wards randomly across the map, and the dataset's histogram, mean, and standard deviation will remain 100% identical. Traditional EDA cannot tell whether poverty is randomly scattered or concentrated in vast regional belts.</p>
                        </div>
                        <div class="card why-card">
                            <div class="viz">{svg_heterogeneous()}</div>
                            <div class="why-head"><div class="why-num">2</div><h4>Hidden Structural Regimes</h4></div>
                            <p>A single national correlation coefficient ($r = 0.45$) can conceal that the relationship between healthcare facilities and population is strongly positive in the South, but non-existent or reversed in remote Sahelian border areas.</p>
                        </div>
                        <div class="card why-card">
                            <div class="viz">{svg_local_outlier()}</div>
                            <div class="why-head"><div class="why-num">3</div><h4>Inability to Detect Local Spatial Anomalies</h4></div>
                            <p>Standard outlier detection (e.g. Tukey boxplots or $z$-scores $&gt; 3$) only finds values that are globally extreme across the entire country. It completely misses spatial outliers, such as an affluent commercial ward surrounded by severe poverty, or an impoverished rural pocket inside a wealthy metropolitan corridor.</p>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 7: WHAT ESDA UNLOCKS
    # =========================================================================
    slide_unlocks = f"""
            <!-- SLIDE 7: WHAT ESDA UNLOCKS -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>What Exploratory Spatial Data Analysis (ESDA) Unlocks</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="unlock-grid">
                        <div class="card unlock-map"><img src="{img_moran}" alt="Global Moran's I scatterplot of ward wealth"></div>
                        <div class="unlock-list unlock-list-big">
                            <div class="unlock-item">
                                <div class="why-num">1</div>
                                <p><strong>Hypothesis-Free Pattern Discovery:</strong> ESDA allows analysts to detect statistically significant geographic structures before formulating complex parametric equations.</p>
                            </div>
                            <div class="unlock-item">
                                <div class="why-num">2</div>
                                <p><strong>Global Spatial Autocorrelation (Moran's $I$):</strong> Statistically proves whether an observed map pattern is genuine clustering or mere random chance ($p &lt; 0.001$).</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 8: WHAT ESDA UNLOCKS (LOCAL PATTERNS)
    # =========================================================================
    slide_unlocks_2 = f"""
            <!-- SLIDE 8: WHAT ESDA UNLOCKS (LOCAL PATTERNS) -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>What Exploratory Spatial Data Analysis (ESDA) Unlocks</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="unlock-grid">
                        <div class="card unlock-map"><img src="{img_lisa}" alt="Anselin LISA wealth clusters across Nigeria"></div>
                        <div class="unlock-list">
                            <div class="unlock-item">
                                <div class="why-num">3</div>
                                <div>
                                    <p><strong>Local Indicators of Spatial Association (Anselin LISA $I_i$):</strong> Pinpoints the exact coordinates of:</p>
                                    <div class="lisa-rows">
                                        <p><span class="chip chip-hh"></span><strong>Hotspots (HH):</strong> Statistically robust clusters of high values (e.g., concentrated wealth in Lagos and Abuja).</p>
                                        <p><span class="chip chip-ll"></span><strong>Coldspots (LL):</strong> Entrenched structural deprivation zones requiring targeted social interventions.</p>
                                        <p><span class="chip chip-hl"></span><span class="chip chip-lh"></span><strong>Spatial Outliers (HL &amp; LH):</strong> Regional economic engines ("Islands of Wealth") and underserved pockets within affluent zones ("Opportunity Sinks").</p>
                                    </div>
                                </div>
                            </div>
                            <div class="unlock-item">
                                <div class="why-num">4</div>
                                <p><strong>Spatial Heterogeneity &amp; Boundary Regimes:</strong> Reveals non-stationary processes across state borders, river basins, and agro-ecological zones.</p>
                            </div>
                        </div>
                    </div>
                    <div class="in-short">
                        <p>In short, spatial statistics transforms raw geodata into <strong>structured pattern intelligence</strong>, enabling decision-makers to see the structural geography that standard data science leaves invisible.</p>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 9: THE SPATIAL STATISTICS WORKFLOW
    # =========================================================================
    slide_workflow = f"""
            <!-- SLIDE 9: THE SPATIAL STATISTICS WORKFLOW -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>The Spatial Statistics Workflow: Each Step Builds on the Last</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="lead-callout why-lead">
                        <p>Every method depends on the one before it: the neighbourhood matrix $W$ feeds Moran's $I$ and LISA, their results justify moving beyond OLS, and the diagnostics decide which spatial model to fit.</p>
                    </div>
                    <div class="wf-grid">
                        <div class="wf-step">
                            <div class="why-num">1</div>
                            <h5>Neighbourhood ($W$)</h5>
                            <p>Define who is a neighbour: contiguity, distance or k-NN.</p>
                            <code>libpysal</code>
                        </div>
                        <div class="wf-arrow"></div>
                        <div class="wf-step">
                            <div class="why-num">2</div>
                            <h5>Global Moran's $I$</h5>
                            <p>Is there spatial clustering at all? Uses $W$.</p>
                            <code>esda</code>
                        </div>
                        <div class="wf-arrow"></div>
                        <div class="wf-step">
                            <div class="why-num">3</div>
                            <h5>Anselin LISA ($I_i$)</h5>
                            <p>Where are the hotspots, coldspots &amp; outliers?</p>
                            <code>esda</code>
                        </div>
                        <div class="wf-arrow"></div>
                        <div class="wf-step">
                            <div class="why-num">4</div>
                            <h5>OLS Baseline</h5>
                            <p>Aspatial model; test its residuals with Moran's $I$ &amp; LM tests.</p>
                            <code>spreg</code>
                        </div>
                        <div class="wf-arrow"></div>
                        <div class="wf-step">
                            <div class="why-num">5</div>
                            <h5>SAR / SEM / SDM</h5>
                            <p>Diagnostics pick the model: contagion, hidden shocks or both.</p>
                            <code>spreg</code>
                        </div>
                        <div class="wf-arrow"></div>
                        <div class="wf-step">
                            <div class="why-num">6</div>
                            <h5>GWR / MGWR</h5>
                            <p>Let each coefficient vary across space and scale.</p>
                            <code>mgwr</code>
                        </div>
                        <div class="wf-arrow"></div>
                        <div class="wf-step">
                            <div class="why-num">7</div>
                            <h5>Spatio-Temporal Models</h5>
                            <p>Add time: how clusters and effects evolve across years.</p>
                            <code>giddy</code>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 10: SPATIAL DEPENDENCE TESTING TOOLKIT
    # =========================================================================
    slide_models = f"""
            <!-- SLIDE 10: SPATIAL DEPENDENCE TESTING TOOLKIT -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Checking Spatial Dependence: The Testing Toolkit</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="tk-legend">
                        <span class="tk-key tk-key-global">Global: one answer for the whole map</span>
                        <span class="tk-key tk-key-local">Local: one answer per location</span>
                        <span class="tk-key tk-key-model">Model diagnostics</span>
                    </div>
                    <div class="tk-grid">
                        <div class="tk-card tk-global">
                            <div class="tk-top"><div class="why-num">1</div><h5>Global Moran's $I$</h5></div>
                            <p>Is there clustering anywhere on the map?</p>
                            <code>esda.Moran</code>
                        </div>
                        <div class="tk-card tk-global">
                            <div class="tk-top"><div class="why-num">2</div><h5>Geary's $C$</h5></div>
                            <p>Are neighbours similar? More sensitive to local differences.</p>
                            <code>esda.Geary</code>
                        </div>
                        <div class="tk-card tk-global">
                            <div class="tk-top"><div class="why-num">3</div><h5>Getis-Ord General $G$</h5></div>
                            <p>Is it the <strong>high</strong> or the <strong>low</strong> values that cluster?</p>
                            <code>esda.G</code>
                        </div>
                        <div class="tk-card tk-global">
                            <div class="tk-top"><div class="why-num">4</div><h5>Join Counts</h5></div>
                            <p>Do categories cluster? (urban / rural, has clinic / none)</p>
                            <code>esda.Join_Counts</code>
                        </div>
                        <div class="tk-card tk-local">
                            <div class="tk-top"><div class="why-num">5</div><h5>Anselin LISA ($I_i$)</h5></div>
                            <p>Where are the hotspots, coldspots &amp; outliers?</p>
                            <code>esda.Moran_Local</code>
                        </div>
                        <div class="tk-card tk-local">
                            <div class="tk-top"><div class="why-num">6</div><h5>Getis-Ord $G_i^*$</h5></div>
                            <p>Where are statistically hot and cold spots?</p>
                            <code>esda.G_Local</code>
                        </div>
                        <div class="tk-card tk-local">
                            <div class="tk-top"><div class="why-num">7</div><h5>Bivariate LISA</h5></div>
                            <p>Does <em>X</em> around me relate to <em>Y</em> here?</p>
                            <code>esda.Moran_Local_BV</code>
                        </div>
                        <div class="tk-card tk-local">
                            <div class="tk-top"><div class="why-num">8</div><h5>Local Geary</h5></div>
                            <p>Where are neighbours unusually alike on many variables?</p>
                            <code>esda.Geary_Local</code>
                        </div>
                        <div class="tk-card tk-model">
                            <div class="tk-top"><div class="why-num">9</div><h5>Residual Moran's $I$ + LM tests</h5></div>
                            <p>Did OLS leave spatial structure? LM-lag vs LM-error picks SAR, SEM or SDM.</p>
                            <code>spreg.OLS(spat_diag=True)</code>
                        </div>
                    </div>
                    <div class="in-short">
                        <p><strong>Rule of thumb:</strong> test globally first (is there dependence?), then locally (where is it?), then fit OLS and read the residual diagnostics to choose the spatial model.</p>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 10: SPATIAL LAG MODEL (SAR): MODELING CONTAGION & PEER EFFECTS
    # =========================================================================
    slide_sar = f"""
            <!-- SLIDE 10: Spatial Lag Model (SAR): Modeling Contagion &amp; Peer Effects -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Spatial Lag Model (SAR): Modeling Contagion &amp; Peer Effects</h2>
                </header>
                <div class="slide-body why-body model-body">
                    <div class="model-top">
                        <div class="model-when">
                            <div class="fallacy-label">When to use</div>
                            <p>The outcome in each location is <em>directly caused</em> by outcomes in neighbouring locations: contagion, diffusion, peer pressure, or market competition.</p>
                        </div>
                        <div class="model-eq">
                            <div class="fallacy-label">The model</div>
                            <div class="eq">$$y = \\rho W y + X\\beta + \\varepsilon$$</div>
                        </div>
                    </div>
                    <div class="model-bottom">
                        <div class="card why-card model-viz">
                            <div class="viz viz-model">{svg_multiplier()}</div>
                            <p><strong>How it solves it:</strong> SAR adds the neighbours' outcome ($Wy$) to the model and measures its pull with $\\rho$. If $\\rho = 0.45$, every local change is multiplied by $\\frac{{1}}{{1-\\rho}} = 1.82$ once the ripple through neighbours is counted.</p>
                        </div>
                        <div class="card why-card model-ex">
                            <div class="fallacy-label">Illustrative examples (numbers are hypothetical)</div>
                            <div class="ex-row"><div class="why-num">1</div><p><strong>Retail:</strong> a campaign at one store also lifts sales at nearby stores. With $\\rho = 0.45$, &#8358;1M of direct sales would become about &#8358;1.82M across the area.</p></div>
                            <div class="ex-row"><div class="why-num">2</div><p><strong>Disease spread:</strong> more malaria in one district raises malaria next door, because people share markets and travel routes.</p></div>
                            <div class="ex-row"><div class="why-num">3</div><p><strong>Crime:</strong> a police crackdown in one area pushes crime into the neighbouring areas.</p></div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 11: SPATIAL ERROR MODEL (SEM): CORRECTING FOR INVISIBLE REGIONAL SHOCKS
    # =========================================================================
    slide_sem = f"""
            <!-- SLIDE 11: Spatial Error Model (SEM): Correcting for Invisible Regional Shocks -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Spatial Error Model (SEM): Correcting for Invisible Regional Shocks</h2>
                </header>
                <div class="slide-body why-body model-body">
                    <div class="model-top">
                        <div class="model-when">
                            <div class="fallacy-label">When to use</div>
                            <p>The outcome is <em>not</em> contagious, but unmeasured regional forces (climate, soil, governance) hit clusters of adjacent units at once, making their errors correlated.</p>
                        </div>
                        <div class="model-eq">
                            <div class="fallacy-label">The model</div>
                            <div class="eq">$$y = X\\beta + u, \\quad u = \\lambda W u + \\varepsilon$$</div>
                        </div>
                    </div>
                    <div class="model-bottom">
                        <div class="card why-card model-viz">
                            <div class="viz viz-model">{svg_shock()}</div>
                            <p><strong>How it solves it:</strong> SEM lets the model's errors move together across neighbours ($\\lambda$). If $\\lambda = 0.6$, most of what the model misses is shared with neighbours; SEM separates it out, so the $p$-values become honest again.</p>
                        </div>
                        <div class="card why-card model-ex">
                            <div class="fallacy-label">Illustrative examples (numbers are hypothetical)</div>
                            <div class="ex-row"><div class="why-num">1</div><p><strong>Farming:</strong> the model leaves out soil quality, and good soil comes in patches, so neighbouring farms are all over- or under-predicted together.</p></div>
                            <div class="ex-row"><div class="why-num">2</div><p><strong>Health:</strong> OLS says clinic distance is highly significant, but its errors are clustered (e.g. residual Moran\'s $I = 0.42$). Once SEM accounts for the shared regional factor, the effect may no longer be significant.</p></div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 12: SPATIAL DURBIN MODEL (SDM): CAPTURING BOTH OUTCOME & CONTEXT SPILLOVERS
    # =========================================================================
    slide_sdm = f"""
            <!-- SLIDE 12: Spatial Durbin Model (SDM): Capturing Both Outcome &amp; Context Spillovers -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Spatial Durbin Model (SDM): Capturing Both Outcome &amp; Context Spillovers</h2>
                </header>
                <div class="slide-body why-body model-body">
                    <div class="model-top">
                        <div class="model-when">
                            <div class="fallacy-label">When to use</div>
                            <p>The outcome spreads to neighbours (like SAR) <em>and</em> your neighbours' own characteristics (investment, wealth, education) directly affect your outcome.</p>
                        </div>
                        <div class="model-eq">
                            <div class="fallacy-label">The model</div>
                            <div class="eq">$$y = \\rho W y + X\\beta + W X\\theta + \\varepsilon$$</div>
                        </div>
                    </div>
                    <div class="model-bottom">
                        <div class="card why-card model-viz">
                            <div class="viz viz-model">{svg_effects()}</div>
                            <p><strong>How it solves it:</strong> SDM reports the effect in <strong>your</strong> area (direct) and in the <strong>neighbouring</strong> areas (indirect); together they give the <strong>total</strong> effect. The bars show example values.</p>
                        </div>
                        <div class="card why-card model-ex">
                            <div class="fallacy-label">Illustrative examples (numbers are hypothetical)</div>
                            <div class="ex-row"><div class="why-num">1</div><p><strong>Hospitals:</strong> a new hospital lowers child deaths in its own district (direct, e.g. 0.42) and in nearby districts whose families travel there (spillover, e.g. 0.31). OLS would show only about 0.39, about half the total.</p></div>
                            <div class="ex-row"><div class="why-num">2</div><p><strong>Safe default:</strong> if you are unsure whether SAR or SEM fits, start with SDM. It contains both and stays reliable when some spatial factors are missing (LeSage &amp; Pace, 2009).</p></div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 13: GWR & MGWR
    # =========================================================================
    slide_gwr = f"""
            <!-- SLIDE 13: LOCAL REGRESSION: GWR & MGWR -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Local Regression: GWR &amp; MGWR</h2>
                </header>
                <div class="slide-body why-body gwr2-body">
                    <div class="gwr2-grid">
                        <div class="gwr2-compare">
                            <div class="gwr2-card gwr2-ols">
                                <div class="fallacy-label">Traditional regression (OLS)</div>
                                <p><strong>One equation for the whole map</strong>, so one slope applies everywhere.</p>
                                <div class="eq">$y = \\beta_0 + \\beta_1 x + \\varepsilon$</div>
                                <p class="gwr2-result">Course result: one national slope, $R^2 = 0.13$</p>
                            </div>
                            <div class="gwr2-card gwr2-gwr">
                                <div class="fallacy-label">Geographically weighted regression (GWR)</div>
                                <p><strong>One equation per place</strong>, fitted with nearby places weighted more than distant ones.</p>
                                <div class="eq">$y_i = \\beta_0(u_i,v_i) + \\sum_k \\beta_k(u_i,v_i)\\,x_{{ik}} + \\varepsilon_i$</div>
                                <p class="gwr2-result">Course result: bandwidth 48 LGAs, $R^2 = 0.57$, AICc 2091 &rarr; 1830</p>
                            </div>
                            <div class="gwr2-mgwr"><strong>MGWR</strong> goes one step further: each variable gets its own bandwidth (village, regional or national scale).</div>
                        </div>
                        <div class="card why-card gwr2-map">
                            <div class="fallacy-label">Course result: local slope of purchasing power &rarr; schools per 10k people</div>
                            <img src="{img_gwr_map}" alt="GWR local slope map across Nigerian LGAs">
                            <div class="gwr2-legend">
                                <span><i style="background:#ed3237"></i>negative</span>
                                <span><i style="background:#fbc9ca"></i><i style="background:#c9ecd9"></i>weak</span>
                                <span><i style="background:#00a859"></i>positive</span>
                                <span><i class="gwr2-outline"></i>significant (48 LGAs)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 15: SPACE-TIME PATTERN MINING (ARCGIS PRO)
    # =========================================================================
    slide_spacetime = f"""
            <!-- SLIDE 15: SPACE-TIME PATTERN MINING -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Space-Time Pattern Mining: Emerging Hot Spot Analysis</h2>
                </header>
                <div class="slide-body why-body st-body">
                    <div class="st-strip">
                        <div class="st-chip"><div class="why-num">1</div><div><strong>Create Space Time Cube</strong><span class="st-sub">Bin values by location &times; time step</span></div></div>
                        <div class="pick-arrow"></div>
                        <div class="st-chip"><div class="why-num">2</div><div><strong>Getis-Ord $G_i^*$ per bin</strong><span class="st-sub">Compare each bin with its space-time neighbours</span></div></div>
                        <div class="pick-arrow"></div>
                        <div class="st-chip"><div class="why-num">3</div><div><strong>Mann-Kendall trend</strong><span class="st-sub">Is each location intensifying or diminishing?</span></div></div>
                    </div>
                    <div class="st-main">
                        <div class="card why-card st-legend">{svg_ehsa_legend()}</div>
                        <div class="card why-card st-map">{svg_ehsa_map()}</div>
                    </div>
                    <div class="in-short st-short">
                        <p><strong>Reading the map:</strong> New, consecutive &amp; intensifying = <strong>emerging, act early</strong>. Persistent = <strong>structural</strong>. Diminishing &amp; historical = <strong>cooling</strong>. ArcGIS Pro: <code>arcpy.stpm</code> &middot; R: <code>sfdep</code>.</p>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 16: TOOLS, SOFTWARE & PYTHON LIBRARIES
    # =========================================================================
    slide_tools = f"""
            <!-- SLIDE 16: TOOLS, SOFTWARE & PYTHON LIBRARIES -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Tools, Software &amp; Libraries for Spatial Statistics</h2>
                </header>
                <div class="slide-body why-body">
                    <div class="tools-grid">
                        <div class="card why-card tool-col">
                            <div class="tool-head"><img src="{logo_python}" alt="Python"><h4>Python</h4><img src="{logo_pysal}" alt="PySAL" class="tool-head-right"><span class="tool-tag">PySAL ecosystem</span></div>
                            <div class="tool-row">
                                <div class="tool-pkgs">
                                    <p><code>libpysal</code> Spatial weights $W$ (contiguity, distance, k-NN)</p>
                                    <p><code>esda</code> Moran's $I$, LISA, Getis-Ord $G_i^*$</p>
                                    <p><code>spreg</code> OLS diagnostics, SAR, SEM, SDM</p>
                                    <p><code>mgwr</code> GWR &amp; MGWR</p>
                                    <p><code>splot</code> Moran scatterplots &amp; LISA maps</p>
                                    <p><code>giddy</code> Space-time dynamics (spatial Markov, LISA over time)</p>
                                </div>
                            </div>
                            <div class="tool-row">
                                <img src="{logo_geopandas}" alt="GeoPandas">
                                <p><strong>GeoPandas</strong> Ward boundaries, spatial joins &amp; choropleth maps (with <code>rasterio</code> / <code>rasterstats</code> for satellite rasters)</p>
                            </div>
                        </div>

                        <div class="card why-card tool-col">
                            <div class="tool-head"><img src="{logo_r}" alt="R"><h4>R</h4></div>
                            <div class="tool-list">
                                <p><code>sf</code> Spatial vector data &amp; mapping</p>
                                <p><code>spdep</code> Weights, Moran's $I$, LISA</p>
                                <p><code>spatialreg</code> SAR, SEM, SDM &amp; impacts</p>
                                <p><code>GWmodel</code> GWR &amp; multiscale GWR</p>
                                <p><code>CARBayesST</code> Spatio-temporal areal models</p>
                            </div>
                        </div>

                        <div class="card why-card tool-col">
                            <div class="tool-head"><h4>Desktop GIS</h4></div>
                            <div class="tool-row">
                                <img src="{logo_arcgis}" alt="ArcGIS Pro">
                                <p><strong>ArcGIS Pro</strong> Spatial Statistics toolbox: Hot Spots, Cluster &amp; Outlier, GWR, Space-Time Cube</p>
                            </div>
                            <div class="tool-list">
                                <p><code>arcpy.stats</code> Spatial Statistics tools in Python</p>
                                <p><code>arcgis</code> ArcGIS API for Python</p>
                            </div>
                            <div class="tool-row">
                                <img src="{logo_geoda}" alt="GeoDa">
                                <p><strong>GeoDa</strong> Free point-and-click ESDA &amp; LISA maps</p>
                            </div>
                        </div>
                    </div>
                    <div class="in-short">
                        <p>The course notebooks run on <strong>free, open-source Python</strong>: <code>geopandas</code>, <code>libpysal</code>, <code>esda</code>, <code>spreg</code> and <code>splot</code>. The same analyses are available in ArcGIS Pro.</p>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 37: DSN ENDING SLIDE (THANK YOU / Q&A)
    # =========================================================================
    slide_ending = f"""
            <!-- SLIDE 37: DSN ENDING SLIDE -->
            <section class="dsn-ending-slide">
                <div class="dsn-ending-container">
                    <img src="{ending_logo_b64}" class="dsn-ending-logo" alt="DSN Logo">
                    <h1 class="dsn-ending-title">Thank you</h1>
                    <h2 class="dsn-ending-subtitle">Q&amp;A / Open Discussion</h2>
                </div>
            </section>
"""

    all_slides_combined = slide_1 + slide_agenda + slide_2 + slide_objective + slide_superpower + slide_misses + slide_unlocks + slide_unlocks_2 + slide_workflow + slide_models + slide_sar + slide_sem + slide_sdm + slide_gwr + slide_spacetime + slide_tools + slide_ending

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Spatial Statistics | Adedoyin S. Ajeyomi</title>
    <meta name="description" content="Advanced Spatial Statistics by Adedoyin S. Ajeyomi">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://sammygis.github.io/dsn_advanced_spatial_stats/">
    <meta property="og:title" content="Advanced Spatial Statistics | Adedoyin S. Ajeyomi">
    <meta property="og:description" content="Advanced Spatial Statistics by Adedoyin S. Ajeyomi">
    <meta property="og:image" content="https://sammygis.github.io/dsn_advanced_spatial_stats/figures/dsn_theme/og_preview.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://sammygis.github.io/dsn_advanced_spatial_stats/figures/dsn_theme/og_preview.png">
    <link rel="icon" type="image/png" href="figures/dsn_theme/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/white.min.css">
    <!-- KaTeX Formulas for crisp mathematical precision -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {{
            --text-dark: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --primary: #0284c7;
            --primary-dark: #0369a1;
            --dsn-green: #00a859;
            --dsn-green-dark: #007f43;
            --dsn-green-light: #e3f5ec;
            --dsn-green-tint: #eef9f3;
            --dsn-green-line: #c4e9d5;
            --dsn-red: #ed3237;
            --dsn-red-tint: #fdf0f0;
            --dsn-red-line: #f8cfd0;
            --border: #e2e8f0;
            --card-bg: #ffffff;
            --sidebar-width: 270px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body, html {{
            height: 100%;
            width: 100%;
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff;
            color: var(--text-dark);
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }}

        /* ========================================================= */
        /* PORTAL WRAPPER & SIDEBAR */
        /* ========================================================= */
        .portal-layout {{
            display: flex;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            position: relative;
        }}

        .portal-sidebar {{
            width: var(--sidebar-width);
            min-width: var(--sidebar-width);
            height: 100vh;
            background: #ffffff;
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            z-index: 1000;
            transition: margin-left 0.25s ease;
            box-shadow: 2px 0 8px rgba(0, 0, 0, 0.03);
        }}

        .portal-sidebar.collapsed {{
            margin-left: calc(-1 * var(--sidebar-width));
        }}

        .sidebar-brand {{
            padding: 16px 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--border);
            background: #ffffff;
        }}

        .brand-logo {{
            height: 38px;
            width: auto;
            max-width: 80px;
            object-fit: contain;
            display: block;
        }}

        .brand-title-wrap {{
            display: flex;
            flex-direction: column;
        }}

        .brand-name {{
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-dark);
            line-height: 1.2;
        }}

        .brand-badge {{
            font-size: 11px;
            font-weight: 600;
            color: var(--dsn-green);
        }}

        .sidebar-menu {{
            flex: 1;
            padding: 12px 10px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .menu-heading {{
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            padding: 10px 8px 4px 8px;
            margin-top: 4px;
        }}

        .nav-link-btn {{
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
            padding: 8px 12px;
            border: 1px solid transparent;
            border-radius: 8px;
            background: transparent;
            color: var(--text-secondary);
            font-family: 'Poppins', sans-serif;
            font-size: 12px;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.15s ease;
        }}

        .nav-link-btn:hover {{
            background: #f8fafc;
            color: var(--text-dark);
            border-color: #e2e8f0;
        }}

        .nav-link-btn.active {{
            background: var(--dsn-green-light);
            color: var(--dsn-green-dark);
            font-weight: 600;
            border-color: #c8e6c9;
        }}

        .nav-icon {{
            font-size: 15px;
            width: 18px;
            text-align: center;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .github-btn {{
            margin-top: 4px;
            color: #0f172a;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
        }}

        .github-btn:hover {{
            background: #f1f5f9;
            border-color: #cbd5e1;
        }}

        .sidebar-footer {{
            padding: 12px 16px;
            border-top: 1px solid var(--border);
            font-size: 11px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .collapse-toggle-btn {{
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 11.5px;
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 4px;
        }}

        .collapse-toggle-btn:hover {{
            background: #f1f5f9;
            color: var(--text-dark);
        }}

        /* ========================================================= */
        /* MAIN WORKSPACE */
        /* ========================================================= */
        .portal-main {{
            flex: 1;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: #ffffff;
            position: relative;
        }}

        .portal-topbar {{
            height: 44px;
            min-height: 44px;
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            z-index: 50;
        }}

        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .sidebar-btn {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11.5px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .sidebar-btn:hover {{
            background: #f1f5f9;
            color: var(--text-dark);
        }}

        .view-title {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text-dark);
        }}

        .topbar-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .fullscreen-btn {{
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11.5px;
            font-family: 'Poppins', sans-serif;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .fullscreen-btn:hover {{
            background: #f8fafc;
            color: var(--text-dark);
        }}

        .portal-viewport {{
            flex: 1;
            position: relative;
            height: calc(100vh - 44px);
            overflow: hidden;
            background: #f1f5f9;
        }}

        .slides-view {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: block;
            background: #f1f5f9;
        }}

        .tech-notes-view {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            overflow-y: auto;
            background: #ffffff;
            padding: 24px 32px;
        }}

        .doc-frame {{
            width: 100%;
            height: 100%;
            border: none;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            background: #ffffff;
        }}

        /* ========================================================= */
        /* REVEAL.JS PRESENTATION STYLES - SLIDE TEMPLATE MATCH */
        /* ========================================================= */
        .reveal {{
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f1f5f9;
            color: var(--text-dark);
            height: 100% !important;
            width: 100% !important;
        }}

        .reveal .slides {{
            text-align: left;
        }}

        .reveal .slides section {{
            top: 0 !important;
            padding: 24px 40px 48px 40px !important;
            box-sizing: border-box;
            overflow: hidden !important;
            height: 100% !important;
            border-radius: 6px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: none !important;
        }}

        /* Permanent Base64 16:9 DSN Backgrounds */
        .reveal .slides section.dsn-cover-slide {{
            background: #ffffff url('{bg_cover_b64}') no-repeat center center / 100% 100% !important;
        }}

        .reveal .slides section.dsn-agenda-slide {{
            background: #ffffff url('{bg_agenda_b64}') no-repeat center center / 100% 100% !important;
            padding: 0 !important;
            position: relative !important;
        }}

        /* Agenda Slide Elements - Matching DSN New Presentation Slides PPTX */
        .agenda-items-wrap {{
            position: absolute;
            top: 13.5%;
            left: 43.6%;
            width: 52%;
            height: 73%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .agenda-item-row {{
            display: flex;
            align-items: center;
            gap: 24px;
        }}

        .agenda-num-box {{
            width: 50px;
            height: 44px;
            background: var(--dsn-red);
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
            font-size: 0.46em;
            font-weight: 700;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 4px 14px rgba(255, 0, 0, 0.28);
            letter-spacing: -0.01em;
        }}

        .agenda-text-box {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.46em;
            font-weight: 500;
            color: #0f172a;
            line-height: 1.25;
            letter-spacing: -0.01em;
        }}

        .agenda-row-divider {{
            width: 96%;
            height: 1px;
            background: #e2e8f0;
            margin-left: 74px;
        }}

        .reveal .slides section.dsn-content-slide {{
            background: #ffffff url('{bg_content_b64}') no-repeat center center / 100% 100% !important;
        }}

        .reveal .slides section.dsn-ending-slide {{
            background: #ffffff url('{bg_ending_b64}') no-repeat center center / 100% 100% !important;
        }}

        /* Slide Container: Fills canvas but leaves breathing room above DSN footer */
        .slide-container, .slide-body {{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 8px;
            max-height: 610px;
            overflow: hidden;
            position: relative;
        }}

        /* DSN Header Logo - Top-Right */
        .dsn-header-logo {{
            position: absolute;
            top: 18px;
            right: 32px;
            width: 80px;
            height: auto;
            z-index: 50;
            pointer-events: none;
            display: block;
        }}

        /* Clean Slide Header - NO PILL TAGS / NO COLORED BACKGROUND BANNERS */
        .slide-header {{
            margin-bottom: 7px;
            padding-bottom: 2px;
            max-width: 1060px;
        }}

        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {{
            font-family: 'Poppins', sans-serif;
            color: var(--text-dark);
            text-transform: none;
        }}

        .reveal h1 {{
            font-size: 1.50em;
            line-height: 1.15;
            font-weight: 700;
        }}

        /* Smart, refined Title - NO WRAPPING OVERFLOW */
        .reveal h2 {{
            font-size: 0.86em !important;
            line-height: 1.25 !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: left !important;
            border: none !important;
        }}

        .reveal h3 {{
            font-size: 0.68em !important;
            color: var(--primary) !important;
            font-weight: 600 !important;
            margin: 2px 0 4px 0 !important;
        }}

        .reveal h4 {{
            font-size: 0.54em !important;
            color: var(--text-dark) !important;
            font-weight: 600 !important;
            margin: 0 0 3px 0 !important;
        }}

        .reveal p, .reveal li {{
            font-size: 0.36em !important;
            line-height: 1.38 !important;
            color: var(--text-secondary) !important;
        }}

        .reveal ul {{
            margin-left: 16px;
            margin-bottom: 4px;
        }}

        .reveal li {{
            margin-bottom: 3px;
        }}

        /* Clean Smart Lead Box - NO COLORED VERTICAL BARS */
        .lead-callout {{
            background: linear-gradient(90deg, var(--dsn-green-tint) 0%, #ffffff 55%, var(--dsn-red-tint) 100%);
            border: 1px solid var(--dsn-green-line);
            border-radius: 8px;
            padding: 7px 11px;
            margin-bottom: 7px;
        }}

        .lead-callout p {{
            font-size: 0.37em !important;
            line-height: 1.38 !important;
            color: #1e293b !important;
        }}

        /* Clean Smart Cards - PURE WHITE, SOFT 1PX BORDER, ZERO COLORED BARS */
        .card {{
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        }}

        .card-rose, .card-blue, .card-amber, .card-teal, .card-emerald, .card-purple, .card-cyan {{
            border: 1px solid #e2e8f0 !important;
        }}

        .callout, .concept-card {{
            background: var(--dsn-green-tint) !important;
            border: 1px solid var(--dsn-green-line) !important;
            border-radius: 8px !important;
            padding: 6px 10px !important;
        }}

        /* Alternate DSN green / red tints for side-by-side boxes */
        .grid-2 > .callout:nth-child(even), .grid-3 > .callout:nth-child(even),
        .grid-4 > .callout:nth-child(even) {{
            background: var(--dsn-red-tint) !important;
            border-color: var(--dsn-red-line) !important;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            flex: 1;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }}

        /* Monospace diagram comparison strip */
        .diagram-strip {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            background: var(--dsn-green-tint);
            border: 1px solid var(--dsn-green-line);
            border-radius: 8px;
            padding: 7px 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.42em;
            color: #1e293b;
            margin-bottom: 6px;
        }}

        .formula-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.44em;
            line-height: 1.4;
            color: #1e293b;
            margin: 4px 0;
        }}

        .tech-note-ref {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 0.38em;
            color: #6d28d9;
            background: #f5f3ff;
            border: 1px solid #ddd6fe;
            border-radius: 4px;
            padding: 2px 7px;
            margin-top: 4px;
            cursor: pointer;
            text-decoration: none;
            font-weight: 500;
        }}

        .tech-note-ref:hover {{
            background: #ede9fe;
            color: #5b21b6;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.40em;
            margin-top: 4px;
        }}

        th {{
            background: var(--dsn-green-tint);
            color: var(--text-dark);
            font-weight: 600;
            padding: 3px 5px;
            border-bottom: 1.5px solid var(--border);
            text-align: left;
        }}

        td {{
            padding: 2px 5px;
            border-bottom: 1px solid var(--border);
            color: var(--text-secondary);
        }}

        tr:nth-child(even) td {{
            background: #fafdfa;
        }}

        /* DSN Cover Slide */
        .dsn-cover-container {{
            max-width: 660px;
            padding-left: 20px;
            padding-top: 20px;
        }}

        .dsn-cover-logo {{
            height: 48px;
            width: auto;
            object-fit: contain;
            margin-bottom: 12px;
            display: block;
        }}

        .dsn-cover-title {{
            font-size: 1.30em !important;
            font-weight: 700 !important;
            line-height: 1.18 !important;
            color: #0f172a;
            margin-bottom: 6px !important;
        }}

        .reveal h3.dsn-cover-subtitle,
        .dsn-cover-subtitle {{
            font-size: 0.65em !important;
            font-weight: 600 !important;
            color: var(--dsn-green) !important;
            margin-bottom: 14px !important;
        }}

        .dsn-cover-author {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            margin-top: 10px;
        }}

        .author-name {{
            font-size: 0.48em !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            letter-spacing: -0.01em;
        }}

        .author-org {{
            font-size: 0.38em !important;
            font-weight: 500 !important;
            color: #64748b !important;
        }}

        /* DSN Ending Slide */
        .dsn-ending-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 640px;
            text-align: center;
            position: relative;
        }}

        .dsn-ending-logo {{
            position: absolute;
            top: 24px;
            right: 32px;
            width: 120px;
            height: auto;
            display: block;
        }}

        .dsn-ending-title {{
            font-size: 2.6em !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-bottom: 6px !important;
        }}

        .dsn-ending-subtitle {{
            font-size: 1.25em !important;
            font-weight: 600 !important;
            color: #86efac !important;
            margin-bottom: 24px !important;
        }}

        .dsn-ending-card {{
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 20px 32px;
            max-width: 720px;
        }}

        .dsn-ending-links {{
            display: flex;
            gap: 16px;
            justify-content: center;
            font-size: 0.55em;
            color: #e2e8f0;
        }}

        /* ========================================================= */
        /* REVEAL NAVIGATION CONTROLS - SEPARATED (LEFT & RIGHT)     */
        /* ========================================================= */
        .reveal .controls {{
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100% !important;
            height: 100% !important;
            pointer-events: none !important;
            z-index: 999 !important;
            display: block !important;
        }}

        .reveal .controls button {{
            pointer-events: auto !important;
            opacity: 0.65 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            background: rgba(255, 255, 255, 0.90) !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 6px !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        .reveal .controls button.enabled {{
            opacity: 0.95 !important;
        }}

        .reveal .controls button:hover {{
            opacity: 1 !important;
            background: #ffffff !important;
            border-color: #0284c7 !important;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25) !important;
        }}

        /* Left-facing arrow moved to bottom-left corner */
        .reveal .controls .navigate-left {{
            position: absolute !important;
            bottom: 14px !important;
            left: 24px !important;
            top: auto !important;
            right: auto !important;
            width: 36px !important;
            height: 36px !important;
            transform: none !important;
        }}

        /* Right-facing arrow in bottom-right corner */
        .reveal .controls .navigate-right {{
            position: absolute !important;
            bottom: 14px !important;
            right: 24px !important;
            top: auto !important;
            left: auto !important;
            width: 36px !important;
            height: 36px !important;
            transform: none !important;
        }}

        /* Hide vertical controls */
        .reveal .controls .navigate-up,
        .reveal .controls .navigate-down {{
            display: none !important;
        }}

        /* Slide Number placement: bottom-right, just inside right arrow */
        .reveal .slide-number {{
            right: 68px !important;
            left: auto !important;
            bottom: 18px !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            color: #475569 !important;
            background: rgba(255, 255, 255, 0.90) !important;
            padding: 2px 7px !important;
            border-radius: 4px !important;
            border: 1px solid #e2e8f0 !important;
            z-index: 998 !important;
        }}

        /* ========================================================= */
        /* SLIDE 3: WHY SPATIAL STATISTICS - FITTED, CLEAN LAYOUT    */
        /* ========================================================= */
        .why-body {{
            height: 540px;
            max-height: 540px !important;
            gap: 18px !important;
        }}

        .why-lead {{
            padding: 16px 22px !important;
            margin-bottom: 0 !important;
        }}

        .why-lead p {{
            font-size: 0.42em !important;
            line-height: 1.5 !important;
            margin: 0 !important;
        }}

        .why-grid {{
            flex: 1;
            gap: 18px !important;
            align-items: stretch;
        }}

        .why-card {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 22px 24px !important;
        }}

        .why-num {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--dsn-green);
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .why-card:nth-child(2) .why-num {{
            background: var(--dsn-red);
        }}

        .why-card {{
            background: linear-gradient(180deg, var(--dsn-green-tint) 0%, #ffffff 38%) !important;
            border-color: var(--dsn-green-line) !important;
        }}

        .why-card:nth-child(2) {{
            background: linear-gradient(180deg, var(--dsn-red-tint) 0%, #ffffff 38%) !important;
            border-color: var(--dsn-red-line) !important;
        }}

        .fallacy-body {{
            height: 480px;
            max-height: 480px !important;
        }}

        .fallacy-grid .why-card p {{
            font-size: 0.46em !important;
        }}

        .fallacy-row + .fallacy-row {{
            margin-top: 10px;
        }}

        .fallacy-grid {{
            gap: 22px !important;
        }}

        .fallacy-row {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 4px;
        }}

        .fallacy-label {{
            align-self: flex-start;
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: var(--dsn-green-dark);
        }}

        .why-card:nth-child(2) .fallacy-label {{
            color: var(--dsn-red);
        }}

        .viz {{
            height: 104px;
            flex-shrink: 0;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.75);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .viz svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        .viz-tall {{
            height: 150px;
        }}

        .viz-banner {{
            height: 168px;
            background: linear-gradient(90deg, var(--dsn-green-tint) 0%, #ffffff 50%, var(--dsn-red-tint) 100%);
            border: 1px solid var(--dsn-green-line);
            padding: 8px 0;
        }}

        .why-head {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .why-head .why-num {{
            width: 32px;
            height: 32px;
            font-size: 16px;
            flex-shrink: 0;
        }}

        .why-card ul {{
            margin: 0 0 0 18px !important;
        }}

        .why-card .callout {{
            margin: 0 !important;
        }}

        .why-lead p + p {{
            margin-top: 6px !important;
        }}

        .why-dense {{
            gap: 14px !important;
            height: 560px;
            max-height: 560px !important;
        }}

        .why-dense .why-lead {{
            padding: 12px 20px !important;
        }}

        .why-dense .why-lead p {{
            font-size: 0.36em !important;
            line-height: 1.45 !important;
        }}

        .why-dense .why-card {{
            padding: 14px 18px !important;
            gap: 10px !important;
        }}

        .why-dense .why-card h4 {{
            font-size: 0.48em !important;
        }}

        .why-dense .why-card p {{
            font-size: 0.355em !important;
            line-height: 1.5 !important;
        }}

        .why-dense .viz-sm {{
            height: 66px;
        }}

        .viz-sm {{
            height: 84px;
        }}

        .body-2line {{
            height: 478px;
            max-height: 478px !important;
            gap: 14px !important;
        }}

        /* Core Objective: five question cards with real map thumbnails */
        .grid-5 {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
        }}

        .q-card {{
            padding: 12px 12px 14px 12px !important;
            gap: 8px !important;
            position: relative;
        }}

        .q-img {{
            height: 150px;
            border-radius: 6px;
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .q-img img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            margin: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .q-svg svg {{
            width: 100%;
            height: 100%;
        }}

        .q-card .why-num {{
            width: 28px;
            height: 28px;
            font-size: 14px;
            margin-top: -26px;
            margin-left: 4px;
            border: 3px solid #ffffff;
            box-sizing: content-box;
        }}

        .reveal .q-card h5 {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.40em !important;
            line-height: 1.3 !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            text-transform: none !important;
            margin: 0 !important;
        }}

        .q-card p {{
            font-size: 0.36em !important;
            line-height: 1.45 !important;
        }}

        .why-card:nth-child(4) .why-num {{
            background: var(--dsn-red);
        }}

        .why-card:nth-child(4) {{
            background: linear-gradient(180deg, var(--dsn-red-tint) 0%, #ffffff 38%) !important;
            border-color: var(--dsn-red-line) !important;
        }}

        /* Superpower: two-lane flow diagram */
        .flow {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 14px;
            min-height: 0;
        }}

        .flow-row {{
            flex: 1;
            display: grid;
            grid-template-columns: 150px 1fr 40px 1.2fr 40px 1.4fr;
            align-items: stretch;
            gap: 10px;
        }}

        .flow-label {{
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            background: var(--dsn-red);
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 17px;
            text-align: center;
        }}

        .flow-label-g {{
            background: var(--dsn-green);
        }}

        .flow-box {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            font-weight: 500;
            color: #1e293b;
            text-align: center;
        }}

        .flow-chip {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 17px;
            font-weight: 600;
        }}

        .flow-viz {{
            width: 124px;
            height: 76px;
        }}

        .flow-icon {{
            width: 64px;
            height: 64px;
        }}

        .flow-viz svg, .flow-icon svg {{
            width: 100%;
            height: 100%;
        }}

        .flow-end {{
            flex-direction: row;
            gap: 14px;
            text-align: left;
            font-size: 17px;
        }}

        .flow-red {{
            background: var(--dsn-red-tint);
            border-color: var(--dsn-red-line);
        }}

        .flow-green {{
            background: var(--dsn-green-tint);
            border-color: var(--dsn-green-line);
        }}

        .flow-arrow {{
            align-self: center;
            height: 22px;
            background: var(--dsn-red);
            clip-path: polygon(0 35%, 60% 35%, 60% 0, 100% 50%, 60% 100%, 60% 65%, 0 65%);
            opacity: 0.8;
        }}

        .flow-arrow-g {{
            background: var(--dsn-green);
        }}

        /* ESDA unlocks: LISA map + numbered list */
        .unlock-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1.15fr;
            gap: 18px;
            min-height: 0;
        }}

        .unlock-map {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px !important;
        }}

        .unlock-map img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            margin: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .unlock-list {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 14px;
        }}

        .unlock-list-big {{
            justify-content: stretch;
            gap: 18px;
        }}

        .unlock-list-big .unlock-item {{
            flex: 1;
            align-items: center;
            padding: 18px 24px;
        }}

        .unlock-list-big .unlock-item p {{
            font-size: 0.46em !important;
            line-height: 1.55 !important;
        }}

        .unlock-list-big .why-num {{
            width: 36px;
            height: 36px;
            font-size: 17px;
        }}

        .unlock-item {{
            display: flex;
            gap: 12px;
            align-items: flex-start;
            padding: 12px 16px;
            border-radius: 8px;
            background: var(--dsn-green-tint);
            border: 1px solid var(--dsn-green-line);
        }}

        .unlock-item:nth-child(even) {{
            background: var(--dsn-red-tint);
            border-color: var(--dsn-red-line);
        }}

        .unlock-item .why-num {{
            width: 28px;
            height: 28px;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .unlock-item:nth-child(even) .why-num {{
            background: var(--dsn-red);
        }}

        .unlock-item p {{
            font-size: 0.37em !important;
            line-height: 1.45 !important;
            margin: 0 !important;
        }}

        .lisa-rows {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-top: 6px;
        }}

        .lisa-rows p {{
            font-size: 0.34em !important;
        }}

        .chip {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 3px;
            margin-right: 6px;
            vertical-align: -1px;
        }}

        .chip-hh {{ background: #e3002b; }}
        .chip-ll {{ background: #0571b0; }}
        .chip-hl {{ background: #f98400; }}
        .chip-lh {{ background: #92dff3; }}

        .in-short {{
            border-radius: 8px;
            padding: 12px 20px;
            background: linear-gradient(90deg, var(--dsn-green) 0%, #00904c 100%);
        }}

        .reveal .in-short p {{
            color: #ffffff !important;
            font-size: 0.40em !important;
            margin: 0 !important;
        }}

        .reveal .in-short strong {{
            color: #ffffff;
        }}

        /* Model slides: when-to-use + equation on top, diagram + examples below */
        .model-body {{
            gap: 16px !important;
        }}

        .model-top {{
            display: grid;
            grid-template-columns: 1.25fr 1fr;
            gap: 16px;
        }}

        .model-when, .model-eq {{
            border-radius: 8px;
            padding: 14px 20px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .model-when {{
            background: var(--dsn-green-tint);
            border: 1px solid var(--dsn-green-line);
        }}

        .model-when p {{
            font-size: 0.40em !important;
            line-height: 1.5 !important;
            color: #1e293b !important;
            margin: 0 !important;
        }}

        .model-eq {{
            background: #ffffff;
            border: 1px solid var(--dsn-red-line);
        }}

        .model-eq .fallacy-label {{
            color: var(--dsn-red);
        }}

        .model-eq .eq {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.62em;
            color: #0f172a;
        }}

        .model-bottom {{
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1.15fr;
            gap: 16px;
            min-height: 0;
        }}

        .model-bottom-even {{
            grid-template-columns: 1fr 1fr;
        }}

        .viz-model {{
            height: 140px;
        }}

        .model-viz p, .model-ex p {{
            font-size: 0.37em !important;
            line-height: 1.5 !important;
            margin: 0 !important;
        }}

        .gwr-body .viz-model {{
            height: 96px;
        }}

        .gwr-body .model-viz {{
            gap: 8px !important;
            padding-top: 14px !important;
            padding-bottom: 14px !important;
        }}

        .gwr-body .model-eq .eq {{
            font-size: 0.56em;
        }}

        .model-viz, .model-ex {{
            justify-content: center;
        }}

        .model-ex {{
            gap: 16px !important;
        }}

        .model-bottom .why-card:nth-child(2) .fallacy-label {{
            color: var(--dsn-red);
        }}

        .ex-row {{
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }}

        .ex-row .why-num {{
            width: 26px;
            height: 26px;
            font-size: 13px;
            flex-shrink: 0;
        }}

        .ex-row:nth-child(odd) .why-num {{
            background: var(--dsn-red);
        }}

        /* Problem -> model picker */
        .pick-list {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .pick-row {{
            flex: 1;
            display: grid;
            grid-template-columns: 36px 1fr 60px 230px;
            align-items: center;
            gap: 16px;
            padding: 8px 18px;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid var(--dsn-green-line);
        }}

        .pick-row:nth-child(even) {{
            border-color: var(--dsn-red-line);
        }}

        .pick-row:nth-child(even) .why-num {{
            background: var(--dsn-red);
        }}

        .pick-row .why-num {{
            width: 34px;
            height: 34px;
            font-size: 16px;
        }}

        .reveal .pick-q {{
            font-size: 0.42em !important;
            line-height: 1.45 !important;
            color: #1e293b !important;
            margin: 0 !important;
        }}

        .pick-arrow {{
            height: 20px;
            background: var(--dsn-green);
            clip-path: polygon(0 35%, 65% 35%, 65% 0, 100% 50%, 65% 100%, 65% 65%, 0 65%);
        }}

        .pick-row:nth-child(even) .pick-arrow {{
            background: var(--dsn-red);
        }}

        .pick-model {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            padding: 10px;
            background: var(--dsn-green);
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
        }}

        .pick-row:nth-child(even) .pick-model {{
            background: var(--dsn-red);
        }}

        .pick-model strong {{
            font-size: 22px;
            line-height: 1.1;
        }}

        .pick-model span {{
            font-size: 13px;
            opacity: 0.92;
        }}

        /* Tools & libraries slide */
        .tools-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1.45fr 0.95fr 1.1fr;
            gap: 16px;
            min-height: 0;
        }}

        .tool-col {{
            gap: 14px !important;
            padding: 16px 18px !important;
        }}

        .tool-head {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .tool-head img {{
            height: 30px;
            width: auto;
            margin: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .reveal .tool-head h4 {{
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
        }}

        .tool-head .tool-head-right {{
            margin-left: auto !important;
            height: 34px;
        }}

        .tool-tag {{
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: var(--dsn-green-dark);
        }}

        .tool-row {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .tool-row img {{
            width: 52px;
            height: 52px;
            object-fit: contain;
            flex-shrink: 0;
            margin: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }}

        .tool-row-hero img {{
            width: 104px;
            height: 104px;
        }}

        .tool-pkgs, .tool-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .tool-col p {{
            font-size: 0.35em !important;
            line-height: 1.45 !important;
            margin: 0 !important;
        }}

        .tool-col code, .in-short code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95em;
            font-weight: 600;
            color: var(--dsn-green-dark);
            background: var(--dsn-green-tint);
            border-radius: 4px;
            padding: 1px 6px;
            margin-right: 4px;
        }}

        .why-card:nth-child(2) .tool-list code {{
            color: #b91c1c;
            background: var(--dsn-red-tint);
        }}

        .in-short code {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.18);
        }}

        .tool-list {{
            gap: 14px;
        }}

        /* Workflow: 7 dependent steps in a snake of two rows */
        .wf-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 26px 1fr 26px 1fr 26px 1fr;
            grid-template-rows: 1fr 1fr;
            row-gap: 18px;
            column-gap: 8px;
            min-height: 0;
        }}

        .wf-step {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding: 14px 16px;
            border-radius: 8px;
            background: linear-gradient(180deg, var(--dsn-green-tint) 0%, #ffffff 60%);
            border: 1px solid var(--dsn-green-line);
        }}

        .wf-step:nth-child(4n+3) {{
            background: linear-gradient(180deg, var(--dsn-red-tint) 0%, #ffffff 60%);
            border-color: var(--dsn-red-line);
        }}

        .wf-step:nth-child(4n+3) .why-num {{
            background: var(--dsn-red);
        }}

        .wf-step .why-num {{
            width: 30px;
            height: 30px;
            font-size: 15px;
        }}

        .reveal .wf-step h5 {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.44em !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            text-transform: none !important;
            margin: 2px 0 0 0 !important;
            line-height: 1.25 !important;
        }}

        .wf-step p {{
            flex: 1;
            font-size: 0.35em !important;
            line-height: 1.45 !important;
            margin: 0 !important;
        }}

        .wf-step code {{
            align-self: flex-start;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            font-weight: 600;
            color: var(--dsn-green-dark);
            background: #ffffff;
            border: 1px solid var(--dsn-green-line);
            border-radius: 4px;
            padding: 1px 7px;
        }}

        .wf-arrow {{
            align-self: center;
            height: 18px;
            background: var(--dsn-green);
            clip-path: polygon(0 35%, 55% 35%, 55% 0, 100% 50%, 55% 100%, 55% 65%, 0 65%);
        }}

        /* Row 2 (steps 5-7) sits under steps 2-4, flowing on from step 4 */
        .wf-grid > :nth-child(8) {{
            grid-column: 7;
            grid-row: 2;
            display: none;
        }}

        .wf-grid > :nth-child(9) {{ grid-column: 1; grid-row: 2; }}
        .wf-grid > :nth-child(10) {{ grid-column: 2; grid-row: 2; }}
        .wf-grid > :nth-child(11) {{ grid-column: 3; grid-row: 2; }}
        .wf-grid > :nth-child(12) {{ grid-column: 4; grid-row: 2; }}
        .wf-grid > :nth-child(13) {{ grid-column: 5; grid-row: 2; }}

        /* Space-time pattern mining slide */
        .st-body {{
            gap: 14px !important;
        }}

        .st-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1.25fr 1fr;
            gap: 16px;
            min-height: 0;
        }}

        .st-steps {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }}

        .st-step {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 12px 14px;
            border-radius: 8px;
            background: linear-gradient(180deg, var(--dsn-green-tint) 0%, #ffffff 55%);
            border: 1px solid var(--dsn-green-line);
        }}

        .st-step:nth-child(2) {{
            background: linear-gradient(180deg, var(--dsn-red-tint) 0%, #ffffff 55%);
            border-color: var(--dsn-red-line);
        }}

        .st-step:nth-child(2) .why-num {{
            background: var(--dsn-red);
        }}

        .st-viz {{
            height: 130px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .st-viz svg {{
            width: 100%;
            height: 100%;
        }}

        .st-step .why-head {{
            padding-bottom: 6px;
        }}

        .st-step .why-num {{
            width: 26px;
            height: 26px;
            font-size: 13px;
        }}

        .reveal .st-step h5, .reveal .ehsa-row strong {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.38em !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            text-transform: none !important;
            margin: 0 !important;
            line-height: 1.25 !important;
        }}

        .st-step p {{
            font-size: 0.33em !important;
            line-height: 1.45 !important;
            margin: 0 !important;
        }}

        .st-strip {{
            display: grid;
            grid-template-columns: 1fr 44px 1fr 44px 1fr;
            align-items: center;
            gap: 10px;
        }}

        .st-chip {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: 8px;
            background: var(--dsn-green-tint);
            border: 1px solid var(--dsn-green-line);
            font-family: 'Poppins', sans-serif;
        }}

        .st-chip:nth-child(3) {{
            background: var(--dsn-red-tint);
            border-color: var(--dsn-red-line);
        }}

        .st-chip:nth-child(3) .why-num {{
            background: var(--dsn-red);
        }}

        .st-chip .why-num {{
            width: 28px;
            height: 28px;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .st-chip strong {{
            display: block;
            font-size: 15px;
            color: #0f172a;
            line-height: 1.25;
        }}

        .st-chip .st-sub {{
            display: block;
            font-size: 12.5px;
            color: #475569;
            line-height: 1.3;
        }}

        .st-main {{
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1.1fr;
            gap: 16px;
            min-height: 0;
        }}

        .st-legend, .st-map {{
            min-height: 0;
            overflow: hidden;
            align-items: center;
            justify-content: center;
            padding: 12px 16px !important;
        }}

        .st-legend svg, .st-map svg {{
            width: 100%;
            height: 100%;
            max-height: 300px;
        }}

        .ehsa-card {{
            gap: 7px !important;
            padding: 12px 16px !important;
            justify-content: space-between;
        }}

        .ehsa-row {{
            display: grid;
            grid-template-columns: 200px 1fr;
            align-items: center;
            gap: 12px;
        }}

        .ehsa-glyph svg {{
            width: 200px;
            height: 14px;
            display: block;
        }}

        .ehsa-row > div:last-child {{
            display: flex;
            flex-direction: column;
            line-height: 1.2;
        }}

        .reveal .ehsa-row strong {{
            font-size: 15px !important;
        }}

        .ehsa-row span {{
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
            color: #475569;
        }}

        .reveal .st-short p {{
            font-size: 0.35em !important;
        }}

        /* Dependence testing toolkit */
        .tk-legend {{
            display: flex;
            gap: 18px;
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #334155;
        }}

        .tk-key::before {{
            content: "";
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 3px;
            margin-right: 6px;
            vertical-align: -1px;
        }}

        .tk-key-global::before {{ background: var(--dsn-green); }}
        .tk-key-local::before {{ background: var(--dsn-red); }}
        .tk-key-model::before {{ background: #0f172a; }}

        .tk-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-auto-rows: 1fr;
            gap: 10px;
            min-height: 0;
        }}

        .tk-card {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 10px 14px;
            border-radius: 8px;
            background: var(--dsn-green-tint);
            border: 1px solid var(--dsn-green-line);
        }}

        .tk-local {{
            background: var(--dsn-red-tint);
            border-color: var(--dsn-red-line);
        }}

        .tk-local .why-num {{
            background: var(--dsn-red);
        }}

        .tk-model {{
            background: #ffffff;
            border-color: #cbd5e1;
        }}

        .tk-model .why-num {{
            background: #0f172a;
        }}

        .tk-top {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .tk-top .why-num {{
            width: 26px;
            height: 26px;
            font-size: 13px;
            flex-shrink: 0;
        }}

        .reveal .tk-card h5 {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.40em !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            text-transform: none !important;
            margin: 0 !important;
            line-height: 1.25 !important;
        }}

        .tk-card p {{
            flex: 1;
            font-size: 0.34em !important;
            line-height: 1.4 !important;
            margin: 0 !important;
        }}

        .tk-card code {{
            align-self: flex-start;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 600;
            color: #0f172a;
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 1px 7px;
        }}

        /* Slide 14: OLS vs GWR with the real local-slope map */
        .gwr2-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1.05fr;
            gap: 16px;
            min-height: 0;
        }}

        .gwr2-compare {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .gwr2-card {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 6px;
            padding: 14px 18px;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid #cbd5e1;
        }}

        .gwr2-gwr {{
            background: var(--dsn-green-tint);
            border-color: var(--dsn-green-line);
        }}

        .gwr2-ols .fallacy-label {{
            color: #475569;
        }}

        .gwr2-card p, .gwr2-mgwr {{
            font-size: 0.36em !important;
            line-height: 1.45 !important;
            margin: 0 !important;
        }}

        .gwr2-card .eq {{
            font-size: 0.50em;
            color: #0f172a;
            padding: 4px 0;
        }}

        .reveal .gwr2-result {{
            font-weight: 600;
            color: var(--dsn-green-dark) !important;
        }}

        .reveal .gwr2-ols .gwr2-result {{
            color: #475569 !important;
        }}

        .gwr2-mgwr {{
            padding: 10px 16px;
            border-radius: 8px;
            background: var(--dsn-red-tint);
            border: 1px solid var(--dsn-red-line);
            font-family: 'Poppins', sans-serif;
            color: #1e293b;
        }}

        .gwr2-map {{
            gap: 8px !important;
            padding: 12px 16px !important;
            min-height: 0;
        }}

        .gwr2-map img {{
            flex: 1;
            min-height: 0;
            width: 100%;
            object-fit: contain;
            margin: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .gwr2-legend {{
            display: flex;
            gap: 16px;
            justify-content: center;
            font-family: 'Poppins', sans-serif;
            font-size: 12.5px;
            color: #334155;
        }}

        .gwr2-legend i {{
            display: inline-block;
            width: 14px;
            height: 12px;
            border-radius: 2px;
            margin-right: 4px;
            vertical-align: -1px;
        }}

        .gwr2-legend i.gwr2-outline {{
            background: #ffffff;
            border: 2px solid #0f172a;
        }}

        .why-card h4 {{
            font-size: 0.58em !important;
            line-height: 1.25 !important;
            margin: 0 !important;
            padding-bottom: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .why-card p {{
            font-size: 0.42em !important;
            line-height: 1.6 !important;
            margin: 0 !important;
        }}

        /* ========================================================= */
        /* SLIDE 2 ENHANCED CREATIVE ARRANGEMENT                     */
        /* ========================================================= */
        .trap-card {{
            display: flex !important;
            flex-direction: column !important;
            gap: 4px !important;
            padding: 8px 10px !important;
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        }}

        .trap-pill {{
            align-self: flex-start;
            font-size: 0.31em !important;
            font-weight: 700 !important;
            letter-spacing: 0.06em;
            color: #475569;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 1px 6px;
            border-radius: 4px;
            margin-bottom: 1px;
        }}

        .trap-title {{
            font-size: 0.48em !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            margin: 0 !important;
            line-height: 1.22 !important;
        }}

        .trap-subtitle {{
            font-size: 0.34em !important;
            font-weight: 600 !important;
            color: #0284c7 !important;
            margin-bottom: 2px !important;
        }}

        .trap-points {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .trap-point {{
            font-size: 0.31em !important;
            line-height: 1.34 !important;
            color: #334155 !important;
            background: #f8fafc;
            padding: 4px 6px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}

        .strategic-takeaway-banner {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .banner-label {{
            font-size: 0.31em !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em;
            color: var(--dsn-green);
            text-transform: uppercase;
        }}

        .banner-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 12px;
        }}

        .banner-step {{
            display: flex;
            align-items: flex-start;
            gap: 6px;
            font-size: 0.31em !important;
            line-height: 1.32 !important;
            color: #1e293b !important;
        }}

        .step-badge {{
            background: #0284c7;
            color: #ffffff;
            font-size: 0.85em;
            font-weight: 700;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
        }}

        .tech-notes-view .doc-container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="portal-layout">
        <!-- Sidebar Navigation -->
        <aside class="portal-sidebar" id="portalSidebar">
            <div class="sidebar-brand">
                <img src="{logo_b64}" alt="DSN Logo" class="brand-logo">
                <div class="brand-title-wrap">
                    <span class="brand-name">Spatial Statistics</span>
                    <span class="brand-badge">DSN Masterclass</span>
                </div>
            </div>

            <nav class="sidebar-menu">
                <div class="menu-heading">Class Presentation</div>
                <button class="nav-link-btn active" id="btn-slides" onclick="switchPortalView('slides')">
                    <span class="nav-icon">📊</span>
                    <span>Lecture Slides</span>
                </button>
                <button class="nav-link-btn" id="btn-technical_notes" onclick="switchPortalView('technical_notes')">
                    <span class="nav-icon">📜</span>
                    <span>Technical Note</span>
                </button>

                <div class="menu-heading">Class Notebook</div>
                <button class="nav-link-btn" id="btn-use_cases" onclick="switchPortalView('use_cases')">
                    <span class="nav-icon">📓</span>
                    <span>Spatial Statistics Use Cases</span>
                </button>

                <div class="menu-heading">Repository</div>
                <a href="https://github.com/SammyGIS/dsn_advanced_spatial_stats" target="_blank" rel="noopener noreferrer" class="nav-link-btn github-btn">
                    <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                    <span>View on GitHub</span>
                </a>
            </nav>

            <div class="sidebar-footer">
                <span>Data Science Nigeria</span>
                <button class="collapse-toggle-btn" onclick="toggleSidebar()" title="Collapse sidebar">
                    <span id="collapseLabel">◀ Hide</span>
                </button>
            </div>
        </aside>

        <!-- Main Workspace -->
        <main class="portal-main">
            <!-- Top Bar -->
            <div class="portal-topbar">
                <div class="topbar-left">
                    <button class="sidebar-btn" onclick="toggleSidebar()" aria-label="Toggle Sidebar">
                        ☰ <span>Navigation</span>
                    </button>
                    <span class="view-title" id="currentViewTitle">Lecture Slides: Theory, Intuition &amp; Spatial Statistics Modeling</span>
                </div>
                <div class="topbar-right">
                    <button class="fullscreen-btn" onclick="toggleFullscreen()" title="Fullscreen Slides (F)">
                        ⛶ <span>Fullscreen</span>
                    </button>
                </div>
            </div>

            <!-- Viewport Container -->
            <div class="portal-viewport" id="portalViewport">
                <!-- 1. Reveal.js Slides View -->
                <div class="slides-view" id="slidesView">
                    <div class="reveal" id="revealDeck">
                        <div class="slides">
{all_slides_combined}
                        </div>
                    </div>
                </div>

                <!-- 2. Document Frame for Technical Note & Notebooks -->
                <iframe id="docFrame" class="doc-frame" title="Document Viewer"></iframe>
            </div>
        </main>
    </div>

    <!-- Reveal.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js"></script>
    <script>
        // Initialize Reveal.js with 16:9 widescreen dimensions and generous gaps/margins
        let deck = new Reveal(document.getElementById('revealDeck'), {{
            width: 1280,
            height: 720,
            margin: 0.06,
            minScale: 0.2,
            maxScale: 1.2,
            controls: true,
            progress: true,
            center: false,
            hash: false,
            slideNumber: 'c / t',
            transition: 'slide'
        }});
        deck.initialize();

        // Portal View Navigation Dictionary
        const portalViews = {{
            'slides': {{
                type: 'slides',
                title: 'Lecture Slides: Theory, Intuition & Spatial Statistics Modeling'
            }},
            'technical_notes': {{
                type: 'frame',
                url: 'technical_notes.html',
                title: 'Technical Note: Mathematical Formulations & Statistical Mechanics'
            }},
            'use_cases': {{
                type: 'frame',
                url: 'notebooks_html/spatial_statistics_use_cases.html',
                title: 'Class Notebook: Spatial Statistics Use Cases on Nigerian Ward Data'
            }}
        }};

        function switchPortalView(key) {{
            const viewConfig = portalViews[key];
            if (!viewConfig) return;

            // Update Active Nav Button
            document.querySelectorAll('.nav-link-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('btn-' + key);
            if (activeBtn) activeBtn.classList.add('active');

            // Update Topbar Title
            document.getElementById('currentViewTitle').innerText = viewConfig.title;

            const slidesView = document.getElementById('slidesView');
            const docFrame = document.getElementById('docFrame');

            if (viewConfig.type === 'slides') {{
                docFrame.style.display = 'none';
                slidesView.style.display = 'block';
                setTimeout(() => {{ deck.layout(); }}, 50);
            }} else {{
                slidesView.style.display = 'none';
                docFrame.style.display = 'block';
                if (docFrame.src !== viewConfig.url && !docFrame.src.endsWith('/' + viewConfig.url)) {{
                    docFrame.src = viewConfig.url;
                }}
            }}

            history.replaceState(null, null, '#' + key);
        }}

        function toggleSidebar() {{
            const sidebar = document.getElementById('portalSidebar');
            sidebar.classList.toggle('collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');
            document.getElementById('collapseLabel').innerText = isCollapsed ? '▶ Show' : '◀ Hide';
            setTimeout(() => {{ deck.layout(); }}, 280);
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(err => {{
                    console.log('Fullscreen error:', err);
                }});
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
            setTimeout(() => {{ deck.layout(); }}, 300);
        }}

        window.addEventListener('resize', () => {{
            deck.layout();
        }});

        function triggerMathRender() {{
            if (typeof renderMathInElement === 'function') {{
                renderMathInElement(document.getElementById('slidesView'), {{
                    delimiters: [
                        {{ left: '$$', right: '$$', display: true }},
                        {{ left: '$', right: '$', display: false }}
                    ],
                    throwOnError: false
                }});
            }}
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash.replace('#', '');
            if (hash && portalViews[hash]) {{
                switchPortalView(hash);
            }} else {{
                switchPortalView('slides');
            }}
            setTimeout(triggerMathRender, 200);
        }});
        deck.on('ready', () => {{ setTimeout(triggerMathRender, 100); }});
    </script>
</body>
</html>
"""
    presentation_path = os.path.join(base_dir, "docs", "presentation.html")
    index_path = os.path.join(base_dir, "docs", "index.html")

    with open(presentation_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated clean DSN Masterclass Presentation at {presentation_path}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Synchronized clean DSN Masterclass Portal at {index_path}")

if __name__ == "__main__":
    main()
