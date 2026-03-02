"""
Django models for Career Guidance Platform
"""
from django.db import models
from django.contrib.auth.models import User
import uuid


class QuizQuestion(models.Model):
    """Quiz questions for career assessment."""
    QUESTION_TYPES = [
        ('scale', 'Likert Scale (1-10)'),
        ('choice', 'Multiple Choice (A/B/C/D)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(help_text="Question text")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = models.JSONField(null=True, blank=True, help_text='{"A": "Option A", "B": "Option B"...}')
    category = models.CharField(max_length=50, help_text="cognitive, motivation, interests, etc.")
    weight = models.FloatField(default=1.0, help_text="Feature importance weight")
    order = models.IntegerField(help_text="Display order in quiz")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Quiz Questions'
    
    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}"


class QuizAnswer(models.Model):
    """User's answers to quiz questions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=255, help_text="A, B, C, D, or numeric 1-10")
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
        verbose_name_plural = 'Quiz Answers'
    
    def __str__(self):
        return f"{self.user.username} - Q{self.question.order}: {self.answer_value}"


class Career(models.Model):
    """Career profiles in the knowledge base."""
    DEMAND_LEVELS = [
        ('high', 'High Demand'),
        ('medium', 'Medium Demand'),
        ('low', 'Low Demand'),
    ]
    
    CATEGORIES = [
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('business', 'Business'),
        ('engineering', 'Engineering'),
        ('creative', 'Creative'),
        ('education', 'Education'),
        ('science', 'Science'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES, default='other', help_text="Industry category")
    salary_min = models.FloatField(null=True, blank=True)
    salary_max = models.FloatField(null=True, blank=True)
    demand_level = models.CharField(max_length=20, choices=DEMAND_LEVELS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CareerRoadmap(models.Model):
    """Learning pathways for careers."""
    STAGES = [
        (1, 'Entry Level'),
        (2, 'Mid-Level'),
        (3, 'Senior'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='roadmaps')
    stage = models.IntegerField(choices=STAGES)
    duration_months = models.IntegerField()
    description = models.TextField()
    skills_to_learn = models.JSONField(help_text="List of skills needed at this stage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('career', 'stage')
        ordering = ['career', 'stage']
    
    def __str__(self):
        return f"{self.career.name} - {self.get_stage_display()}"


class Skill(models.Model):
    """Skills required for careers."""
    CATEGORIES = [
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('domain', 'Domain Knowledge'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class CareerSkill(models.Model):
    """Skills required for specific careers."""
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='required_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS)
    
    class Meta:
        unique_together = ('career', 'skill')
        verbose_name_plural = 'Career Skills'
    
    def __str__(self):
        return f"{self.career.name} - {self.skill.name}"


class UserSkill(models.Model):
    """User's personal skills and experience."""
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS)
    years_experience = models.FloatField(default=0)
    
    class Meta:
        unique_together = ('user', 'skill')
        verbose_name_plural = 'User Skills'
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


class UserResult(models.Model):
    """Saved quiz results and career predictions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz_session_id = models.CharField(max_length=255, unique=True, db_index=True)
    
    # Top 5 career predictions
    top_career_1 = models.CharField(max_length=255, null=True, blank=True)
    score_1 = models.FloatField(null=True, blank=True)
    top_career_2 = models.CharField(max_length=255, null=True, blank=True)
    score_2 = models.FloatField(null=True, blank=True)
    top_career_3 = models.CharField(max_length=255, null=True, blank=True)
    score_3 = models.FloatField(null=True, blank=True)
    top_career_4 = models.CharField(max_length=255, null=True, blank=True)
    score_4 = models.FloatField(null=True, blank=True)
    top_career_5 = models.CharField(max_length=255, null=True, blank=True)
    score_5 = models.FloatField(null=True, blank=True)
    
    # Explainability
    explanation = models.JSONField(null=True, blank=True, help_text="Why these careers match")
    top_careers_snapshot = models.JSONField(
        null=True,
        blank=True,
        help_text="Full top careers payload from prediction response"
    )
    profile_snapshot = models.JSONField(
        null=True,
        blank=True,
        help_text="Profile chart data (abilities/work_style/interests)"
    )
    model_version = models.CharField(max_length=50, default="1.0")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Results'
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"


class Bookmark(models.Model):
    """User's bookmarked careers."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'career')
        ordering = ['-created_at']
        verbose_name_plural = 'Bookmarks'
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.career.name}"
