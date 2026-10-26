import ee
from config import PROJECT_ID


def initialize_earth_engine():
    """
    Initialize Google Earth Engine.
    """

    if not PROJECT_ID or PROJECT_ID == "your-google-cloud-project-id":
        raise ValueError(
            "Earth Engine project is not configured. Set EE_PROJECT_ID to a real "
            "Google Cloud project ID with the Earth Engine API enabled."
        )

    try:
        ee.Initialize(project=PROJECT_ID)
        print("✓ Earth Engine initialized")

    except ee.EEException:
        print("Authenticating Earth Engine...")
        ee.Authenticate()
        ee.Initialize(project=PROJECT_ID)
        print("✓ Earth Engine initialized after authentication")
