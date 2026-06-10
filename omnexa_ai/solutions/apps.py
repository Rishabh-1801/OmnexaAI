"""
Solutions app configuration.
"""

from django.apps import AppConfig


class SolutionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.solutions'
    verbose_name = 'Solutions'
