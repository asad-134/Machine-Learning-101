"""
Smoke test for fetch_sentinel.py
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_pipeline.fetch_sentinel import fetch_least_cloudy

def test_smoke():
    """Download one tiny tile to make sure the function runs."""
    aoi = {
        "type": "Polygon",
        "coordinates": [[
            [-148.565, 60.801],
            [-147.443, 60.801],
            [-147.443, 61.184],
            [-148.565, 61.184],
            [-148.565, 60.801],
        ]],
    }
    local_path = fetch_least_cloudy(
        aoi=aoi,
        date_range="2019-06-01/2019-08-01",
        max_cloud=50,
    )
    assert local_path.exists()
    assert local_path.stat().st_size > 0
