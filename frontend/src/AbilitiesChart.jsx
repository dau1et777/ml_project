import React from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from "recharts";

/**
 * AbilitiesChart - Display abilities as a radar chart
 * @param {Object} abilities - Object with ability names and scores
 */
function AbilitiesChart({ abilities }) {
  if (!abilities || Object.keys(abilities).length === 0) {
    return null;
  }

  // Convert object to array format for radar chart
  const data = Object.entries(abilities).map(([name, value]) => ({
    name,
    value: parseFloat(value),
  }));

  return (
    <div className="chart-card abilities-card">
      <h3>Your Abilities & Capabilities</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={data} margin={{ top: 40, right: 80, bottom: 40, left: 80 }}>
          <PolarGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <PolarAngleAxis dataKey="name" tick={{ fill: "#666", fontSize: 12 }} />
          <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} />
          <Radar name="Abilities" dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.6} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default AbilitiesChart;
