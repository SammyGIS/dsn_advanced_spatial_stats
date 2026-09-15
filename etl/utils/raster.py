import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import geopandas as gpd
import pyogrio
import rasterio
import rasterio.crs
import rasterio.mask
import rasterio.warp
import shapely

from config import get_logger

logger = get_logger("Utils_Raster")


def _get_boundary_shapes(boundary_path: str, working_crs) -> list:
    """Read the bounds of the boundary file and return shapely mapping in working_crs."""
    info = pyogrio.read_info(boundary_path)
    total_bounds = info["total_bounds"]
    bbox_geom = shapely.box(*total_bounds)
    
    bbox_gdf = gpd.GeoDataFrame(geometry=[bbox_geom], crs="EPSG:4326").to_crs(working_crs)
    return [shapely.geometry.mapping(bbox_gdf.geometry.values[0])]


def _resolve_working_crs(src_crs):
    """Resolve pseudo-mercator issues from src raster to standard EPSG:3857 if needed."""
    crs_str = str(src_crs)
    if "Pseudo-Mercator" in crs_str or "3857" in crs_str:
        return rasterio.crs.CRS.from_epsg(3857)
    return src_crs


def _mask_raster(src, shapes):
    """Masks a rasterio dataset with a set of shapes."""
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    return out_image, out_transform


def _save_raster_direct(out_raster_path, out_meta, out_image):
    """Directly save an array to a raster if crs matches."""
    with rasterio.open(out_raster_path, "w", **out_meta) as dst:
        dst.write(out_image)


def _save_raster_reproject(out_raster_path, out_meta, out_image, out_transform, working_crs, target_crs, dtype_str, src_nodata, out_nodata):
    """Reproject an array and save to a raster if crs doesn't match."""
    bounds_src = rasterio.transform.array_bounds(out_image.shape[1], out_image.shape[2], out_transform)
    transform, width, height = rasterio.warp.calculate_default_transform(
        working_crs, target_crs, out_image.shape[2], out_image.shape[1], *bounds_src
    )
    
    out_meta.update({
        "crs": target_crs,
        "transform": transform,
        "width": width,
        "height": height
    })
    
    resampling = rasterio.warp.Resampling.nearest if "int" in dtype_str else rasterio.warp.Resampling.bilinear

    with rasterio.open(out_raster_path, "w", **out_meta) as dst:
        rasterio.warp.reproject(
            source=out_image,
            destination=rasterio.band(dst, 1),
            src_transform=out_transform,
            src_crs=working_crs,
            src_nodata=src_nodata,
            dst_transform=transform,
            dst_crs=target_crs,
            dst_nodata=out_nodata,
            resampling=resampling,
        )


def clip_raster_to_boundary(src_raster_path: str, out_raster_path: str, boundary_path: str, target_crs: str = "EPSG:4326") -> str:
    """Clip and reproject an input raster to the bounding envelope of an administrative boundary."""
    if os.path.exists(out_raster_path) and os.path.getsize(out_raster_path) > 100_000:
        logger.info(f"Clipped raster already exists at {out_raster_path}. Skipping.")
        return out_raster_path

    os.makedirs(os.path.dirname(os.path.abspath(out_raster_path)), exist_ok=True)
    t0 = time.time()
    logger.info(f"Clipping raster {os.path.basename(src_raster_path)} to boundary...")

    with rasterio.open(src_raster_path) as src:
        working_crs = _resolve_working_crs(src.crs)
        shapes = _get_boundary_shapes(boundary_path, working_crs)
        
        out_image, out_transform = _mask_raster(src, shapes)
        out_meta = src.meta.copy()
        
        src_nodata = src.nodata
        dtype_str = str(src.dtypes[0])

    out_nodata = src_nodata if src_nodata is not None else (-9999.0 if "float" in dtype_str else 0)

    out_meta.update({
        "driver": "GTiff",
        "nodata": out_nodata,
        "compress": "lzw",
    })

    if str(working_crs) == str(target_crs) or working_crs == rasterio.crs.CRS.from_string(target_crs):
        out_meta.update({
            "crs": target_crs,
            "transform": out_transform,
            "width": out_image.shape[2],
            "height": out_image.shape[1]
        })
        _save_raster_direct(out_raster_path, out_meta, out_image)
    else:
        _save_raster_reproject(out_raster_path, out_meta, out_image, out_transform, working_crs, target_crs, dtype_str, src_nodata, out_nodata)

    duration = time.time() - t0
    logger.info(f"Clipped raster saved to {out_raster_path} ({os.path.getsize(out_raster_path) / 1e6:.1f} MB) in {duration:.2f}s")
    return out_raster_path
