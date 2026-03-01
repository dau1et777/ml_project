"""
Django URL Configuration for career recommendation API.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
    path('health/', views.health, name='health'),
    path('info/', views.info, name='info'),
]
