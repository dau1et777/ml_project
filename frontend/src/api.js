/**
 * API Service - Handles communication with Django REST backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

function authHeaders(token) {
  return token ? { Authorization: `Token ${token}` } : {};
}

export const API = {
  // ===== Authentication =====
  
  async signup({ email, username, password }) {
    const res = await fetch(`${API_BASE_URL}/auth/signup/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, username, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Signup failed");
    }
    return res.json(); // { success, token, user }
  },

  async login({ username, password }) {
    const res = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Login failed");
    }
    return res.json(); // { success, token, user }
  },

  async getProfile(token) {
    const res = await fetch(`${API_BASE_URL}/auth/profile/`, {
      headers: { ...authHeaders(token) },
    });
    if (!res.ok) throw new Error("Profile fetch failed");
    const data = await res.json();
    return data.profile;
  },

  // ===== Predictions =====
  
  async predict(answers, token, save = true) {
    const res = await fetch(`${API_BASE_URL}/predict/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(token),
      },
      body: JSON.stringify({ answers, save_result: save }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Prediction failed");
    }
    return res.json(); // { success, predictions: {top_careers, ...}, result_id }
  },

  async getPredictionHistory(token) {
    const res = await fetch(`${API_BASE_URL}/predict/history/`, {
      headers: { ...authHeaders(token) },
    });
    if (!res.ok) throw new Error("Could not load history");
    return res.json();
  },

  // ===== Careers =====
  
  async getCareers(page = 1) {
    const res = await fetch(`${API_BASE_URL}/careers/?page=${page}`);
    if (!res.ok) throw new Error("Career list failed");
    return res.json();
  },

  async getCareer(id) {
    const res = await fetch(`${API_BASE_URL}/careers/${id}/`);
    if (!res.ok) throw new Error("Career detail failed");
    return res.json();
  },

  async getCareerRoadmap(id) {
    const res = await fetch(`${API_BASE_URL}/careers/${id}/roadmap/`);
    if (!res.ok) throw new Error("Roadmap fetch failed");
    return res.json();
  },

  async bookmarkCareer(id, token, action = "add") {
    const res = await fetch(`${API_BASE_URL}/careers/${id}/bookmark/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(token),
      },
      body: JSON.stringify({ action }),
    });
    if (!res.ok) throw new Error("Bookmark failed");
    return res.json();
  },

  // ===== Analysis =====
  
  async getSkillGap(careerName, token) {
    const res = await fetch(
      `${API_BASE_URL}/skill-gap/?career=${encodeURIComponent(careerName)}`,
      { headers: { ...authHeaders(token) } }
    );
    if (!res.ok) throw new Error("Skill gap analysis failed");
    return res.json();
  },

  async getLearningPath(careerName, token) {
    const res = await fetch(
      `${API_BASE_URL}/learning-path/?career=${encodeURIComponent(careerName)}`,
      { headers: { ...authHeaders(token) } }
    );
    if (!res.ok) throw new Error("Learning path failed");
    return res.json();
  },

  // ===== System =====
  
  async getHealth() {
    const res = await fetch(`${API_BASE_URL}/health/`);
    if (!res.ok) throw new Error("Health check failed");
    return res.json();
  },

  async getInfo() {
    const res = await fetch(`${API_BASE_URL}/info/`);
    if (!res.ok) throw new Error("API info failed");
    return res.json();
  },
};

export default API;
