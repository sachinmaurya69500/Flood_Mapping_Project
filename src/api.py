import os
import sys
from pathlib import Path

import ee
from flask import Flask, jsonify, request, send_from_directory

sys.path.insert(0, str(Path(__file__).resolve().parent))

from auth import initialize_earth_engine
from config import AFTER_END, AFTER_START, BEFORE_END, BEFORE_START, PROJECT_ID
from flood import FloodDetector
from sentinel1 import Sentinel1Downloader
from utils import get_roi
from config import POLARIZATION, SCALE, INSTRUMENT_MODE, RESOLUTION, EXPORT_FOLDER

WEB_DIR = Path(__file__).resolve().parents[1] / "web"
app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({"status": "error", "error": str(error)}), 500

@app.get("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok", "earth_engine_project_configured": bool(PROJECT_ID)})

@app.post("/api/run")
def run_mapping():
    payload = request.get_json(silent=True) or {}
    result = analyze(payload, include_export=True)
    return jsonify(result)


@app.post("/api/analyze")
def analyze_mapping():
    return jsonify(analyze(request.get_json(silent=True) or {}, include_export=True))


def analyze(payload, include_export=False):
    initialize_earth_engine()
    roi = get_roi(payload.get("bbox"))
    polarization = payload.get("polarization", POLARIZATION).upper()
    if polarization not in {"VV", "VH"}:
        raise ValueError("polarization must be VV or VH")
    before_start = payload.get("before_start", BEFORE_START)
    before_end = payload.get("before_end", BEFORE_END)
    after_start = payload.get("after_start", AFTER_START)
    after_end = payload.get("after_end", AFTER_END)
    threshold = float(payload.get("threshold", 3))
    west, south, east, north = map(float, payload.get("bbox") or [68.1, 6.5, 97.4, 35.7])
    # Whole-country requests at 10 m are unnecessarily slow and expensive.
    # Use 100 m for large regions and keep 10 m detail for local analysis.
    region_area = (east - west) * (north - south)
    analysis_scale = int(payload.get("scale", 100 if region_area > 100 else SCALE))
    # Earth Engine limits download dimensions to 32,768 pixels per side.
    # A country-sized GeoTIFF therefore needs a coarser export grid.
    download_scale = max(analysis_scale, 250 if region_area > 100 else analysis_scale)
    sentinel = Sentinel1Downloader(roi)
    collection = sentinel.collection.filter(
        ee.Filter.listContains("transmitterReceiverPolarisation", polarization)
    )
    before = collection.filterDate(before_start, before_end).select(polarization).median().clip(roi)
    after = collection.filterDate(after_start, after_end).select(polarization).median().clip(roi)
    detector = FloodDetector(before, after)
    difference = before.subtract(after)
    mask = detector.clean_mask(difference.gt(threshold))
    area = detector.calculate_area(mask, scale=analysis_scale).getInfo()
    band = next(iter(area), None)
    square_meters = area.get(band, 0) if band else 0
    response = {
        "status": "complete",
        "before": [before_start, before_end], "after": [after_start, after_end],
        "polarization": polarization, "threshold": threshold,
        "scale_m": analysis_scale,
        "download_scale_m": download_scale,
        "image_count": collection.filterDate(before_start, after_end).size().getInfo(),
        "flooded_area_m2": square_meters,
        "flooded_area_km2": square_meters / 1_000_000,
        "layers": {
            "before": before.getMapId({"min": -25, "max": 0}),
            "after": after.getMapId({"min": -25, "max": 0}),
            "difference": difference.getMapId({"min": -5, "max": 5, "palette": ["blue", "white", "red"]}),
            "flood": mask.selfMask().getMapId({"palette": ["00aaff"]}),
        },
    }
    for layer in response["layers"].values():
        layer["url"] = layer.pop("tile_fetcher").url_format
        layer.pop("image", None)
    if include_export:
        if region_area <= 100:
            response["download_url"] = mask.getDownloadURL({"scale": download_scale, "region": roi, "format": "GEO_TIFF"})
        else:
            task = ee.batch.Export.image.toDrive(
                image=mask,
                description="flood_extent_india",
                folder=EXPORT_FOLDER,
                fileNamePrefix="flood_extent_india",
                region=roi.coordinates().getInfo(),
                scale=download_scale,
                maxPixels=1e13,
                fileFormat="GeoTIFF",
            )
            task.start()
            response["export_task"] = task.id
            response["export_message"] = "Whole-region GeoTIFF export started in Google Drive."
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8086")))
