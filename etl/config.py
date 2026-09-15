import os
import sys

# Configure PROJ directory before C-extensions load to prevent external PROJ conflicts on Windows
_PROJ_DIR = os.path.join(sys.prefix, "Lib", "site-packages", "rasterio", "proj_data")
if not os.path.exists(_PROJ_DIR):
    _PROJ_DIR = os.path.join(sys.prefix, "Lib", "site-packages", "pyproj", "proj_dir", "share", "proj")
if os.path.exists(_PROJ_DIR):
    os.environ["PROJ_LIB"] = _PROJ_DIR
    os.environ["PROJ_DATA"] = _PROJ_DIR

import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
STAGING_DATA_DIR = os.path.join(DATA_DIR, "staging")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

BOUNDARIES_DIR = os.path.join(RAW_DATA_DIR, "boundaries")
RWI_RAW_DIR = os.path.join(RAW_DATA_DIR, "rwi")
WORLDPOP_DIR = os.path.join(RAW_DATA_DIR, "worldpop")
GRID3_DIR = os.path.join(RAW_DATA_DIR, "grid3")

DEMOGRAPHICS_DIR = os.path.join(RAW_DATA_DIR, "demographics")

for d in [BOUNDARIES_DIR, RWI_RAW_DIR, WORLDPOP_DIR, GRID3_DIR, DEMOGRAPHICS_DIR, STAGING_DATA_DIR, PROCESSED_DATA_DIR]:
    os.makedirs(d, exist_ok=True)

LOG_DIR = os.path.join(DATA_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "etl.log")

WARD_BOUNDARIES_PATH = os.path.join(BOUNDARIES_DIR, "nigeria_wards.geojson")
RAW_RWI_PATH = os.path.join(RWI_RAW_DIR, "Relative_Wealth_Index.tif")
CLIPPED_RWI_PATH = os.path.join(STAGING_DATA_DIR, "rwi_nigeria.tif")
WORLDPOP_2025_PATH = os.path.join(WORLDPOP_DIR, "nga_pop_2025_100m.tif")

FINAL_MASTER_PARQUET = os.path.join(PROCESSED_DATA_DIR, "nigeria_wards_master.parquet")
FINAL_MASTER_GPKG = os.path.join(PROCESSED_DATA_DIR, "nigeria_wards_master.gpkg")
FINAL_MASTER_CSV = os.path.join(PROCESSED_DATA_DIR, "nigeria_wards_master.csv")

RWI_URL = "https://undpngddlsgeohubdev01.blob.core.windows.net/end-poverty/Relative_Wealth_Index.tif?sv=2026-02-06&ss=b&srt=o&se=2027-09-04T08%3A14%3A24Z&sp=r&sig=vvlA3Dc2UmyZICZSfdO4nhBW3AZD7LLqFgDCxccSguw%3D"
WORLDPOP_2025_URL = "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/NGA/v1/100m/constrained/nga_pop_2025_CN_100m_R2025A_v1.tif"
WORLDPOP_AGESEX_BASE_URL = "https://data.worldpop.org/GIS/AgeSex_structures/Global_2000_2020/2020/NGA/"
WARD_BOUNDARIES_URL = "https://services3.arcgis.com/BU6Aadhn6tbBEdyk/arcgis/rest/services/NGA_Ward_Boundaries/FeatureServer/0/query"

CHILDREN_U5_PATH = os.path.join(DEMOGRAPHICS_DIR, "children_u5.tif")
WOMEN_15_49_PATH = os.path.join(DEMOGRAPHICS_DIR, "women_15_49.tif")

NIGERIA_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Federal Capital Territory",
    "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara",
    "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
    "Sokoto", "Taraba", "Yobe", "Zamfara"
]

GRID3_DATASETS = {
    "churches": "Churches_in_Nigeria",
    "mosques": "Mosques_in_Nigeria",
    "schools": "Schools_in_Nigeria",
    "health_facilities": "GRID3_NGA_health_facility_v3_0",
    "markets": "Markets_in_Nigeria",
    "water_points": "Water_points_in_Nigeria",
    "police_stations": "GRID3_NGA_Police_Stations",
    "fire_stations": "GRID3_NGA_Fire_Stations"
}

STANDARD_CRS = "EPSG:4326"
PROJECTED_CRS = "EPSG:32632"


def get_logger(name: str = "ETL") -> logging.Logger:
    """Configures and returns a logger that logs to both console and log.txt."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
