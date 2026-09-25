"""
Export the GWR local-slope map (course result) as an SVG for the class slides.

Reads data/processed/lga_gwr_results.parquet (written by use case 10 of
notebooks/spatial_statistics_use_cases.ipynb), joins it to LGA boundaries dissolved
from the ward polygons, and colours each LGA by its local slope of purchasing power
on schools per 10,000 people (red = negative, green = positive). LGAs where the local
slope is statistically significant are outlined in dark.

Output: docs/figures/gwr_slope_map.svg
"""

import os

import geopandas as gpd
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WARDS = os.path.join(BASE, "data", "processed", "nigeria_wards_master.parquet")
RESULTS = os.path.join(BASE, "data", "processed", "lga_gwr_results.parquet")
OUT = os.path.join(BASE, "docs", "figures", "gwr_slope_map.svg")

W, H = 520, 430
NEG = ["#ed3237", "#f58a8c", "#fbc9ca"]      # strong -> weak negative
POS = ["#c9ecd9", "#6fcf9d", "#00a859"]      # weak -> strong positive
NS = "#e5e7eb"


def colour(v, vmax):
    if np.isnan(v):
        return NS
    k = min(2, int(abs(v) / vmax * 3))
    return POS[k] if v > 0 else NEG[k]


def path(geom, tx):
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for p in polys:
        pts = [tx(x, y) for x, y in p.exterior.coords]
        out.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z")
    return " ".join(out)


def main():
    wards = gpd.read_parquet(WARDS)[["statename", "lganame", "geometry"]]
    lga = wards.dissolve(by=["statename", "lganame"]).reset_index()
    lga["geometry"] = lga.geometry.simplify(0.01)
    res = pd.read_parquet(RESULTS)
    lga = lga.merge(res, on=["statename", "lganame"], how="left")

    minx, miny, maxx, maxy = lga.total_bounds
    scale = min(W / (maxx - minx), H / (maxy - miny))

    def tx(x, y):
        return (x - minx) * scale, (maxy - y) * scale

    vmax = np.nanmax(np.abs(lga.gwr_slope_pp.values))
    body = "".join(
        f'<path d="{path(g, tx)}" fill="{colour(v, vmax)}" stroke="#ffffff" stroke-opacity="0.35" stroke-width="0.2"/>'
        for g, v in zip(lga.geometry, lga.gwr_slope_pp)
    )
    # Outline the LGAs where the local slope is statistically significant
    body += "".join(
        f'<path d="{path(g, tx)}" fill="none" stroke="#0f172a" stroke-width="1.1"/>'
        for g in lga.loc[lga.gwr_slope_sig.notna(), "geometry"]
    )
    svg = (f'<svg viewBox="0 0 {W:.0f} {(maxy - miny) * scale:.0f}" xmlns="http://www.w3.org/2000/svg" '
           f'role="img" aria-label="GWR local slope map across Nigerian LGAs">{body}</svg>')
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT} ({(lga.gwr_slope_sig > 0).sum()} positive, {(lga.gwr_slope_sig < 0).sum()} negative LGAs)")


if __name__ == "__main__":
    main()
