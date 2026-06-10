"""
Home app configuration.
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.home'
    verbose_name = 'Home'
