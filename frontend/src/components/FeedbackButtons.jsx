import React from "react";

export default function FeedbackButtons({ id }) {
  const sendFeedback = async (label) => {
    await fetch("http://127.0.0.1:8000/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        transaction_id: id,
        label: label,
      }),
    });
  };

  return (
    <div className="flex gap-2 mt-3">
      <button
        onClick={() => sendFeedback("normal")}
        className="bg-green-600 px-3 py-1 rounded"
      >
        Normal
      </button>

      <button
        onClick={() => sendFeedback("suspicious")}
        className="bg-red-600 px-3 py-1 rounded"
      >
        Suspicious
      </button>
    </div>
  );
}