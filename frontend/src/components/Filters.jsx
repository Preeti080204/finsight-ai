import React from "react";

export default function Filters({ transactions, setFiltered }) {
  // Extract unique categories
  const categories = [
    "All",
    ...new Set(transactions.map((t) => t.category)),
  ];

  // Extract months
  const months = [
    "All",
    ...new Set(transactions.map((t) => t.date.slice(0, 7))),
  ];

  const handleFilter = (category, month) => {
    let filtered = transactions;

    if (category !== "All") {
      filtered = filtered.filter((t) => t.category === category);
    }

    if (month !== "All") {
      filtered = filtered.filter((t) =>
        t.date.startsWith(month)
      );
    }

    setFiltered(filtered);
  };

  return (
    <div className="bg-gray-900 p-4 rounded-2xl flex gap-4">

      {/* CATEGORY */}
      <select
        onChange={(e) =>
          handleFilter(e.target.value, "All")
        }
        className="bg-gray-800 p-2 rounded"
      >
        {categories.map((c, i) => (
          <option key={i}>{c}</option>
        ))}
      </select>

      {/* MONTH */}
      <select
        onChange={(e) =>
          handleFilter("All", e.target.value)
        }
        className="bg-gray-800 p-2 rounded"
      >
        {months.map((m, i) => (
          <option key={i}>{m}</option>
        ))}
      </select>
    </div>
  );
}