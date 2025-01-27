import React, { useState, useEffect } from "react";
import { Navigation } from "./components/navigation";
import { Header } from "./components/header";
import { Features } from "./components/features";
import { About } from "./components/about";
import { Services } from "./components/services";
import { ItineraryPlanner } from "./components/itinerary_planner"; 
import { FlightTracker } from './components/flight_tracker'; 
import { Team } from "./components/Team";
import { Contact } from "./components/contact";
import Chatbot from "./components/chatbot";
import JsonData from "./data/data.json";
import SmoothScroll from "smooth-scroll";
import { auth } from "./api/firebase";
import { db } from "./api/firebase";
import { collection, query, where, orderBy, limit, getDocs } from "firebase/firestore";
import "./App.css";

export const scroll = new SmoothScroll('a[href*="#"]', {
  speed: 1000,
  speedAsDuration: true,
});

const App = () => {
  const [landingPageData, setLandingPageData] = useState({});
  const [currentUser, setCurrentUser] = useState(null);
  const [lastSavedFlight, setLastSavedFlight] = useState(null);

  useEffect(() => {
    setLandingPageData(JsonData);

    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      if (user) {
        setCurrentUser(user);
        console.log("User signed in:", user.uid); // Debugging

        // Fetch last saved flight for the user
        try {
          console.log("Fetching last saved flight...");
          const flightQuery = query(
            collection(db, "flights"),
            where("userId", "==", user.uid),
            orderBy("createdAt", "desc"),
            limit(1)
          );
          console.log("Query parameters:", { userId: user.uid });

          const flightSnapshot = await getDocs(flightQuery);
          console.log("Query result:", flightSnapshot.docs.map(doc => doc.data()));

          if (!flightSnapshot.empty) {
            const flightData = flightSnapshot.docs[0].data();
            console.log("Last saved flight fetched:", flightData); // Debugging
            setLastSavedFlight(flightData);
          } else {
            setLastSavedFlight(null);
            console.log("No saved flights found for this user.");
          }
        } catch (error) {
          console.error("Error fetching last saved flight:", error);
        }
      } else {
        setCurrentUser(null);
        setLastSavedFlight(null);
        console.log("No user signed in.");
      }
    });

    return () => unsubscribe(); // Cleanup listener on unmount
  }, []);

  useEffect(() => {
    console.log("App.jsx: lastSavedFlight state updated:", lastSavedFlight); // Debugging
  }, [lastSavedFlight]);

  return (
    <div>
      <Navigation />
      <Header data={landingPageData.Header} />
      <Features data={landingPageData.Features} />
      <About data={landingPageData.About} />
      <Services data={landingPageData.Services} />
      <ItineraryPlanner userId={currentUser?.uid} lastSavedFlight={lastSavedFlight} />
      <FlightTracker lastSavedFlight={lastSavedFlight} />
      <div id="chatbot-section" style={{ marginTop: "20px" }}>
        <Chatbot userId={currentUser?.uid} lastSavedFlight={lastSavedFlight} />
      </div>
      <Team data={landingPageData.Team} />
      <Contact data={landingPageData.Contact} />
    </div>
  );
};

export default App;
