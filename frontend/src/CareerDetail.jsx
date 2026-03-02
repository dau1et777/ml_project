import React, { useEffect, useState } from "react";
import API from "./api";
import SkillGap from "./SkillGap";
import "./CareerDetail.css";

function CareerDetail({ career, onBack, isBookmarked = false, onBookmarkChange }) {
  const [roadmap, setRoadmap] = useState([]);
  const [showSkillGap, setShowSkillGap] = useState(false);
  const [bookmarked, setBookmarked] = useState(isBookmarked);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setBookmarked(isBookmarked);
  }, [isBookmarked, career.id]);

  useEffect(() => {
    loadRoadmap();
  }, [career.id]);

  const loadRoadmap = async () => {
    try {
      const data = await API.getCareerRoadmap(career.id);
      setRoadmap(data.roadmap || []);
    } catch (err) {
      console.error("Failed to load roadmap:", err);
    }
  };

  const handleBookmark = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      setLoading(true);
      const nextAction = bookmarked ? "remove" : "add";
      await API.bookmarkCareer(career.id, token, nextAction);
      const nextState = !bookmarked;
      setBookmarked(nextState);
      if (onBookmarkChange) {
        onBookmarkChange(career.name, nextState);
      }
    } catch (err) {
      console.error("Bookmark failed:", err);
    } finally {
      setLoading(false);
    }
  };

  if (showSkillGap) {
    return (
      <SkillGap
        careerName={career.name}
        onBack={() => setShowSkillGap(false)}
      />
    );
  }

  return (
    <div className="career-detail-container">
      <button onClick={onBack} className="back-button">
        ← Back to Careers
      </button>

      <div className="career-detail-header">
        <div>
          <h1>{career.name}</h1>
          <p className="career-detail-category">{career.category}</p>
        </div>
        <button
          onClick={handleBookmark}
          disabled={loading}
          className="btn btn-secondary"
        >
          {bookmarked ? "Remove Bookmark" : "Bookmark"}
        </button>
      </div>

      <div className="career-detail-content">
        <section className="detail-section">
          <h2>Overview</h2>
          <p>{career.description}</p>
        </section>

        <section className="detail-section">
          <div className="detail-stats">
            <div className="stat-card">
              <div className="stat-label">Salary Range</div>
              <div className="stat-value">{career.salary_range}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Demand Level</div>
              <div className="stat-value">{career.demand_level}</div>
            </div>
          </div>
        </section>

          <section className="detail-section">
            <h2>Career Highlights</h2>
            <div className="info-grid">
              <div className="info-box">
                <div className="info-icon">💼</div>
                <div className="info-label">Work Environment</div>
                <div className="info-text">Office, Remote, Hybrid options available</div>
              </div>
              <div className="info-box">
                <div className="info-icon">📊</div>
                <div className="info-label">Growth Potential</div>
                <div className="info-text">Strong advancement opportunities</div>
              </div>
              <div className="info-box">
                <div className="info-icon">🎓</div>
                <div className="info-label">Education</div>
                <div className="info-text">Bachelor's degree typically required</div>
              </div>
              <div className="info-box">
                <div className="info-icon">⏱️</div>
                <div className="info-label">Work-Life Balance</div>
                <div className="info-text">Varies by company and role level</div>
              </div>
            </div>
          </section>

        {career.required_skills && career.required_skills.length > 0 && (
          <section className="detail-section">
            <h2>Required Skills</h2>
            <div className="skills-list">
              {career.required_skills.map((skill, idx) => (
                <span key={idx} className="skill-tag">
                  {skill.name}
                </span>
              ))}
            </div>
          </section>
        )}

        {roadmap.length > 0 && (
          <section className="detail-section">
            <h2>Learning Roadmap</h2>
            <div className="roadmap-timeline">
              {roadmap.map((stage, idx) => (
                <div key={idx} className="roadmap-stage">
                  <div className="stage-marker">{idx + 1}</div>
                  <div className="stage-content">
                    <h3>{stage.stage}</h3>
                    <p className="stage-duration">
                      ~{stage.duration_months} months
                    </p>
                    <p>{stage.description}</p>
                    {stage.skills_to_learn && (
                      <div className="stage-skills">
                        <strong>Learn:</strong> {stage.skills_to_learn.join(", ")}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        <div className="detail-actions">
          <button
            onClick={() => setShowSkillGap(true)}
            className="btn btn-primary"
          >
            Analyze Skill Gap
          </button>
        </div>
      </div>
    </div>
  );
}

export default CareerDetail;
