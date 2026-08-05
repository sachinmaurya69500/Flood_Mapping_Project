from auth import initialize_earth_engine
from sentinel1 import Sentinel1Downloader
from flood import FloodDetector
from utils import get_roi
from config import *
from export import GeoTIFFExporter


def main():

    initialize_earth_engine()

    roi = get_roi()

    sentinel = Sentinel1Downloader(roi)

    print("Total Sentinel-1 Images:")
    print(sentinel.collection.size().getInfo())

    before = sentinel.get_image(
        BEFORE_START,
        BEFORE_END
    )

    after = sentinel.get_image(
        AFTER_START,
        AFTER_END
    )
    before_export = GeoTIFFExporter(
    before,
    roi
    )

    before_export.export(
    "before_flood"
    )


    after_export = GeoTIFFExporter(
    after,
    roi
    )

    after_export.export(
    "after_flood"
    )

    detector = FloodDetector(before, after)

    difference = detector.calculate_difference()

    flood_mask = detector.create_flood_mask(
        threshold=3
    )

    flood_mask = detector.clean_mask(
        flood_mask
    )

    flood_area = detector.calculate_area(
        flood_mask
    )

    area = flood_area.getInfo()

    print("\nFlood Area:")
    print(area)

    if "VV" in area:
        area_km2 = area["VV"] / 1_000_000
        print(f"\nFlooded Area: {area_km2:.2f} km²")

# -------- Export GeoTIFF --------

    exporter = GeoTIFFExporter(
    flood_mask,
    roi
)

    exporter.export("flood_extent")

if __name__ == "__main__":
    main()