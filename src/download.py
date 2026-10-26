import ee
from auth import initialize_earth_engine
from config import *
from utils import get_roi

initialize_earth_engine()
roi = get_roi()

collection = (
    ee.ImageCollection("COPERNICUS/S1_GRD")
    .filterBounds(roi)
    .filter(ee.Filter.eq("instrumentMode", INSTRUMENT_MODE))
    .filter(
        ee.Filter.listContains(
            "transmitterReceiverPolarisation",
            POLARIZATION
        )
    )
)

before = (
    collection
    .filterDate(BEFORE_START, BEFORE_END)
    .select(POLARIZATION)
    .median()
    .clip(roi)
)

after = (
    collection
    .filterDate(AFTER_START, AFTER_END)
    .select(POLARIZATION)
    .median()
    .clip(roi)
)

print("Before image:")
print(before.getInfo()["bands"])

print()

print("After image:")
print(after.getInfo()["bands"])
