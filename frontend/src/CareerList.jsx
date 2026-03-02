import React, { useEffect, useState } from "react";
import API from "./api";
import CareerDetail from "./CareerDetail";
import "./CareerList.css";

function CareerList({ careerToOpen, onCareerOpened }) {
  const [careers, setCareers] = useState([]);
  const [allCareers, setAllCareers] = useState([]);
  const [bookmarkedNames, setBookmarkedNames] = useState([]);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    loadCareers();
  }, []);

  // Auto-open career when careerToOpen is provided
  useEffect(() => {
    if (careerToOpen && allCareers.length > 0) {
      const career = allCareers.find(c => c.name === careerToOpen);
      if (career) {
        openCareer(career);
        if (onCareerOpened) {
          onCareerOpened();
        }
      }
    }
  }, [careerToOpen, allCareers]);

  const loadCareers = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      let profile = null;
      if (token) {
        try {
          profile = await API.getProfile(token);
        } catch (profileErr) {
          console.warn("Could not load profile for bookmarks:", profileErr);
        }
      }

      const loadedCareers = [];
      let nextPage = 1;
      let hasNext = true;

      while (hasNext) {
        const data = await API.getCareers(nextPage);
        loadedCareers.push(...(data.results || []));
        hasNext = !!data.next;
        nextPage += 1;
      }

      setAllCareers(loadedCareers);
      setBookmarkedNames(profile?.bookmarked_careers || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const normalizeText = (value) => (value || "").toString().toLowerCase();

  const filteredCareers = allCareers.filter((career) => {
    const q = normalizeText(searchTerm).trim();
    if (!q) return true;

    return (
      normalizeText(career.name).includes(q) ||
      normalizeText(career.description).includes(q) ||
      normalizeText(career.category_display || career.category).includes(q)
    );
  });

  const bookmarkedCareers = filteredCareers.filter((career) =>
    bookmarkedNames.includes(career.name)
  );

  const nonBookmarkedCareers = filteredCareers.filter(
    (career) => !bookmarkedNames.includes(career.name)
  );

  const openCareer = async (career) => {
    try {
      const detailed = await API.getCareer(career.id);
      setSelectedCareer(detailed);
    } catch (detailErr) {
      console.error("Failed to load career detail:", detailErr);
      setSelectedCareer(career);
    }
  };

  const handleBookmarkChange = (careerName, isBookmarked) => {
    setBookmarkedNames((prev) => {
      if (isBookmarked && !prev.includes(careerName)) {
        return [...prev, careerName];
      }
      if (!isBookmarked) {
        return prev.filter((name) => name !== careerName);
      }
      return prev;
    });
  };

  if (selectedCareer) {
    return (
      <CareerDetail
        career={selectedCareer}
        onBack={() => setSelectedCareer(null)}
        isBookmarked={bookmarkedNames.includes(selectedCareer.name)}
        onBookmarkChange={handleBookmarkChange}
      />
    );
  }

  return (
    <div className="career-list-container">
      <div className="career-list-header">
        <h1>Explore Careers</h1>
          <p>Search and discover from {allCareers.length} career profiles</p>
          <div className="header-stats">
            <div className="header-stat">
              <span className="stat-number">{allCareers.length}</span>
              <span className="stat-text">Total Careers</span>
            </div>
            <div className="header-stat">
              <span className="stat-number">{bookmarkedNames.length}</span>
              <span className="stat-text">Bookmarked</span>
            </div>
            <div className="header-stat">
              <span className="stat-number">{filteredCareers.length}</span>
              <span className="stat-text">Showing</span>
            </div>
          </div>
      </div>

      <div className="career-search-row">
        <input
          type="text"
          className="career-search-input"
          placeholder="Search by name, category, or keyword..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading careers...</p>
        </div>
      ) : error ? (
        <div className="error-state">
          <p>{error}</p>
          <button onClick={loadCareers} className="btn btn-secondary">
            Try Again
          </button>
        </div>
      ) : (
        <>
          <div className="career-section-title">Bookmarked Careers</div>
          {bookmarkedCareers.length === 0 ? (
            <div className="empty-bookmarks">No bookmarked careers yet.</div>
          ) : (
            <div className="career-grid bookmarked-grid">
              {bookmarkedCareers.map((career) => (
                <div
                  key={career.id}
                  className="career-card bookmarked"
                  onClick={() => openCareer(career)}
                >
                  <div className="career-card-header">
                    <h3>{career.name}</h3>
                    <span className="career-category">{career.category_display || career.category}</span>
                  </div>
                  <p className="career-description">{career.description}</p>
                  <div className="career-card-footer">
                    <div className="career-salary">💰 {career.salary_range}</div>
                    <div className="career-demand">📈 {career.demand_level_display || career.demand_level}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="career-section-title">All Careers</div>
          <div className="career-grid">
            {nonBookmarkedCareers.map((career) => (
              <div
                key={career.id}
                className="career-card"
                onClick={() => openCareer(career)}
              >
                <div className="career-card-header">
                  <h3>{career.name}</h3>
                  <span className="career-category">{career.category_display || career.category}</span>
                </div>
                <p className="career-description">{career.description}</p>
                <div className="career-card-footer">
                  <div className="career-salary">
                    💰 {career.salary_range}
                  </div>
                  <div className="career-demand">
                    📈 {career.demand_level_display || career.demand_level}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredCareers.length === 0 && (
            <div className="empty-bookmarks">No careers match your search.</div>
          )}
        </>
      )}
    </div>
  );
}

export default CareerList;
