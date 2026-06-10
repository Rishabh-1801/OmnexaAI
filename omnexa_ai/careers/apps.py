"""
Careers app configuration.
"""

from django.apps import AppConfig


class CareersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.careers'
    verbose_name = 'Careers'
