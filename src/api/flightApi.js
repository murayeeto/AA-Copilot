import axios from "axios";

const BASE_URL = "http://localhost:5000";

// Fetch flight status
export const fetchFlightStatus = async (flightNumber) => {
  try {
    const response = await axios.post(`${BASE_URL}/flight-status`, {
      flight_number: flightNumber,
    });
    return response.data;
  } catch (err) {
    console.error("Error fetching flight status:", err);
    throw err;
  }
};

// Save flight data to Firebase
export const saveFlightData = async (userId, flightData) => {
  try {
    const response = await axios.post(`${BASE_URL}/save-flight`, {
      user_id: userId,
      flight_data: flightData,
    });
    return response.data;
  } catch (err) {
    console.error("Error saving flight data:", err);
    throw err;
  }
};

// Get saved flights from Firebase
export const getSavedFlights = async (userId) => {
  try {
    const response = await axios.get(`${BASE_URL}/get-flights`, {
      params: { user_id: userId },
    });
    return response.data;
  } catch (err) {
    console.error("Error fetching saved flights:", err);
    throw err;
  }
};
