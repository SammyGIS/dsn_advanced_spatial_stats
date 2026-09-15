import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
from config import (
    CLIPPED_RWI_PATH,
    RAW_RWI_PATH,
    RWI_URL,
    WARD_BOUNDARIES_PATH,
    get_logger,
)
from utils.raster import clip_raster_to_boundary
from utils.download import download_file

logger = get_logger("GetRWI")


def fetch_and_clip_rwi() -> str:
    """Download the global/regional Relative Wealth Index (RWI) GeoTIFF into raw data,
    and clip the raster to the Nigerian national boundary into the staging folder."""
    logger.info("=== Processing Relative Wealth Index (RWI) ===")

    # Step 1: Download the raw RWI raster
    download_file(RWI_URL, RAW_RWI_PATH, min_expected_mb=25.0)

    # Step 2: Clip to Nigeria boundary into data/staging/
    clip_raster_to_boundary(RAW_RWI_PATH, CLIPPED_RWI_PATH, WARD_BOUNDARIES_PATH)

    logger.info(f"RWI clipping complete. Clipped output at {CLIPPED_RWI_PATH}")
    return CLIPPED_RWI_PATH


if __name__ == "__main__":
    fetch_and_clip_rwi()
