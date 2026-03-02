import React, { useEffect, useState } from "react";
import ProgressBar from "./ProgressBar";
import Results from "./Results";
import API from "./api";
import "./QuizWizard.css";

const QUIZ_STATE_STORAGE_KEY = "career_quiz_state_v1";

// Quiz questions definition (exactly as specified)
const QUIZ_QUESTIONS = [
  // Q1-Q20: Scale (1-10)
  {
    id: "q1",
    text: "How comfortable are you with solving complex, multi-step problems?",
    type: "scale",
  },
  {
    id: "q2",
    text: "Do you enjoy analyzing data and finding patterns?",
    type: "scale",
  },
  {
    id: "q3",
    text: "How good are you at logical reasoning and abstract thinking?",
    type: "scale",
  },
  {
    id: "q4",
    text: "Do you prefer working with theoretical concepts or practical applications?",
    type: "scale",
  },
  {
    id: "q5",
    text: "How much do you enjoy debugging and troubleshooting problems?",
    type: "scale",
  },
  {
    id: "q6",
    text: "How creative are you in generating new ideas?",
    type: "scale",
  },
  {
    id: "q7",
    text: "Do you enjoy designing visual or user experiences?",
    type: "scale",
  },
  {
    id: "q8",
    text: "How much do you value innovation and doing things differently?",
    type: "scale",
  },
  {
    id: "q9",
    text: "Can you translate abstract concepts into tangible deliverables?",
    type: "scale",
  },
  {
    id: "q10",
    text: "How comfortable are you with ambiguity and open-ended challenges?",
    type: "scale",
  },
  {
    id: "q11",
    text: "How skilled are you at explaining complex ideas to others?",
    type: "scale",
  },
  {
    id: "q12",
    text: "Do you enjoy mentoring or helping others grow?",
    type: "scale",
  },
  {
    id: "q13",
    text: "How comfortable are you with public speaking or presentations?",
    type: "scale",
  },
  {
    id: "q14",
    text: "How good are you at negotiation and persuasion?",
    type: "scale",
  },
  {
    id: "q15",
    text: "How naturally do you take on leadership roles?",
    type: "scale",
  },
  {
    id: "q16",
    text: "How strong is your foundation in mathematics?",
    type: "scale",
  },
  {
    id: "q17",
    text: "How interested are you in scientific research and discovery?",
    type: "scale",
  },
  {
    id: "q18",
    text: "How proficient are you with programming and software development?",
    type: "scale",
  },
  {
    id: "q19",
    text: "How comfortable are you learning new technical tools and frameworks?",
    type: "scale",
  },
  {
    id: "q20",
    text: "How much do you value continuous learning and self-improvement?",
    type: "scale",
  },

  // Q21-Q25: Forced choice (A/B/C/D)
  {
    id: "q21",
    text: "What environment energizes you the most?",
    type: "choice",
    options: {
      A: "Fast-paced, high-pressure, deadline-driven",
      B: "Collaborative, team-oriented, social",
      C: "Independent, focused, minimally supervised",
      D: "Structured, organized, predictable",
    },
  },
  {
    id: "q22",
    text: "What type of problems excite you?",
    type: "choice",
    options: {
      A: "Technical/engineering challenges",
      B: "Human/social problems",
      C: "Business/strategic problems",
      D: "Creative/artistic challenges",
    },
  },
  {
    id: "q23",
    text: "What matters most in your career?",
    type: "choice",
    options: {
      A: "Impact and making a difference",
      B: "Financial rewards and stability",
      C: "Personal growth and learning",
      D: "Work-life balance and flexibility",
    },
  },
  {
    id: "q24",
    text: "Which work style resonates with you?",
    type: "choice",
    options: {
      A: "Hands-on, building things",
      B: "Strategic planning and analysis",
      C: "Customer-facing and relationship-building",
      D: "Creative expression and innovation",
    },
  },
  {
    id: "q25",
    text: "What's your ideal success measure?",
    type: "choice",
    options: {
      A: "Results and quantifiable outcomes",
      B: "Mastery and expertise",
      C: "Team satisfaction and culture",
      D: "Innovation and thought leadership",
    },
  },

  // ============================================================
  // NEW QUESTIONS (Q26-Q35) - EXTENSION BLOCK
  // These improve career differentiation without affecting Q1-Q25
  // ============================================================

  // Q26-Q33: Interest Profile (Scale 1-10)
  {
    id: "q26",
    text: "How interested are you in technology, programming, and digital innovation?",
    type: "scale",
  },
  {
    id: "q27",
    text: "How interested are you in business, entrepreneurship, and finance?",
    type: "scale",
  },
  {
    id: "q28",
    text: "How interested are you in creative expression, design, and artistic work?",
    type: "scale",
  },
  {
    id: "q29",
    text: "How interested are you in helping people, social causes, and community impact?",
    type: "scale",
  },
  {
    id: "q30",
    text: "How interested are you in data analysis, research, and scientific investigation?",
    type: "scale",
  },
  {
    id: "q31",
    text: "How interested are you in product development, strategy, and bringing ideas to market?",
    type: "scale",
  },
  {
    id: "q32",
    text: "How interested are you in training, education, and developing others?",
    type: "scale",
  },
  {
    id: "q33",
    text: "How interested are you in operations, process improvement, and efficiency?",
    type: "scale",
  },

  // Q34-Q35: Work Style Preferences (Scale 1-10)
  {
    id: "q34",
    text: "Do you prefer working independently and autonomously (1) or having clear structure and guidance (10)?",
    type: "scale",
  },
  {
    id: "q35",
    text: "Do you prefer job stability and predictable career paths (1) or taking risks for potentially greater rewards (10)?",
    type: "scale",
  },
];

