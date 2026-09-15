import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats
from config import (
    WARD_BOUNDARIES_PATH,
    CLIPPED_RWI_PATH,
    WORLDPOP_2025_PATH,
    CHILDREN_U5_PATH,
    WOMEN_15_49_PATH,
    PROCESSED_DATA_DIR,
    get_logger
)

logger = get_logger("ZonalStats")


def compute_zonal_statistics():
    """
    Computes zonal statistics for RWI and Population (2025)
    aggregated at the Nigeria Ward level.
    """
    logger.info("=== Computing Zonal Statistics ===")

    # Load boundaries
    if not os.path.exists(WARD_BOUNDARIES_PATH):
        logger.error(f"Ward boundaries not found at {WARD_BOUNDARIES_PATH}")
        return

    logger.info("Loading ward boundaries...")
    wards = gpd.read_file(WARD_BOUNDARIES_PATH)
    
    # Keep only relevant administrative columns
    keep_cols = ["wardname", "wardcode", "lganame", "lgacode", "statename", "statecode", "geometry"]
    wards = wards[[c for c in keep_cols if c in wards.columns]]
    
    # Filter out empty or None geometries to prevent rasterstats errors
    wards = wards[wards.geometry.notnull() & ~wards.geometry.is_empty]
    
    # RWI Zonal Stats
    logger.info("Calculating RWI zonal stats...")
    if os.path.exists(CLIPPED_RWI_PATH):
        rwi_stats = zonal_stats(
            wards, 
            CLIPPED_RWI_PATH,
            stats=["mean", "median", "std", "min", "max"],
            prefix="rwi_",
            geojson_out=False,
            nodata=-9999.0
        )
        rwi_df = pd.DataFrame(rwi_stats)
        for col in rwi_df.columns:
            wards[col] = rwi_df[col]
    else:
        logger.warning(f"RWI raster not found at {CLIPPED_RWI_PATH}. Skipping RWI.")

    # Population 2025 Zonal Stats
    logger.info("Calculating Population 2025 zonal stats...")
    if os.path.exists(WORLDPOP_2025_PATH):
        pop_stats = zonal_stats(
            wards,
            WORLDPOP_2025_PATH,
            stats=["sum"],
            prefix="pop_2025_",
            geojson_out=False,
            nodata=-99999.0
        )
        pop_df = pd.DataFrame(pop_stats)
        wards["pop_2025_sum"] = pop_df["pop_2025_sum"]
    else:
        logger.warning(f"Population raster not found at {WORLDPOP_2025_PATH}. Skipping Population.")
        
    # Children < 5 Zonal Stats
    logger.info("Calculating Children < 5 zonal stats...")
    if os.path.exists(CHILDREN_U5_PATH):
        child_stats = zonal_stats(
            wards,
            CHILDREN_U5_PATH,
            stats=["sum"],
            prefix="children_u5_",
            geojson_out=False,
            nodata=-99999.0
        )
        child_df = pd.DataFrame(child_stats)
        wards["children_u5_sum"] = child_df["children_u5_sum"]
    else:
        logger.warning(f"Children < 5 raster not found at {CHILDREN_U5_PATH}. Skipping.")

    # Women 15-49 Zonal Stats
    logger.info("Calculating Women 15-49 zonal stats...")
    if os.path.exists(WOMEN_15_49_PATH):
        women_stats = zonal_stats(
            wards,
            WOMEN_15_49_PATH,
            stats=["sum"],
            prefix="women_15_49_",
            geojson_out=False,
            nodata=-99999.0
        )
        women_df = pd.DataFrame(women_stats)
        wards["women_15_49_sum"] = women_df["women_15_49_sum"]
    else:
        logger.warning(f"Women 15-49 raster not found at {WOMEN_15_49_PATH}. Skipping.")
        
    # Ward Area & Population Density
    logger.info("Calculating area and population density...")
    # Reproject to a metric CRS for area calculation (UTM Zone 32N for Nigeria)
    wards_proj = wards.to_crs(epsg=32632)
    wards["ward_area_sqkm"] = wards_proj.geometry.area / 1e6
    
    if "pop_2025_sum" in wards.columns:
        wards["population_density_per_sqkm"] = wards["pop_2025_sum"] / wards["ward_area_sqkm"]
        wards["population_density_per_sqkm"] = wards["population_density_per_sqkm"].fillna(0)

    # Save outputs to staging
    out_path = os.path.join(PROCESSED_DATA_DIR, "wards_with_zonal_stats.parquet")
    logger.info(f"Saving zonal stats to {out_path}...")
    wards.to_parquet(out_path)
    logger.info("Zonal stats computation complete.")

if __name__ == "__main__":
    compute_zonal_statistics()
