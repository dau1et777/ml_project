"""
Django app configuration for Career Guidance Platform.
"""
from django.apps import AppConfig


class CareerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'career_app'
    verbose_name = 'Career Guidance Platform'
    
    def ready(self):
        """Register signal handlers when app is ready."""
        from django.db.models.signals import post_migrate
        from . import signals
        post_migrate.connect(signals.create_default_data, sender=self)
