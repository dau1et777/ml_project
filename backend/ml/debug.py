"""
Debug Module - Provides detailed debugging and explanation output.

Helps understand:
- How vectors are constructed
- Which dimensions contributed most to similarity
- Why a particular career was recommended
- Detailed breakdown of scores
"""

import numpy as np
from validator import QUIZ_QUESTIONS
from vectorizer import UserVectorizer
from careers import get_all_careers, CAREER_DESCRIPTIONS
from weights import FeatureWeights
from similarity import SimilarityCalculator


class DebugHelper:
    """Helper class for debugging recommendations."""
    
    @staticmethod
    def print_quiz_structure():
        """Print quiz structure with categories."""
        print("\n" + "="*60)
        print("QUIZ STRUCTURE")
        print("="*60)
        
        categories = {}
        for q_id, q_info in QUIZ_QUESTIONS.items():
            cat = q_info["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(q_id)
        
        for cat, questions in sorted(categories.items()):
            print(f"\n{cat.upper()}: {', '.join(questions)}")
            for q_id in questions:
                q = QUIZ_QUESTIONS[q_id]
                print(f"  {q_id}: {q['text']}")
    
    @staticmethod
    def print_user_vector_breakdown(user_vector, answers):
        """Print detailed breakdown of user vector."""
        print("\n" + "="*60)
        print("USER VECTOR ANALYSIS")
        print("="*60)
        
        print("\nRaw Answers:")
        for i in range(1, 26):
            q_id = f"q{i}"
            answer = answers[q_id]
            print(f"  {q_id}: {answer}")
        
        readable = UserVectorizer.vector_to_readable(user_vector)
        print("\nVectorized Answers:")
        for q_id in [f"q{i}" for i in range(1, 26)]:
            print(f"  {q_id}: {readable[q_id]:.2f}" if isinstance(readable[q_id], float) else f"  {q_id}: {readable[q_id]}")
        
        print("\nVector Values (first 5, choice samples):")
        print(f"  Q1-Q5: {user_vector[0:5]}")
        print(f"  Q6-Q10: {user_vector[5:10]}")
        print(f"  Q11-Q15: {user_vector[10:15]}")
        print(f"  Q16-Q20: {user_vector[15:20]}")
        print(f"  Q21 (one-hot): {user_vector[20:24]}")
        print(f"  Q22 (one-hot): {user_vector[24:28]}")
        print(f"  Q23 (one-hot): {user_vector[28:32]}")
        print(f"  Q24 (one-hot): {user_vector[32:36]}")
        print(f"  Q25 (one-hot): {user_vector[36:40]}")
    
    @staticmethod
    def print_weights():
        """Print weight profile."""
        print("\n" + "="*60)
        print("FEATURE WEIGHTS")
        print("="*60)
        
        profile = FeatureWeights.get_weight_profile()
        for category, info in profile.items():
            print(f"\n{category.upper()}")
            print(f"  Dimensions: {info['dimensions']}")
            print(f"  Weight: {info['weight']}x")
            print(f"  Description: {info['description']}")
    
    @staticmethod
    def print_weighted_vector_breakdown(user_vector, weighted_user_vector):
        """Print comparison of original vs weighted vector."""
        print("\n" + "="*60)
        print("WEIGHTED VECTOR COMPARISON")
        print("="*60)
        
        print("\nDimensions with weights:")
        ranges = [
            ("Q1-Q5 (Cognitive)", 0, 5),
            ("Q6-Q10 (Creativity)", 5, 10),
            ("Q11-Q15 (Communication)", 10, 15),
            ("Q16-Q20 (Academic)", 15, 20),
            ("Q21-Q25 (Preferences)", 20, 40)
        ]
        
        for label, start, end in ranges:
            orig = user_vector[start:end]
            weighted = weighted_user_vector[start:end]
            print(f"\n{label}:")
            print(f"  Original:  {[f'{v:.3f}' for v in orig[:5]]}")
            print(f"  Weighted:  {[f'{v:.3f}' for v in weighted[:5]]}")
            if end - start > 5:
                print(f"  (showing first 5 of {end-start} dims)")
    
    @staticmethod
    def print_top_careers_vectors(top_careers, weighted_career_vectors, user_vector):
        """Print vectors of top 5 recommended careers."""
        print("\n" + "="*60)
        print("TOP 5 CAREER VECTORS")
        print("="*60)
        
        for rank, (career_name, similarity) in enumerate(top_careers, 1):
            career_vector = weighted_career_vectors[career_name]
            percentage = SimilarityCalculator.score_to_percentage(similarity)
            
            print(f"\n{rank}. {career_name} ({percentage}%)")
            print(f"   Similarity: {similarity:.4f}")
            print(f"   Vector sample (first 20 dims):")
            print(f"   {[f'{v:.3f}' for v in career_vector[:20]]}")
    
    @staticmethod
    def print_similarity_breakdown(user_vector, career_vector, career_name):
        """Print detailed similarity calculation breakdown."""
        print("\n" + "="*60)
        print(f"SIMILARITY BREAKDOWN: {career_name}")
        print("="*60)
        
        # Overall similarity
        similarity = SimilarityCalculator.cosine_similarity(user_vector, career_vector)
        percentage = SimilarityCalculator.score_to_percentage(similarity)
        print(f"\nOverall Similarity: {similarity:.4f} ({percentage}%)")
        
        # Category contributions
        dimension_products = user_vector * career_vector
        categories = {
            "Cognitive (Q1-Q5)": (0, 5),
            "Creativity (Q6-Q10)": (5, 10),
            "Communication (Q11-Q15)": (10, 15),
            "Academic (Q16-Q20)": (15, 20),
            "Preferences (Q21-Q25)": (20, 40)
        }
        
        print("\nCategory Contributions:")
        contributions = []
        for cat_name, (start, end) in categories.items():
            contribution = np.sum(dimension_products[start:end])
            contributions.append((cat_name, contribution))
        
        # Sort and display
        for cat_name, contribution in sorted(contributions, key=lambda x: x[1], reverse=True):
            print(f"  {cat_name}: {contribution:.4f}")
    
    @staticmethod
    def print_full_debug_report(answers, results, weighted_user_vector, weighted_career_vectors):
        """Print complete debug report."""
        print("\n" + "="*80)
        print("COMPLETE DEBUG REPORT")
        print("="*80)
        
        DebugHelper.print_quiz_structure()
        DebugHelper.print_weights()
        DebugHelper.print_user_vector_breakdown(
            UserVectorizer.vectorize(answers),
            answers
        )
        
        user_vector = UserVectorizer.vectorize(answers)
        weighted_user = FeatureWeights.apply_weights(user_vector)
        DebugHelper.print_weighted_vector_breakdown(user_vector, weighted_user)
        
        # Top careers
        top_careers = [
            (rec["career"], rec["match_percentage"] / 100.0)
            for rec in results["recommendations"]
        ]
        DebugHelper.print_top_careers_vectors(top_careers, weighted_career_vectors, weighted_user)
        
        # Detailed breakdown of top recommendation
        if results["recommendations"]:
            top_career = results["recommendations"][0]["career"]
            DebugHelper.print_similarity_breakdown(
                weighted_user,
                weighted_career_vectors[top_career],
                top_career
            )


def debug_recommendation(answers, results):
    """
    Helper function to print debug output for a recommendation.
    
    Args:
        answers (dict): Quiz answers
        results (dict): Recommendation results
    """
    user_vector = UserVectorizer.vectorize(answers)
    weighted_user = FeatureWeights.apply_weights(user_vector)
    career_vecs = get_all_careers()
    weighted_careers = {name: FeatureWeights.apply_weights_to_career(vec)
                       for name, vec in career_vecs.items()}
    
    DebugHelper.print_full_debug_report(answers, results, weighted_user, weighted_careers)
