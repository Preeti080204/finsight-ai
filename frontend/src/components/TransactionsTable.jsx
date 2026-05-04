import React from "react";

export default function TransactionsTable({ transactions }) {
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
          </tr>
        </thead>

        <tbody>
          {transactions.map((t, i) => (
            <tr
              key={`${t.date}-${t.desc}-${t.amount}-${i}`}
              className="border-t border-gray-800"
            >
              <td>{t.date}</td>
              <td>{t.desc}</td>
              <td>₹{t.amount}</td>
              <td>{t.category}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}