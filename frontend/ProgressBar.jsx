import React from "react";
import "./ProgressBar.css";

/**
 * ProgressBar Component - Shows quiz progress
 * @param {number} current - Current question number (0-24)
 * @param {number} total - Total questions (25)
 */
function ProgressBar({ current, total }) {
  const percentage = ((current + 1) / total) * 100;

  return (
    <div className="progress-container">
      <div className="progress-info">
        <span className="progress-text">
          Question {current + 1} of {total}
        </span>
        <span className="progress-percentage">{Math.round(percentage)}%</span>
      </div>
      <div className="progress-bar">
        <div
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
}

export default ProgressBar;
