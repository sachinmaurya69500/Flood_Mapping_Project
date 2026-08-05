import ee
from config import PROJECT_ID


def initialize_earth_engine():
    """
    Initialize Google Earth Engine.
    """

    try:
        ee.Initialize(project=PROJECT_ID)
        print("✓ Earth Engine initialized")

    except Exception:
        print("Authenticating Earth Engine...")
        ee.Authenticate()
        ee.Initialize(project=PROJECT_ID)
        print("✓ Authentication successful")