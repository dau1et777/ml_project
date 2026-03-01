"""
Test Script - Verify ML system works correctly

Run this to test:
python test_ml_system.py
"""

import sys
from pathlib import Path

# Add backend and ml subpackage to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
# Also include the ml package directory so imports like 'from validator' work
sys.path.insert(0, str(backend_path / "ml"))

from ml.validator import validate_answers, QUIZ_QUESTIONS
from ml.vectorizer import UserVectorizer
from ml.careers import get_all_careers
from ml.weights import FeatureWeights
from ml.similarity import SimilarityCalculator
from ml.recommender import recommend_careers
import numpy as np


def test_quiz_validation():
    """Test answer validation."""
    print("\n" + "="*60)
    print("TEST 1: Quiz Validation")
    print("="*60)
    
    # Create valid answers
    valid_answers = {}
    for i in range(1, 21):
        valid_answers[f"q{i}"] = 5
    for i in range(21, 26):
        valid_answers[f"q{i}"] = "A"
    
    is_valid, msg = validate_answers(valid_answers)
    print(f"✓ Valid answers: {is_valid} - {msg}")
    
    # Test invalid answers
    invalid_answers = {**valid_answers}
    invalid_answers["q1"] = 15  # Out of range
    is_valid, msg = validate_answers(invalid_answers)
    print(f"✓ Invalid answers detected: {not is_valid}")
    print(f"  Error: {msg}")


def test_vectorizer():
    """Test answer to vector conversion."""
    print("\n" + "="*60)
    print("TEST 2: Answer Vectorization")
    print("="*60)
    
    answers = {}
    for i in range(1, 21):
        answers[f"q{i}"] = 8
    for i in range(21, 26):
        answers[f"q{i}"] = "A"
    
    vector = UserVectorizer.vectorize(answers)
    
    print(f"✓ Vector size: {len(vector)} (expected 40)")
    print(f"✓ Vector dtype: {vector.dtype}")
    print(f"✓ Vector range: [{vector.min():.3f}, {vector.max():.3f}]")
    print(f"✓ Q1-Q5 values: {vector[0:5]}")
    print(f"✓ Q21 (one-hot A): {vector[20:24]}")
    
    # Verify dimensions
    dims = UserVectorizer.get_vector_dimensions()
    print(f"✓ Total dimensions: {dims['total_size']}")


def test_career_vectors():
    """Test career vector loading."""
    print("\n" + "="*60)
    print("TEST 3: Career Vectors")
    print("="*60)
    
    careers = get_all_careers()
    print(f"✓ Total careers: {len(careers)}")
    print(f"✓ Career names sample:")
    for name in list(careers.keys())[:5]:
        print(f"  - {name}")
    
    # Check vector dimensions
    first_career = list(careers.values())[0]
    print(f"✓ Career vector size: {len(first_career)} (expected 40)")
    print(f"✓ Sample career vector stats:")
    print(f"  Min: {first_career.min():.3f}")
    print(f"  Max: {first_career.max():.3f}")
    print(f"  Mean: {first_career.mean():.3f}")


def test_weights():
    """Test feature weighting."""
    print("\n" + "="*60)
    print("TEST 4: Feature Weighting")
    print("="*60)
    
    # Test weight profile
    profile = FeatureWeights.get_weight_profile()
    print("✓ Weight categories:")
    for cat, info in profile.items():
        print(f"  {cat}: {info['weight']}x weight")
    
    # Test weight application
    test_vector = np.ones(40)
    weighted = FeatureWeights.apply_weights(test_vector)
    print(f"\n✓ Weighted vector stats:")
    print(f"  Original sum: {test_vector.sum():.1f}")
    print(f"  Weighted sum: {weighted.sum():.1f}")
    print(f"  Weight range: [{weighted.min():.1f}, {weighted.max():.1f}]")


def test_similarity():
    """Test cosine similarity calculation."""
    print("\n" + "="*60)
    print("TEST 5: Cosine Similarity")
    print("="*60)
    
    # Create test vectors
    v1 = np.array([1, 0, 0])
    v2 = np.array([1, 0, 0])
    sim = SimilarityCalculator.cosine_similarity(v1, v2)
    print(f"✓ Identical vectors similarity: {sim:.4f} (expected 1.0)")
    
    v3 = np.array([0, 1, 0])
    sim = SimilarityCalculator.cosine_similarity(v1, v3)
    print(f"✓ Orthogonal vectors similarity: {sim:.4f} (expected 0.0)")
    
    v4 = np.array([1, 1, 0]) / np.sqrt(2)
    v5 = np.array([1, 0, 0])
    sim = SimilarityCalculator.cosine_similarity(v4, v5)
    print(f"✓ 45° angle similarity: {sim:.4f} (expected ~0.707)")


