import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rasterio
import numpy as np
from config import (
    WORLDPOP_AGESEX_BASE_URL,
    DEMOGRAPHICS_DIR,
    CHILDREN_U5_PATH,
    WOMEN_15_49_PATH,
    get_logger
)
from utils.download import download_file

logger = get_logger("GetDemographics")

def fetch_and_sum_rasters(cohorts: list, output_path: str):
    """Downloads individual age/sex rasters and sums them into a single raster."""
    if os.path.exists(output_path):
        logger.info(f"Aggregated raster {output_path} already exists. Skipping.")
        return output_path

    logger.info(f"Aggregating {len(cohorts)} rasters into {output_path}...")
    
    downloaded_files = []
    # Download all necessary rasters
    for cohort in cohorts:
        filename = f"nga_{cohort}_2020.tif"
        url = f"{WORLDPOP_AGESEX_BASE_URL}{filename}"
        local_path = os.path.join(DEMOGRAPHICS_DIR, filename)
        
        if not os.path.exists(local_path):
            logger.info(f"Downloading {filename}...")
            download_file(url, local_path)
        downloaded_files.append(local_path)

    # Read and sum
    logger.info(f"Summing rasters for {output_path}...")
    with rasterio.open(downloaded_files[0]) as src:
        meta = src.meta.copy()
        nodata = src.nodata
        sum_array = np.zeros((src.height, src.width), dtype=np.float32)
        valid_mask = np.zeros((src.height, src.width), dtype=bool)

    for f in downloaded_files:
        with rasterio.open(f) as src:
            data = src.read(1)
            # Mask out nodata values before summing
            mask = data != nodata
            sum_array[mask] += data[mask]
            valid_mask = valid_mask | mask

    # Set nodata where all were nodata
    sum_array[~valid_mask] = -99999.0
    meta.update(dtype=rasterio.float32, nodata=-99999.0)

    # Write output
    with rasterio.open(output_path, 'w', **meta) as dst:
        dst.write(sum_array, 1)

    logger.info(f"Saved aggregated raster to {output_path}")
    return output_path

def fetch_demographics():
    logger.info("=== Fetching WorldPop Demographic Data ===")
    
    # Children Under 5 (f_0, m_0, f_1, m_1)
    children_cohorts = ['f_0', 'm_0', 'f_1', 'm_1']
    fetch_and_sum_rasters(children_cohorts, CHILDREN_U5_PATH)
    
    # Women 15-49
    women_cohorts = ['f_15', 'f_20', 'f_25', 'f_30', 'f_35', 'f_40', 'f_45']
    fetch_and_sum_rasters(women_cohorts, WOMEN_15_49_PATH)

if __name__ == "__main__":
    fetch_demographics()
