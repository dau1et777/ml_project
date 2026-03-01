import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

/**
 * InterestChart - Display interests as bar chart
 * @param {Object} interests - Object with interest names and scores
 */
function InterestChart({ interests }) {
  if (!interests || Object.keys(interests).length === 0) {
    return null;
  }

  // Convert object to array format for bar chart
  const data = Object.entries(interests).map(([name, value]) => ({
    name,
    value: parseFloat(value),
  }));

  return (
    <div className="chart-card interests-card">
      <h3>Your Interest Profile</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey="name" tick={{ fill: "#666", fontSize: 12 }} />
          <YAxis tick={{ fill: "#999" }} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#fff",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
            formatter={(value) => `${value.toFixed(1)}`}
          />
          <Bar dataKey="value" fill="#10b981" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default InterestChart;
