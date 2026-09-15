import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import pyogrio
from config import WARD_BOUNDARIES_PATH, WARD_BOUNDARIES_URL, get_logger
from utils.download import download_file

logger = get_logger("GetBoundaries")


def fetch_ward_boundaries() -> str:
    """Fetch and verify the Nigeria Admin 3 (Ward Level) boundaries GeoJSON."""
    logger.info("Verifying Nigeria Ward Boundaries (Admin 3)...")

    if not os.path.exists(WARD_BOUNDARIES_PATH):
        logger.info("Boundaries file not found locally. Initiating download...")
        download_file(WARD_BOUNDARIES_URL, WARD_BOUNDARIES_PATH, min_expected_mb=10.0)

    info = pyogrio.read_info(WARD_BOUNDARIES_PATH)
    logger.info(f"Verified Ward Boundaries: {info['features']:,} wards, CRS: {info['crs']}")
    return WARD_BOUNDARIES_PATH


if __name__ == "__main__":
    fetch_ward_boundaries()
