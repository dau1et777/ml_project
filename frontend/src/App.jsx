import React, { useState, useEffect } from "react";
import API from "./api";
import Login from "./Login";
import Signup from "./Signup";
import Profile from "./Profile";
import QuizWizard from "./QuizWizard";
import CareerList from "./CareerList";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState("quiz"); // 'quiz', 'profile', 'careers'
  const [showSignup, setShowSignup] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem("token");
    if (token) {
      API.getProfile(token)
        .then((profile) => setUser(profile))
        .catch(() => {
          localStorage.removeItem("token");
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    setView("quiz");
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  // Show auth screen if not logged in
  if (!user) {
    return showSignup ? (
      <Signup
        onSignup={handleLogin}
        onSwitchToLogin={() => setShowSignup(false)}
      />
    ) : (
      <Login
        onLogin={handleLogin}
        onSwitchToSignup={() => setShowSignup(true)}
      />
    );
  }

  // Main app with navigation
  return (
    <div className="app-container">
      <nav className="app-nav">
        <div className="nav-brand">Career Guidance</div>
        <div className="nav-links">
          <button
            className={view === "quiz" ? "active" : ""}
            onClick={() => setView("quiz")}
          >
            Take Quiz
          </button>
          <button
            className={view === "careers" ? "active" : ""}
            onClick={() => setView("careers")}
          >
            Browse Careers
          </button>
          <button
            className={view === "profile" ? "active" : ""}
            onClick={() => setView("profile")}
          >
            Profile
          </button>
        </div>
      </nav>

      <main className="app-main">
        {view === "quiz" && <QuizWizard />}
        {view === "careers" && <CareerList />}
        {view === "profile" && <Profile user={user} onLogout={handleLogout} />}
      </main>
    </div>
  );
}

export default App;
