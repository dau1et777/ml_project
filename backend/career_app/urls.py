"""
URL routing for Career Guidance API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for viewsets
router = DefaultRouter()
router.register(r'careers', views.CareerViewSet, basename='career')

# API endpoints
urlpatterns = [
    # Router (careers viewset)
    path('', include(router.urls)),
    
    # Authentication
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.login, name='login'),
    path('auth/profile/', views.profile, name='profile'),
    
    # Predictions
    path('predict/', views.predict, name='predict'),
    path('predict/history/', views.prediction_history, name='prediction_history'),
    
    # Analysis
    path('skill-gap/', views.skill_gap_analysis, name='skill_gap'),
    path('learning-path/', views.learning_recommendations, name='learning_path'),
    
    # System
    path('health/', views.health, name='health'),
    path('info/', views.info, name='info'),
]
