"""
Models for services app.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel, MetaTagModel


class Service(TimeStampedModel, MetaTagModel):
    """
    Each of the 11 OMNEXA AI services.
    Editable from Django Admin.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=300)
    icon_class = models.CharField(
        max_length=100,
        help_text="Font Awesome icon class, e.g. 'fa-solid fa-brain'"
    )
    order = models.PositiveIntegerField(default=0)

    # 6-part service detail structure (matches frontend spec)
    problem = models.TextField(help_text="Problem businesses face")
    ai_solution = models.TextField(help_text="How AI solves it")
    what_we_do = models.TextField(help_text="Specific actions OMNEXA AI takes")
    process = models.TextField(help_text="Step-by-step process (use newlines)")
    result = models.TextField(help_text="What client gets")

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name
