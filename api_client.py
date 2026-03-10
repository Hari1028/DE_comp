import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from logger import logger
from config import BASE_URL, API_KEY

# Disable SSL Warnings 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_resilient_session():
    """
    Creates a session that automatically handles 429 rate limits 
    and network instability using exponential backoff.
    """
    session = requests.Session() # Open a reusable connection pool
    session.verify = False 

    # handle the Retry 
    retry = Retry( 
        total=3, # No of try 
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503] 
    )
    adapter = HTTPAdapter(max_retries=retry)# Used to write the retry logic we used to place here 
    session.mount("https://", adapter) # Implement the adapater
    session.mount("http://", adapter)
    return session

def fetch_dependencies(session, platform, library):
    url = f"{BASE_URL}/{platform}/{library}/latest/dependencies?api_key={API_KEY}"
    try:
        response = session.get(url, timeout=10,verify=False) # use the connection pool ,wait for 10 second if server crash , bypass the SSL certificate
        response.raise_for_status()# if the request returned an usucessful status code rasie and error
        return response.json()# return the python dict
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching dependencies for {library}: {e}")
        return None

# handle the pagination part 
'''def fetch_dependencies(session, platform, library):
    """
    Fetches all pages of dependencies for a given library.
    Handles pagination by looping until an empty or partial page is returned.
    """
    base_data = None
    page = 1
    per_page = 100  # Maximize items per request to save API calls
    
    while True:
        # Add page and per_page to the API URL
        url = f"{BASE_URL}/{platform}/{library}/latest/dependencies?api_key={API_KEY}&page={page}&per_page={per_page}"
        
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Libraries.io returns a dictionary with a "dependencies" list inside.
            current_deps = data.get("dependencies", [])
            
            if page == 1:
                # On the first request, keep the entire JSON structure 
                # (which includes runtime_dependencies_count, etc.)
                base_data = data
            else:
                # On subsequent pages, only extract the list of dependencies 
                # and append them to our original base_data
                base_data["dependencies"].extend(current_deps)
            
            # Stop condition: If the API returns fewer items than we asked for,
            # it means we have reached the final page.
            if len(current_deps) < per_page:
                break
                
            page += 1  # Increment to fetch the next page
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching dependencies for {library} on page {page}: {e}")
            # If any page fails, return None so the pipeline doesn't save incomplete data.
            # The watermark won't update, and it will try again cleanly on the next run.
            return None
            
    return base_data'''