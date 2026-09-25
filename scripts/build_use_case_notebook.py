"""
Build the single class notebook: notebooks/spatial_statistics_use_cases.ipynb

Eleven use cases on the class ward data, each defined in the same stages:
problem -> hypothesis -> the usual (aspatial / ML) approach -> run it -> what it tells us
-> the spatial statistics method -> run it -> interpretation of the actual results.

Interpretation cells are written from the executed outputs (see INTERP below);
re-run `python scripts/build_use_case_notebook.py --execute` after changing code.
"""

import os
import subprocess
import sys

import nbformat as nbf

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_PATH = os.path.join(BASE, "notebooks", "spatial_statistics_use_cases.ipynb")
HTML_DIR = os.path.join(BASE, "docs", "notebooks_html")

from use_case_interpretations import INTERP  # noqa: E402

cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))


def interp(key):
    md(INTERP.get(key, "_Interpretation pending: run the notebook, then describe what the output shows._"))


# =============================================================================
# INTRODUCTION
# =============================================================================
md(r"""
# Spatial Statistics Use Cases: Nigerian Wards as a Worked Example

**Advanced Spatial Statistics · Class Notebook · Data Science Nigeria**

All problems in this notebook are well defined in stages:

1. **The problem**: a real decision someone has to make.
2. **The hypothesis**: what we expect, stated so the data can prove us wrong.
3. **The usual approach**: how a standard (aspatial) statistics or ML workflow would answer it.
4. **The spatial statistics approach**: the method that respects geography, and why.
5. **Code → results → interpretation**: we run it and read what the numbers actually say.

### Contents

- [Setup: data, neighbours and map helpers](#setup)
1. [Poverty clustering](#uc1): is purchasing power randomly spread, or clustered?
2. [Poverty and religion](#uc2): do wealthier areas sit next to particular faith institutions?
3. [Religious sorting and diversity](#uc3): where do churches and mosques mix?
4. [Healthcare deserts](#uc4): where should mobile clinics go first?
5. [Retail expansion](#uc5): where is purchasing power high but market supply low?
6. [Water inequality](#uc6): how unequal is water infrastructure, and where are the water deserts?
7. [School provision, and honest $p$-values](#uc7): what explains school counts?
8. [Market spillovers](#uc8): do markets attract markets next door?
9. [Security coverage](#uc9): do wards without a police station cluster?
10. [One slope or many? (GWR)](#uc10): does purchasing power relate to schooling the same way everywhere?
11. [Malaria and poverty](#uc11): where should malaria campaigns go, and is poverty the driver?
""")

# =============================================================================
# SETUP
# =============================================================================
md("""
<a id="setup"></a>

## Setup: data, neighbours and map helpers
""")
code(r"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import libpysal
import esda
import spreg

np.random.seed(42)
plt.rcParams.update({"figure.dpi": 110, "font.size": 10, "axes.titleweight": "bold"})

DSN_GREEN, DSN_RED = "#00a859", "#ed3237"
LISA_COLOURS = {1: "#e3002b", 2: "#92dff3", 3: "#0571b0", 4: "#f98400", 0: "#eeeeee"}
# Thin, semi-transparent boundaries so ward outlines never hide the cluster colours
EDGE = (1, 1, 1, 0.35)
LISA_LABELS = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low", 0: "Not significant"}

wards = gpd.read_parquet("../data/processed/nigeria_wards_master.parquet")
wards = wards[wards.rwi_mean.notna() & wards.pop_2025_sum.notna()].reset_index(drop=True)
wards = wards.rename(columns={"rwi_mean": "purchasing_power"})
wards["geometry_plot"] = wards.geometry.simplify(0.003)
print(f"{len(wards):,} wards across {wards.statename.nunique()} states")
""")
code(r"""
# Queen contiguity: two wards are neighbours if they share a border or a corner.
w_queen = libpysal.weights.Queen.from_dataframe(wards, use_index=False, silence_warnings=True)
# A few wards touch no other ward (islands); link each one to its nearest ward.
w_knn1 = libpysal.weights.KNN.from_dataframe(wards.set_geometry(wards.centroid), k=1)
w = libpysal.weights.util.attach_islands(w_queen, w_knn1)
w.transform = "r"   # row-standardise: neighbour values become an average
print(f"Islands fixed: {len(w_queen.islands)} | mean neighbours per ward: {w.mean_neighbors:.1f}")
""")
code(r"""
def base_map(ax, title):
    ax.set_title(title, loc="left")
    ax.set_axis_off()


def choropleth(column, title, cmap="RdYlGn", ax=None, legend=True, **kw):
    ax = ax or plt.subplots(figsize=(7, 6))[1]
    wards.set_geometry("geometry_plot").plot(column=column, cmap=cmap, ax=ax, legend=legend,
                                             linewidth=0.2, edgecolor=EDGE, **kw)
    base_map(ax, title)
    return ax


def lisa_map(lisa, title, alpha=0.05, ax=None, labels=None):
    labels = labels or LISA_LABELS
    ax = ax or plt.subplots(figsize=(7, 6))[1]
    cls = np.where(lisa.p_sim < alpha, lisa.q, 0)
    colours = [LISA_COLOURS[c] for c in cls]
    wards.set_geometry("geometry_plot").plot(color=colours, ax=ax, linewidth=0.2, edgecolor=EDGE)
    counts = pd.Series(cls).value_counts()
    handles = [mpatches.Patch(color=LISA_COLOURS[k], label=f"{labels[k]} ({counts.get(k, 0):,})")
               for k in (1, 3, 4, 2, 0)]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, frameon=False)
    base_map(ax, title)
    return ax


