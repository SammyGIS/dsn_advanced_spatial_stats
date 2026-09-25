"""
Add real ward-level malaria prevalence to the master dataset.

Source: Malaria Atlas Project (MAP), Plasmodium falciparum parasite rate (PfPR 2-10),
release 2026-08, year 2025, ~5 km resolution, served through MAP's public WCS.

Steps:
1. Download the Nigeria window of the raster to data/raw/malaria/nga_pfpr_2025.tif (if missing).
2. Average it within each ward polygon (all_touched=True so small urban wards get a value).
3. Write `malaria_pfpr_2025_pct` into data/processed/nigeria_wards_master.parquet and drop
   the earlier simulated teaching columns (malaria_prevalence_pct, malaria_annual_cases_est).
"""

import os
import urllib.request

import geopandas as gpd
import numpy as np
from rasterstats import zonal_stats

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RASTER = os.path.join(BASE, "data", "raw", "malaria", "nga_pfpr_2025.tif")
MASTER = os.path.join(BASE, "data", "processed", "nigeria_wards_master.parquet")
WCS_URL = (
    "https://data.malariaatlas.org/geoserver/Malaria/ows?service=WCS&version=2.0.1&request=GetCoverage"
    "&coverageId=Malaria__202608_Global_Pf_Parasite_Rate&format=image/geotiff"
    "&subset=Lat(4,14)&subset=Long(2.5,15)&subset=time(%222025-01-01T00:00:00.000Z%22)"
)


def main():
    if not os.path.exists(RASTER):
        os.makedirs(os.path.dirname(RASTER), exist_ok=True)
        print("Downloading MAP PfPR 2025 raster for Nigeria...")
        urllib.request.urlretrieve(WCS_URL, RASTER)

    wards = gpd.read_parquet(MASTER)
    stats = zonal_stats(wards.geometry, RASTER, stats=["mean"], all_touched=True, nodata=-9999)
    pfpr = np.array([s["mean"] if s["mean"] is not None else np.nan for s in stats], dtype=float)
    wards["malaria_pfpr_2025_pct"] = np.round(pfpr * 100, 2)
    wards = wards.drop(columns=["malaria_prevalence_pct", "malaria_annual_cases_est"], errors="ignore")
    wards.to_parquet(MASTER)
    print(wards["malaria_pfpr_2025_pct"].describe().round(2).to_string())


if __name__ == "__main__":
    main()
