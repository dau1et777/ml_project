"""
Django Views - REST API endpoint for career recommendations.

Endpoint: POST /api/recommend/

Input:
{
  "answers": {
    "q1": 8,
    "q2": 7,
    ... (Q1-Q20: integers 1-10)
    "q21": "B",
    ... (Q21-Q25: single letter A/B/C/D)
  }
}

Output:
{
  "success": true,
  "results": [
    {
      "rank": 1,
      "career": "Software Engineer",
      "match_percentage": 92,
      "explanation": "Strong match in problem solving and logic...",
      "description": "Design and develop applications..."
    },
    ...
  ]
}
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import sys
from pathlib import Path

# Add ML module to path
ml_path = Path(__file__).parent / "ml"
sys.path.insert(0, str(ml_path))

from ml.recommender import recommend_careers
from ml.validator import validate_answers


@csrf_exempt
@require_http_methods(["POST"])
def recommend(request):
    """
    API endpoint for career recommendations.
    
    POST /api/recommend/
    
    Input JSON:
    {
      "answers": {
        "q1": 8,
        ...
        "q25": "A"
      },
      "debug": false  // optional
    }
    
    Returns:
    {
      "success": true/false,
      "results": [...],
      "error": "..." // if success is false
    }
    """
    try:
        # Parse JSON body
        body = json.loads(request.body.decode('utf-8'))
        answers = body.get("answers", {})
        debug = body.get("debug", False)
        
        # Validate input
        if not answers:
            return JsonResponse({
                "success": False,
                "error": "No answers provided"
            }, status=400)
        
        # Validate answers
        is_valid, validation_error = validate_answers(answers)
        if not is_valid:
            return JsonResponse({
                "success": False,
                "error": validation_error
            }, status=400)
        
        # Get recommendations
        results = recommend_careers(answers, debug=debug)
        
        # Check for errors in recommendation
        if "error" in results:
            return JsonResponse({
                "success": False,
                "error": results["error"]
            }, status=400)
        
        # Return success including profile scores if present
        response_payload = {
            "success": True,
            "results": results.get("recommendations", []),
        }
        if debug:
            response_payload["debug"] = results.get("debug")
        # attach profile data for charts
        if "profile_scores" in results:
            response_payload["profile_scores"] = results.get("profile_scores")

        return JsonResponse(response_payload, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON in request body"
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": f"Server error: {str(e)}"
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def health(request):
    """Health check endpoint."""
    return JsonResponse({
        "status": "healthy",
        "message": "Career recommendation service is running"
    })


@csrf_exempt
@require_http_methods(["GET"])
def info(request):
    """Get API information."""
    return JsonResponse({
        "api_version": "1.0",
        "endpoints": [
            {
                "path": "/api/recommend/",
                "method": "POST",
                "description": "Get career recommendations from quiz answers"
            },
            {
                "path": "/api/health/",
                "method": "GET",
                "description": "Health check endpoint"
            },
            {
                "path": "/api/info/",
                "method": "GET",
                "description": "API information"
            }
        ],
        "recommendation_algorithm": "Cosine Similarity with Feature Weighting",
        "total_careers": 90,
        "recommendation_count": 5,
        "quiz_questions": 25
    })
