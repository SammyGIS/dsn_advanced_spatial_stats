import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import geopandas as gpd
from config import (
    GRID3_DATASETS,
    GRID3_DIR,
    get_logger,
)
from nigeria_geodata import Grid3

logger = get_logger("GetGrid3POIs")


def fetch_grid3_pois():
    """
    Downloads Points of Interest (POIs) from GRID3 datasets such as schools,
    health facilities, markets, churches, etc.
    """
    logger.info("=== Fetching GRID3 POIs ===")
    
    grid3 = Grid3()
    
    for key, dataset_name in GRID3_DATASETS.items():
        out_path = os.path.join(GRID3_DIR, f"grid3_{key}.geojson")
        
        if os.path.exists(out_path):
            logger.info(f"Dataset {key} already exists at {out_path}. Skipping.")
            continue
            
        logger.info(f"Downloading {key} ({dataset_name})...")
        try:
            # Try downloading for the whole country at once
            df = grid3.filter(dataset_name, geodataframe=True)
            if df is not None and not df.empty:
                df.to_file(out_path, driver="GeoJSON")
                logger.info(f"Successfully saved {key} to {out_path} ({len(df)} records)")
            else:
                logger.warning(f"Returned empty dataset for {key}")
        except Exception as e:
            logger.error(f"Failed to fetch {key}: {e}")

if __name__ == "__main__":
    fetch_grid3_pois()
