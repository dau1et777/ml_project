"""
Example Usage - Career Recommendation System

This file demonstrates all ways to use the career recommendation system:
1. Direct Python API
2. Django REST API
3. Frontend UI
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from ml.recommender import recommend_careers
from ml.validator import QUIZ_QUESTIONS
from ml.debug import DebugHelper
import json


# ==============================================================================
# EXAMPLE 1: Complete User Profile (High Technical, Low Social)
# ==============================================================================
def example_software_engineer_candidate():
    """
    Scenario: Person who is excellent at problem-solving, technical work,
    but prefers independent work and learning over leadership/social interaction.
    
    Expected: Software Engineer, ML Engineer, Data Scientist, Backend Dev, DevOps
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Technical Specialist (Software Engineer Profile)")
    print("="*80)
    
    answers = {
        # Cognitive & Problem Solving - VERY HIGH
        "q1": 9,   # Complex problems: Very comfortable
        "q2": 8,   # Data analysis: Enjoy
        "q3": 9,   # Logical reasoning: Very good
        "q4": 8,   # Practical over theoretical: Practical
        "q5": 8,   # Debugging: Very much enjoy
        
        # Creativity & Innovation - MEDIUM-LOW
        "q6": 5,   # Generating ideas: Medium
        "q7": 4,   # Visual/UX design: Less so
        "q8": 6,   # Innovation value: Moderate
        "q9": 7,   # Translate concepts: Good
        "q10": 5,  # Ambiguity comfort: Medium
        
        # Communication & Leadership - LOW
        "q11": 3,  # Explaining ideas: Not very skilled
        "q12": 2,  # Mentoring: Not interested
        "q13": 3,  # Public speaking: Uncomfortable
        "q14": 3,  # Negotiation: Not strong
        "q15": 2,  # Leadership: Not natural
        
        # Academic & Technical - VERY HIGH
        "q16": 9,  # Math foundation: Strong
        "q17": 7,  # Research interest: Fairly interested
        "q18": 9,  # Programming: Very proficient
        "q19": 9,  # Learning tools: Very comfortable
        "q20": 8,  # Continuous learning: Highly value
        
        # Forced Choices
        "q21": "A",  # Work environment: Fast-paced
        "q22": "A",  # Problem type: Technical challenges
        "q23": "C",  # Career values: Personal growth & learning
        "q24": "A",  # Work style: Hands-on, building
        "q25": "A"   # Success measure: Results & outcomes
    }
    
    results = recommend_careers(answers, debug=False)
    
    print("\nProfile Scores:")
    for category, percent in results.get("profile_scores", {}).items():
        print(f"  {category}: {percent}%")
    
    print("\nTop 5 Recommendations:")
    for rec in results["recommendations"]:
        print(f"\n  {rec['rank']}. {rec['career']} ({rec['match_percentage']}%)")
        print(f"     📌 {rec['explanation']}")
        print(f"     📝 {rec['description']}")


# ==============================================================================
# EXAMPLE 2: Creative Designer Profile
# ==============================================================================
def example_creative_designer():
    """
    Scenario: Visually creative person who enjoys design and innovation,
    but struggles with heavy technical/mathematical work.
    
    Expected: UX Designer, UI Designer, Product Designer, Graphic Designer
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Creative Innovator (Designer Profile)")
    print("="*80)
    
    answers = {
        # Cognitive & Problem Solving - MEDIUM
        "q1": 5, "q2": 4, "q3": 5, "q4": 5, "q5": 4,
        
        # Creativity & Innovation - VERY HIGH
        "q6": 10, "q7": 10, "q8": 9, "q9": 9, "q10": 9,
        
        # Communication & Leadership - HIGH
        "q11": 8, "q12": 6, "q13": 8, "q14": 6, "q15": 5,
        
        # Academic & Technical - LOW-MEDIUM
        "q16": 4, "q17": 3, "q18": 4, "q19": 5, "q20": 7,
        
        # Preferences
        "q21": "B",  # Collaborative environment
        "q22": "D",  # Creative challenges
        "q23": "A",  # Impact
        "q24": "D",  # Creative expression
        "q25": "D"   # Innovation leadership
    }
    
    results = recommend_careers(answers, debug=False)
    
    print("\nProfile Scores:")
    for category, percent in results.get("profile_scores", {}).items():
        print(f"  {category}: {percent}%")
    
    print("\nTop 5 Recommendations:")
    for rec in results["recommendations"]:
        print(f"\n  {rec['rank']}. {rec['career']} ({rec['match_percentage']}%)")
        print(f"     📌 {rec['explanation']}")


# ==============================================================================
# EXAMPLE 3: Business Leader Profile
# ==============================================================================
def example_business_leader():
    """
    Scenario: Natural leader who excels in communication, influencing others,
    strategic thinking. Moderately technical.
    
    Expected: Product Manager, Sales Manager, Consultant, Entrepreneur
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Business Leader (Manager Profile)")
    print("="*80)
    
    answers = {
        # Cognitive - MEDIUM-HIGH
        "q1": 7, "q2": 6, "q3": 7, "q4": 8, "q5": 6,
        
        # Creativity - MEDIUM-HIGH
        "q6": 7, "q7": 5, "q8": 8, "q9": 8, "q10": 7,
        
        # Communication & Leadership - VERY HIGH
        "q11": 9, "q12": 8, "q13": 9, "q14": 9, "q15": 9,
        
        # Academic & Technical - MEDIUM
        "q16": 6, "q17": 5, "q18": 5, "q19": 6, "q20": 7,
        
        # Preferences
        "q21": "A",  # Fast-paced
        "q22": "C",  # Strategic problems
        "q23": "A",  # Impact
        "q24": "B",  # Strategic planning
        "q25": "D"   # Thought leadership
    }
    
    results = recommend_careers(answers, debug=False)
    
    print("\nProfile Scores:")
    for category, percent in results.get("profile_scores", {}).items():
        print(f"  {category}: {percent}%")
    
    print("\nTop 5 Recommendations:")
    for rec in results["recommendations"]:
        print(f"\n  {rec['rank']}. {rec['career']} ({rec['match_percentage']}%)")
        print(f"     📌 {rec['explanation']}")


