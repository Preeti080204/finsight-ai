import React, { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";

import SummaryCards from "../components/SummaryCards";
import ChartsPanel from "../components/ChartsPanel";
import AlertsPanel from "../components/AlertsPanel";
import ExplainabilityPanel from "../components/ExplainabilityPanel";
import StoryPanel from "../components/StoryPanel";
import TransactionsTable from "../components/TransactionsTable";
import Filters from "../components/Filters";

export default function Dashboard({ data }) {
  const username = localStorage.getItem("username");

  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      const user_id = localStorage.getItem("user_id");

      const res = await fetch(
        `https://finsight-api-muwe.onrender.com/data?user_id=${user_id}`
      );

      const data = await res.json();
      setHistory(data);
    };

    fetchHistory();
  }, []);

  const logout = () => {
    localStorage.clear();
    window.location.reload();
  };

  // ✅ safe fallback
  const transactions = useMemo(
    () => data?.transactions || [],
    [data]
  );

  console.log("TRANSACTIONS:", transactions);

  const [analysis, setAnalysis] = useState(data?.analysis || []);
  const [healthScore, setHealthScore] = useState(0);

  const income = transactions
    .filter(t => t.category === "Income")
    .reduce((sum, t) => sum + t.amount, 0);

  const spending = transactions
    .filter(t => t.category !== "Income")
    .reduce((sum, t) => sum + t.amount, 0);

  const savings_rate = income
    ? Math.round(((income - spending) / income) * 100)
    : 0;

  const story = `
  You earned ₹${income} this period and spent ₹${spending}.
  Your savings rate is ${savings_rate}%.
  ${
    Array.isArray(analysis) && analysis.some(a => a.score > 0.5)
      ? "We detected unusual transactions that need review."
      : "Your financial activity looks consistent."
  }
`;

  const [filtered, setFiltered] = useState(transactions);

  useEffect(() => {
    setFiltered(transactions);
  }, [transactions]);

  useEffect(() => {
    if (!data) return;

    // 🔥 FORCE NEW DATA EVERY TIME
    setAnalysis(data.analysis || []);
    setFiltered(data.transactions || []);

    if (data.analysis && data.analysis.length > 0) {
      setHealthScore(data.analysis[0].health_score || 0);
    } else {
      setHealthScore(0);
    }
  }, [data]);

  // 🔥 FIXED (user_id added)
  const rerunAnalysis = async () => {
    const user_id = localStorage.getItem("user_id");

    const res = await fetch(
      `https://finsight-api-muwe.onrender.com/analyze?user_id=${user_id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(transactions),
      }
    );

    const updated = await res.json();
    setAnalysis(updated);

    if (updated.length > 0) {
      setHealthScore(updated[0].health_score || 0);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="min-h-screen bg-gradient-to-br from-black via-gray-950 to-blue-950 text-white p-6 space-y-6"
    >
      {/* 🔥 HEADER */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold glow-text">Dashboard</h1>

        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-300">
            👤 {username}
          </span>

          <button
            onClick={logout}
            className="bg-red-600 px-3 py-1 rounded hover:bg-red-500"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="bg-gray-900 p-4 rounded-xl">
        <h2 className="text-lg font-bold mb-2">User History</h2>

        {history.length === 0 ? (
          <p className="text-gray-400">No previous data found</p>
        ) : (
          <ul className="text-sm space-y-1 max-h-40 overflow-y-auto">
            {history.slice(0, 10).map((t) => (
              <li key={t.id}>
                {t.date} — {t.desc} — ₹{t.amount}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* 🔥 HEALTH SCORE */}
      <h2 className="text-xl font-semibold">
        Financial Health Score: {healthScore}/100
      </h2>

      {/* 🔥 RECOMMENDATIONS (SAFE) */}
      {analysis.length > 0 && (
        <div className="bg-gray-900 p-4 rounded-xl">
          <h3 className="font-bold mb-2">Recommendations</h3>
          <ul className="list-disc pl-5">
            {(analysis[0].recommendations || []).map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}

      <SummaryCards
        data={{
          income,
          spending,
          savings_rate,
        }}
      />

      <Filters
        transactions={transactions}
        setFiltered={setFiltered}
      />

      <ChartsPanel transactions={filtered} />

      <div className="grid grid-cols-2 gap-6">
        <AlertsPanel
          alerts={analysis.filter(a => a.score > 0)}
          rerunAnalysis={rerunAnalysis}
        />

        <ExplainabilityPanel explain={analysis} />
      </div>

      <StoryPanel story={story} />

      <TransactionsTable 
        transactions={filtered} 
        rerunAnalysis={rerunAnalysis} 
      />
    </motion.div>
  );
}