"""
ML Service Layer - Wraps the existing trained ML model
Handles preprocessing, inference, and postprocessing
"""
import numpy as np
from typing import Tuple, Dict, List, Any
import json
from pathlib import Path
import sys

# Add ml module to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'ml'))

from recommender import recommend_careers


class Preprocessor:
    """Converts quiz answers to feature vector."""
    
    @staticmethod
    def answers_to_vector(answers: Dict[int, Any]) -> Tuple[np.ndarray, List[str]]:
        """
        Convert quiz answers dict to 50-dimensional feature vector.
        
        Args:
            answers: Dict mapping question_id (1-35) to answer values
                    Q1-Q20: numeric 1-10 (scales)
                    Q21-Q25: A/B/C/D (choice)
                    Q26-Q35: numeric 1-10 (scales)
        
        Returns:
            Tuple of (feature_vector: np.array(50,), errors: List[str])
        """
        errors = []
        normalized = {}
        
        # Validate Q1-Q20: Scale questions
        for q_id in range(1, 21):
            if q_id in answers:
                try:
                    val = int(answers[q_id])
                    if 1 <= val <= 10:
                        normalized[q_id] = val
                    else:
                        errors.append(f"Q{q_id}: Must be 1-10, got {val}")
                        normalized[q_id] = 5  # default
                except (ValueError, TypeError):
                    errors.append(f"Q{q_id}: Invalid numeric value")
                    normalized[q_id] = 5  # default
            else:
                normalized[q_id] = 5  # default middle value
        
        # Validate Q21-Q25: Choice questions
        for q_id in range(21, 26):
            if q_id in answers:
                val = str(answers[q_id]).upper()
                if val in ['A', 'B', 'C', 'D']:
                    normalized[q_id] = val
                else:
                    errors.append(f"Q{q_id}: Must be A/B/C/D, got {val}")
                    normalized[q_id] = 'A'  # default
            else:
                normalized[q_id] = 'A'  # default
        
        # Validate Q26-Q35: Scale questions
        for q_id in range(26, 36):
            if q_id in answers:
                try:
                    val = int(answers[q_id])
                    if 1 <= val <= 10:
                        normalized[q_id] = val
                    else:
                        errors.append(f"Q{q_id}: Must be 1-10, got {val}")
                        normalized[q_id] = 5
                except (ValueError, TypeError):
                    errors.append(f"Q{q_id}: Invalid numeric value")
                    normalized[q_id] = 5
            else:
                normalized[q_id] = 5
        
        # Convert to 50-dimensional vector (existing vectorizer logic)
        vector = np.zeros(50)
        
        # Indices 0-19: Q1-Q20 directly (cognitive/personality dimensions)
        for i in range(20):
            vector[i] = normalized[i + 1] / 10.0  # normalize to 0-1
        
        # Indices 20-23: Q21-Q24 as one-hot (motivation style)
        for i, q_id in enumerate(range(21, 25)):
            choice = normalized[q_id]
            choice_idx = ord(choice) - ord('A')  # A=0, B=1, C=2, D=3
            if i * 4 + choice_idx < 4:  # Q21-Q24: indices 20-23
                vector[20 + i * 4 + choice_idx] = 1.0
        
        # Index 24: Q25 (single choice) -> encoded as A=0.25, B=0.5, C=0.75, D=1.0
        choice = normalized[25]
        choice_val = (ord(choice) - ord('A') + 1) / 4.0
        vector[24] = choice_val
        
        # Indices 25-31: Q26-Q33 one-hot or interest profile
        # Q26-Q33: 8 interest dimensions
        for i in range(8):
            q_id = 26 + i
            vector[25 + i] = normalized[q_id] / 10.0
        
        # Indices 33-39: Q34-Q35 work style (not currently used - future expansion)
        vector[33] = normalized[34] / 10.0
        vector[34] = normalized[35] / 10.0
        # Remaining indices (35-49) reserved for future features
        
        return vector, errors
    
    @staticmethod
    def validate_answers(answers: Dict[int, Any]) -> Tuple[bool, List[str]]:
        """Quick validation without converting to vector."""
        _, errors = Preprocessor.answers_to_vector(answers)
        return len(errors) == 0, errors


