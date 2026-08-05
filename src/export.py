import ee


class GeoTIFFExporter:

    def __init__(self, image, region):
        self.image = image
        self.region = region

    def export(self, description):

        task = ee.batch.Export.image.toDrive(
            image=self.image,
            description=description,
            folder="FloodMapping",
            fileNamePrefix=description,
            region=self.region.coordinates().getInfo(),
            scale=10,
            maxPixels=1e13,
            fileFormat="GeoTIFF"
        )

        task.start()

        print("Export started.")
        print("Open Google Drive after a few minutes.")