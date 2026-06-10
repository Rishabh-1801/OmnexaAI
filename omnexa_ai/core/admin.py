"""
Admin configuration for core app.
"""

from django.contrib import admin
from .models import TimeStampedModel, MetaTagModel, PublishableModel

# These are abstract models, so they don't need admin registration
# This file exists for future core model additions