# ==============================================================================
# EXAMPLE 4: Academic Researcher
# ==============================================================================
def example_academic_researcher():
    """
    Scenario: Person focused on research, learning, and knowledge advancement.
    High technical + high thinking skills. Lower interest in commercialization.
    
    Expected: Research Scientist, Professor, PhD specialized roles
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Academic Researcher Profile")
    print("="*80)
    
    answers = {
        # Cognitive - VERY HIGH
        "q1": 9, "q2": 9, "q3": 9, "q4": 9, "q5": 8,
        
        # Creativity - MEDIUM-HIGH
        "q6": 6, "q7": 4, "q8": 7, "q9": 6, "q10": 7,
        
        # Communication - MEDIUM
        "q11": 5, "q12": 6, "q13": 6, "q14": 4, "q15": 4,
        
        # Academic & Technical - VERY HIGH
        "q16": 9, "q17": 9, "q18": 6, "q19": 8, "q20": 10,
        
        # Preferences
        "q21": "D",  # Structured environment
        "q22": "A",  # Technical problems (research)
        "q23": "C",  # Learning and growth
        "q24": "B",  # Analysis
        "q25": "B"   # Knowledge/mastery
    }
    
    results = recommend_careers(answers, debug=False)
    
    print("\nProfile Scores:")
    for category, percent in results.get("profile_scores", {}).items():
        print(f"  {category}: {percent}%")
    
    print("\nTop 5 Recommendations:")
    for rec in results["recommendations"]:
        print(f"\n  {rec['rank']}. {rec['career']} ({rec['match_percentage']}%)")
        print(f"     📌 {rec['explanation']}")


# ==============================================================================
# EXAMPLE 5: API Usage (as if called from frontend)
# ==============================================================================
def example_api_usage():
    """
    Shows how the API would be called from the React frontend.
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: API Usage (React Frontend Integration)")
    print("="*80)
    
    print("\nJavaScript Code Example:")
    print("""
    // frontend/api.js
    const response = await fetch('/api/recommend/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        answers: {
          q1: 8, q2: 7, ..., q25: 'A'
        }
      })
    });
    
    const data = await response.json();
    
    // Results look like:
    {
      "success": true,
      "results": [
        {
          "rank": 1,
          "career": "Software Engineer",
          "match_percentage": 92,
          "explanation": "Strong match in problem solving...",
          "description": "Design and develop applications..."
        },
        ...
      ]
    }
    """)


# ==============================================================================
# EXAMPLE 6: Debug Output
# ==============================================================================
def example_debug_output():
    """
    Shows detailed debug information for understanding the recommendation.
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Debug Output")
    print("="*80)
    
    answers = {
        "q1": 9, "q2": 8, "q3": 9, "q4": 8, "q5": 8,
        "q6": 5, "q7": 4, "q8": 6, "q9": 7, "q10": 5,
        "q11": 3, "q12": 2, "q13": 3, "q14": 3, "q15": 2,
        "q16": 9, "q17": 7, "q18": 9, "q19": 9, "q20": 8,
        "q21": "A", "q22": "A", "q23": "C", "q24": "A", "q25": "A"
    }
    
    print("\nRunning with debug=True to see internal vectors...\n")
    results = recommend_careers(answers, debug=True)
    
    print("Debug Information Available:")
    if "debug" in results:
        print(f"  • User vector: {len(results['debug']['user_vector'])} dimensions")
        print(f"  • Weighted vector: {len(results['debug']['weighted_user_vector'])} dimensions")
        print(f"  • Top 5 career vectors loaded")
    else:
        print("  (Run with debug=True in recommend_careers for detailed info)")


# ==============================================================================
# MAIN
# ==============================================================================
def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "CAREER RECOMMENDATION SYSTEM - USAGE EXAMPLES".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run examples
    example_software_engineer_candidate()
    example_creative_designer()
    example_business_leader()
    example_academic_researcher()
    example_api_usage()
    example_debug_output()
    
    # Summary
    print("\n" + "="*80)
    print("EXAMPLES COMPLETED")
    print("="*80)
    print("""
Key Takeaways:
    ✓ The system adapts to different profiles
    ✓ Technical profiles → Software/AI roles
    ✓ Creative profiles → Design roles
    ✓ Social profiles → Business/Sales roles
    ✓ Academic profiles → Research roles
    
    ✓ Each recommendation includes:
        • Rank (1-5)
        • Career name
        • Match percentage (0-100)
        • Explanation of why it matches
        • Career description
    
    ✓ API is simple REST endpoint
    ✓ Input: Quiz answers (25 questions)
    ✓ Output: Top 5 careers with explanations
    
    ✓ Debug mode shows:
        • User vector composition
        • Weighted values
        • Top career vectors
        • Similarity calculations
    """)


if __name__ == "__main__":
    main()
