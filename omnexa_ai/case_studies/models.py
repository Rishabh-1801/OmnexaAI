"""
Models for case_studies app.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel, MetaTagModel


class CaseStudy(TimeStampedModel, MetaTagModel):
    """
    Each client case study with before/after data and testimonial.
    """
    client_type = models.CharField(
        max_length=200,
        help_text="e.g., 'Real Estate Developer', 'Healthcare Clinic'"
    )
    industry = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    # 8-step structure
    problem = models.TextField()
    services_used = models.TextField(help_text="Services OMNEXA AI implemented")
    ai_strategy = models.TextField()
    process_timeline = models.TextField(
        help_text="Timeline description, e.g. 'Week 1–2: Setup, Week 3–4: Launch...'"
    )
    results = models.TextField(
        help_text="Bold highlighted numbers — e.g. '300% traffic growth in 60 days'"
    )

    # Before vs After table data (store as JSON)
    before_after_data = models.JSONField(
        help_text="List of dicts: [{'metric': 'Traffic', 'before': '1K/mo', 'after': '4K/mo'}]",
        default=list
    )

    # Testimonial
    testimonial_quote = models.TextField()
    testimonial_client_name = models.CharField(max_length=200)
    testimonial_client_title = models.CharField(max_length=200, blank=True)

    # Stats (for animated counter cards)
    stat_1_label = models.CharField(max_length=100, blank=True)
    stat_1_value = models.CharField(max_length=50, blank=True)
    stat_2_label = models.CharField(max_length=100, blank=True)
    stat_2_value = models.CharField(max_length=50, blank=True)
    stat_3_label = models.CharField(max_length=100, blank=True)
    stat_3_value = models.CharField(max_length=50, blank=True)

    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'

    def __str__(self):
        return f"{self.client_type} — {self.industry}"
