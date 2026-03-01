"""
URL Configuration for Django project.
"""

from django.urls import path, include

urlpatterns = [
    path('api/', include('ml.urls')),
]
