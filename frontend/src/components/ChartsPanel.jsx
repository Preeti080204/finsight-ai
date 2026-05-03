import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export default function ChartsPanel({ transactions }) {
  // ---- Prepare Monthly Spending Data ----
  // ---- NEW: Daily Spending Trend (FIXED) ----
  const grouped = {};

  transactions.forEach((t) => {
    if (t.category !== "Income") {
      if (!grouped[t.date]) grouped[t.date] = 0;
      grouped[t.date] += Math.abs(t.amount);
    }
  });

  const lineData = Object.keys(grouped).map((date) => ({
    month: date,   // keep 'month' because chart uses it
    spending: grouped[date],
  }));

  // ---- Category Breakdown ----
  const categoryData = {};

  transactions.forEach((t) => {
    if (t.category !== "Income") {
      if (!categoryData[t.category]) categoryData[t.category] = 0;
      categoryData[t.category] += Math.abs(t.amount);
    }
  });

  const pieData = Object.keys(categoryData).map((c) => ({
    name: c,
    value: categoryData[c],
  }));

  const COLORS = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"];

  return (
    <div className="grid grid-cols-2 gap-6">
      {/* LINE CHART */}
      <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5 backdrop-blur-xl shadow-xl hover:shadow-blue-500/10 transition">
        <h2 className="text-xl mb-4">Spending Trend</h2>

        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={lineData}>
            <XAxis dataKey="month" stroke="#aaa" />
            <YAxis stroke="#aaa" />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="spending"
              stroke="#3b82f6"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* PIE CHART */}
      <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-2xl border border-white/5 backdrop-blur-xl shadow-xl hover:shadow-blue-500/10 transition">
        <h2 className="text-xl mb-4">Spending by Category</h2>

        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={pieData}
              dataKey="value"
              outerRadius={80}
              label
            >
              {pieData.map((entry, index) => (
                <Cell
                  key={index}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}