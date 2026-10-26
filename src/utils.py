import ee


def get_roi(bbox=None):
    """Return the configured ROI, or a [west, south, east, north] bounding box."""
    if bbox is not None:
        if len(bbox) != 4:
            raise ValueError("bbox must contain west, south, east, north")
        west, south, east, north = map(float, bbox)
        if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
            raise ValueError("Invalid geographic bounds")
        return ee.Geometry.Rectangle([west, south, east, north])

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
