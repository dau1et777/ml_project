"""
URL Configuration for Django project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Career Guidance API (includes ml recommendations, health checks, and all endpoints)
    path('api/', include('career_app.urls')),
]
