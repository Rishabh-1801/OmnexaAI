"""
Case studies app configuration.
"""

from django.apps import AppConfig


class CaseStudiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.case_studies'
    verbose_name = 'Case Studies'
