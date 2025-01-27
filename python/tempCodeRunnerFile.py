from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_assistant import chat_with_assistant, get_bag_eta
from firebase_config import db
import requests
import os
from dotenv import load_dotenv
from config import AVIATIONSTACK_API_KEY
from firebase_admin import firestore


# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get("prompt")
    user_id = data.get("user_id")

    if not prompt or not user_id:
        return jsonify({"error": "Missing required fields: 'prompt' or 'user_id'"}), 400

    try:
        # Connect to Firestore
        db = firestore.client()

        # Fetch the user's document
        user_doc = db.collection("users").document(user_id).get()

        # Check if the document exists
        if not user_doc.exists:
            return jsonify({"response": "No user found with the provided ID."}), 200

        user_data = user_doc.to_dict()
        flights = user_data.get("flights", [])  # Access the flights field (array)

        # If no flights are found, return an appropriate message
        if not flights:
            return jsonify({"response": "No flights found for the user."}), 200

        # Process flights based on the prompt
        if "where did i land" in prompt.lower():
            # Get the last flight's arrival airport
            last_flight = flights[-1]  # Assume last entry is the most recent
            arrival_airport = last_flight.get("arrival_airport")
            if arrival_airport:
                response = f"Your last flight landed at {arrival_airport}."
            else:
                response = "I could not determine your last flight's arrival airport."
        elif "what are my saved flights" in prompt.lower():
            # List all saved flights
            flights_list = [
                f"Flight {f.get('flight_number')} from {f.get('departure_airport')} to {f.get('arrival_airport')}"
                for f in flights
            ]
            response = "Here are your saved flights:\n" + "\n".join(flights_list)
        else:
            response = "I'm not sure how to respond to that."

        return jsonify({"response": response}), 200

    except Exception as e:
        print("Error in chatbot logic:", e)
        return jsonify({"error": str(e)}), 500





@app.route('/bag_eta', methods=['POST'])
def bag_eta():
    """
    Endpoint for retrieving bag ETA information.
    """
    try:
        print("POST /bag_eta accessed")
        data = request.json
        print("Received data:", data)

        destination = data.get("destination", "")
        if not destination:
            print("Error: Missing 'destination'")
            return jsonify({"error": "Destination is required"}), 400

        eta = get_bag_eta(destination)
        print("Bag ETA:", eta)
        return jsonify({"eta": eta})

    except Exception as e:
        print("Error in /bag_eta endpoint:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/flight-status', methods=['POST'])
def flight_status():
    """
    Fetch live flight data using the Aviationstack API.
    """
    try:
        data = request.json
        flight_number = data.get("flight_number")
        print("Received flight_number:", flight_number)  # Debugging
        if not flight_number:
            return jsonify({"error": "Flight number is required"}), 400

        # Call Aviationstack API
        url = f"http://api.aviationstack.com/v1/flights"
        params = {
            'access_key': AVIATIONSTACK_API_KEY,
            'flight_iata': flight_number
        }
        response = requests.get(url, params=params)
        print("Aviationstack API Response:", response.json())  # Debugging
        response_data = response.json()

        if response_data and 'data' in response_data and len(response_data['data']) > 0:
            flight_data = response_data['data'][0]
            result = {
                "flight_number": flight_number,  # Include flight number in response
                "departure_airport": flight_data['departure']['airport'],
                "arrival_airport": flight_data['arrival']['airport'],
                "destination_city": flight_data['arrival']['iata'],
                "status": flight_data['flight_status'],
                "departure_time": flight_data['departure']['estimated'],
                "arrival_time": flight_data['arrival']['estimated'],
            }
            return jsonify(result), 200
        else:
            return jsonify({"error": "Flight not found"}), 404

    except Exception as e:
        print("Error in /flight-status endpoint:", e)  # Debugging
        return jsonify({"error": str(e)}), 500

@app.route('/save-flight', methods=['POST'])
def save_flight():
    """
    Save flight data for a user to Firebase Firestore.
    """
    try:
        data = request.json
        user_id = data.get("user_id")
        flight_data = data.get("flight_data")

        if not user_id or not flight_data:
            return jsonify({"error": "Missing user_id or flight_data"}), 400

        # Save flight data to Firestore
        print(f"Saving flight for user_id: {user_id}")
        print(f"Flight data: {flight_data}")
        user_ref = db.collection('users').document(user_id)
        user_ref.set({"flights": firestore.ArrayUnion([flight_data])}, merge=True)
        print("Write to Firestore successful!")

        return jsonify({"message": "Flight saved successfully!"}), 200

    except Exception as e:
        print("Error saving flight data:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/get-flights', methods=['GET'])
def get_flights():
    """
    Retrieve saved flights for a user from Firebase Firestore.
    """
    try:
        user_id = request.args.get("user_id")
        print("Received user_id for get-flights:", user_id)  # Debugging
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        # Retrieve data from Firestore
        user_ref = db.collection('users').document(user_id)
        doc = user_ref.get()
        print("Firestore document fetched:", doc.to_dict())  # Debugging

        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "No data found for this user"}), 404

    except Exception as e:
        print("Error in /get-flights endpoint:", e)  # Debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.run(debug=True, port=5000)
