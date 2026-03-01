/**
 * API Service - Handles communication with backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export const API = {
  /**
   * Get career recommendations from quiz answers
   * @param {Object} answers - Quiz answers {q1: 8, ..., q25: 'A'}
   * @param {Boolean} debug - Enable debug mode
   * @returns {Promise} Recommendation results
   */
  async getRecommendations(answers, debug = false) {
    try {
      const response = await fetch(`${API_BASE_URL}/recommend/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          answers,
          debug,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to get recommendations");
      }

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || "Recommendation failed");
      }

      return data;
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },

  /**
   * Check API health
   * @returns {Promise} Health status
   */
  async getHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error("API health check failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Health check failed:", error);
      throw error;
    }
  },

  /**
   * Get API information
   * @returns {Promise} API info
   */
  async getInfo() {
    try {
      const response = await fetch(`${API_BASE_URL}/info/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error("Failed to get API info");
      }

      return await response.json();
    } catch (error) {
      console.error("Failed to get API info:", error);
      throw error;
    }
  },
};

export default API;
