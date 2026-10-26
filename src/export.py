import ee
from config import EXPORT_FOLDER, SCALE


class GeoTIFFExporter:

    def __init__(self, image, region):
        self.image = image
        self.region = region

    def export(self, description):

        task = ee.batch.Export.image.toDrive(
            image=self.image,
            description=description,
            folder=EXPORT_FOLDER,
            fileNamePrefix=description,
            region=self.region.coordinates().getInfo(),
            scale=SCALE,
            maxPixels=1e13,
            fileFormat="GeoTIFF"
        )

        task.start()

        print("Export started.")
        print("Open Google Drive after a few minutes.")
