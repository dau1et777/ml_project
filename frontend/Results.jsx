import React from "react";
import "./Results.css";

/**
 * Results Component - Display recommendation results
 * @param {Array} recommendations - Array of recommended careers
 * @param {Function} onRestart - Callback to restart quiz
 */
function Results({ recommendations, onRestart }) {
  return (
    <div className="results-container">
      <div className="results-header">
        <h1>Your Career Recommendations</h1>
        <p>Based on your answers, here are the top 5 careers for you</p>
      </div>

      <div className="results-list">
        {recommendations.map((rec, index) => (
          <div key={index} className={`result-card rank-${rec.rank}`}>
            <div className="result-rank">#{rec.rank}</div>

            <div className="result-content">
              <h2 className="result-career">{rec.career}</h2>

              <div className="result-match">
                <div className="match-circle">
                  <div className="match-percentage">{rec.match_percentage}%</div>
                  <div className="match-label">Match</div>
                </div>
              </div>

              <p className="result-description">{rec.description}</p>

              <div className="result-explanation">
                <h4>Why this role matches you:</h4>
                <p>{rec.explanation}</p>
              </div>
            </div>

            <div className="result-visual">
              <div className="match-bar">
                <div
                  className="match-bar-fill"
                  style={{ width: `${rec.match_percentage}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="results-footer">
        <button className="btn btn-primary btn-large" onClick={onRestart}>
          Retake Quiz
        </button>
        <p className="footer-text">
          💡 Share these results with mentors or career counselors for more insights
        </p>
      </div>
    </div>
  );
}

export default Results;
