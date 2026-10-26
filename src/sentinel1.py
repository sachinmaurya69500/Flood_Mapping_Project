import ee
from config import INSTRUMENT_MODE, POLARIZATION, RESOLUTION


class Sentinel1Downloader:

    def __init__(self, roi):

        self.roi = roi

        self.collection = (
            ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(self.roi)
            .filter(
                ee.Filter.eq(
                    "instrumentMode",
                    INSTRUMENT_MODE
                )
            )
            .filter(
                ee.Filter.eq(
                    "resolution_meters",
                    RESOLUTION
                )
            )
        )


    def get_image(self, start_date, end_date):

        image = (
            self.collection
            .filterDate(
                start_date,
                end_date
            )
            .select(POLARIZATION)
            .median()
            .clip(self.roi)
        )

        return image
