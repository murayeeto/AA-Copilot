import React, { useState } from "react";
import { googleSignIn, googleSignOut } from "../api/firebase";

export const Navigation = (props) => {
  const [user, setUser] = useState(null);

  const handleSignIn = async () => {
    try {
      const result = await googleSignIn();
      setUser(result);
      alert(`Welcome, ${result.displayName}!`);
    } catch (err) {
      console.error("Google Sign-In failed:", err);
    }
  };

  const handleSignOut = async () => {
    try {
      await googleSignOut();
      setUser(null);
      alert("Signed out successfully.");
    } catch (err) {
      console.error("Sign-Out failed:", err);
    }
  };

  return (
    <nav id="menu" className="navbar navbar-default navbar-fixed-top">
      <div className="container">
        <div className="navbar-header">
          <button
            type="button"
            className="navbar-toggle collapsed"
            data-toggle="collapse"
            data-target="#bs-example-navbar-collapse-1"
          >
            {" "}
            <span className="sr-only">Toggle navigation</span>{" "}
            <span className="icon-bar"></span>{" "}
            <span className="icon-bar"></span>{" "}
            <span className="icon-bar"></span>{" "}
          </button>
          <a className="navbar-brand page-scroll" href="#page-top">
            AA-Copilot
          </a>{" "}
        </div>

        <div
          className="collapse navbar-collapse"
          id="bs-example-navbar-collapse-1"
        >
          <ul className="nav navbar-nav navbar-right">
            <li>
              <a href="#features" className="page-scroll">
                Features
              </a>
            </li>
            <li>
              <a href="#about" className="page-scroll">
                About
              </a>
            </li>
            <li>
              <a href="#services" className="page-scroll">
                Services
              </a>
            </li>
            <li>
              <a href="#itinerary-planner" className="page-scroll">
                Itinerary Planner
              </a>
            </li>
            <li>
              <a href="#flight-tracker" className="page-scroll">
                Flight Tracker
              </a>
            </li>
            <li>
              <a href="#chatbot-section" className="page-scroll">
                Chatbot
              </a>
            </li>
            <li>
              <a href="#team" className="page-scroll">
                Team
              </a>
            </li>
            <li>
              <a href="#contact" className="page-scroll">
                Contact
              </a>
            </li>
            <li>
              {user ? (
                <button className="btn btn-secondary" onClick={handleSignOut}>
                  Sign Out
                </button>
              ) : (
                <button className="btn btn-primary" onClick={handleSignIn}>
                  Sign In with Google
                </button>
              )}
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};
