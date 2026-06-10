"""
Models for about app.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel, MetaTagModel


class TeamMember(TimeStampedModel):
    """
    Team members displayed on the about page.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200, help_text="e.g., 'CEO & Founder', 'AI Engineer'")
    bio = models.TextField(help_text="Short biography")
    image = models.ImageField(upload_to='team/images/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.name} — {self.title}"


class CompanyValue(TimeStampedModel):
    """
    Company values/mission statements for about page.
    """
    title = models.CharField(max_length=200)
    icon_class = models.CharField(
        max_length=100,
        help_text="Font Awesome icon class, e.g. 'fa-solid fa-lightbulb'"
    )
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Company Value'
        verbose_name_plural = 'Company Values'

    def __str__(self):
        return self.title


class CompanyMilestone(TimeStampedModel):
    """
    Company milestones/achievements timeline.
    """
    year = models.CharField(max_length=50, help_text="e.g., '2024', 'Q1 2024'")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Company Milestone'
        verbose_name_plural = 'Company Milestones'

    def __str__(self):
        return f"{self.year} — {self.title}"


class AboutPageContent(TimeStampedModel, MetaTagModel):
    """
    Main content for the about page.
    """
    hero_title = models.CharField(max_length=300)
    hero_subtitle = models.TextField()
    hero_image = models.ImageField(upload_to='about/hero/', blank=True, null=True)

    mission_statement = models.TextField()
    vision_statement = models.TextField()

    about_us_content = models.TextField(help_text="Main about us section content")

    stats_clients = models.PositiveIntegerField(default=0, help_text="Number of clients served")
    stats_projects = models.PositiveIntegerField(default=0, help_text="Number of projects completed")
    stats_years = models.PositiveIntegerField(default=0, help_text="Years in business")
    stats_team = models.PositiveIntegerField(default=0, help_text="Team members")

    cta_title = models.CharField(max_length=200, blank=True)
    cta_description = models.TextField(blank=True)
    cta_button_text = models.CharField(max_length=100, default="Get Started")
    cta_button_link = models.CharField(max_length=200, default="/contact/")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'About Page Content'
        verbose_name_plural = 'About Page Content'

    def __str__(self):
        return "About Page Content"
