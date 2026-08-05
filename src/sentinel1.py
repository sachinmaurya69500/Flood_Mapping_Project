import ee


class Sentinel1Downloader:

    def __init__(self, roi):

        self.roi = roi

        self.collection = (
            ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(self.roi)
            .filter(
                ee.Filter.eq(
                    "instrumentMode",
                    "IW"
                )
            )
            .filter(
                ee.Filter.listContains(
                    "transmitterReceiverPolarisation",
                    "VV"
                )
            )
            .filter(
                ee.Filter.eq(
                    "resolution_meters",
                    10
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
            .select("VV")
            .median()
            .clip(self.roi)
        )

        return image