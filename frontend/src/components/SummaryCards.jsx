import React from "react";
import { motion } from "framer-motion";

export default function SummaryCards({ data }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <Card title="Income" value={`₹${data.income}`} />
      <Card title="Spending" value={`₹${data.spending}`} />
      <Card title="Savings Rate" value={`${data.savings_rate}%`} />
    </div>
  );
}

function Card({ title, value }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="bg-gray-900 p-6 rounded-2xl shadow-lg hover:shadow-blue-500/20 transition"
    >
      <p className="text-gray-400">{title}</p>
      <h2 className="text-2xl font-bold">{value}</h2>
    </motion.div>
  );
}