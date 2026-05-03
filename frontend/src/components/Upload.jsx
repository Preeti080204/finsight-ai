import React, { useState, useCallback } from "react";

export default function Upload({ setData }) {
  const [file, setFile] = useState(null);

  // ✅ LOAD USER DATA (FIXED)
  const loadUserData = useCallback(async () => {
    const user_id = localStorage.getItem("user_id");

    if (!user_id) return;

    const res = await fetch(`http://127.0.0.1:8000/data?user_id=${user_id}`);
    const transactions = await res.json();

    if (!transactions.length) {
      alert("No previous data found");
      return;
    }

    // 🔥 FIX: remove id before sending
    const cleanTransactions = transactions.map(({ id, ...rest }) => rest);

    const analysisRes = await fetch(
      `http://127.0.0.1:8000/analyze?user_id=${user_id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(cleanTransactions), // ✅ FIXED
      }
    );

    const analysis = await analysisRes.json();

    setData({ transactions, analysis });
  }, [setData]);

  // ✅ HANDLE UPLOAD (FIXED)
  const handleUpload = async () => {
    const user_id = localStorage.getItem("user_id");

    if (!user_id) {
      alert("Please login first");
      return;
    }

    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log("UPLOAD CLICKED");

      const uploadRes = await fetch(
        `http://127.0.0.1:8000/upload?user_id=${user_id}`,
        {
          method: "POST",
          body: formData,
        }
      );

      const uploadData = await uploadRes.json();
      console.log("UPLOAD DATA:", uploadData);

      const transactions = uploadData.transactions;

      // 🔥 FIX: remove id before sending to backend
      const cleanTransactions = transactions.map(({ id, ...rest }) => rest);

      // ✅ build profile
      await fetch(`http://127.0.0.1:8000/build-profile?user_id=${user_id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(cleanTransactions), // ✅ FIXED
      });

      // ✅ analyze
      const analysisRes = await fetch(
        `http://127.0.0.1:8000/analyze?user_id=${user_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(cleanTransactions), // ✅ FIXED
        }
      );

      const analysis = await analysisRes.json();

      setData({ transactions, analysis });

    } catch (err) {
      console.error("UPLOAD FAILED:", err);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-6 bg-gradient-to-br from-black via-gray-950 to-blue-950 text-white">
      <h1 className="text-5xl font-extrabold text-white tracking-wide">
        FinSight AI
      </h1>

      <p className="text-lg text-gray-400 mt-3">
        Upload your financial data and get AI-powered insights
      </p>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="text-white"
      />

      <button
        onClick={handleUpload}
        className="bg-green-600 px-6 py-2 rounded-lg hover:bg-green-500"
      >
        Upload CSV
      </button>

      <button
        onClick={loadUserData}
        className="bg-blue-600 px-6 py-2 rounded-lg hover:bg-blue-500"
      >
        Load My Data
      </button>
    </div>
  );
}