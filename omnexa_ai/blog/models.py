"""
Models for blog app.
"""

from django.db import models
from django.contrib.auth.models import User
from omnexa_ai.core.models import TimeStampedModel, MetaTagModel, PublishableModel


BLOG_CATEGORY_CHOICES = [
    ('aeo', 'AEO'),
    ('ai_marketing', 'AI Marketing'),
    ('ai_tools', 'AI Tools'),
    ('automation', 'Automation'),
    ('meta_ads', 'Meta Ads with AI'),
    ('lead_generation', 'Lead Generation'),
    ('ai_content', 'AI Content Creation'),
]


class BlogPost(TimeStampedModel, MetaTagModel, PublishableModel):
    """
    Each blog article. Displayed on blog.html with category filters.
    """
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    category = models.CharField(
        max_length=50,
        choices=BLOG_CATEGORY_CHOICES,
        default='ai_marketing'
    )
    excerpt = models.TextField(
        max_length=300,
        help_text="2-line description shown on blog card"
    )
    content = models.TextField(help_text="Full article content (HTML or Markdown)")
    featured_image = models.ImageField(
        upload_to='blog/images/',
        blank=True, null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # Stats
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
