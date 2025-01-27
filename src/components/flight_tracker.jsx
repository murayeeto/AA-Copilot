import React, { useState, useEffect } from "react";
import { fetchFlightStatus, saveFlightData, getSavedFlights } from "../api/flightApi";
import { auth } from "../api/firebase"; // Import Firebase Auth instance
import { onAuthStateChanged } from "firebase/auth";

export const FlightTracker = () => {
  const [flightNumber, setFlightNumber] = useState("");
  const [flightData, setFlightData] = useState(null);
  const [userId, setUserId] = useState(null); // Use null if not signed in
  const [savedFlights, setSavedFlights] = useState([]);
  const [error, setError] = useState("");

  // Check if the user is signed in
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setUserId(user.uid); // Set the Firebase UID as the user ID
      } else {
        setUserId(null); // Reset the user ID if not signed in
      }
    });
    return () => unsubscribe(); // Clean up the listener on unmount
  }, []);

  const handleFetchFlightStatus = async () => {
    try {
      setError("");
      const data = await fetchFlightStatus(flightNumber);
      console.log("Fetched Flight Data:", data); // Debugging
      setFlightData(data);
    } catch (err) {
      setError("Failed to fetch flight status. Please try again.");
    }
  };

  const handleSaveFlight = async () => {
    if (!userId) {
      alert("You must be signed in to save flight data.");
      return;
    }
  
    if (!flightData || !flightData.flight_number) {
      console.log("No flight data available to save:", flightData); // Debugging
      alert("No flight data available to save.");
      return;
    }
  
    const flightToSave = {
      flight_number: flightData.flight_number, // Ensure flight_number is saved
      departure_airport: flightData.departure_airport || "Unknown",
      arrival_airport: flightData.arrival_airport || "Unknown",
      status: flightData.status || "Unknown",
      departure_time: flightData.departure_time || "Unknown",
      arrival_time: flightData.arrival_time || "Unknown",
    };
  
    try {
      await saveFlightData(userId, flightToSave); // Save flight data with flight_number
      alert("Flight saved successfully!");
    } catch (err) {
      console.error("Error saving flight data:", err);
      alert("Failed to save flight data. Please try again.");
    }
  };

  const handleGetSavedFlights = async () => {
    if (!userId) {
      alert("You must be signed in to view saved past flights.");
      return;
    }
    try {
      const data = await getSavedFlights(userId);
      console.log("Fetched Saved Flights:", data); // Debugging
      setSavedFlights(data.flights || []);
    } catch (err) {
      setError("Failed to fetch saved flights. Please try again.");
    }
  };

  return (
    <div id="flight-tracker">
      <div className="container">
        <div className="section-title text-center">
          <h2>Flight Tracker</h2>
          <p>Track flights and save them to your account if signed in.</p>
        </div>
        <div className="row">
          <div className="col-md-6 col-md-offset-3">
            <input
              type="text"
              className="form-control"
              placeholder="Enter flight number (e.g., AA100)"
              value={flightNumber}
              onChange={(e) => setFlightNumber(e.target.value)}
            />
            <button className="btn btn-primary" onClick={handleFetchFlightStatus}>
              Fetch Flight Status
            </button>
            {userId ? (
              <>
                <button className="btn btn-secondary" onClick={handleSaveFlight}>
                  Save Flight
                </button>
                <button className="btn btn-success" onClick={handleGetSavedFlights}>
                  Get Saved Flights
                </button>
              </>
            ) : (
              <p className="text-warning text-center">Sign in to save or view flights.</p>
            )}
          </div>
        </div>
        {error && <p className="text-danger text-center">{error}</p>}
        {flightData && (
          <div className="flight-info">
            <h3>Flight Information</h3>
            <p><strong>Flight Number:</strong> {flightData.flight_number}</p>
            <p><strong>Departure Airport:</strong> {flightData.departure_airport || "Unknown"}</p>
            <p><strong>Arrival Airport:</strong> {flightData.arrival_airport || "Unknown"}</p>
            <p><strong>Status:</strong> {flightData.status || "Unknown"}</p>
            <p><strong>Departure Time:</strong> {flightData.departure_time || "Unknown"}</p>
            <p><strong>Arrival Time:</strong> {flightData.arrival_time || "Unknown"}</p>
          </div>
        )}
        {savedFlights.length > 0 && (
          <div className="saved-flights">
            <h3>Saved Flights</h3>
            <ul>
              {savedFlights.map((flight, index) => (
                <li key={index}>
                  <p><strong>Flight Number:</strong> {flight.flight_number}</p>
                  <p><strong>Departure Airport:</strong> {flight.departure_airport || "Unknown"}</p>
                  <p><strong>Arrival Airport:</strong> {flight.arrival_airport || "Unknown"}</p>
                  <p><strong>Status:</strong> {flight.status || "Unknown"}</p>
                  <p><strong>Departure Time:</strong> {flight.departure_time || "Unknown"}</p>
                  <p><strong>Arrival Time:</strong> {flight.arrival_time || "Unknown"}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};
