"""
fetch_sentinel.py
Pull the least-cloudy Sentinel-2 L2A tile for a given AOI + date range.
Returns the local path to the visual (true-color) GeoTIFF.
"""

import tempfile
from pathlib import Path
import pystac_client
import planetary_computer
import rasterio
from pystac.extensions.eo import EOExtension as eo

def fetch_least_cloudy(
    aoi: dict,
    date_range: str,
    max_cloud: int = 10,
    out_dir: Path = Path("MLOps/Wildfire/data/raw"),
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects=aoi,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": max_cloud}},
    )
    items = search.item_collection()
    if not items:
        raise RuntimeError("No tiles found")
    best = min(items, key=lambda it: eo.ext(it).cloud_cover)
    href = best.assets["visual"].href
    local_path = out_dir / f"{best.id}_visual.tif"

    if not local_path.exists():
        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
            tmp_path = tmp.name
        with rasterio.open(href) as src:
            profile = src.profile
            data = src.read()
        with rasterio.open(tmp_path, "w", **profile) as dst:
            dst.write(data)
        Path(tmp_path).rename(local_path)

    return local_path
