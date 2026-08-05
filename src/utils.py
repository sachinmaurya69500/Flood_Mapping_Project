import ee


def get_roi():

    roi = ee.Geometry.Polygon(
        [
            [
                [76.10, 10.20],
                [76.50, 10.20],
                [76.50, 9.80],
                [76.10, 9.80],
                [76.10, 10.20]
            ]
        ]
    )

    return roi