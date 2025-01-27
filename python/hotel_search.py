from config import AVIATIONSTACK_API_KEY, HOTEL_API_KEY, OPENAI_API_KEY
import requests
import urllib.parse
from datetime import datetime, timedelta


def get_city_id(city_name):
    """
    Retrieve the city ID for a given city name using the Makcorps Mapping API.
    Ensure the city name is URL encoded.
    """
    city_name_encoded = urllib.parse.quote(city_name.strip())  # URL encode the city name

    url = "https://api.makcorps.com/mapping"
    params = {
        'api_key': HOTEL_API_KEY,
        'name': city_name_encoded  # Use the encoded city name
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]['document_id']
        else:
            print(f"City '{city_name}' not found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching city ID: {e}")
        return None

def get_hotels_by_city_id(city_id, rooms, adults, checkin, checkout, currency='USD'):
    """
    Use Makcorps Hotel API to find hotels in a city by city ID.
    """
    url = "https://api.makcorps.com/city"
    params = {
        'api_key': HOTEL_API_KEY,
        'cityid': city_id,
        'pagination': 0,  # Page number, starts with 0
        'cur': currency,
        'rooms': rooms,
        'adults': adults,
        'checkin': checkin,
        'checkout': checkout
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        hotels = response.json()
        if hotels:
            for hotel in hotels:
                hotel_name = hotel.get('name', 'No name available')
                hotel_price = hotel.get('price1', 'No price available')  # Adjusted for price1
                hotel_vendor = hotel.get('vendor1', 'No vendor available')
                hotel_rating = hotel.get('reviews', {}).get('rating', 'No rating')
                print(f"Hotel: {hotel_name}")
                print(f"Price: {hotel_price} {currency}")
                print(f"Vendor: {hotel_vendor}")
                print(f"Rating: {hotel_rating}")
                print("-" * 50)
        else:
            print("No hotels found.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hotel data: {e}")
