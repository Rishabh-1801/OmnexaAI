"""
Base models for OMNEXA AI project.
"""

from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MetaTagModel(models.Model):
    """
    An abstract base class model that provides SEO meta fields.
    """
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """
    An abstract base class model that provides publish status.
    """
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
