from config import AVIATIONSTACK_API_KEY, HOTEL_API_KEY, OPENAI_API_KEY
import openai
from datetime import datetime, timedelta
openai.api_key = OPENAI_API_KEY

# Function to generate itinerary
def generate_itinerary(days, city):
    prompt = f"Create a travel itinerary for a {days}-day trip to {city}. Each day should have a list of recommended activities and places to visit."
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating itinerary: {e}"
