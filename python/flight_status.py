from config import AVIATIONSTACK_API_KEY
import requests
import pandas as pd

# Load airport data
file_path = r"V:/Downloads/React-Landing-Page-Template-master/React-Landing-Page-Template-master/data/airports.csv"
airports_data = pd.read_csv(file_path)

def get_city_from_airport(iata_code):
    """
    Retrieve the city for a given airport IATA code using the CSV data.
    If not found, return "Unknown City".
    """
    airport_info = airports_data[airports_data['iata'] == iata_code]
    if not airport_info.empty:
        return airport_info.iloc[0]['city']
    return "Unknown City"

def get_flight_status(flight_number):
    """
    Fetch flight status for a given flight number from the Aviationstack API.
    Returns structured data about the flight including departure/arrival times, airport names, and status.
    """
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'flight_iata': flight_number
    }

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if data and 'data' in data and len(data['data']) > 0:
            flight_data = data['data'][0]

            # Extract relevant information
            departure_airport = flight_data['departure']['airport']
            arrival_airport = flight_data['arrival']['airport']
            flight_status = flight_data['flight_status']
            departure_time = flight_data['departure']['estimated']
            arrival_time = flight_data['arrival']['estimated']
            arrival_iata = flight_data['arrival']['iata']
            destination_city = get_city_from_airport(arrival_iata)

            # Return structured data
            return {
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "destination_city": destination_city,
                "status": flight_status,
                "departure_time": departure_time,
                "arrival_time": arrival_time
            }
        else:
            print(f"No data found for flight {flight_number}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight status for {flight_number}: {e}")
        return None
