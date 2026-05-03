import React from "react";

export default function ExplainabilityPanel({ explain = [] }) {
  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5 backdrop-blur-xl shadow-xl hover:shadow-blue-500/10 transition">
      <h2 className="text-xl mb-4">Why this was flagged</h2>

      {explain.length === 0 && (
        <p className="text-gray-400">No explanations yet</p>
      )}

      {explain.map((item, i) => (
        <div key={i} className="mb-4">
          <p className="text-blue-400 font-semibold">
            Score: {(item.score ?? 0).toFixed(2)}
          </p>

          <ul className="text-gray-300 text-sm mt-2">
            {(item.reasons || []).map((r, idx) => (
              <li key={idx}>• {r}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}