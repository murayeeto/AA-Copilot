
import json

# Load the configuration from the file once
with open("python/config.json", "r") as f:
    config = json.load(f)

AVIATIONSTACK_API_KEY = config["flight_api_key"]
HOTEL_API_KEY = config["hotel_api_key"]
OPENAI_API_KEY = config["openai_api_key"]