/**
 * QuizWizard Component - Main quiz interface
 */
function QuizWizard() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [profile, setProfile] = useState(null); // user profile breakdown for charts
  const [error, setError] = useState(null);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    try {
      const rawState = localStorage.getItem(QUIZ_STATE_STORAGE_KEY);
      if (!rawState) {
        setIsHydrated(true);
        return;
      }

      const savedState = JSON.parse(rawState);
      if (typeof savedState.currentQuestion === "number") {
        setCurrentQuestion(
          Math.min(
            Math.max(savedState.currentQuestion, 0),
            QUIZ_QUESTIONS.length - 1
          )
        );
      }
      if (savedState.answers && typeof savedState.answers === "object") {
        setAnswers(savedState.answers);
      }
      if (Array.isArray(savedState.results)) {
        setResults(savedState.results);
      }
      if (savedState.profile && typeof savedState.profile === "object") {
        setProfile(savedState.profile);
      }
    } catch (restoreError) {
      console.error("Failed to restore quiz state:", restoreError);
    } finally {
      setIsHydrated(true);
    }
  }, []);

  useEffect(() => {
    if (!isHydrated) return;

    const stateToSave = {
      currentQuestion,
      answers,
      results,
      profile,
    };

    localStorage.setItem(QUIZ_STATE_STORAGE_KEY, JSON.stringify(stateToSave));
  }, [currentQuestion, answers, results, profile, isHydrated]);

  const currentQ = QUIZ_QUESTIONS[currentQuestion];
  const isLastQuestion = currentQuestion === QUIZ_QUESTIONS.length - 1;

  const handleAnswer = (value) => {
    setAnswers({
      ...answers,
      [currentQ.id]: value,
    });

    // Auto-advance if not last question
    if (!isLastQuestion) {
      setTimeout(() => {
        setCurrentQuestion(currentQuestion + 1);
      }, 300);
    }
  };

  const handleNext = () => {
    if (currentQuestion < QUIZ_QUESTIONS.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrev = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    // Validate all questions answered
    if (Object.keys(answers).length !== QUIZ_QUESTIONS.length) {
      setError("Please answer all questions before submitting");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Convert q1, q2, ... to 1, 2, ... for backend
      const numericAnswers = {};
      Object.keys(answers).forEach(key => {
        const numKey = parseInt(key.replace('q', ''));
        numericAnswers[numKey] = answers[key];
      });

      const token = localStorage.getItem("token");
      const response = await API.predict(numericAnswers, token);
      
      if (response.success && response.predictions) {
        setResults(response.predictions.top_careers || []);
        if (response.predictions.profile) {
          setProfile(response.predictions.profile);
        }
      }
    } catch (err) {
      setError(
        err.message ||
          "Failed to get recommendations. Please try again or check the backend connection."
      );
      console.error("Recommendation error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setCurrentQuestion(0);
    setAnswers({});
    setResults(null);
    setProfile(null);
    setError(null);
    localStorage.removeItem(QUIZ_STATE_STORAGE_KEY);
  };

  // Show results if quiz is completed
  if (results) {
    return (
      <Results
        recommendations={results}
        profile={profile}
        onRestart={handleRestart}
      />
    );
  }

  // Show quiz
  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h1>Career Recommendation Quiz</h1>
        <p className="quiz-subtitle">Answer 35 questions to discover your ideal careers</p>
      </div>

      <ProgressBar current={currentQuestion} total={QUIZ_QUESTIONS.length} />

      <div className="quiz-content">
        <div className="question-box">
          <h2>{currentQ.text}</h2>

          {currentQ.type === "scale" ? (
            <div className="scale-container">
              <div className="scale-labels">
                <span>Not at all</span>
                <span>Very much</span>
              </div>
              <div className="scale-options">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((value) => (
                  <button
                    key={value}
                    className={`scale-btn ${
                      answers[currentQ.id] === value ? "active" : ""
                    }`}
                    onClick={() => handleAnswer(value)}
                  >
                    {value}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="choice-options">
              {Object.entries(currentQ.options).map(([key, text]) => (
                <button
                  key={key}
                  className={`choice-btn ${
                    answers[currentQ.id] === key ? "active" : ""
                  }`}
                  onClick={() => handleAnswer(key)}
                >
                  <span className="choice-letter">{key}</span>
                  <span className="choice-text">{text}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="button-group">
          <button
            className="btn btn-secondary"
            onClick={handlePrev}
            disabled={currentQuestion === 0}
          >
            ← Previous
          </button>

          {isLastQuestion ? (
            <button
              className="btn btn-primary"
              onClick={handleSubmit}
              disabled={isLoading || Object.keys(answers).length !== QUIZ_QUESTIONS.length}
            >
              {isLoading ? "Loading..." : "Submit & Get Results"}
            </button>
          ) : (
            <button
              className="btn btn-primary"
              onClick={handleNext}
              disabled={!answers[currentQ.id]}
            >
              Next →
            </button>
          )}
        </div>

        <div className="quiz-footer">
          <span>
            {Object.keys(answers).length}/{QUIZ_QUESTIONS.length} answered
          </span>
        </div>
      </div>
    </div>
  );
}

export default QuizWizard;
