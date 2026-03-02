"""
Business Logic Services - Orchestrate ML predictions and database operations
"""
from typing import Dict, List, Tuple, Any, Optional
import uuid
import numpy as np
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone

from career_app.models import UserResult, QuizAnswer, QuizQuestion, Career, CareerSkill, UserSkill, Skill
from ml.ml_service import get_ml_service, Preprocessor


class PredictionService:
    """
    Orchestrates career prediction pipeline:
    1. Validate answers
    2. Run ML model
    3. Persist results
    4. Generate explanations
    """
    
    @staticmethod
    def predict_and_save(
        user: User,
        answers: Dict[int, Any],
        save_result: bool = True
    ) -> Dict[str, Any]:
        """
        Complete prediction pipeline with optional result persistence.
        
        Args:
            user: Django User instance
            answers: Quiz answers {question_id: answer_value}
            save_result: Whether to save result to database
        
        Returns:
            {
                'success': bool,
                'predictions': {...},  # if success=True
                'error': str,  # if success=False
                'result_id': str  # if saved
            }
        """
        try:
            # Validate input
            is_valid, errors = Preprocessor.validate_answers(answers)
            if not is_valid:
                return {
                    'success': False,
                    'error': 'Invalid answers provided',
                    'details': errors
                }
            
            # Run ML model
            ml_service = get_ml_service()
            predictions = ml_service.predict(answers)
            
            # Save result if requested
            result_id = None
            if save_result:
                result_id = PredictionService._save_result(user, predictions, answers)
            
            return {
                'success': True,
                'predictions': predictions,
                'result_id': result_id
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    @staticmethod
    def _save_result(
        user: User,
        predictions: Dict[str, Any],
        answers: Dict[int, Any]
    ) -> str:
        """
        Persist prediction result to database.
        
        Args:
            user: Django User
            predictions: ML model output
            answers: Original quiz answers
        
        Returns:
            Result UUID
        """
        session_id = str(uuid.uuid4())
        
        with transaction.atomic():
            # Create UserResult record
            top_careers = predictions.get('top_careers', [])
            explanation_snapshot = predictions.get('explanation')
            if not explanation_snapshot and top_careers:
                explanation_snapshot = {
                    item.get('name'): item.get('explanation')
                    for item in top_careers
                    if item.get('name') and item.get('explanation')
                }
            
            result = UserResult.objects.create(
                user=user,
                quiz_session_id=session_id,
                model_version='1.0',
                explanation=explanation_snapshot or {},
                top_careers_snapshot=top_careers,
                profile_snapshot=predictions.get('profile')
            )
            
            # Store top 5 careers
            for idx, career_info in enumerate(top_careers[:5], 1):
                setattr(result, f'top_career_{idx}', career_info['name'])
                setattr(result, f'score_{idx}', career_info['match_score'])
            
            result.save()
            
            # Store individual quiz answers
            for question_id, answer_value in answers.items():
                try:
                    question = QuizQuestion.objects.get(order=question_id)
                    QuizAnswer.objects.update_or_create(
                        user=user,
                        question=question,
                        defaults={'answer_value': str(answer_value)}
                    )
                except QuizQuestion.DoesNotExist:
                    pass  # Skip if question doesn't exist in DB
        
        return str(result.id)
    
    @staticmethod
    def get_user_results(user: User, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve user's past prediction results.
        
        Args:
            user: Django User
            limit: Maximum number of results to return
        
        Returns:
            List of result dicts
        """
        results = UserResult.objects.filter(user=user).order_by('-created_at')[:limit]
        
        return [
            {
                'id': str(result.id),
                'created_at': result.created_at.isoformat(),
                'top_careers': result.top_careers_snapshot or [
                    {'rank': 1, 'name': result.top_career_1, 'score': result.score_1},
                    {'rank': 2, 'name': result.top_career_2, 'score': result.score_2},
                    {'rank': 3, 'name': result.top_career_3, 'score': result.score_3},
                    {'rank': 4, 'name': result.top_career_4, 'score': result.score_4},
                    {'rank': 5, 'name': result.top_career_5, 'score': result.score_5},
                ] if result.top_career_1 else [],
                'explanation': result.explanation,
                'profile': result.profile_snapshot
            }
            for result in results
        ]


class SkillGapService:
    """
    Analyzes skill gaps between current skills and career requirements.
    """
    
    @staticmethod
    def analyze_gap(user: User, career_name: str) -> Dict[str, Any]:
        """
        Analyze skill gap for a specific career.
        
        Args:
            user: Django User
            career_name: Target career name
        
        Returns:
            {
                'career': str,
                'required_skills': [...],
                'user_skills': [...],
                'gap_analysis': {
                    'missing': [...],  # Skills user doesn't have
                    'develop': [...],  # Skills to improve
                    'strong': [...]    # Skills user already has
                },
                'learning_path': [...]
            }
        """
        try:
            career = Career.objects.get(name=career_name)
        except Career.DoesNotExist:
            return {'error': f'Career "{career_name}" not found'}
        
        # Get required skills for career
        required_skills = CareerSkill.objects.filter(career=career).select_related('skill')
        
        # Get user's current skills
        user_skills = UserSkill.objects.filter(user=user).select_related('skill')
        user_skill_map = {us.skill.name: us.proficiency_level for us in user_skills}
        
        # Analyze gaps
        missing_skills = []
        develop_skills = []
        strong_skills = []
        
        for cs in required_skills:
            skill_name = cs.skill.name
            required_level = cs.proficiency_level
            user_level = user_skill_map.get(skill_name, None)
            
            if user_level is None:
                missing_skills.append({
                    'name': skill_name,
                    'required_level': required_level,
                    'reason': 'Not started'
                })
            elif user_level != required_level:
                level_order = {'beginner': 1, 'intermediate': 2, 'expert': 3}
                if level_order.get(user_level, 0) < level_order.get(required_level, 0):
                    develop_skills.append({
                        'name': skill_name,
                        'current_level': user_level,
                        'required_level': required_level,
                        'gap': f'{user_level} → {required_level}'
                    })
                else:
                    strong_skills.append({
                        'name': skill_name,
                        'current_level': user_level,
                        'required_level': required_level
                    })
            else:
                strong_skills.append({
                    'name': skill_name,
                    'current_level': user_level,
                    'required_level': required_level
                })
        
        return {
            'career': career_name,
            'gap_analysis': {
                'missing': missing_skills,
                'develop': develop_skills,
                'strong': strong_skills,
                'total_gap_score': len(missing_skills) + len(develop_skills)
            }
        }
    
    @staticmethod
    def get_learning_recommendations(user: User, career_name: str) -> List[Dict[str, Any]]:
        """
        Generate learning recommendations for a career.
        
        Args:
            user: Django User
            career_name: Target career
        
        Returns:
            List of learning path steps
        """
        try:
            career = Career.objects.get(name=career_name)
        except Career.DoesNotExist:
            return []
        
        gap_data = SkillGapService.analyze_gap(user, career_name)
        
        recommendations = []
        
        # Priority 1: Missing skills
        for skill in gap_data['gap_analysis']['missing']:
            recommendations.append({
                'priority': 1,
                'skill': skill['name'],
                'action': 'Start learning',
                'level': skill['required_level']
            })
        
        # Priority 2: Skills to develop
        for skill in gap_data['gap_analysis']['develop']:
            recommendations.append({
                'priority': 2,
                'skill': skill['name'],
                'action': 'Improve proficiency',
                'current': skill['current_level'],
                'target': skill['required_level']
            })
        
        return recommendations


class UserService:
    """
    User account and profile management.
    """
    
    @staticmethod
    def create_user(email: str, username: str, password: str, first_name: str = '') -> Tuple[bool, str, Optional[User]]:
        """
        Create new user account.
        
        Args:
            email: User email
            username: Unique username
            password: User password (will be hashed)
            first_name: Optional first name
        
        Returns:
            (success: bool, message: str, user: User|None)
        """
        if User.objects.filter(email=email).exists():
            return False, "Email already registered", None
        
        if User.objects.filter(username=username).exists():
            return False, "Username already taken", None
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name
            )
            return True, "User created successfully", user
        except Exception as e:
            return False, f"Error creating user: {str(e)}", None
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Authenticate user by email and password.
        
        Args:
            email: User email
            password: User password
        
        Returns:
            (authenticated: bool, message: str, user: User|None)
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return False, "Invalid credentials", None
        
        if not user.check_password(password):
            return False, "Invalid credentials", None
        
        return True, "Authenticated", user
    
    @staticmethod
    def get_user_profile(user: User) -> Dict[str, Any]:
        """
        Get complete user profile with history and bookmarks.
        
        Args:
            user: Django User
        
        Returns:
            User profile dict
        """
        results = PredictionService.get_user_results(user, limit=5)
        bookmarks = list(
            user.bookmarks.select_related('career').values_list('career__name', flat=True)
        )
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'joined_at': user.date_joined.isoformat(),
            'recent_results': results,
            'bookmarked_careers': bookmarks
        }
