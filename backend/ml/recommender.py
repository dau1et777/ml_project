"""
Recommender - Main orchestrator for career recommendation.

Process:
1. Validate quiz answers
2. Convert to user vector
3. Apply feature weights
4. Calculate similarity with all career vectors  
5. Get top 5 careers
6. Generate explanations for each match
7. Return results with match % and WHY explanation
"""

import numpy as np
from validator import validate_answers, QUIZ_QUESTIONS
from vectorizer import UserVectorizer
from careers import get_all_careers, get_career_description
from weights import FeatureWeights
from similarity import SimilarityCalculator


class CareerRecommender:
    """Main recommendation engine."""
    
    def __init__(self, debug=False):
        """
        Initialize recommender.
        
        Args:
            debug (bool): Enable debug mode for detailed output
        """
        self.debug = debug
        self.career_vectors = get_all_careers()
    
    def recommend(self, answers):
        """
        Generate career recommendations from quiz answers.
        
        Backward Compatibility:
        - Accepts Q1-Q25 (original system) OR Q1-Q35 (extended system)
        - Missing Q26-Q35 default to neutral value (5)
        
        Args:
            answers (dict): Quiz answers {q1: value, ..., q25: 'A'/'B'/'C'/'D'}
        
        Returns:
            dict: Recommendation results or error
        """
        # Step 0: Validate and normalize answers (handles backward compat)
        is_valid, error_msg, normalized_answers = validate_answers(answers)
        if not is_valid:
            return {"error": error_msg}
        
        # Step 1: Convert to user vector with extended features
        user_vector = UserVectorizer.vectorize(normalized_answers)
        
        # compute profile breakdown for charts (before weighting)
        profile_scores = CareerRecommender._calculate_profile(user_vector)
        
        # Step 2: Apply feature weights (differential weighting for new features)
        weighted_user_vector = FeatureWeights.apply_weights(user_vector)
        
        # Step 3: Weight career vectors and calculate similarities
        weighted_career_vectors = {}
        for career_name, career_vector in self.career_vectors.items():
            weighted_career_vectors[career_name] = FeatureWeights.apply_weights_to_career(career_vector)
        
        similarities = SimilarityCalculator.calculate_all_similarities(
            weighted_user_vector,
            weighted_career_vectors
        )
        
        # Step 4: Get top 5 careers
        top_careers = SimilarityCalculator.get_top_careers(similarities, top_n=5)
        
        # Step 6: Generate detailed results with explanations
        results = {
            "recommendations": [],
            "debug": {}
        }
        
        for rank, (career_name, similarity_score) in enumerate(top_careers, 1):
            match_percentage = SimilarityCalculator.score_to_percentage(similarity_score)
            explanation = self._generate_explanation(
                career_name,
                weighted_user_vector,
                weighted_career_vectors[career_name],
                answers
            )
            
            results["recommendations"].append({
                "rank": rank,
                "career": career_name,
                "match_percentage": match_percentage,
                "explanation": explanation,
                "description": get_career_description(career_name)
            })
        
        # attach profile scores to results
        results["profile_scores"] = profile_scores
        
        # Add comprehensive debug info if debug mode enabled
        if self.debug:
            results["debug"] = {
                # System version info
                "system_version": "2.0 (Extended with Q26-Q35)",
                "backward_compatible": len(answers) <= 25,
                
                # Input statistics
                "input_questions_count": len(answers),
                "normalized_answers_count": len(normalized_answers),
                "answers_provided": sorted(answers.keys()),
                
                # Vector statistics
                "vector_size": len(user_vector),
                "old_feature_count": 40,
                "new_feature_count": 10,
                "new_features_info": {
                    "interest_profile": "Q26-Q33 (8 dimensions, weight=0.6)",
                    "work_style": "Q34-Q35 (2 dimensions, weight=0.4)"
                },
                
                # Feature analysis
                "user_vector_stats": {
                    "old_block_mean": float(np.mean(user_vector[:40])),
                    "new_block_mean": float(np.mean(user_vector[40:])) if len(user_vector) > 40 else None,
                    "weighted_old_mean": float(np.mean(weighted_user_vector[:40])),
                    "weighted_new_mean": float(np.mean(weighted_user_vector[40:])) if len(weighted_user_vector) > 40 else None
                },
                
                # Detailed vectors
                "user_vector": user_vector.tolist(),
                "weighted_user_vector": weighted_user_vector.tolist(),
                
                # Top 5 comparison
                "top_5_careers": [
                    {
                        "name": name,
                        "similarity": round(score, 4),
                        "vector": weighted_career_vectors[name].tolist()
                    }
                    for name, score in top_careers
                ]
            }
        
        
        return results

    @staticmethod
    def _calculate_profile(user_vector):
        """Compute detailed categorical profile scores from user vector.

        Returns detailed profile with abilities, work style, and interests.
        """
        # Overall category percentages (for compatibility)
        categories = {
            "Cognitive & Problem Solving": (0, 5),
            "Creativity & Innovation": (5, 10),
            "Communication & Leadership": (10, 15),
            "Academic & Technical Orientation": (15, 20),
            "Work Style & Motivation": (20, 40),
        }
        profile = {}
        for name, (start, end) in categories.items():
            total = float(np.sum(user_vector[start:end]))
            max_val = (end - start) * 1.0
            percent = round((total / max_val) * 100, 1)
            profile[name] = percent
        
        # Detailed visualization data
        # Abilities & Capabilities (radar chart - 6 dimensions)
        profile["abilities"] = {
            "Logical Thinking": round((np.sum(user_vector[0:2]) / 2.0) * 100, 1),
            "Problem Solving": round((np.sum(user_vector[2:4]) / 2.0) * 100, 1),
            "Teamwork": round((np.sum(user_vector[10:12]) / 2.0) * 100, 1),
            "Leadership": round((np.sum(user_vector[12:14]) / 2.0) * 100, 1),
            "Communication": round((np.sum(user_vector[14:16]) / 2.0) * 100, 1),
            "Creativity": round((np.sum(user_vector[5:8]) / 3.0) * 100, 1),
        }
        
        # Work Style Preferences (bar chart - derive from preference one-hot blocks)
        # We assume the one-hot blocks for Q23 and Q24 were placed sequentially
        # in the vector. To be robust, compute aggregated scores from ranges.
        # Q23 choices occupy indices 32-34 (three options), Q24 occupy 35-37 (three options)
        def _range_sum(start, end):
            if len(user_vector) > end:
                return float(np.sum(user_vector[start:end]))
            return 0.0

        q23_sum = _range_sum(32, 35)
        q24_sum = _range_sum(35, 38)

        # Normalize to 0-100 using number of options
        q23_norm = round((q23_sum / 3.0) * 100, 1) if q23_sum > 0 else 0.0
        q24_norm = round((q24_sum / 3.0) * 100, 1) if q24_sum > 0 else 0.0

        profile["work_style"] = {
            "Independent": q23_norm if q23_norm >= q24_norm else round(100 - q24_norm, 1),
            "Collaborative": q24_norm if q24_norm >= q23_norm else round(100 - q23_norm, 1),
        }
        
        # Interest Profile (bar chart - 8 dimensions from Q26-Q33)
        # Q26-Q33: Technology, Business, Creative, Social, Analytical, Product, Education, Operations
        # [indices 40-47 in extended vector, normalized 0-1 range, multiply by 100 for percentage]
        profile["interests"] = {
            "Technology": round(user_vector[40] * 100 if len(user_vector) > 40 else 0, 1),
            "Business": round(user_vector[41] * 100 if len(user_vector) > 41 else 0, 1),
            "Creative": round(user_vector[42] * 100 if len(user_vector) > 42 else 0, 1),
            "Social": round(user_vector[43] * 100 if len(user_vector) > 43 else 0, 1),
            "Analytical": round(user_vector[44] * 100 if len(user_vector) > 44 else 0, 1),
            "Product": round(user_vector[45] * 100 if len(user_vector) > 45 else 0, 1),
            "Education": round(user_vector[46] * 100 if len(user_vector) > 46 else 0, 1),
            "Operations": round(user_vector[47] * 100 if len(user_vector) > 47 else 0, 1),
        }
        
        return profile
    
    def _generate_explanation(self, career_name, user_vector, career_vector, answers):
        """
        Generate human-readable explanation for WHY a career matches.
        
        Args:
            career_name (str): Name of career
            user_vector (np.ndarray): Weighted user vector
            career_vector (np.ndarray): Weighted career vector
            answers (dict): Original quiz answers
        
        Returns:
            str: Explanation text
        """
        # Calculate dimension contributions
        dimension_products = user_vector * career_vector
        
        # Group contributions by category
        categories = {
            "cognitive": {
                "name": "Problem Solving & Logic",
                "range": (0, 5),
                "impact_questions": ["q1", "q2", "q3", "q4", "q5"]
            },
            "creativity": {
                "name": "Creativity & Innovation",
                "range": (5, 10),
                "impact_questions": ["q6", "q7", "q8", "q9", "q10"]
            },
            "communication": {
                "name": "Communication & Leadership",
                "range": (10, 15),
                "impact_questions": ["q11", "q12", "q13", "q14", "q15"]
            },
            "academic": {
                "name": "Technical & Academic",
                "range": (15, 20),
                "impact_questions": ["q16", "q17", "q18", "q19", "q20"]
            },
            "preferences": {
                "name": "Your Preferences",
                "range": (20, 40),
                "impact_questions": ["q21", "q22", "q23", "q24", "q25"]
            }
        }
        
        # Calculate contributions
        top_categories = []
        for cat_key, cat_info in categories.items():
            start, end = cat_info["range"]
            contribution = np.sum(dimension_products[start:end])
            top_categories.append((cat_info["name"], contribution))
        
        # Sort by contribution
        top_categories.sort(key=lambda x: x[1], reverse=True)
        
        # Build explanation
        explanation_parts = []
        
        for idx, (cat_name, contribution) in enumerate(top_categories[:3]):
            if contribution > 0:
                if idx == 0:
                    explanation_parts.append(f"Strong match in {cat_name.lower()}")
                else:
                    explanation_parts.append(f"also strong in {cat_name.lower()}")
        
        return ", ".join(explanation_parts) + "."
    
    def explain_result(self, career_name, weighted_user_vector, weighted_career_vector):
        """
        Generate detailed explanation of recommendation.
        
        Args:
            career_name (str): Name of recommended career
            weighted_user_vector (np.ndarray): Weighted user vector
            weighted_career_vector (np.ndarray): Weighted career vector
        
        Returns:
            dict: Detailed explanation breakdown
        """
        return SimilarityCalculator.explain_similarity(
            weighted_user_vector,
            weighted_career_vector,
            career_name
        )


def recommend_careers(answers, debug=False):
    """
    Convenience function to get career recommendations.
    
    Args:
        answers (dict): Quiz answers
        debug (bool): Enable debug mode
    
    Returns:
        dict: Recommendation results
    """
    recommender = CareerRecommender(debug=debug)
    return recommender.recommend(answers)
