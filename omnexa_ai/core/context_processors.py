"""
Context processors for OMNEXA AI project.
"""

from django.conf import settings


def site_settings(request):
    """
    Add site-wide settings to template context.
    """
    return {
        'SITE_NAME': 'OMNEXA AI',
        'SITE_URL': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost',
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
        'DEBUG': settings.DEBUG,
    }
