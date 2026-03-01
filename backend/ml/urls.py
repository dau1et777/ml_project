"""
Django URLs for Career Recommendation API
"""

from django.urls import path
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import sys
from pathlib import Path

# Add ML module to path for imports
ml_path = Path(__file__).parent
sys.path.insert(0, str(ml_path))

from recommender import recommend_careers
from validator import validate_answers


@csrf_exempt
@require_http_methods(["POST"])
def recommend(request):
    """
    API endpoint for career recommendations.
    POST /api/recommend/
    """
    try:
        body = json.loads(request.body.decode('utf-8'))
        answers = body.get("answers", {})
        debug = body.get("debug", False)
        
        if not answers:
            return JsonResponse({
                "success": False,
                "error": "No answers provided"
            }, status=400)
        
        is_valid, validation_error, normalized_answers = validate_answers(answers)
        if not is_valid:
            return JsonResponse({
                "success": False,
                "error": validation_error
            }, status=400)
        
        results = recommend_careers(normalized_answers, debug=debug)
        
        if "error" in results:
            return JsonResponse({
                "success": False,
                "error": results["error"]
            }, status=400)
        
        response_payload = {
            "success": True,
            "results": results.get("recommendations", []),
        }
        if debug:
            response_payload["debug"] = results.get("debug")
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
    })


app_name = 'api'

urlpatterns = [
    path('recommend/', recommend, name='recommend'),
    path('health/', health, name='health'),
    path('info/', info, name='info'),
]

