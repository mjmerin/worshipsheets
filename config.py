import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_bool_env(key, default="False"):
    return os.getenv(key, default).lower() == "true"

# AdSense Configuration
SHOW_ADS = get_bool_env("SHOW_ADS", "False")
ADSENSE_CLIENT_ID = os.getenv("ADSENSE_CLIENT_ID", "")

ADSENSE_SLOTS = {
    "login": os.getenv("ADSENSE_SLOT_LOGIN", ""),
    "result": os.getenv("ADSENSE_SLOT_RESULT", ""),
    "bottom": os.getenv("ADSENSE_SLOT_BOTTOM", "")
}

# App Configuration
APP_PASSWORD = os.getenv("APP_PASSWORD", "NHIC2025")
