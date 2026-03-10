import os 
from dotenv import load_dotenv # read the env file 
load_dotenv() 

API_KEY = os.getenv("LIBRARIES_API_KEY")
BASE_URL = "https://libraries.io/api"# store the root url
COMAPNAY_FILE = "company_libraries.csv"
WATERMARK_FILE = "watermark_state.json"
LOG_FILE = "pipeline_execution_summary.txt"