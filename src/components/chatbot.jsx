import React, { useState } from "react";
import axios from "axios";

const Chatbot = ({ userId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;

    console.log("User ID in Chatbot:", userId); // Debugging

    if (!userId) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Please sign in to use this feature." },
      ]);
      return;
    }

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post("http://localhost:5000/chat", {
        prompt: input,
        user_id: userId, // Send userId to backend
      });

      const botMessage = { role: "assistant", content: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error communicating with the chatbot:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "An error occurred. Please try again." },
      ]);
    }

    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // Prevent default form submission
      sendMessage();
    }
  };

  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "10px" }}>
      <h2>AAron The Chatbot</h2>
      <div style={{ maxHeight: "300px", overflowY: "auto", marginBottom: "10px" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ margin: "5px 0" }}>
            <strong>{msg.role === "user" ? "You:" : "AAron:"}</strong> {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress} // Trigger sendMessage on Enter
        placeholder="Type your message..."
        style={{ width: "80%", padding: "5px" }}
      />
    </div>
  );
};

export default Chatbot;
