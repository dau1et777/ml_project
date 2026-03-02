"""
API Views for Career Guidance Platform
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from career_app.models import Career, Skill, CareerSkill, Bookmark
from career_app.serializers import (
    CareerSerializer, CareerDetailSerializer, SkillSerializer,
    QuizQuestionSerializer, PredictionRequestSerializer, 
    UserResultSerializer, UserProfileSerializer, SignupSerializer, 
    LoginSerializer
)
from career_app.services import PredictionService, SkillGapService, UserService
from ml.ml_service import get_ml_service


def _normalize_answer_keys(raw_answers):
    """Normalize answer keys to integer question numbers (1..35)."""
    normalized = {}
    for key, value in raw_answers.items():
        key_str = str(key).strip().lower()
        if key_str.startswith('q'):
            key_str = key_str[1:]

        question_id = int(key_str)
        normalized[question_id] = value

    return normalized


# ===== Authentication Endpoints =====

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    POST /api/auth/signup/
    Create new user account
    """
    serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    success, message, user = UserService.create_user(
        email=serializer.validated_data['email'],
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        first_name=serializer.validated_data.get('first_name', '')
    )
    
    if not success:
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'success': True,
        'message': message,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token.key
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    POST /api/auth/login/
    Authenticate user and return token
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    success, message, user = UserService.authenticate_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )
    
    if not success:
        return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'success': True,
        'message': message,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token.key
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    GET /api/auth/profile/
    Get authenticated user's profile
    """
    profile_data = UserService.get_user_profile(request.user)
    return Response({
        'success': True,
        'profile': profile_data
    })


# ===== Prediction Endpoints =====

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict(request):
    """
    POST /api/predict/
    
    Run ML model on quiz answers and return career predictions.
    
    Request:
    {
        "answers": {
            "1": 7,
            "2": 8,
            ...
            "35": 6
        },
        "save_result": true
    }
    
    Response:
    {
        "success": true,
        "predictions": {
            "top_careers": [
                {
                    "rank": 1,
                    "name": "Software Engineer",
                    "match_score": 0.8934
                },
                ...
            ],
            "scores": {...},
            "explanation": {...}
        },
        "result_id": "uuid-of-saved-result"
    }
    """
    serializer = PredictionRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Convert answer keys to integers (accepts "1" or "q1" styles)
    try:
        answers = _normalize_answer_keys(serializer.validated_data['answers'])
    except (ValueError, TypeError):
        return Response(
            {'success': False, 'error': 'Answer keys must be in 1-35 or q1-q35 format'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Run prediction pipeline
    result = PredictionService.predict_and_save(
        user=request.user,
        answers=answers,
        save_result=serializer.validated_data.get('save_result', True)
    )
    
    if result['success']:
        return Response(result)
    else:
        return Response(
            result,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediction_history(request):
    """
    GET /api/predict/history/
    Get user's past prediction results (last 10)
    """
    results = PredictionService.get_user_results(request.user, limit=10)
    return Response({
        'success': True,
        'count': len(results),
        'results': results
    })


# ===== Career Endpoints =====

class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for career knowledge base.
    
    GET /api/careers/ - List all careers
    GET /api/careers/{id}/ - Get career details with required skills
    GET /api/careers/{id}/roadmap/ - Get learning pathway
    POST /api/careers/{id}/bookmark/ - Bookmark a career
    """
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        """Return detailed career info with skills and requirements."""
        career = self.get_object()
        serializer = CareerDetailSerializer(career)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'], permission_classes=[AllowAny])
    def roadmap(self, request, id=None):
        """
        GET /api/careers/{id}/roadmap/
        Get learning pathway for career
        """
        career = self.get_object()
        roadmaps = career.roadmaps.all().order_by('stage')
        
        roadmap_data = [
            {
                'stage': rm.get_stage_display(),
                'duration_months': rm.duration_months,
                'description': rm.description,
                'skills_to_learn': rm.skills_to_learn
            }
            for rm in roadmaps
        ]
        
        return Response({
            'career': career.name,
            'roadmap': roadmap_data
        })
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, id=None):
        """
        POST /api/careers/{id}/bookmark/
        Bookmark or remove bookmark for a career
        
        Request:
        {
            "action": "add" | "remove"
        }
        """
        career = self.get_object()
        action_type = request.data.get('action', 'add')
        
        if action_type == 'add':
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                career=career
            )
            return Response({
                'success': True,
                'action': 'bookmarked',
                'career': career.name
            })
        
        elif action_type == 'remove':
            Bookmark.objects.filter(
                user=request.user,
                career=career
            ).delete()
            return Response({
                'success': True,
                'action': 'removed',
                'career': career.name
            })
        
        else:
            return Response(
                {'error': f'Unknown action: {action_type}'},
                status=status.HTTP_400_BAD_REQUEST
            )


# ===== Skill Gap Analysis =====

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def skill_gap_analysis(request):
    """
    GET /api/skill-gap/?career=Software%20Engineer
    Analyze skill gaps for a target career
    
    Response:
    {
        "success": true,
        "career": "Software Engineer",
        "gap_analysis": {
            "missing": [...],  # Skills user lacks
            "develop": [...],  # Skills to improve
            "strong": [...],   # Matching skills
            "total_gap_score": 3
        }
    }
    """
    career_name = request.query_params.get('career')
    if not career_name:
        return Response(
            {'error': 'Query parameter "career" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    gap_data = SkillGapService.analyze_gap(request.user, career_name)
    
    if 'error' in gap_data:
        return Response(
            {'success': False, 'error': gap_data['error']},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({
        'success': True,
        **gap_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def learning_recommendations(request):
    """
    GET /api/learning-path/?career=Software%20Engineer
    Get learning recommendations for a target career
    
    Response:
    {
        "success": true,
        "career": "Software Engineer",
        "recommendations": [
            {
                "priority": 1,
                "skill": "Python",
                "action": "Start learning",
                "level": "intermediate"
            },
            ...
        ]
    }
    """
    career_name = request.query_params.get('career')
    if not career_name:
        return Response(
            {'error': 'Query parameter "career" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    recommendations = SkillGapService.get_learning_recommendations(request.user, career_name)
    
    return Response({
        'success': True,
        'career': career_name,
        'recommendations': recommendations
    })


# ===== Health Check =====

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """
    GET /api/health/
    System health check
    """
    try:
        ml_service = get_ml_service()
        ml_ready = ml_service.model_ready
    except Exception as e:
        ml_ready = False
    
    return Response({
        'status': 'healthy',
        'ml_model': 'ready' if ml_ready else 'loading',
        'database': 'connected'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def info(request):
    """
    GET /api/info/
    Platform information and quiz metadata
    """
    return Response({
        'platform': 'Career Guidance System',
        'version': '1.0.0',
        'api_version': 'v1',
        'total_questions': 35,
        'total_careers': Career.objects.count(),
        'total_skills': Skill.objects.count(),
        'endpoints': {
            'authentication': [
                'POST /api/auth/signup/',
                'POST /api/auth/login/',
                'GET /api/auth/profile/'
            ],
            'predictions': [
                'POST /api/predict/',
                'GET /api/predict/history/'
            ],
            'careers': [
                'GET /api/careers/',
                'GET /api/careers/{id}/',
                'GET /api/careers/{id}/roadmap/',
                'POST /api/careers/{id}/bookmark/'
            ],
            'analysis': [
                'GET /api/skill-gap/?career=name',
                'GET /api/learning-path/?career=name'
            ]
        }
    })
