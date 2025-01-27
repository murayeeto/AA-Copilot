import React, { useState, useEffect } from "react";
import axios from "axios";

export const ItineraryPlanner = ({ userId }) => {
  const [itinerary, setItinerary] = useState([]);
  const [location, setLocation] = useState("");
  const [duration, setDuration] = useState(3); // Default duration: 3 days
  const [useLastSaved, setUseLastSaved] = useState(false);
  const [saveItinerary, setSaveItinerary] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (useLastSaved) {
      fetchLastSavedLocation();
    }
  }, [useLastSaved]);

  const fetchLastSavedLocation = async () => {
    try {
      setError("");
      const response = await axios.post("http://localhost:5000/itinerary", {
        user_id: userId,
        action: "get_last_location",
      });

      console.log("Response from backend:", response.data);

      const { location: fetchedLocation } = response.data;
      if (fetchedLocation) {
        setLocation(fetchedLocation);
      } else {
        setError("Unable to determine your last saved location.");
      }
    } catch (err) {
      console.error("Error fetching last saved location:", err);
      setError("Failed to fetch last saved location. Please try again.");
    }
  };

  const generateItinerary = async () => {
    if (!location && !useLastSaved) {
      setError("Please provide a location or select 'Use Last Saved Location'.");
      return;
    }

    if (duration <= 0) {
      setError("Please provide a valid number of days.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:5000/itinerary", {
        user_id: userId,
        location,
        duration,
        action: "generate_itinerary",
      });

      console.log("Generated itinerary response:", response.data);

      const { itinerary: generatedItineraryRaw } = response.data;

      // Split by newlines for proper display or treat as plain text if formatting allows.
      const generatedItinerary = generatedItineraryRaw.split("\n").filter(line => line.trim() !== "");

      if (generatedItinerary.length === 0) {
        setError("No itinerary could be generated.");
        return;
      }

      setItinerary(generatedItinerary);

      if (saveItinerary) {
        saveItineraryToDatabase(generatedItinerary);
      }
    } catch (err) {
      console.error("Error generating itinerary:", err);
      setError("Failed to generate itinerary. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const saveItineraryToDatabase = async (generatedItinerary) => {
    try {
      await axios.post("http://localhost:5000/itinerary", {
        user_id: userId,
        location,
        duration,
        itinerary: generatedItinerary,
        action: "save_itinerary",
      });
      alert("Itinerary saved successfully!");
    } catch (err) {
      console.error("Error saving itinerary:", err);
      setError("Failed to save itinerary.");
    }
  };

  return (
    <div id="itinerary-planner" style={{ paddingBottom: "50px" }}>
      <h2>Itinerary Planner</h2>
      <div>
        <label>
          <input
            type="checkbox"
            checked={useLastSaved}
            onChange={(e) => setUseLastSaved(e.target.checked)}
          />
          Use Last Saved Location ({location || "No saved location yet"})
        </label>
        {!useLastSaved && (
          <input
            type="text"
            placeholder="Enter location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        )}
        <input
          type="number"
          placeholder="Number of days"
          value={duration}
          onChange={(e) => setDuration(Number(e.target.value))}
          min="1"
        />
        <label>
          <input
            type="checkbox"
            checked={saveItinerary}
            onChange={(e) => setSaveItinerary(e.target.checked)}
          />
          Save Itinerary
        </label>
        <button onClick={generateItinerary} disabled={loading}>
          {loading ? "Generating..." : "Generate Itinerary"}
        </button>
        {error && <p className="text-danger">{error}</p>}
      </div>
      <h3>Generated Itinerary</h3>
      {itinerary.length > 0 ? (
        <div style={{ whiteSpace: "pre-wrap", maxHeight: "none", overflow: "visible" }}>
          <ul className="itinerary-list">
            {itinerary.map((item, index) => (
              <li key={index} style={{ margin: "10px 0", padding: "5px", borderBottom: "1px solid #ddd" }}>
                {item}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No itinerary available to display.</p>
      )}
    </div>
  );
};
