import React, { useEffect, useState } from "react";
import API from "./api";
import Results from "./Results";
import "./Profile.css";

function Profile({ user, onLogout }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedHistoryItem, setSelectedHistoryItem] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      API.getPredictionHistory(token)
        .then((data) => {
          if (data.success) {
            setHistory(data.results || []);
          }
        })
        .catch((err) => console.error("Failed to load history:", err))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const getTopCareerName = (result) => {
    if (!result?.top_careers || result.top_careers.length === 0) return "No result";
    return result.top_careers[0]?.name || "No result";
  };

  const getResultDate = (result) => {
    const raw = result?.created_at;
    if (!raw) return "Unknown date";
    const d = new Date(raw);
    return `${d.toLocaleDateString()} at ${d.toLocaleTimeString()}`;
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    onLogout();
  };

  const normalizeRecommendations = (result) => {
    const explanations = result?.explanation || {};

    return (result?.top_careers || [])
      .filter((career) => career?.name || career?.career)
      .map((career, index) => {
        const rawScore = career.match_score ?? career.score ?? 0;
        const normalizedScore = rawScore <= 1 ? Math.round(rawScore * 100) : Math.round(rawScore);
        const careerName = career.name || career.career;

        return {
          rank: career.rank || index + 1,
          career: careerName,
          match_percentage: normalizedScore,
          description: career.description || "",
          explanation:
            career.explanation ||
            explanations[careerName] ||
            "This career aligns with your quiz profile.",
        };
      });
  };

  if (selectedHistoryItem) {
    return (
      <Results
        recommendations={normalizeRecommendations(selectedHistoryItem)}
        profile={selectedHistoryItem.profile}
        onRestart={() => setSelectedHistoryItem(null)}
        actionLabel="Back to Quiz History"
      />
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="profile-info">
          <div className="profile-avatar">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2>{user.username}</h2>
            <p className="profile-email">{user.email}</p>
          </div>
        </div>
        <button onClick={handleLogout} className="btn btn-secondary">
          Logout
        </button>
      </div>

      <div className="profile-section">
        <h3>Quiz History</h3>
        {loading ? (
          <p>Loading...</p>
        ) : history.length === 0 ? (
          <p className="empty-state">No quiz results yet. Take the quiz to get started!</p>
        ) : (
          <div className="history-list">
            {history.map((result) => (
              <button
                key={result.id}
                className="history-item"
                onClick={() => setSelectedHistoryItem(result)}
                type="button"
              >
                <div className="history-date">
                  {getResultDate(result)}
                </div>
                <div className="history-careers">
                  <strong>Top Result:</strong> {getTopCareerName(result)}
                </div>
                <div className="history-open-hint">Tap to open full results and charts →</div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
