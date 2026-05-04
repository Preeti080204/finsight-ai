import React, { useState } from "react";
import API_URL from "../api/config";

export default function TransactionsTable({ transactions, rerunAnalysis }) {

  const [feedbackState, setFeedbackState] = useState({});

  const sendFeedback = async (id, label) => {
    try {
      await fetch(`${API_URL}/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          transaction_id: id,
          label: label,
        }),
      });

      setFeedbackState((prev) => ({
        ...prev,
        [id]: label,
      }));

      console.log(`Feedback sent: ${label} for ID ${id}`);

      // 🔥 THIS IS THE REAL FIX
      if (rerunAnalysis) {
        rerunAnalysis();
      }

    } catch (error) {
      console.error("Feedback error:", error);
    }
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5 backdrop-blur-xl shadow-xl">
      <h2 className="text-xl mb-4">Transactions</h2>

      <table className="w-full text-left">
        <thead>
          <tr className="text-gray-400">
            <th>Date</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Category</th>
            <th>Feedback</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((t) => (
            <tr key={`${t.date}-${t.desc}-${t.amount}`} className="border-t border-gray-800">
              <td>{t.date}</td>
              <td>{t.desc}</td>
              <td>₹{t.amount}</td>
              <td>{t.category}</td>

              <td>
                <div className="flex gap-2">
                  <button
                    onClick={() => sendFeedback(t.id, "normal")}
                    className={`px-2 py-1 text-xs rounded ${
                      feedbackState[t.id] === "normal"
                        ? "bg-green-400"
                        : "bg-green-600 hover:bg-green-500"
                    }`}
                  >
                    Normal
                  </button>

                  <button
                    onClick={() => sendFeedback(t.id, "suspicious")}
                    className={`px-2 py-1 text-xs rounded ${
                      feedbackState[t.id] === "suspicious"
                        ? "bg-red-400"
                        : "bg-red-600 hover:bg-red-500"
                    }`}
                  >
                    Suspicious
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}