"""
Blog app configuration.
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.blog'
    verbose_name = 'Blog'
