import os
from dotenv import load_dotenv

# Load variables from .env file into the operating system's environment
load_dotenv()

# --- API CONFIGURATION ---
API_KEY = os.getenv("LIBRARIES_API_KEY")
BASE_URL = "https://libraries.io/api"

# --- LOCAL FILE CONFIGURATION ---
SEED_FILE = "seed_libraries.csv"
LOG_FILE = "pipeline_execution.txt"

# --- GCP CONFIGURATION ---
# We grab the bucket name so our storage.py script knows where to upload data
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# Note: We are keeping the WATERMARK_FILE name, but in storage.py 
# we will point this to GCS instead of your local laptop.
WATERMARK_FILE = "watermark_state.json"