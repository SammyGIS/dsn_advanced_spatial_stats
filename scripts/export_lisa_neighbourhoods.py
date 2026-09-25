"""
Export an SVG showing the four LISA categories on REAL ward boundaries.

For each category (High-High, Low-Low, High-Low, Low-High) one strongly
significant ward (p = 0.001, 5-7 queen neighbours) is drawn with its actual
neighbouring wards, coloured by whether each ward's purchasing power (RWI mean)
is above or below the national mean.

Output: docs/figures/lisa_real_neighbourhoods.svg (embedded in the Technical Note).
"""

import os
import warnings

import esda
import geopandas as gpd
import libpysal

warnings.filterwarnings("ignore")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "processed", "nigeria_wards_master.parquet")
OUT = os.path.join(BASE, "docs", "figures", "lisa_real_neighbourhoods.svg")

HIGH, HIGH_LIGHT = "#e8322e", "#f6a3a5"
LOW, LOW_LIGHT = "#2b83ba", "#b9d6ea"
INK, MUTE = "#0f172a", "#64748b"
FONT = "Inter, Poppins, sans-serif"

PANEL_W, PANEL_H, GAP = 210, 170, 20
CATEGORIES = [(1, "High-High", "hotspot"), (3, "Low-Low", "coldspot"),
              (4, "High-Low", "outlier"), (2, "Low-High", "outlier")]


def ring_path(coords, tx):
    pts = [tx(x, y) for x, y in coords]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def geom_path(geom, tx):
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    return " ".join(ring_path(p.exterior.coords, tx) for p in polys)


def main():
    g = gpd.read_parquet(DATA)
    g = g[g.rwi_mean.notna()].reset_index(drop=True)
    w = libpysal.weights.Queen.from_dataframe(g, use_index=False, silence_warnings=True)
    w.transform = "r"
    lisa = esda.Moran_Local(g.rwi_mean.values, w, permutations=999, seed=42)
    g["q"], g["p"] = lisa.q, lisa.p_sim
    mean = g.rwi_mean.mean()

    body = ""
    for k, (q, name, kind) in enumerate(CATEGORIES):
        cand = g[(g.q == q) & (g.p < 0.01)]
        cand = cand[[5 <= len(w.neighbors[i]) <= 7 for i in cand.index]]
        expect_high_nb = q in (1, 2)
        purity = [((g.loc[w.neighbors[i], "rwi_mean"] > mean) == expect_high_nb).mean() for i in cand.index]
        cand = cand.assign(pur=purity).sort_values(["pur", "p"], ascending=[False, True])
        focal = cand.index[0]
        nbrs = w.neighbors[focal]
        sub = g.loc[[focal] + list(nbrs)]

        minx, miny, maxx, maxy = sub.total_bounds
        scale = min(PANEL_W / (maxx - minx), (PANEL_H - 10) / (maxy - miny))
        ox = k * (PANEL_W + GAP) + (PANEL_W - (maxx - minx) * scale) / 2
        oy = (PANEL_H - (maxy - miny) * scale) / 2

        def tx(x, y, minx=minx, maxy=maxy, scale=scale, ox=ox, oy=oy):
            return ox + (x - minx) * scale, oy + (maxy - y) * scale

        for i in nbrs:
            fill = HIGH_LIGHT if g.at[i, "rwi_mean"] > mean else LOW_LIGHT
            body += f'<path d="{geom_path(g.at[i, "geometry"], tx)}" fill="{fill}" stroke="#ffffff" stroke-width="1.5"/>'
        focal_fill = HIGH if g.at[focal, "rwi_mean"] > mean else LOW
        body += (f'<path d="{geom_path(g.at[focal, "geometry"], tx)}" fill="{focal_fill}" '
                 f'stroke="{INK}" stroke-width="2.5"/>')

        cx = k * (PANEL_W + GAP) + PANEL_W / 2
        ward = g.at[focal, "wardname"].replace("&", "&amp;")
        place = f'{g.at[focal, "lganame"]}, {g.at[focal, "statename"]}'.replace("&", "&amp;")
        body += (f'<text x="{cx}" y="{PANEL_H + 26}" text-anchor="middle" font-family="{FONT}" font-size="15" '
                 f'font-weight="700" fill="{INK}">{name} <tspan fill="{MUTE}" font-weight="500">({kind})</tspan></text>'
                 f'<text x="{cx}" y="{PANEL_H + 46}" text-anchor="middle" font-family="{FONT}" font-size="12.5" '
                 f'fill="{MUTE}">{ward}</text>'
                 f'<text x="{cx}" y="{PANEL_H + 63}" text-anchor="middle" font-family="{FONT}" font-size="12.5" '
                 f'fill="{MUTE}">{place}</text>')

    width = 4 * PANEL_W + 3 * GAP
    svg = (f'<svg viewBox="0 0 {width} {PANEL_H + 72}" xmlns="http://www.w3.org/2000/svg" '
           f'role="img" aria-label="LISA categories on real Nigerian ward boundaries">{body}</svg>')
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
