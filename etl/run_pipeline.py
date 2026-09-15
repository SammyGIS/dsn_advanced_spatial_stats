from config import get_logger
from extract.get_boundaries import fetch_ward_boundaries
from extract.get_rwi import fetch_and_clip_rwi
from extract.get_population import fetch_population_rasters
from extract.get_grid3_pois import fetch_grid3_pois
from extract.get_demographics import fetch_demographics
from transform.zonal_stats import compute_zonal_statistics
from transform.aggregate_pois import aggregate_grid3_pois
from load.merge_ward_master import export_final_master

logger = get_logger("PipelineRunner")

def run_all():
    logger.info("========================================")
    logger.info("  STARTING NIGERIA SPATIAL ETL PIPELINE ")
    logger.info("========================================")
    
    # 1. Download & Prepare Boundaries
    fetch_ward_boundaries()
    
    # 2. Download & Clip RWI
    fetch_and_clip_rwi()
    
    # 3. Download Population Rasters
    fetch_population_rasters()
    
    # 4. Download GRID3 POIs
    fetch_grid3_pois()
    
    # 5. Download WorldPop Demographics
    fetch_demographics()
    
    # 5. Compute Zonal Statistics (RWI & Population)
    compute_zonal_statistics()
    
    # 6. Aggregate POIs to Wards
    aggregate_grid3_pois()
    
    # 7. Merge and Export Final Formats
    export_final_master()
    
    logger.info("========================================")
    logger.info("       PIPELINE COMPLETED SUCCESSFULLY   ")
    logger.info("========================================")

if __name__ == "__main__":
    run_all()
