"""
API Serializers and Schemas for Career Guidance Platform
"""
from rest_framework import serializers
from career_app.models import (
    Career, CareerRoadmap, Skill, CareerSkill, 
    UserResult, Bookmark, QuizQuestion, QuizAnswer
)
from django.contrib.auth.models import User


class CareerSerializer(serializers.ModelSerializer):
    """Career profile serialization."""
    salary_range = serializers.SerializerMethodField()
    demand_level_display = serializers.CharField(source='get_demand_level_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Career
        fields = ['id', 'name', 'description', 'category', 'category_display', 
                  'salary_min', 'salary_max', 'salary_range', 'demand_level', 'demand_level_display']
    
    def get_salary_range(self, obj):
        """Format salary as a readable range."""
        if obj.salary_min and obj.salary_max:
            return f"${obj.salary_min:,.0f} - ${obj.salary_max:,.0f}"
        return "Varies by experience"


class SkillSerializer(serializers.ModelSerializer):
    """Individual skill serialization."""
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description']


class CareerSkillSerializer(serializers.ModelSerializer):
    """Skills required for a career."""
    skill = SkillSerializer(read_only=True)
    
    class Meta:
        model = CareerSkill
        fields = ['skill', 'proficiency_level']


class CareerDetailSerializer(serializers.ModelSerializer):
    """Detailed career with roadmap and skills."""
    required_skills = CareerSkillSerializer(many=True, read_only=True)
    salary_range = serializers.SerializerMethodField()
    demand_level_display = serializers.CharField(source='get_demand_level_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Career
        fields = ['id', 'name', 'description', 'category', 'category_display',
                  'salary_min', 'salary_max', 'salary_range', 'demand_level', 
                  'demand_level_display', 'required_skills']
    
    def get_salary_range(self, obj):
        """Format salary as a readable range."""
        if obj.salary_min and obj.salary_max:
            return f"${obj.salary_min:,.0f} - ${obj.salary_max:,.0f}"
        return "Varies by experience"


class CareerRoadmapSerializer(serializers.ModelSerializer):
    """Learning pathway for a career."""
    class Meta:
        model = CareerRoadmap
        fields = ['id', 'stage', 'duration_months', 'description', 'skills_to_learn']


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Quiz question for frontend rendering."""
    class Meta:
        model = QuizQuestion
        fields = ['id', 'text', 'question_type', 'options', 'category', 'order']


class QuizAnswerSerializer(serializers.ModelSerializer):
    """User's quiz answer."""
    class Meta:
        model = QuizAnswer
        fields = ['id', 'question', 'answer_value', 'answered_at']


class PredictionRequestSerializer(serializers.Serializer):
    """Request schema for /api/predict/ endpoint."""
    answers = serializers.DictField(
        child=serializers.JSONField(),
        help_text="Map of question_id -> answer_value (1-35)"
    )
    save_result = serializers.BooleanField(default=True, required=False)


class PredictionResponseSerializer(serializers.Serializer):
    """Response schema for /api/predict/ endpoint."""
    success = serializers.BooleanField()
    predictions = serializers.JSONField(required=False)
    errors = serializers.ListField(child=serializers.CharField(), required=False)


class UserResultSerializer(serializers.ModelSerializer):
    """Saved quiz result with predictions."""
    class Meta:
        model = UserResult
        fields = [
            'id', 'quiz_session_id', 
            'top_career_1', 'score_1',
            'top_career_2', 'score_2',
            'top_career_3', 'score_3',
            'top_career_4', 'score_4',
            'top_career_5', 'score_5',
            'explanation', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BookmarkSerializer(serializers.ModelSerializer):
    """User's bookmarked careers."""
    career = CareerSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'career', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile with saved results and bookmarks."""
    quiz_results = UserResultSerializer(many=True, read_only=True, source='quiz_results')
    bookmarks = BookmarkSerializer(many=True, read_only=True, source='bookmarks')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'quiz_results', 'bookmarks']
        read_only_fields = ['id', 'date_joined']


class SignupSerializer(serializers.Serializer):
    """User signup request schema."""
    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)


class LoginSerializer(serializers.Serializer):
    """User login request schema."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
