"""
Vectorizer - Converts quiz answers to 50-dimensional user vector.

Vector Structure (50 dimensions):
ORIGINAL FEATURES (indices 0-39) - DO NOT MODIFY:
- [0-19]:   Q1-Q20 normalized (value/10, range 0-1)
- [20-23]:  Q21 one-hot (A/B/C/D)
- [24-27]:  Q22 one-hot (A/B/C/D)
- [28-31]:  Q23 one-hot (A/B/C/D)
- [32-35]:  Q24 one-hot (A/B/C/D)
- [36-39]:  Q25 one-hot (A/B/C/D)

NEW FEATURES (indices 40-49) - EXTENSION:
- [40-47]:  Q26-Q33 normalized (value/10, range 0-1) - Interest Profile
- [48-49]:  Q34-Q35 normalized (value/10, range 0-1) - Work Style
"""

import numpy as np
from validator import QUIZ_QUESTIONS


class UserVectorizer:
    """Converts quiz answers to normalized 50-dimensional vector."""
    
    # IMPORTANT: Keep these EXACT for backward compatibility
    VECTOR_SIZE = 50  # Extended from 40
    SCALE_QUESTIONS = [f"q{i}" for i in range(1, 21)]  # Q1-Q20 (original)
    CHOICE_QUESTIONS = [f"q{i}" for i in range(21, 26)]  # Q21-Q25 (original)
    
    # NEW: Score questions for extension
    NEW_SCALE_QUESTIONS = [f"q{i}" for i in range(26, 36)]  # Q26-Q35 (new)
    NEW_SCALE_START_IDX = 40  # Where new features begin in vector
    
    # Mapping choice indices for one-hot encoding
    CHOICE_OPTIONS = {
        "q21": {"A": 0, "B": 1, "C": 2, "D": 3},
        "q22": {"A": 0, "B": 1, "C": 2, "D": 3},
        "q23": {"A": 0, "B": 1, "C": 2, "D": 3},
        "q24": {"A": 0, "B": 1, "C": 2, "D": 3},
        "q25": {"A": 0, "B": 1, "C": 2, "D": 3},
    }
    
    @staticmethod
    def vectorize(answers):
        """
        Convert quiz answers to 50-dimensional vector.
        
        CRITICAL: Backward compatibility
        - Old features (0-39) use original logic
        - New features (40-49) appended without altering old features
        - Missing Q26-Q35 default to 5 (neutral) by validator
        
        Args:
            answers (dict): Quiz answers {q1-q35} (q26-q35 optional)
        
        Returns:
            np.ndarray: 50-dimensional vector
        """
        vector = np.zeros(UserVectorizer.VECTOR_SIZE)
        
        # ==================== ORIGINAL FEATURES (0-39) ====================
        # Q1-Q20: Normalize scale answers (0-1 range)
        for i, q_id in enumerate(UserVectorizer.SCALE_QUESTIONS):
            normalized_value = answers[q_id] / 10.0
            vector[i] = normalized_value
        
        # Q21-Q25: One-hot encode choice answers
        choice_start_idx = 20
        for choice_idx, q_id in enumerate(UserVectorizer.CHOICE_QUESTIONS):
            choice_value = answers[q_id]  # 'A', 'B', 'C', or 'D'
            one_hot_idx = UserVectorizer.CHOICE_OPTIONS[q_id][choice_value]
            vector[choice_start_idx + choice_idx * 4 + one_hot_idx] = 1.0
        
        # ==================== NEW FEATURES (40-49) ====================
        # Q26-Q35: Normalize scale answers (0-1 range)
        for i, q_id in enumerate(UserVectorizer.NEW_SCALE_QUESTIONS):
            normalized_value = answers[q_id] / 10.0
            vector[UserVectorizer.NEW_SCALE_START_IDX + i] = normalized_value
        
        return vector
    
    @staticmethod
    def get_vector_dimensions():
        """Return information about vector dimensions."""
        return {
            "total_size": 50,
            "original_features": {
                "count": 40,
                "stability": "FIXED - DO NOT MODIFY",
                "scale_questions": {
                    "range": "0-19",
                    "count": 20,
                    "questions": "Q1-Q20",
                    "normalization": "value / 10 (0-1 range)"
                },
                "choice_questions": {
                    "range": "20-39",
                    "count": 5,
                    "questions": "Q21-Q25",
                    "encoding": "one-hot (4 values per question)"
                }
            },
            "new_features": {
                "count": 10,
                "status": "EXTENSION - appended safely",
                "interest_profile_questions": {
                    "range": "40-47",
                    "count": 8,
                    "questions": "Q26-Q33",
                    "normalization": "value / 10 (0-1 range)",
                    "weight": 0.6
                },
                "work_style_questions": {
                    "range": "48-49",
                    "count": 2,
                    "questions": "Q34-Q35",
                    "normalization": "value / 10 (0-1 range)",
                    "weight": 0.4
                }
            }
        }
    
    @staticmethod
    def vector_to_readable(vector):
        """
        Convert vector back to readable format for debugging.
        
        Returns:
            dict: Readable representation of vector
        """
        readable = {}
        
        # Scale answers
        for i, q_id in enumerate(UserVectorizer.SCALE_QUESTIONS):
            readable[q_id] = vector[i] * 10  # Back to 1-10 scale
        
        # Choice answers
        choice_start_idx = 20
        for choice_idx, q_id in enumerate(UserVectorizer.CHOICE_QUESTIONS):
            one_hot_section = vector[choice_start_idx + choice_idx * 4:choice_start_idx + (choice_idx + 1) * 4]
            selected_idx = np.argmax(one_hot_section)
            option_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
            readable[q_id] = option_map[selected_idx]
        
        return readable
