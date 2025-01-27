from flight_status import get_flight_status
from hotel_search import get_city_id, get_hotels_by_city_id
from itinerary import generate_itinerary
from nascar_races import suggest_nascar_races_v2
from ai_assistant import chat_with_assistant, get_bag_eta
from datetime import datetime, timedelta

def main():
    print("Welcome to the Travel Assistant!")
    while True:
        print("\nHow can I assist you today?")
        print("1. Check flight status")
        print("2. Ask a general question")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            flight_number = input("Enter the flight number: ")
            try:
                arrival_airport, destination_city = get_flight_status(flight_number)
                if arrival_airport:
                    print(f"\nFlight Status for {flight_number}:")
                    print(f"Arrival Airport: {arrival_airport}")
                    print(f"Destination City: {destination_city}")
                    
                    # Ask if the user is staying in the city they arrived at
                    stay_in_city = input(f"Are you going to stay in {destination_city}? (yes/no): ").strip().lower()
                    
                    # Initialize variables for duration and start date
                    duration = 0
                    start_date = None
                    end_date = None
                    
                    # If the user is staying in the arrival city
                    if stay_in_city == "yes":
                        start_date = datetime.strptime(input("Enter your stay's start date (YYYY-MM-DD): "), "%Y-%m-%d")
                        duration = int(input(f"How long will you be staying in {destination_city}? (in days): ").strip())
                        end_date = start_date + timedelta(days=duration)

                        # Ask for hotel needs
                        need_hotel = input("Do you need a hotel? (yes/no): ").strip().lower()
                        if need_hotel == "yes":
                            city_id = get_city_id(destination_city)
                            if city_id:
                                rooms = int(input("How many rooms will you need? "))
                                people = int(input("How many people will be staying? "))
                                checkin = start_date.strftime("%Y-%m-%d")
                                checkout = end_date.strftime("%Y-%m-%d")
                                get_hotels_by_city_id(city_id, rooms, people, checkin, checkout)

                        # Ask if they want an itinerary
                        create_itinerary = input(f"Would you like an itinerary created for your {duration}-day stay in {destination_city}? (yes/no): ").strip().lower()
                        if create_itinerary == "yes":
                            itinerary = generate_itinerary(duration, destination_city)
                            print("\nHere is your itinerary:")
                            print(itinerary)

                    # If the user is NOT staying in the arrival city
                    elif stay_in_city == "no":
                        # Ask for alternative city, state, or country
                        new_location = input(f"Where will you be staying for the duration of your trip (City, State or City, Country)? ").strip()
                        
                        # Initialize the start date and duration for the new location
                        start_date = datetime.strptime(input("Enter your stay's start date (YYYY-MM-DD): "), "%Y-%m-%d")
                        duration = int(input(f"How long will you be staying in {new_location}? (in days): ").strip())
                        end_date = start_date + timedelta(days=duration)

                        # Ask for hotel needs for the new location before asking for room details
                        need_hotel = input(f"Do you need a hotel in {new_location}? (yes/no): ").strip().lower()
                        if need_hotel == "yes":
                            city_id = get_city_id(new_location)
                            if city_id:
                                rooms = int(input("How many rooms will you need? "))
                                people = int(input("How many people will be staying? "))
                                checkin = start_date.strftime("%Y-%m-%d")
                                checkout = end_date.strftime("%Y-%m-%d")
                                get_hotels_by_city_id(city_id, rooms, people, checkin, checkout)

                        # Ask if they want an itinerary for the new location
                        create_itinerary = input(f"Would you like an itinerary created for your {duration}-day stay in {new_location}? (yes/no): ").strip().lower()
                        if create_itinerary == "yes":
                            itinerary = generate_itinerary(duration, new_location)
                            print("\nHere is your itinerary:")
                            print(itinerary)

                    # Suggest NASCAR races based on the new location if the user chose not to stay in arrival city
                    if stay_in_city == "no":
                        suggested_races = suggest_nascar_races_v2(start_date, end_date, new_location)
                    else:
                        suggested_races = suggest_nascar_races_v2(start_date, end_date, destination_city)

                    if suggested_races:
                        print("\nHere are the NASCAR races during your stay:")
                        for race in suggested_races:
                            print(f"Race: {race['Race Name']} | Location: {race['Location']} | Date: {race['Date']}")
                    else:
                        print("No NASCAR races are happening during your stay.")

                else:
                    print("No data found for this flight.")
            except Exception as e:
                print(f"Error fetching flight status: {e}")

        elif choice == "2":
            user_query = input("Ask your question: ")
            try:
                assistant_response = chat_with_assistant(user_query)
                print("\nAI Assistant Response:")
                print(assistant_response)
            except Exception as e:
                print(f"Error processing your query: {e}")

        elif choice == "3":
            print("Thank you for using the Travel Assistant. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    print("Welcome to the Travel Assistant!")
    while True:
        print("\nHow can I assist you today?")
        print("1. Check flight status")
        print("2. Ask a general question")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            flight_number = input("Enter the flight number: ")
            try:
                arrival_airport, destination_city = get_flight_status(flight_number)
                if arrival_airport:
                    print(f"\nFlight Status for {flight_number}:")
                    print(f"Arrival Airport: {arrival_airport}")
                    print(f"Destination City: {destination_city}")
                    
                    # Ask if the user is staying in the city they arrived at
                    stay_in_city = input(f"Are you going to stay in {destination_city}? (yes/no): ").strip().lower()
                    
                    # Initialize variables for duration and start date
                    duration = 0
                    start_date = None
                    end_date = None
                    
                    # If the user is staying in the arrival city
                    if stay_in_city == "yes":
                        start_date = datetime.strptime(input("Enter your stay's start date (YYYY-MM-DD): "), "%Y-%m-%d")
                        duration = int(input(f"How long will you be staying in {destination_city}? (in days): ").strip())
                        end_date = start_date + timedelta(days=duration)

                        # Ask for hotel needs
                        need_hotel = input("Do you need a hotel? (yes/no): ").strip().lower()
                        if need_hotel == "yes":
                            city_id = get_city_id(destination_city)
                            if city_id:
                                rooms = int(input("How many rooms will you need? "))
                                people = int(input("How many people will be staying? "))
                                checkin = start_date.strftime("%Y-%m-%d")
                                checkout = end_date.strftime("%Y-%m-%d")
                                get_hotels_by_city_id(city_id, rooms, people, checkin, checkout)

                        # Ask if they want an itinerary
                        create_itinerary = input(f"Would you like an itinerary created for your {duration}-day stay in {destination_city}? (yes/no): ").strip().lower()
                        if create_itinerary == "yes":
                            itinerary = generate_itinerary(duration, destination_city)
                            print("\nHere is your itinerary:")
                            print(itinerary)

                    # If the user is NOT staying in the arrival city
                    elif stay_in_city == "no":
                        # Ask for alternative city, state, or country
                        new_location = input(f"Where will you be staying for the duration of your trip (City, State or City, Country)? ").strip()
                        
                        # Initialize the start date and duration for the new location
                        start_date = datetime.strptime(input("Enter your stay's start date (YYYY-MM-DD): "), "%Y-%m-%d")
                        duration = int(input(f"How long will you be staying in {new_location}? (in days): ").strip())
                        end_date = start_date + timedelta(days=duration)

                        # Ask for hotel needs for the new location before asking for room details
                        need_hotel = input(f"Do you need a hotel in {new_location}? (yes/no): ").strip().lower()
                        if need_hotel == "yes":
                            city_id = get_city_id(new_location)
                            if city_id:
                                rooms = int(input("How many rooms will you need? "))
                                people = int(input("How many people will be staying? "))
                                checkin = start_date.strftime("%Y-%m-%d")
                                checkout = end_date.strftime("%Y-%m-%d")
                                get_hotels_by_city_id(city_id, rooms, people, checkin, checkout)

                        # Ask if they want an itinerary for the new location
                        create_itinerary = input(f"Would you like an itinerary created for your {duration}-day stay in {new_location}? (yes/no): ").strip().lower()
                        if create_itinerary == "yes":
                            itinerary = generate_itinerary(duration, new_location)
                            print("\nHere is your itinerary:")
                            print(itinerary)

                    # Suggest NASCAR races if available during the user's stay
                    suggested_races = suggest_nascar_races_v2(start_date, end_date)
                    if suggested_races:
                        print("\nHere are the NASCAR races during your stay:")
                        for race in suggested_races:
                            print(f"Race: {race['Race Name']} | Location: {race['Location']} | Date: {race['Date']}")
                    else:
                        print("No NASCAR races are happening during your stay.")

                else:
                    print("No data found for this flight.")
            except Exception as e:
                print(f"Error fetching flight status: {e}")

        elif choice == "2":
            user_query = input("Ask your question: ")
            try:
                assistant_response = chat_with_assistant(user_query)
                print("\nAI Assistant Response:")
                print(assistant_response)
            except Exception as e:
                print(f"Error processing your query: {e}")

        elif choice == "3":
            print("Thank you for using the Travel Assistant. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Global context to remember variables
context = {
    "flight_number": None,
    "destination_airport": None,
    "destination_city": None
}
    
