import React from "react";

export default function StoryPanel({ story }) {
  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5 backdrop-blur-xl shadow-xl hover:shadow-blue-500/10 transition">
      <h2 className="text-xl mb-3">Financial Story</h2>
      <p className="text-gray-300">{story}</p>
    </div>
  );
}