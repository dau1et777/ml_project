"""
Test the complete fixed 35-question recommendation system
"""
import sys
import json
sys.path.insert(0, 'ml')
from validator import validate_answers
from recommender import recommend_careers

# Create test answers for all 35 questions
answers = {}

# Q1-Q20: Scale (1-10) - numeric
for i in range(1, 21):
    answers[f'q{i}'] = 5 + (i % 6)  # Values between 5-10

# Q21-Q25: Choice (A, B, C, D) - strings
for i in range(21, 26):
    answers[f'q{i}'] = chr(65 + ((i - 21) % 4))  # Cycle through A, B, C, D

# Q26-Q35: Scale (1-10) - numeric
for i in range(26, 36):
    answers[f'q{i}'] = 7 + (i % 4)  # Values between 7-10

print("=" * 50)
print("Testing Full 35-Question System")
print("=" * 50)
print(f"\nInput: {len(answers)} answers")

# Validate
is_valid, error_msg, normalized_answers = validate_answers(answers)
print(f"Validation: {'PASSED' if is_valid else 'FAILED'}")
if not is_valid:
    print(f"Error: {error_msg}")
else:
    print(f"Normalized answers: {len(normalized_answers)} entries")
    
    # Get recommendations
    try:
        results = recommend_careers(normalized_answers, debug=False)
        if "error" in results:
            print(f"\nERROR in recommendations: {results['error']}")
        else:
            print(f"\nTop Career Recommendations:")
            for i, rec in enumerate(results.get('recommendations', [])[:3], 1):
                print(f"{i}. {rec['career']} - {rec['match_percentage']}% match")
            print(f"\nProfile Scores:")
            profile = results.get('profile_scores', {})
            for key, value in profile.items():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
