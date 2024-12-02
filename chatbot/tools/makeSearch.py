import time
import requests
import json
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Define the directory and filename for the log file
log_directory = "chatbot/logs/websearch_log/"
timestamp = datetime.now().strftime("%d - %m - %y - %H_%M_%S")
log_filename = f"search {timestamp}.log"
log_filepath = os.path.join(log_directory, log_filename)

# Ensure the log directory exists
os.makedirs(log_directory, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_filepath,
    filemode='w'
)

def google_web_search(query, api_key = os.getenv("GOOGLE_SEARCH_API_KEY"), search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")):
    """Perform a web search using the Google Custom Search JSON API."""
    logging.info(f"Searching for: {query}")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": 3
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()
        logging.info(f"Search results: {search_results}")
        return json.dumps(search_results)
    except Exception as e:
        logging.error(f"Error performing web search: {e}")
        return json.dumps({"error": "Error performing web search"})

# Example usage
# google_api_key = "YOUR_GOOGLE_API_KEY"
# search_engine_id = "YOUR_SEARCH_ENGINE_ID"
# search_query = "skibidi toilet"
# search_results = google_web_search(search_query)
# print(search_results)
