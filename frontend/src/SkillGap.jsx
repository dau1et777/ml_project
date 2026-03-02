import React, { useEffect, useState } from "react";
import API from "./api";
import "./SkillGap.css";

function SkillGap({ careerName, onBack }) {
  const [analysis, setAnalysis] = useState(null);
  const [learningPath, setLearningPath] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAnalysis();
  }, [careerName]);

  const loadAnalysis = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please log in to view skill gap analysis");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const [gapData, pathData] = await Promise.all([
        API.getSkillGap(careerName, token),
        API.getLearningPath(careerName, token).catch(() => null),
      ]);
      setAnalysis(gapData);
      setLearningPath(pathData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="skill-gap-container">
        <button onClick={onBack} className="back-button">
          ← Back
        </button>
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Analyzing your skills...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="skill-gap-container">
        <button onClick={onBack} className="back-button">
          ← Back
        </button>
        <div className="error-state">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const { missing_skills, developing_skills, matching_skills } = analysis || {};

  return (
    <div className="skill-gap-container">
      <button onClick={onBack} className="back-button">
        ← Back to Career
      </button>

      <div className="skill-gap-header">
        <h1>Skill Gap Analysis</h1>
        <p>For {careerName}</p>
      </div>

      <div className="skill-gap-content">
        {missing_skills && missing_skills.length > 0 && (
          <section className="skill-section missing">
            <h2>🔴 Skills to Learn</h2>
            <p className="section-description">
              These skills are required but not yet in your profile
            </p>
            <div className="skill-grid">
              {missing_skills.map((skill, idx) => (
                <div key={idx} className="skill-card missing-card">
                  <h3>{skill.name}</h3>
                  <div className="skill-category">{skill.category}</div>
                  <div className="skill-level">
                    Required: <strong>{skill.required_level}</strong>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {developing_skills && developing_skills.length > 0 && (
          <section className="skill-section developing">
            <h2>🟡 Skills to Improve</h2>
            <p className="section-description">
              You have these skills but need to reach higher proficiency
            </p>
            <div className="skill-grid">
              {developing_skills.map((skill, idx) => (
                <div key={idx} className="skill-card developing-card">
                  <h3>{skill.name}</h3>
                  <div className="skill-category">{skill.category}</div>
                  <div className="skill-progress">
                    <div className="progress-labels">
                      <span>Current: {skill.current_level}</span>
                      <span>Target: {skill.required_level}</span>
                    </div>
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{ width: `${skill.gap_percentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {matching_skills && matching_skills.length > 0 && (
          <section className="skill-section matching">
            <h2>🟢 Skills You Have</h2>
            <p className="section-description">
              These skills meet or exceed the requirements
            </p>
            <div className="skill-grid">
              {matching_skills.map((skill, idx) => (
                <div key={idx} className="skill-card matching-card">
                  <h3>{skill.name}</h3>
                  <div className="skill-category">{skill.category}</div>
                  <div className="skill-level">
                    Level: <strong>{skill.current_level}</strong> ✓
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {learningPath && learningPath.recommendations && (
          <section className="learning-path-section">
            <h2>📚 Recommended Learning Path</h2>
            <div className="learning-recommendations">
              {learningPath.recommendations.map((rec, idx) => (
                <div key={idx} className="learning-item">
                  <div className="learning-priority">Priority {rec.priority}</div>
                  <h3>{rec.skill_name}</h3>
                  <p>{rec.reason}</p>
                  {rec.estimated_time && (
                    <div className="learning-time">⏱ {rec.estimated_time}</div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

export default SkillGap;
