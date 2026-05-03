import React, { useState } from "react";

const getColor = (score) => {
  if (score > 0.7) return "text-red-400";
  if (score > 0.3) return "text-yellow-400";
  return "text-green-400";
};

export default function AlertsPanel({ alerts = [], rerunAnalysis }) {
  const [feedbackState, setFeedbackState] = useState({});

  const sendFeedback = async (id, label) => {
    try {
      await fetch("http://127.0.0.1:8000/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          transaction_id: id,
          label,
        }),
      });

      // 🔥 re-run analysis
      await rerunAnalysis();

      // ✅ update UI instantly
      setFeedbackState((prev) => ({
        ...prev,
        [id]: label,
      }));

    } catch (err) {
      console.error(err);
    }
  };

  if (!alerts.length) {
    return (
      <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5">
        <h2 className="text-xl mb-4">Smart Alerts</h2>
        <p className="text-gray-400">No anomalies detected</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5">
      <h2 className="text-xl mb-4">Smart Alerts</h2>

      {alerts.map((a, i) => (
        <div
          key={`${a.transaction.date}-${a.transaction.desc}-${a.transaction.amount}-${i}`}
          className="bg-gray-800 p-4 mb-3 rounded-xl border border-red-500/20"
        >
          <p className={`font-semibold ${getColor(a.score)}`}>
            {a.score > 0.7
              ? "⚠ High Risk Transaction"
              : a.score > 0.3
              ? "⚡ Medium Risk"
              : "✅ Low Risk"}
          </p>

          <p className="text-xs text-gray-400">
            Score: {a.score}
          </p>

          <p className="text-gray-300 text-sm">
            ₹{a.transaction.amount} — {a.transaction.desc}
          </p>

          <p className="text-gray-400 text-xs mt-1">
            {a.reasons?.[0]}
          </p>

          {/* 🔥 FEEDBACK BUTTONS */}
          <div className="flex gap-2 mt-3">
            <button
              onClick={() => sendFeedback(a.id, "normal")}
              disabled={feedbackState[a.id] === "normal"}
              className={`px-3 py-1 rounded ${
                feedbackState[a.id] === "normal"
                  ? "bg-green-800"
                  : "bg-green-600 hover:bg-green-500"
              }`}
            >
              {feedbackState[a.id] === "normal" ? "✔ Marked Normal" : "Normal"}
            </button>

            <button
              onClick={() => sendFeedback(a.id, "suspicious")}
              disabled={feedbackState[a.id] === "suspicious"}
              className={`px-3 py-1 rounded ${
                feedbackState[a.id] === "suspicious"
                  ? "bg-red-800"
                  : "bg-red-600 hover:bg-red-500"
              }`}
            >
              {feedbackState[a.id] === "suspicious"
                ? "✔ Marked Suspicious"
                : "Suspicious"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}