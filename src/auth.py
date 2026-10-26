import json
import os

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
        credentials_json = os.getenv("EE_SERVICE_ACCOUNT_JSON")
        if credentials_json:
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(credentials_json),
                scopes=["https://www.googleapis.com/auth/earthengine"],
            )
            ee.Initialize(credentials=credentials, project=PROJECT_ID)
        else:
            ee.Initialize(project=PROJECT_ID)
        print("✓ Earth Engine initialized")

    except ee.EEException:
        print("Authenticating Earth Engine...")
        ee.Authenticate()
        ee.Initialize(project=PROJECT_ID)
        print("✓ Earth Engine initialized after authentication")
