import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import geopandas as gpd
from config import (
    PROCESSED_DATA_DIR,
    FINAL_MASTER_PARQUET,
    FINAL_MASTER_GPKG,
    FINAL_MASTER_CSV,
    get_logger
)

logger = get_logger("MergeWardMaster")


def export_final_master():
    """
    Exports the fully enriched Ward dataset to multiple formats (Parquet, GPKG, CSV).
    """
    logger.info("=== Exporting Final Master Dataset ===")

    in_path = os.path.join(PROCESSED_DATA_DIR, "wards_with_pois.parquet")
    if not os.path.exists(in_path):
        logger.error(f"Input file not found at {in_path}. Run aggregate_pois.py first.")
        return

    logger.info("Loading fully enriched dataset...")
    wards = gpd.read_parquet(in_path)
    
    # Save as Parquet (final name)
    logger.info(f"Saving to {FINAL_MASTER_PARQUET}...")
    wards.to_parquet(FINAL_MASTER_PARQUET)
    
    logger.info("Master export complete.")

if __name__ == "__main__":
    export_final_master()
