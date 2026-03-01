"""
Quiz Validator - Defines 25 questions and validates user answers.
Organized by cognitive categories for better ML design.
"""

QUIZ_QUESTIONS = {
    # Q1-Q5: Cognitive & Problem Solving (Scale 1-10)
    "q1": {
        "text": "How comfortable are you with solving complex, multi-step problems?",
        "category": "cognitive",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q2": {
        "text": "Do you enjoy analyzing data and finding patterns?",
        "category": "cognitive",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q3": {
        "text": "How good are you at logical reasoning and abstract thinking?",
        "category": "cognitive",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q4": {
        "text": "Do you prefer working with theoretical concepts or practical applications?",
        "category": "cognitive",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q5": {
        "text": "How much do you enjoy debugging and troubleshooting problems?",
        "category": "cognitive",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    
    # Q6-Q10: Creativity & Innovation (Scale 1-10)
    "q6": {
        "text": "How creative are you in generating new ideas?",
        "category": "creativity",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q7": {
        "text": "Do you enjoy designing visual or user experiences?",
        "category": "creativity",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q8": {
        "text": "How much do you value innovation and doing things differently?",
        "category": "creativity",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q9": {
        "text": "Can you translate abstract concepts into tangible deliverables?",
        "category": "creativity",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q10": {
        "text": "How comfortable are you with ambiguity and open-ended challenges?",
        "category": "creativity",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    
    # Q11-Q15: Communication & Leadership (Scale 1-10)
    "q11": {
        "text": "How skilled are you at explaining complex ideas to others?",
        "category": "communication",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q12": {
        "text": "Do you enjoy mentoring or helping others grow?",
        "category": "communication",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q13": {
        "text": "How comfortable are you with public speaking or presentations?",
        "category": "communication",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q14": {
        "text": "How good are you at negotiation and persuasion?",
        "category": "communication",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q15": {
        "text": "How naturally do you take on leadership roles?",
        "category": "communication",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    
    # Q16-Q20: Academic & Technical Orientation (Scale 1-10)
    "q16": {
        "text": "How strong is your foundation in mathematics?",
        "category": "academic",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q17": {
        "text": "How interested are you in scientific research and discovery?",
        "category": "academic",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q18": {
        "text": "How proficient are you with programming and software development?",
        "category": "academic",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q19": {
        "text": "How comfortable are you learning new technical tools and frameworks?",
        "category": "academic",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q20": {
        "text": "How much do you value continuous learning and self-improvement?",
        "category": "academic",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    
    # Q21-Q25: Forced Choice (Multiple Choice A/B/C/D)
    "q21": {
        "text": "What environment energizes you the most?",
        "category": "workstyle",
        "type": "choice",
        "options": {
            "A": "Fast-paced, high-pressure, deadline-driven",
            "B": "Collaborative, team-oriented, social",
            "C": "Independent, focused, minimally supervised",
            "D": "Structured, organized, predictable"
        }
    },
    "q22": {
        "text": "What type of problems excite you?",
        "category": "interests",
        "type": "choice",
        "options": {
            "A": "Technical/engineering challenges",
            "B": "Human/social problems",
            "C": "Business/strategic problems",
            "D": "Creative/artistic challenges"
        }
    },
    "q23": {
        "text": "What matters most in your career?",
        "category": "motivation",
        "type": "choice",
        "options": {
            "A": "Impact and making a difference",
            "B": "Financial rewards and stability",
            "C": "Personal growth and learning",
            "D": "Work-life balance and flexibility"
        }
    },
    "q24": {
        "text": "Which work style resonates with you?",
        "category": "workstyle",
        "type": "choice",
        "options": {
            "A": "Hands-on, building things",
            "B": "Strategic planning and analysis",
            "C": "Customer-facing and relationship-building",
            "D": "Creative expression and innovation"
        }
    },
    "q25": {
        "text": "What's your ideal success measure?",
        "category": "motivation",
        "type": "choice",
        "options": {
            "A": "Results and quantifiable outcomes",
            "B": "Mastery and expertise",
            "C": "Team satisfaction and culture",
            "D": "Innovation and thought leadership"
        }
    },
    
    # ============================================================
    # NEW QUESTIONS (Q26-Q35) - EXTENSION BLOCK
    # Added to improve career differentiation without breaking 
    # existing logic. These feature 10 new dimensions (40→50).
    # ============================================================
    
    # Q26-Q33: Interest Profile (8 questions) - Scale 1-10
    # These capture dominant career interest domains
    "q26": {
        "text": "How interested are you in technology, programming, and digital innovation?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q27": {
        "text": "How interested are you in business, entrepreneurship, and finance?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q28": {
        "text": "How interested are you in creative expression, design, and artistic work?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q29": {
        "text": "How interested are you in helping people, social causes, and community impact?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q30": {
        "text": "How interested are you in data analysis, research, and scientific investigation?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q31": {
        "text": "How interested are you in product development, strategy, and bringing ideas to market?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q32": {
        "text": "How interested are you in training, education, and developing others?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q33": {
        "text": "How interested are you in operations, process improvement, and efficiency?",
        "category": "interest_domain",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    
    # Q34-Q35: Work Style Preferences (2 questions) - Scale 1-10
    # These capture work style and risk tolerance
    "q34": {
        "text": "Do you prefer working independently and autonomously (1) or having clear structure and guidance (10)?",
        "category": "work_style",
        "type": "scale",
        "min": 1,
        "max": 10
    },
    "q35": {
        "text": "Do you prefer job stability and predictable career paths (1) or taking risks for potentially greater rewards (10)?",
        "category": "work_style",
        "type": "scale",
        "min": 1,
        "max": 10
    }
}


def validate_answers(answers):
    """
    Validates that answers are present and within expected ranges.
    
    Backward Compatibility:
    - Q1-Q25 are REQUIRED (original questions)
    - Q26-Q35 are OPTIONAL (new extension)
    - If Q26-Q35 missing, they default to 5 (neutral on 1-10 scale)
    
    Args:
        answers (dict): Dictionary of quiz answers {q1: value, q2: value, ...}
    
    Returns:
        tuple: (is_valid, error_message, normalized_answers)
    """
    required_questions = set([f"q{i}" for i in range(1, 26)])  # Q1-Q25 required
    optional_questions = set([f"q{i}" for i in range(26, 36)])  # Q26-Q35 optional
    provided_questions = set(answers.keys())
    
    # Check all required questions answered
    missing_required = required_questions - provided_questions
    if missing_required:
        return False, f"Missing required questions: {missing_required}", None
    
    # Check for unexpected questions
    all_valid_questions = required_questions | optional_questions
    extra = provided_questions - all_valid_questions
    if extra:
        return False, f"Extra unexpected questions: {extra}", None
    
    # Normalize answers: add defaults for missing Q26-Q35
    normalized_answers = dict(answers)
    missing_optional = optional_questions - provided_questions
    for q_id in missing_optional:
        normalized_answers[q_id] = 5  # Default to neutral (scale 1-10)
    
    # Validate each answer
    for q_id, answer_value in normalized_answers.items():
        question = QUIZ_QUESTIONS[q_id]
        
        if question["type"] == "scale":
            if not isinstance(answer_value, (int, float)):
                return False, f"{q_id}: Answer must be numeric, got {type(answer_value)}", None
            if not (question["min"] <= answer_value <= question["max"]):
                return False, f"{q_id}: Answer must be between {question['min']} and {question['max']}, got {answer_value}", None
        
        elif question["type"] == "choice":
            valid_options = set(question["options"].keys())
            if answer_value not in valid_options:
                return False, f"{q_id}: Invalid option '{answer_value}'. Must be one of {valid_options}", None
    
    return True, "Valid", normalized_answers


def get_question_by_id(q_id):
    """Get a specific question by ID."""
    return QUIZ_QUESTIONS.get(q_id)


def get_questions_by_category(category):
    """Get all questions in a specific category."""
    return {q_id: q for q_id, q in QUIZ_QUESTIONS.items() if q["category"] == category}
