"""
Export the water-desert map used on the "What Spatial Statistics Can Do" slide (card 4).

Runs Anselin LISA on log water points per 10,000 people (queen contiguity, islands
attached to their nearest ward) and colours the significant Low-Low clusters
(contiguous water deserts) in DSN red and High-High clusters in DSN green.
Matches use case 6 of notebooks/spatial_statistics_use_cases.ipynb.

Output: docs/figures/dsn_theme/slides/q4_water_deserts.png
"""

import os
import warnings

import esda
import geopandas as gpd
import libpysal
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "processed", "nigeria_wards_master.parquet")
OUT = os.path.join(BASE, "docs", "figures", "dsn_theme", "slides", "q4_water_deserts.png")


def main():
    wards = gpd.read_parquet(DATA)
    wards = wards[wards.rwi_mean.notna() & wards.pop_2025_sum.notna()].reset_index(drop=True)
    w_queen = libpysal.weights.Queen.from_dataframe(wards, use_index=False, silence_warnings=True)
    w_knn1 = libpysal.weights.KNN.from_dataframe(wards.set_geometry(wards.centroid), k=1)
    w = libpysal.weights.util.attach_islands(w_queen, w_knn1)
    w.transform = "r"

    water = np.log1p(wards.water_points_count / wards.pop_2025_sum * 1e4).values
    lisa = esda.Moran_Local(water, w, permutations=999, seed=42)
    sig = lisa.p_sim < 0.05
    colours = np.where(sig & (lisa.q == 3), "#ed3237", np.where(sig & (lisa.q == 1), "#8fd6b0", "#e5e7eb"))

    fig, ax = plt.subplots(figsize=(6, 5), dpi=160)
    wards.geometry.simplify(0.003).plot(ax=ax, color=colours, linewidth=0.2, edgecolor=(1, 1, 1, 0.35))
    ax.set_axis_off()
    fig.savefig(OUT, bbox_inches="tight", pad_inches=0.02, facecolor="white")
    deserts = sig & (lisa.q == 3)
    print(f"Wrote {OUT}: {deserts.sum()} water-desert wards, {wards.pop_2025_sum[deserts].sum() / 1e6:.1f} M people")


if __name__ == "__main__":
    main()
