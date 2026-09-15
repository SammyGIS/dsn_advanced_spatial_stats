import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import geopandas as gpd
from config import (
    GRID3_DATASETS,
    GRID3_DIR,
    PROCESSED_DATA_DIR,
    get_logger
)

logger = get_logger("AggregatePOIs")


def aggregate_grid3_pois():
    """
    Spatially aggregates the downloaded GRID3 POIs into the Nigeria Wards dataset.
    Reads the output from zonal_stats and adds the POI counts.
    """
    logger.info("=== Aggregating GRID3 POIs ===")

    wards_path = os.path.join(PROCESSED_DATA_DIR, "wards_with_zonal_stats.parquet")
    if not os.path.exists(wards_path):
        logger.error(f"Wards data not found at {wards_path}. Run zonal_stats.py first.")
        return

    logger.info("Loading wards data...")
    wards = gpd.read_parquet(wards_path)
    
    for key, dataset_name in GRID3_DATASETS.items():
        poi_path = os.path.join(GRID3_DIR, f"grid3_{key}.geojson")
        
        if not os.path.exists(poi_path):
            logger.warning(f"POI dataset {key} not found at {poi_path}. Skipping.")
            continue
            
        logger.info(f"Aggregating {key}...")
        try:
            pois = gpd.read_file(poi_path)
            # Ensure CRS matches
            if pois.crs != wards.crs:
                pois = pois.to_crs(wards.crs)
                
            # Spatial join to count POIs per ward
            # We assume wards has a unique identifier 'wardcode' or we use index
            wards['ward_index'] = wards.index
            joined = gpd.sjoin(pois, wards[['ward_index', 'geometry']], how="inner", predicate="intersects")
            
            # Count per ward
            counts = joined.groupby('ward_index').size().reset_index(name=f"{key}_count")
            
            # Merge back
            wards = wards.merge(counts, on='ward_index', how='left')
            wards[f"{key}_count"] = wards[f"{key}_count"].fillna(0).astype(int)
            
            logger.info(f"Added {key}_count to wards.")
        except Exception as e:
            logger.error(f"Failed to aggregate {key}: {e}")

    # Drop temporary index
    if 'ward_index' in wards.columns:
        wards = wards.drop(columns=['ward_index'])

    out_path = os.path.join(PROCESSED_DATA_DIR, "wards_with_pois.parquet")
    logger.info(f"Saving aggregated data to {out_path}...")
    wards.to_parquet(out_path)
    logger.info("POI aggregation complete.")

if __name__ == "__main__":
    aggregate_grid3_pois()
