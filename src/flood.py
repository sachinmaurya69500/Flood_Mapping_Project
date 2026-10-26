import ee
from config import SCALE


class FloodDetector:

    def __init__(self, before, after):
        self.before = before
        self.after = after

    def calculate_difference(self):
        return self.before.subtract(self.after)

    def create_flood_mask(self, threshold=3):
        difference = self.calculate_difference()
        return difference.gt(threshold)

    def clean_mask(self, mask):
        return (
            mask
            .focal_min(radius=30, units="meters")
            .focal_max(radius=30, units="meters")
        )

    def calculate_area(self, mask, scale=None):
        return (
            mask
            .multiply(ee.Image.pixelArea())
            .reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=self.before.geometry(),
                scale=scale or SCALE,
                maxPixels=1e13
            )
        )
