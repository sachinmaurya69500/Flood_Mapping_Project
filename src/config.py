
import os


# Set EE_PROJECT_ID in the shell to use a different Google Cloud project.
# This default matches the project used by src/download.py.
PROJECT_ID = os.getenv("EE_PROJECT_ID", "")
POLARIZATION = os.getenv("POLARIZATION", "VV")
BEFORE_START = os.getenv("BEFORE_START", "2018-07-20")
BEFORE_END = os.getenv("BEFORE_END", "2018-08-05")
AFTER_START = os.getenv("AFTER_START", "2018-08-20")
AFTER_END = os.getenv("AFTER_END", "2018-09-05")
SCALE = int(os.getenv("SCALE", "10"))

# Sentinel-1 settings

INSTRUMENT_MODE = os.getenv("INSTRUMENT_MODE", "IW")
ORBIT_DIRECTION = os.getenv("ORBIT_DIRECTION", "DESCENDING")
RESOLUTION = int(os.getenv("RESOLUTION", "10"))
EXPORT_FOLDER = os.getenv("EXPORT_FOLDER", "FloodMapping")
