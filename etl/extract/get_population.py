import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
from config import (
    WORLDPOP_2025_PATH,
    WORLDPOP_2025_URL,
    get_logger
)
from utils.download import download_file

logger = get_logger("GetPopulation")

def fetch_population_rasters():
    """
    Downloads the 100m population raster for Nigeria for the year 2025.
    
    Returns:
        tuple: Path to the downloaded 2025 population raster.
    """
    logger.info("=== Processing WorldPop 100m Population Rasters ===")

    download_file(
        url=WORLDPOP_2025_URL,
        dest_path=WORLDPOP_2025_PATH,
        min_expected_mb=100.0,
    )

    return (WORLDPOP_2025_PATH,)


if __name__ == "__main__":
    fetch_population_rasters()