def lisa_summary(lisa, alpha=0.05, labels=None):
    labels = labels or LISA_LABELS
    cls = np.where(lisa.p_sim < alpha, lisa.q, 0)
    return pd.Series(cls).map(labels).value_counts().rename("wards").to_frame()
""")

# =============================================================================
# USE CASE 1
# =============================================================================
md(r"""
<a id="uc1"></a>

## Use Case 1: Poverty clustering

**The problem.** A development agency wants to target a cash-transfer programme. Should it pick the poorest *states*, or is poverty organised in pockets that cross state lines?

**Hypothesis.**
- $H_0$: purchasing power is spread randomly across wards (no spatial pattern).
- $H_1$: poor wards sit next to poor wards and rich next to rich (positive spatial autocorrelation).

**The usual approach.** Rank states by their average purchasing power and look at the histogram.
""")
code(r"""
state_avg = wards.groupby("statename").purchasing_power.mean().sort_values()
print("Poorest states (mean purchasing power):"); print(state_avg.head(5).round(2).to_string())
print("\nRichest states:"); print(state_avg.tail(5).round(2).to_string())

fig, ax = plt.subplots(figsize=(6, 3))
ax.hist(wards.purchasing_power, bins=50, color="#94a3b8")
ax.set_title("Distribution of ward purchasing power", loc="left"); ax.set_xlabel("purchasing power (RWI mean)")
plt.show()
""")
interp("uc1_a")
md(r"""
**The spatial statistics approach.** Global Moran's $I$ tests $H_0$ for the whole map; Anselin's Local Moran ($I_i$, LISA) then shows *where* the clusters and outliers are. Significance comes from 999 random permutations of the map.
""")
code(r"""
moran_pp = esda.Moran(wards.purchasing_power.values, w, permutations=999)
print(f"Global Moran's I = {moran_pp.I:.3f}  (expected under randomness {moran_pp.EI:.4f})")
print(f"z = {moran_pp.z_sim:.1f}, pseudo p = {moran_pp.p_sim:.3f}")