class Postprocessor:
    """Formats ML model output for API responses."""
    
    @staticmethod
    def format_predictions(recommendations: List[Tuple[str, float]]) -> Dict[str, Any]:
        """
        Convert recommender output to API-friendly format.
        Enriches predictions with career details from database.
        
        Args:
            recommendations: List of (career_name, similarity_score) tuples
        
        Returns:
            Formatted dict with top 5 careers and explanations
        """
        # Import here to avoid circular dependency
        from career_app.models import Career
        
        formatted = {
            "top_careers": [],
            "scores": {},
            "explanation": {
                "primary_factors": [],
                "secondary_factors": [],
                "skill_fit": []
            }
        }
        
        for idx, (career_name, score) in enumerate(recommendations[:5], 1):
            # Fetch career details from database
            career_obj = None
            try:
                career_obj = Career.objects.filter(name__iexact=career_name).first()
            except Exception:
                pass
            
            match_score = round(float(score), 4)
            match_percentage = int(match_score * 100)
            
            career_data = {
                "rank": idx,
                "name": career_name,
                "career": career_name,  # alias for compatibility
                "match_score": match_score,
                "match_percentage": match_percentage,
                "description": career_obj.description if career_obj else f"A career in {career_name}.",
                "explanation": Postprocessor._generate_explanation(career_name, match_score)
            }
            
            # Add salary and demand data if available
            if career_obj:
                if career_obj.salary_min and career_obj.salary_max:
                    career_data["salary_range"] = f"${career_obj.salary_min:,.0f} - ${career_obj.salary_max:,.0f}"
                else:
                    career_data["salary_range"] = "Varies by experience"
                career_data["demand_level"] = career_obj.get_demand_level_display() if hasattr(career_obj, 'get_demand_level_display') else career_obj.demand_level
            
            formatted["top_careers"].append(career_data)
            formatted["scores"][career_name] = match_score
        
        return formatted
    
    @staticmethod
    def _generate_explanation(career_name: str, match_score: float) -> str:
        """Generate a simple explanation for why a career matches."""
        percentage = int(match_score * 100)
        
        if percentage >= 90:
            return f"Your skills, interests, and work style align exceptionally well with {career_name}. This is a strong match based on your quiz responses."
        elif percentage >= 80:
            return f"Your profile shows strong compatibility with {career_name}. Many of your strengths and preferences align with this career path."
        elif percentage >= 70:
            return f"Your background and interests show good alignment with {career_name}. This career could be a solid fit for you."
        elif percentage >= 60:
            return f"You have several qualities that match {career_name}. With some skill development, this could be a viable path."
        else:
            return f"{career_name} shows moderate alignment with your profile. Consider exploring related roles that might be a better fit."
    
    @staticmethod
    def add_explainability(predictions: Dict[str, Any], user_vector: np.ndarray) -> Dict[str, Any]:
        """
        Add XAI-lite explanations to predictions.
        
        Args:
            predictions: Formatted predictions dict
            user_vector: User's 50-dimensional feature vector
        
        Returns:
            Predictions dict with added explanations
        """
        # Identify strong dimensions (above 0.7)
        strong_dims = []
        for idx, val in enumerate(user_vector):
            if val > 0.7:
                if idx < 20:
                    strong_dims.append(f"High cognitive dimension {idx+1}")
                elif idx < 25:
                    strong_dims.append(f"Strong motivation style")
                elif idx < 33:
                    strong_dims.append(f"Interest area {idx-24}")
        
        predictions["explanation"]["primary_factors"] = strong_dims[:3]
        predictions["explanation"]["secondary_factors"] = strong_dims[3:6]
        
        return predictions


class MLService:
    """
    Orchestrates ML inference pipeline.
    Singleton pattern ensures single model instance.
    """
    
    _instance = None
    _model_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize ML service (loads model once)."""
        if not MLService._model_loaded:
            self._load_model()
            MLService._model_loaded = True
    
    def _load_model(self):
        """Load the pre-trained ML model."""
        # The get_career_recommendations() function loads careers internally
        # This is a wrapper around the existing vectorizer + recommender
        self.model_ready = True
    
    def predict(self, answers: Dict[int, Any]) -> Dict[str, Any]:
        """
        Complete ML inference pipeline.
        
        Args:
            answers: Dict of quiz answers {question_id: answer_value}
        
        Returns:
            Dict with predictions, scores, and explanations
        
        Raises:
            ValueError: If validation fails
        """
        # 1. Validate
        is_valid, errors = Preprocessor.validate_answers(answers)
        if not is_valid:
            raise ValueError(f"Invalid answers: {'; '.join(errors)}")
        
        # 2. Preprocess
        user_vector, _ = Preprocessor.answers_to_vector(answers)
        
        # 3. Inference using existing recommender
        # Legacy recommender validator expects q-prefixed keys (q1..q35)
        recommender_answers = {f"q{int(k)}": v for k, v in answers.items()}
        result = recommend_careers(recommender_answers)
        
        # Check if error occurred
        if 'error' in result:
            raise ValueError(f"ML model error: {result['error']}")
        
        # Extract recommendations
        recommendations = [(r['career'], r['match_percentage']/100.0) 
                          for r in result.get('recommendations', [])]
        
        # 4. Postprocess
        predictions = Postprocessor.format_predictions(recommendations)
        
        # 5. Add explanations
        predictions = Postprocessor.add_explainability(predictions, user_vector)

        # 6. Include detailed profile data for frontend charts
        if 'profile_scores' in result:
            predictions['profile'] = result['profile_scores']
        
        return predictions
    
    def batch_predict(self, answers_list: List[Dict[int, Any]]) -> List[Dict[str, Any]]:
        """
        Predict for multiple answer sets.
        
        Args:
            answers_list: List of answer dicts
        
        Returns:
            List of prediction dicts
        """
        results = []
        for answers in answers_list:
            try:
                result = self.predict(answers)
                results.append({"success": True, "data": result})
            except ValueError as e:
                results.append({"success": False, "error": str(e)})
        return results


def get_ml_service() -> MLService:
    """Singleton accessor for ML service."""
    return MLService()
