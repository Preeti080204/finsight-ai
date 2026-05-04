import React, { useState } from "react";
import API_URL from "../api/config";

export default function Login({ setUserId }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const loginUser = async () => {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (data.user_id) {
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("username", username); // 🔥 keep username for UI
      setUserId(data.user_id);
    } else {
      alert("Login failed");
    }
  };

  const signupUser = async () => {
    const res = await fetch(`${API_URL}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (data.message) {
      alert("Signup successful");
    } else {
      alert(data.error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-950 to-blue-950 text-white flex flex-col items-center justify-center">
      
      <h1 className="text-3xl mb-6">Login / Signup</h1>

      <input
        className="bg-gray-900 text-white border border-gray-600 p-3 m-2 rounded-lg focus:outline-none focus:border-blue-500 w-64"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        className="bg-gray-900 text-white border border-gray-600 p-3 m-2 rounded-lg focus:outline-none focus:border-blue-500 w-64"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <div className="flex gap-4 mt-4">
        <button
          className="px-4 py-2 bg-blue-500 rounded hover:bg-blue-400"
          onClick={loginUser}
        >
          Login
        </button>

        <button
          className="px-4 py-2 bg-green-500 rounded hover:bg-green-400"
          onClick={signupUser}
        >
          Signup
        </button>
      </div>

    </div>
  );
}