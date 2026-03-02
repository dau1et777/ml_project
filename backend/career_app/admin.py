"""
Django Admin Configuration for Career Guidance Platform
"""
from django.contrib import admin
from .models import (
    QuizQuestion, QuizAnswer, Career, CareerRoadmap, 
    Skill, CareerSkill, UserSkill, UserResult, Bookmark
)


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'text', 'question_type', 'category', 'weight']
    list_filter = ['question_type', 'category']
    search_fields = ['text']
    ordering = ['order']


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer_value', 'answered_at']
    list_filter = ['answered_at', 'question__category']
    search_fields = ['user__username', 'question__text']
    readonly_fields = ['answered_at']


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'demand_level', 'salary_min', 'salary_max']
    list_filter = ['demand_level']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Compensation & Demand', {
            'fields': ('salary_min', 'salary_max', 'demand_level')
        }),
    )


@admin.register(CareerRoadmap)
class CareerRoadmapAdmin(admin.ModelAdmin):
    list_display = ['career', 'stage', 'duration_months']
    list_filter = ['stage', 'career']
    search_fields = ['career__name', 'description']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(CareerSkill)
class CareerSkillAdmin(admin.ModelAdmin):
    list_display = ['career', 'skill', 'proficiency_level']
    list_filter = ['career', 'proficiency_level']
    search_fields = ['career__name', 'skill__name']


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'years_experience']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['user__username', 'skill__name']


@admin.register(UserResult)
class UserResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'top_career_1', 'score_1']
    list_filter = ['created_at', 'model_version']
    search_fields = ['user__username', 'quiz_session_id']
    readonly_fields = ['quiz_session_id', 'created_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'career', 'created_at']
    list_filter = ['created_at', 'career']
    search_fields = ['user__username', 'career__name']
    readonly_fields = ['created_at']