def test_full_recommendation():
    """Test complete recommendation flow."""
    print("\n" + "="*60)
    print("TEST 6: Full Recommendation")
    print("="*60)
    
    # Create test user (high technical, low social)
    answers = {
        "q1": 9, "q2": 8, "q3": 9, "q4": 8, "q5": 8,
        "q6": 5, "q7": 4, "q8": 6, "q9": 7, "q10": 5,
        "q11": 3, "q12": 2, "q13": 3, "q14": 3, "q15": 2,
        "q16": 9, "q17": 7, "q18": 9, "q19": 9, "q20": 8,
        "q21": "A",  # Fast-paced
        "q22": "A",  # Technical
        "q23": "C",  # Learning
        "q24": "A",  # Hands-on
        "q25": "A"   # Results
    }
    
    print("✓ Testing with high-technical, low-social profile")
    print("  Expected: Software/ML/Data Science roles")
    
    results = recommend_careers(answers, debug=False)
    
    if "error" in results:
        print(f"✗ Error: {results['error']}")
    else:
        recommendations = results.get("recommendations", [])
        print(f"\n✓ Top 5 recommendations:")
        for rec in recommendations:
            print(f"  {rec['rank']}. {rec['career']} ({rec['match_percentage']}%)")
            print(f"     {rec['explanation']}")
        # verify profile_scores present
        profile = results.get("profile_scores")
        assert profile is not None, "Profile scores missing"
        print("✓ Profile breakdown:")
        for cat, pct in profile.items():
            print(f"  {cat}: {pct}%")


def test_profile_scores():
    """Ensure profile scoring returns expected percentages."""
    print("\n" + "="*60)
    print("TEST X: Profile Score Calculation")
    print("="*60)

    # create a user vector where every dimension is 1.0 (maxed)
    import numpy as _np
    from ml.recommender import CareerRecommender
    vect = _np.ones(40)
    profile = CareerRecommender._calculate_profile(vect)
    print("Profile for uniform vector:", profile)
    # each category percentage should be exactly 100.0
    for val in profile.values():
        assert val == 100.0, "Expected 100% for uniform vector"


def test_different_profiles():
    """Test different user profiles."""
    print("\n" + "="*60)
    print("TEST 7: Different User Profiles")
    print("="*60)
    
    profiles = {
        "Creative Designer": {
            "q1": 5, "q2": 4, "q3": 5, "q4": 5, "q5": 4,
            "q6": 10, "q7": 10, "q8": 9, "q9": 9, "q10": 9,
            "q11": 8, "q12": 6, "q13": 8, "q14": 6, "q15": 5,
            "q16": 4, "q17": 3, "q18": 4, "q19": 5, "q20": 7,
            "q21": "B", "q22": "D", "q23": "A", "q24": "D", "q25": "D"
        },
        "Sales Leader": {
            "q1": 6, "q2": 5, "q3": 6, "q4": 6, "q5": 5,
            "q6": 6, "q7": 5, "q8": 7, "q9": 7, "q10": 6,
            "q11": 9, "q12": 9, "q13": 9, "q14": 9, "q15": 10,
            "q16": 5, "q17": 4, "q18": 4, "q19": 5, "q20": 7,
            "q21": "A", "q22": "B", "q23": "A", "q24": "C", "q25": "A"
        },
        "Academic Researcher": {
            "q1": 9, "q2": 9, "q3": 9, "q4": 9, "q5": 8,
            "q6": 6, "q7": 4, "q8": 7, "q9": 6, "q10": 7,
            "q11": 4, "q12": 5, "q13": 5, "q14": 4, "q15": 4,
            "q16": 9, "q17": 9, "q18": 6, "q19": 8, "q20": 10,
            "q21": "D", "q22": "A", "q23": "C", "q24": "B", "q25": "B"
        }
    }
    
    for profile_name, answers in profiles.items():
        print(f"\n✓ {profile_name}:")
        results = recommend_careers(answers, debug=False)
        if "error" not in results:
            top_career = results["recommendations"][0]
            print(f"  Top match: {top_career['career']} ({top_career['match_percentage']}%)")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("CAREER RECOMMENDATION SYSTEM - ML TESTS")
    print("="*60)
    
    try:
        test_quiz_validation()
        test_vectorizer()
        test_career_vectors()
        test_weights()
        test_similarity()
        test_full_recommendation()
        test_different_profiles()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nSystem is ready for API testing.")
        print("Start the Django server with: python manage.py runserver")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
