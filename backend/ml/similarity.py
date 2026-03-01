"""
Similarity Calculation - Cosine similarity for vector-based recommendation.

Algorithm:
- Calculate cosine similarity between user vector and each career vector
- Both vectors pre-weighted with feature importance
- Sort careers by similarity score (descending)
- Return top 5 with match percentages

Formula:
cosine_similarity = (u · c) / (||u|| * ||c||)
where u = user vector, c = career vector
"""

import numpy as np


class SimilarityCalculator:
    """Calculates cosine similarity between user and career vectors."""
    
    @staticmethod
    def cosine_similarity(vector1, vector2):
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vector1 (np.ndarray): First vector
            vector2 (np.ndarray): Second vector
        
        Returns:
            float: Cosine similarity (range 0-1)
        """
        # Dot product
        dot_product = np.dot(vector1, vector2)
        
        # Magnitudes
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        
        # Clamp to [0, 1] range (account for floating point errors)
        similarity = max(0.0, min(1.0, similarity))
        
        return similarity
    
    @staticmethod
    def calculate_all_similarities(user_vector, career_vectors):
        """
        Calculate similarity between user and all career vectors.
        
        Args:
            user_vector (np.ndarray): User's weighted vector (40-dim)
            career_vectors (dict): {career_name: car_vector} pairs
        
        Returns:
            dict: {career_name: similarity_score}
        """
        similarities = {}
        
        for career_name, career_vector in career_vectors.items():
            similarity = SimilarityCalculator.cosine_similarity(user_vector, career_vector)
            similarities[career_name] = similarity
        
        return similarities
    
    @staticmethod
    def get_top_careers(similarities, top_n=5):
        """
        Get top N careers sorted by similarity score.
        
        Args:
            similarities (dict): {career_name: score}
            top_n (int): Number of top results to return
        
        Returns:
            list: List of tuples (career_name, similarity_score) sorted descending
        """
        sorted_careers = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return sorted_careers[:top_n]
    
    @staticmethod
    def score_to_percentage(similarity_score):
        """
        Convert cosine similarity score (0-1) to percentage (0-100).
        
        Args:
            similarity_score (float): Cosine similarity (0-1)
        
        Returns:
            int: Percentage (0-100)
        """
        percentage = int(round(similarity_score * 100))
        return max(0, min(100, percentage))  # Clamp to 0-100
    
    @staticmethod
    def format_results(top_careers):
        """
        Format top careers with scores and percentages.
        
        Args:
            top_careers (list): List of (career_name, score) tuples
        
        Returns:
            list: List of dicts with career, score, percentage
        """
        results = []
        for idx, (career_name, score) in enumerate(top_careers, 1):
            percentage = SimilarityCalculator.score_to_percentage(score)
            results.append({
                "rank": idx,
                "career": career_name,
                "similarity_score": round(score, 4),
                "match_percentage": percentage
            })
        return results
    
    @staticmethod
    def explain_similarity(user_vector, career_vector, career_name):
        """
        Explain similarity calculation with breakdown by dimension category.
        
        Args:
            user_vector (np.ndarray): User's weighted vector
            career_vector (np.ndarray): Career's weighted vector
            career_name (str): Name of career
        
        Returns:
            dict: Detailed similarity explanation
        """
        similarity = SimilarityCalculator.cosine_similarity(user_vector, career_vector)
        percentage = SimilarityCalculator.score_to_percentage(similarity)
        
        # Calculate dimension contributions
        dimension_products = user_vector * career_vector
        
        # Group by category
        categories = {
            "cognitive": (0, 5, dimension_products[0:5]),
            "creativity": (5, 10, dimension_products[5:10]),
            "communication": (10, 15, dimension_products[10:15]),
            "academic": (15, 20, dimension_products[15:20]),
            "preferences": (20, 40, dimension_products[20:40])
        }
        
        category_contributions = {}
        for cat_name, (start, end, values) in categories.items():
            contribution = np.sum(values)
            category_contributions[cat_name] = round(contribution, 4)
        
        return {
            "career": career_name,
            "overall_similarity": round(similarity, 4),
            "match_percentage": percentage,
            "category_contributions": category_contributions,
            "strongest_match_categories": sorted(
                category_contributions.items(),
                key=lambda x: x[1],
                reverse=True
            )[:2]
        }
