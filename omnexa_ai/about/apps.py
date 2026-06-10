"""
About app configuration.
"""

from django.apps import AppConfig


class AboutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.about'
    verbose_name = 'About'