lisa_pp = esda.Moran_Local(wards.purchasing_power.values, w, permutations=999, seed=42)
print(lisa_summary(lisa_pp).to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
choropleth("purchasing_power", "Purchasing power by ward", ax=axes[0])
lisa_map(lisa_pp, "LISA clusters of purchasing power (p < 0.05)", ax=axes[1])
plt.tight_layout(); plt.show()
""")
interp("uc1_b")

# =============================================================================
# USE CASE 2
# =============================================================================
md(r"""
<a id="uc2"></a>

## Use Case 2: Poverty and religion

**The problem.** Civil-society groups often partner with faith institutions to reach poor households. Do areas with more churches or more mosques differ in purchasing power, and is that relationship *geographic*?

We measure each ward's **church share** = churches / (churches + mosques) among registered faith institutions. This describes institutions on the map, not the beliefs of individual residents.

**Hypothesis.**
- $H_0$: a ward's purchasing power is unrelated to the faith-institution mix around it.
- $H_1$: purchasing power and the surrounding church share are spatially associated.

**The usual approach.** A Pearson correlation between the two columns.
""")
code(r"""
faith = wards.churches_count + wards.mosques_count
wards["church_share"] = np.where(faith > 0, wards.churches_count / faith, np.nan)
has_faith = wards.church_share.notna()
r = np.corrcoef(wards.purchasing_power[has_faith], wards.church_share[has_faith])[0, 1]
print(f"Wards with at least one registered church or mosque: {has_faith.sum():,}")
print(f"Pearson r (purchasing power vs church share): {r:.3f}  ->  r^2 = {r**2:.3f}")
""")
interp("uc2_a")
md(r"""
**The spatial statistics approach.** The **bivariate Moran's $I$** correlates purchasing power *in a ward* with the church share *in its neighbours*. The **bivariate LISA** maps where that relationship is locally significant. Wards with no faith institution take the national mean share so they neither add nor remove signal.
""")
code(r"""
share_filled = wards.church_share.fillna(wards.church_share.mean()).values
bv = esda.Moran_BV(wards.purchasing_power.values, share_filled, w, permutations=999)
print(f"Bivariate Moran's I = {bv.I:.3f}, pseudo p = {bv.p_sim:.3f}")

bv_lisa = esda.Moran_Local_BV(wards.purchasing_power.values, share_filled, w, permutations=999, seed=42)
bv_labels = {1: "High power, high church share nearby", 2: "Low power, high church share nearby",
             3: "Low power, low church share nearby", 4: "High power, low church share nearby",
             0: "Not significant"}
print(lisa_summary(bv_lisa, labels=bv_labels).to_string())
lisa_map(bv_lisa, "Bivariate LISA: purchasing power vs neighbours' church share", labels=bv_labels)
plt.show()
""")
interp("uc2_b")

# =============================================================================
# USE CASE 3
# =============================================================================
md(r"""
<a id="uc3"></a>

## Use Case 3: Religious sorting and diversity

**The problem.** A peace-building NGO wants to locate *transition zones* where churches and mosques sit side by side (places to host inter-faith dialogue), and zones that are strongly one-sided.

**Hypothesis.**
- $H_0$: the church/mosque mix is randomly arranged across wards.
- $H_1$: faith institutions are geographically sorted, with a band of mixed wards between.

**The usual approach.** A table of shares by state.
""")
code(r"""
by_state = (wards.groupby("statename")[["churches_count", "mosques_count"]].sum()
            .assign(church_share=lambda d: d.churches_count / (d.churches_count + d.mosques_count))
            .sort_values("church_share"))
print(by_state.church_share.round(2).describe().to_string())
print("\nMost mosque-dominated states:", ", ".join(by_state.index[:4]))
print("Most church-dominated states:", ", ".join(by_state.index[-4:]))
""")
interp("uc3_a")
md(r"""
**The spatial statistics approach.** First, Moran's $I$ on church share measures how strongly faiths are sorted in space. Second, we compute **Shannon diversity** for each ward, $H = -\sum_k p_k \ln p_k$ (0 = one faith only, $\ln 2 \approx 0.69$ = perfectly mixed), and run **Getis-Ord $G_i^*$** to find statistically significant clusters of high diversity (mixing zones) and low diversity.
""")
code(r"""
moran_share = esda.Moran(share_filled, w, permutations=999)
print(f"Moran's I (church share) = {moran_share.I:.3f}, pseudo p = {moran_share.p_sim:.3f}")

p_c = (wards.churches_count / faith).where(faith > 0, 0)
p_m = (wards.mosques_count / faith).where(faith > 0, 0)
entropy = -(p_c * np.log(p_c.where(p_c > 0, 1)) + p_m * np.log(p_m.where(p_m > 0, 1)))
wards["faith_diversity"] = entropy.where(faith > 0, 0)

gi_div = esda.G_Local(wards.faith_diversity.values, w, star=True, permutations=999, seed=42)
wards["diversity_cluster"] = np.select(
    [(gi_div.Zs > 0) & (gi_div.p_sim < 0.05), (gi_div.Zs < 0) & (gi_div.p_sim < 0.05)],
    ["Mixing zone (hot)", "Single-faith zone (cold)"], "Not significant")
print(wards.diversity_cluster.value_counts().to_string())
print("\nStates with most mixing-zone wards:")
print(wards.loc[wards.diversity_cluster == "Mixing zone (hot)", "statename"].value_counts().head(6).to_string())

colours = wards.diversity_cluster.map({"Mixing zone (hot)": DSN_RED, "Single-faith zone (cold)": "#0571b0",
                                      "Not significant": "#eeeeee"})
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
choropleth("church_share", "Church share of faith institutions", cmap="coolwarm", ax=axes[0])
wards.set_geometry("geometry_plot").plot(color=colours, ax=axes[1], linewidth=0.2, edgecolor=EDGE)
axes[1].legend(handles=[mpatches.Patch(color=DSN_RED, label="Mixing zone (hot)"),
                        mpatches.Patch(color="#0571b0", label="Single-faith zone (cold)")],
               loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, frameon=False)
base_map(axes[1], "Gi* clusters of faith diversity")
plt.tight_layout(); plt.show()
""")
interp("uc3_b")

# =============================================================================
# USE CASE 4
# =============================================================================
md(r"""
<a id="uc4"></a>

## Use Case 4: Healthcare deserts

**The problem.** A state health ministry has a limited fleet of mobile clinics. Which areas should they serve first?

**Hypothesis.**
- $H_0$: wards with large populations and no registered health facility are scattered at random.
- $H_1$: these "healthcare deserts" form contiguous clusters, where a single mobile route can serve many wards.

**The usual approach.** List every ward with more than 17,000 residents and zero registered facilities, sorted by population.
""")
code(r"""
wards["desert"] = (wards.pop_2025_sum > 17_000) & (wards.health_facilities_count == 0)
deserts = wards[wards.desert].sort_values("pop_2025_sum", ascending=False)
print(f"Healthcare deserts: {len(deserts):,} wards, {deserts.pop_2025_sum.sum()/1e6:.1f} million residents")
print(deserts[["wardname", "lganame", "statename", "pop_2025_sum"]].head(8).round(0).to_string(index=False))
""")
interp("uc4_a")
md(r"""
**The spatial statistics approach.** Instead of a flat list, run **Getis-Ord $G_i^*$** on *unserved population* (population in wards with no registered facility, 0 elsewhere). A hot spot is a neighbourhood where unserved people are concentrated beyond chance: exactly where one mobile route reaches the most people.
""")
code(r"""
unserved = np.where(wards.health_facilities_count == 0, wards.pop_2025_sum, 0.0)
gi_unserved = esda.G_Local(unserved, w, star=True, permutations=999, seed=42)
wards["unserved_hotspot"] = (gi_unserved.Zs > 0) & (gi_unserved.p_sim < 0.05)

print(f"Hot-spot wards: {wards.unserved_hotspot.sum():,}")
print(f"Deserts inside hot spots: {(wards.desert & wards.unserved_hotspot).sum():,} of {wards.desert.sum():,}")
print("\nStates with the most hot-spot wards:")
print(wards[wards.unserved_hotspot].statename.value_counts().head(6).to_string())

fig, ax = plt.subplots(figsize=(7, 6))
wards.set_geometry("geometry_plot").plot(color="#eeeeee", ax=ax, linewidth=0.2, edgecolor=EDGE)
wards[wards.unserved_hotspot].set_geometry("geometry_plot").plot(color=DSN_RED, ax=ax, linewidth=0.2, edgecolor=EDGE)
wards[wards.desert].set_geometry(wards[wards.desert].centroid).plot(ax=ax, color="#0f172a", markersize=1)
ax.legend(handles=[mpatches.Patch(color=DSN_RED, label="Gi* hot spot of unserved population"),
                   mpatches.Patch(color="#0f172a", label="Desert ward (dot)")], loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, frameon=False)
base_map(ax, "Where unserved populations concentrate")
plt.show()
""")
interp("uc4_b")

# =============================================================================
# USE CASE 5
# =============================================================================
md(r"""
<a id="uc5"></a>

## Use Case 5: Retail expansion

**The problem.** A supermarket chain wants to open new branches where customers have money to spend but markets are scarce *in the surrounding area* (not just in one ward).

**Hypothesis.**
- $H_0$: market density around a ward is unrelated to the ward's purchasing power.
- $H_1$: there are significant pockets where high purchasing power sits beside low market supply (under-served demand).

**The usual approach.** Correlate purchasing power with markets per 10,000 people.
""")
code(r"""
wards["markets_per_10k"] = wards.markets_count / wards.pop_2025_sum * 1e4
r5 = np.corrcoef(wards.purchasing_power, wards.markets_per_10k)[0, 1]
print(f"Pearson r (purchasing power vs markets per 10k people): {r5:.3f}")
""")
interp("uc5_a")
md(r"""
**The spatial statistics approach.** A **bivariate LISA** of purchasing power (in the ward) against markets per 10k (in the neighbours). The **High-Low** category (high purchasing power, low market supply around) is the expansion shortlist.
""")
code(r"""
retail = esda.Moran_Local_BV(wards.purchasing_power.values, wards.markets_per_10k.values, w,
                             permutations=999, seed=42)
retail_labels = {1: "High power, many markets around", 2: "Low power, many markets around",
                 3: "Low power, few markets around", 4: "High power, few markets around (target)",
                 0: "Not significant"}
print(lisa_summary(retail, labels=retail_labels).to_string())

targets = wards[(retail.q == 4) & (retail.p_sim < 0.05)]
print("\nTop target states:"); print(targets.statename.value_counts().head(6).to_string())
lisa_map(retail, "Bivariate LISA: purchasing power vs neighbours' market supply", labels=retail_labels)
plt.show()
""")
interp("uc5_b")

# =============================================================================
# USE CASE 6
# =============================================================================
md(r"""
<a id="uc6"></a>

## Use Case 6: Water inequality

**The problem.** A WASH programme needs to show donors how unequal water-point provision is, and where the largest *contiguous* water deserts are.

**Hypothesis.**
- $H_0$: water points per person are spread evenly and without spatial pattern.
- $H_1$: provision is highly unequal and the gaps cluster geographically.

**The usual approach.** A Gini coefficient and Lorenz curve of water points across wards.
""")
code(r"""
def gini(values):
    x = np.sort(np.asarray(values, dtype=float)); n = len(x)
    return (2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum())

wp = wards.water_points_count.values
print(f"Gini of water points across wards: {gini(wp):.3f}")
print(f"Wards with no registered water point: {(wp == 0).mean():.1%}")

x = np.sort(wp); lorenz = np.insert(np.cumsum(x) / x.sum(), 0, 0)
fig, ax = plt.subplots(figsize=(4.5, 4.5))
ax.plot(np.linspace(0, 1, len(lorenz)), lorenz, color=DSN_RED, lw=2.5, label="Water points")
ax.plot([0, 1], [0, 1], "k--", lw=1, label="Perfect equality")
ax.set_xlabel("cumulative share of wards"); ax.set_ylabel("cumulative share of water points")
ax.set_title("Lorenz curve", loc="left"); ax.legend(frameon=False); plt.show()
""")
interp("uc6_a")
md(r"""
**The spatial statistics approach.** The Gini says *how unequal*, not *where*. Moran's $I$ and LISA on water points per 10,000 people (log-scaled) reveal **Low-Low clusters**: contiguous water deserts where a single borehole programme can cover many neighbouring wards.
""")
code(r"""
wards["water_per_10k_log"] = np.log1p(wards.water_points_count / wards.pop_2025_sum * 1e4)
moran_w = esda.Moran(wards.water_per_10k_log.values, w, permutations=999)
print(f"Moran's I (water points per 10k, log) = {moran_w.I:.3f}, pseudo p = {moran_w.p_sim:.3f}")

lisa_w = esda.Moran_Local(wards.water_per_10k_log.values, w, permutations=999, seed=42)
print(lisa_summary(lisa_w).to_string())
water_deserts = wards[(lisa_w.q == 3) & (lisa_w.p_sim < 0.05)]
print(f"\nPeople living in Low-Low water-desert clusters: {water_deserts.pop_2025_sum.sum()/1e6:.1f} million")
print(water_deserts.statename.value_counts().head(6).to_string())
lisa_map(lisa_w, "LISA clusters of water points per 10k people"); plt.show()
""")
interp("uc6_b")

# =============================================================================
# USE CASE 7
# =============================================================================
md(r"""
<a id="uc7"></a>

## Use Case 7: School provision, and honest $p$-values

**The problem.** The education ministry asks: does purchasing power predict how many schools a ward has, after accounting for population and area? They will use the $p$-values to justify funding rules.

**Hypothesis.**
- $H_0$: once population and area are controlled for, purchasing power has no effect on school counts.
- $H_1$: wealthier wards have more schools.

**The usual approach.** Ordinary Least Squares (OLS) on the log of school counts.
""")
code(r"""
y7 = np.log1p(wards.schools_count.values).reshape(-1, 1)
X7 = np.column_stack([np.log(wards.pop_2025_sum), wards.purchasing_power, np.log(wards.ward_area_sqkm)])
names7 = ["log_population", "purchasing_power", "log_area"]
ols7 = spreg.OLS(y7, X7, w=w, spat_diag=True, moran=True, name_y="log_schools", name_x=names7)
print(pd.DataFrame({"coef": ols7.betas.ravel(), "std_err": ols7.std_err, "p": [t[1] for t in ols7.t_stat]},
                   index=["constant"] + names7).round(4).to_string())
print(f"\nR^2 = {ols7.r2:.3f}")
""")
interp("uc7_a")
md(r"""
**The spatial statistics approach.** OLS assumes the errors are independent. Test that with **Moran's $I$ on the residuals**, then use the **Lagrange Multiplier (LM) tests** to choose between a Spatial Lag and a Spatial Error model. If LM-error dominates, fit a **Spatial Error Model** (here the heteroskedasticity-robust GMM version).
""")
code(r"""
print(f"Residual Moran's I = {ols7.moran_res[0]:.3f} (z = {ols7.moran_res[1]:.1f})")
diag = pd.DataFrame({"statistic": [ols7.lm_lag[0], ols7.lm_error[0], ols7.rlm_lag[0], ols7.rlm_error[0]],
                     "p": [ols7.lm_lag[1], ols7.lm_error[1], ols7.rlm_lag[1], ols7.rlm_error[1]]},
                    index=["LM-lag", "LM-error", "Robust LM-lag", "Robust LM-error"])
print(diag.round(4).to_string())

sem7 = spreg.GM_Error_Het(y7, X7, w=w, name_y="log_schools", name_x=names7)
compare = pd.DataFrame({"OLS coef": ols7.betas.ravel()[:4], "SEM coef": sem7.betas.ravel()[:4],
                        "OLS std err": ols7.std_err[:4], "SEM std err": sem7.std_err[:4]},
                       index=["constant"] + names7)
print("\n", compare.round(4).to_string())
print(f"\nlambda (spatial error parameter) = {sem7.betas.ravel()[-1]:.3f}")
""")
interp("uc7_b")

# =============================================================================
# USE CASE 8
# =============================================================================
md(r"""
<a id="uc8"></a>

## Use Case 8: Market spillovers

**The problem.** A state government plans to upgrade urban wards and wants to know how many extra markets that brings, *including* markets that appear in neighbouring wards.

**Hypothesis.**
- $H_0$: the number of markets in a ward depends only on the ward's own characteristics.
- $H_1$: markets attract markets next door (spatial contagion), so effects ripple outward.

**The usual approach.** OLS of log market counts on population, urban status and area.
""")
code(r"""
y8 = np.log1p(wards.markets_count.values).reshape(-1, 1)
X8 = np.column_stack([np.log(wards.pop_2025_sum), (wards.urban == "Yes").astype(float),
                      np.log(wards.ward_area_sqkm)])
names8 = ["log_population", "urban", "log_area"]
ols8 = spreg.OLS(y8, X8, w=w, spat_diag=True, name_y="log_markets", name_x=names8)
print(pd.DataFrame({"coef": ols8.betas.ravel(), "p": [t[1] for t in ols8.t_stat]},
                   index=["constant"] + names8).round(4).to_string())
print(f"\nR^2 = {ols8.r2:.3f} | Robust LM-lag = {ols8.rlm_lag[0]:.1f} | Robust LM-error = {ols8.rlm_error[0]:.1f}")
""")
interp("uc8_a")
md(r"""
**The spatial statistics approach.** A **Spatial Lag Model (SAR)**, $y = \rho W y + X\beta + \varepsilon$, estimated by maximum likelihood. Because of the $\rho W y$ term, the raw $\beta$ is *not* the effect: we report **direct** (own ward), **indirect** (spillover to neighbours) and **total** impacts.
""")
code(r"""
from scipy.sparse import SparseEfficiencyWarning
warnings.simplefilter("ignore", SparseEfficiencyWarning)
sar8 = spreg.ML_Lag(y8, X8, w=w, method="LU", spat_impacts="simple", name_y="log_markets", name_x=names8)
print(f"rho = {float(sar8.rho):.3f} | spatial multiplier 1/(1-rho) = {1/(1-float(sar8.rho)):.2f}")
report = str(sar8.summary)
start = report.find("SPATIAL LAG MODEL IMPACTS")
print(report[start:report.find("=====", start)])
""")
interp("uc8_b")

# =============================================================================
# USE CASE 9
# =============================================================================
md(r"""
<a id="uc9"></a>

## Use Case 9: Security coverage

**The problem.** The police service wants to know whether wards without a police station are scattered, or whether whole neighbourhoods of wards are uncovered (making response times worse).

**Hypothesis.**
- $H_0$: wards with no police station are arranged at random.
- $H_1$: uncovered wards cluster together ("security dark zones").

**The usual approach.** The share of wards with no registered police station.
""")
code(r"""
wards["no_police"] = (wards.police_stations_count == 0).astype(int)
print(f"Wards with no registered police station: {wards.no_police.mean():.1%}")
print(wards.groupby("urban").no_police.mean().rename("share without police").round(3).to_string())
""")
interp("uc9_a")
md(r"""
**The spatial statistics approach.** For a yes/no variable we use **Join Counts**: count neighbour pairs that are both "no police" (BB joins) and compare with random shuffles. Then **local join counts** find each ward whose entire neighbourhood is uncovered.
""")
code(r"""
w_binary = libpysal.weights.util.attach_islands(w_queen, w_knn1)
w_binary.transform = "b"
jc = esda.Join_Counts(wards.no_police.values, w_binary, permutations=999)
print(f"BB joins (no-police next to no-police): observed {jc.bb:,.0f}, expected under randomness {jc.mean_bb:,.0f}")
print(f"pseudo p = {jc.p_sim_bb:.3f}")

ljc = esda.Join_Counts_Local(connectivity=w_binary, permutations=999, seed=42).fit(wards.no_police.values)
wards["dark_zone"] = (wards.no_police == 1) & (ljc.p_sim < 0.05)
print(f"\nSignificant security dark-zone wards: {wards.dark_zone.sum():,}")
print(f"People living in them: {wards.loc[wards.dark_zone, 'pop_2025_sum'].sum()/1e6:.1f} million")
print(wards[wards.dark_zone].statename.value_counts().head(6).to_string())

fig, ax = plt.subplots(figsize=(7, 6))
wards.set_geometry("geometry_plot").plot(color="#eeeeee", ax=ax, linewidth=0.2, edgecolor=EDGE)
wards[wards.dark_zone].set_geometry("geometry_plot").plot(color=DSN_RED, ax=ax, linewidth=0.2, edgecolor=EDGE)
base_map(ax, "Local join counts: clusters of wards with no police station")
plt.show()
""")
interp("uc9_b")

# =============================================================================
# USE CASE 10
# =============================================================================
md(r"""
<a id="uc10"></a>

## Use Case 10: One slope or many? (GWR)

**The problem.** A national education policy assumes that as purchasing power rises, school provision per child rises by the same amount everywhere. Is one national rule fair?

**Hypothesis.**
- $H_0$: the relationship between purchasing power and schools per 10,000 people is the same everywhere (stationary).
- $H_1$: the relationship changes across the country (spatial heterogeneity).

To keep the computation fast we work at **LGA level** (wards aggregated into their Local Government Areas).

**The usual approach.** One national OLS slope.
""")
code(r"""
lga = wards.dissolve(by=["statename", "lganame"], aggfunc={"pop_2025_sum": "sum", "schools_count": "sum",
                                                           "purchasing_power": "mean"}).reset_index()
lga = lga[lga.pop_2025_sum > 0].reset_index(drop=True)
lga["schools_per_10k"] = lga.schools_count / lga.pop_2025_sum * 1e4
lga["log_density"] = np.log(lga.pop_2025_sum / (lga.to_crs(3857).area / 1e6))

y10 = lga.schools_per_10k.values.reshape(-1, 1)
X10 = lga[["purchasing_power", "log_density"]].values
ols10 = spreg.OLS(y10, X10, name_y="schools_per_10k", name_x=["purchasing_power", "log_density"])
print(f"LGAs: {len(lga)}")
print(f"National slope for purchasing power: {ols10.betas[1][0]:.2f} (p = {ols10.t_stat[1][1]:.4f})")
print(f"R^2 = {ols10.r2:.3f}")
""")
interp("uc10_a")
md(r"""
**The spatial statistics approach.** **Geographically Weighted Regression** fits a separate regression around every LGA, weighting nearby LGAs more (adaptive bisquare kernel, bandwidth chosen by AICc). The result is a *map of slopes*. We compare its fit to the global model and map where the local slope is significant.
""")
code(r"""
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW

coords = np.column_stack([lga.centroid.x, lga.centroid.y])
Xs = (X10 - X10.mean(0)) / X10.std(0)
ys = (y10 - y10.mean()) / y10.std()
bw = Sel_BW(coords, ys, Xs, kernel="bisquare", fixed=False).search(criterion="AICc")
gwr10 = GWR(coords, ys, Xs, bw, kernel="bisquare", fixed=False).fit()
ols_std = spreg.OLS(ys, Xs)
print(f"Optimal bandwidth: {bw:.0f} nearest LGAs")
print(f"AICc  global OLS = {ols_std.aic:.1f}  |  GWR = {gwr10.aicc:.1f}")
print(f"R^2   global OLS = {ols_std.r2:.3f}  |  GWR = {gwr10.R2:.3f}")

lga["gwr_slope_pp"] = gwr10.params[:, 1]
filtered = gwr10.filter_tvals()[:, 1]
lga["gwr_slope_sig"] = np.where(filtered != 0, lga.gwr_slope_pp, np.nan)
print(f"\nLocal slope for purchasing power ranges from {lga.gwr_slope_pp.min():.2f} to {lga.gwr_slope_pp.max():.2f}")
print(f"Significant positive in {(lga.gwr_slope_sig > 0).sum()} LGAs, significant negative in {(lga.gwr_slope_sig < 0).sum()}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
lga.plot(column="gwr_slope_pp", cmap="RdYlGn", legend=True, ax=axes[0], linewidth=0.2, edgecolor=EDGE)
base_map(axes[0], "GWR local slope: purchasing power -> schools (standardised)")
lga.plot(color="#eeeeee", ax=axes[1], linewidth=0.2, edgecolor=EDGE)
lga.dropna(subset=["gwr_slope_sig"]).plot(column="gwr_slope_sig", cmap="RdYlGn", legend=True, ax=axes[1], linewidth=0.2, edgecolor=EDGE)
base_map(axes[1], "Only where the local slope is significant")
plt.tight_layout(); plt.show()
lga[["statename", "lganame", "gwr_slope_pp", "gwr_slope_sig"]].to_parquet("../data/processed/lga_gwr_results.parquet")
""")
interp("uc10_b")

# =============================================================================
# USE CASE 11
# =============================================================================
md(r"""
<a id="uc11"></a>

## Use Case 11: Malaria and poverty

**The problem.** A malaria programme has bed nets and seasonal chemoprevention for a limited number of areas. Where is prevalence highest, and does poverty explain it?

The data is the **Malaria Atlas Project** *Plasmodium falciparum* parasite rate in children aged 2–10 (PfPR$_{2-10}$) for 2025, averaged within each ward.

**Hypothesis.**
- $H_0$: malaria prevalence is spread randomly and is unrelated to purchasing power.
- $H_1$: prevalence clusters geographically, and poorer wards carry more malaria.

**The usual approach.** Rank wards by prevalence and fit an OLS of prevalence on purchasing power, urban status and population density.
""")
code(r"""
has_mal = wards.malaria_pfpr_2025_pct.notna()
mal = wards[has_mal].reset_index(drop=True)
print(f"Wards with a malaria estimate: {len(mal):,}")
print(mal.malaria_pfpr_2025_pct.describe().round(1).to_string())
print("\nHighest-prevalence states (ward average, %):")
print(mal.groupby("statename").malaria_pfpr_2025_pct.mean().sort_values(ascending=False).head(5).round(1).to_string())

y11 = mal.malaria_pfpr_2025_pct.values.reshape(-1, 1)
X11 = np.column_stack([mal.purchasing_power, (mal.urban == "Yes").astype(float),
                       np.log(mal.pop_2025_sum / mal.ward_area_sqkm)])
names11 = ["purchasing_power", "urban", "log_density"]
w11 = libpysal.weights.util.attach_islands(
    libpysal.weights.Queen.from_dataframe(mal, use_index=False, silence_warnings=True),
    libpysal.weights.KNN.from_dataframe(mal.set_geometry(mal.centroid), k=1))
w11.transform = "r"
ols11 = spreg.OLS(y11, X11, w=w11, spat_diag=True, moran=True, name_y="pfpr_pct", name_x=names11)
print()
print(pd.DataFrame({"coef": ols11.betas.ravel(), "p": [t[1] for t in ols11.t_stat]},
                   index=["constant"] + names11).round(4).to_string())
print(f"\nR^2 = {ols11.r2:.3f}")
""")
interp("uc11_a")
md(r"""
**The spatial statistics approach.** Map where prevalence clusters with **Moran's $I$ and LISA**, then check the OLS residuals with the **LM tests** and refit with the spatial model they point to. Note that the MAP surface is about 5 km per pixel, so small neighbouring wards can share pixels; this smooths the map and makes some autocorrelation expected.
""")
code(r"""
moran_mal = esda.Moran(mal.malaria_pfpr_2025_pct.values, w11, permutations=999)
print(f"Moran's I (malaria prevalence) = {moran_mal.I:.3f}, pseudo p = {moran_mal.p_sim:.3f}")
lisa_mal = esda.Moran_Local(mal.malaria_pfpr_2025_pct.values, w11, permutations=999, seed=42)
hh = (lisa_mal.q == 1) & (lisa_mal.p_sim < 0.05)
print(f"High-High malaria hot-spot wards: {hh.sum():,} with {mal.pop_2025_sum[hh].sum()/1e6:.1f} million people")
print(mal[hh].statename.value_counts().head(6).to_string())

print(f"\nResidual Moran's I = {ols11.moran_res[0]:.3f} | Robust LM-lag = {ols11.rlm_lag[0]:.1f} | "
      f"Robust LM-error = {ols11.rlm_error[0]:.1f}")
sem11 = spreg.GM_Error_Het(y11, X11, w=w11, name_y="pfpr_pct", name_x=names11)
print(pd.DataFrame({"OLS coef": ols11.betas.ravel()[:4], "SEM coef": sem11.betas.ravel()[:4],
                    "OLS std err": ols11.std_err[:4], "SEM std err": sem11.std_err[:4]},
                   index=["constant"] + names11).round(3).to_string())
print(f"lambda = {sem11.betas.ravel()[-1]:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
mal.set_geometry("geometry_plot").plot(column="malaria_pfpr_2025_pct", cmap="YlOrRd", legend=True,
                                       ax=axes[0], linewidth=0.2, edgecolor=EDGE)
base_map(axes[0], "Malaria prevalence, PfPR 2-10 (%), 2025")
cls = np.where(lisa_mal.p_sim < 0.05, lisa_mal.q, 0)
mal.set_geometry("geometry_plot").plot(color=[LISA_COLOURS[c] for c in cls], ax=axes[1],
                                       linewidth=0.2, edgecolor=EDGE)
counts = pd.Series(cls).value_counts()
axes[1].legend(handles=[mpatches.Patch(color=LISA_COLOURS[k], label=f"{LISA_LABELS[k]} ({counts.get(k, 0):,})")
                        for k in (1, 3, 4, 2, 0)],
               loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, frameon=False)
base_map(axes[1], "LISA clusters of malaria prevalence")
plt.tight_layout(); plt.show()
""")
interp("uc11_b")

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                  "language_info": {"name": "python"}}
os.makedirs(os.path.dirname(NB_PATH), exist_ok=True)
if "--text-only" in sys.argv:
    # Refresh markdown only: keep the executed code cells and their outputs.
    executed = nbf.read(NB_PATH, as_version=4)
    fresh_md = [c for c in cells if c.cell_type == "markdown"]
    old_md = [c for c in executed.cells if c.cell_type == "markdown"]
    assert len(fresh_md) == len(old_md), "Cell structure changed: run with --execute instead"
    for old, new in zip(old_md, fresh_md):
        old.source = new.source
    nb = executed
nbf.write(nb, NB_PATH)
print(f"Wrote {NB_PATH}")

PAGER = r"""
<style>
  .uc-pager { position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000; display: flex; align-items: center;
              justify-content: space-between; gap: 12px; padding: 10px 24px; background: #ffffff;
              border-top: 1px solid #e2e8f0; font-family: Inter, system-ui, sans-serif; font-size: 14px; }
  .uc-pager button { border: none; border-radius: 6px; padding: 8px 16px; font-weight: 600; cursor: pointer;
                     background: #00a859; color: #ffffff; }
  .uc-pager button.prev { background: #ed3237; }
  .uc-pager button:disabled { background: #cbd5e1; cursor: default; }
  .uc-pager .uc-title { font-weight: 600; color: #0f172a; text-align: center; flex: 1; }
  body { padding-bottom: 70px !important; }
</style>
<div class="uc-pager">
  <button class="prev" id="ucPrev">&#9664; Previous</button>
  <span class="uc-title" id="ucTitle"></span>
  <button id="ucNext">Next &#9654;</button>
</div>
<script>
(function () {
  const cells = Array.from(document.querySelectorAll(".jp-Cell"));
  const pages = [];
  cells.forEach((cell, i) => {
    if (i === 0 || cell.querySelector('a[id="setup"], a[id^="uc"]')) pages.push([]);
    pages[pages.length - 1].push(cell);
  });
  const titleOf = (page) => {
    const found = page[0].querySelector("h1, h2");
    const h = found ? found.cloneNode(true) : null;
    if (h) h.querySelectorAll(".katex-mathml, .jp-InternalAnchorLink").forEach(n => n.remove());
    return h ? h.textContent.replace(/¶/g, "").trim() : "";
  };
  let current = 0;
  function show(k, anchor) {
    current = Math.max(0, Math.min(pages.length - 1, k));
    pages.forEach((p, i) => p.forEach(c => { c.style.display = i === current ? "" : "none"; }));
    document.getElementById("ucPrev").disabled = current === 0;
    document.getElementById("ucNext").disabled = current === pages.length - 1;
    document.getElementById("ucTitle").textContent = `Page ${current + 1} of ${pages.length}: ${titleOf(pages[current])}`;
    window.scrollTo(0, 0);
    if (anchor) history.replaceState(null, "", "#" + anchor);
  }
  document.getElementById("ucPrev").onclick = () => show(current - 1);
  document.getElementById("ucNext").onclick = () => show(current + 1);
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute("href").slice(1);
    const k = pages.findIndex(p => p.some(c => c.querySelector(`a[id="${id}"]`)));
    if (k >= 0) { e.preventDefault(); show(k, id); }
  });
  const start = location.hash.slice(1);
  const k0 = start ? pages.findIndex(p => p.some(c => c.querySelector(`a[id="${start}"]`))) : 0;
  show(k0 >= 0 ? k0 : 0);
})();
</script>
"""


def paginate_html(path):
    """Show one use case per page (with its code and maps) and add Previous / Next buttons."""
    with open(path, encoding="utf-8") as f:
        html = f.read()
    html = html.replace("</body>", PAGER + "\n</body>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


if "--execute" in sys.argv or "--text-only" in sys.argv:
    if "--execute" in sys.argv:
        subprocess.run([sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
                        "--ExecutePreprocessor.timeout=1800", NB_PATH], check=True)
    subprocess.run([sys.executable, "-m", "nbconvert", "--to", "html", "--output-dir", HTML_DIR, NB_PATH],
                   check=True)
    paginate_html(os.path.join(HTML_DIR, "spatial_statistics_use_cases.html"))
    print(f"Executed and exported paged HTML to {HTML_DIR}")
