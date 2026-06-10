"""
Models for contact app - lead capture and consultation bookings.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel


SERVICE_CHOICES = [
    ('aeo', 'AEO (Answer Engine Optimization)'),
    ('ai_marketing', 'AI Marketing & Automation'),
    ('ai_software', 'AI Software Development'),
    ('ai_chatbots', 'AI Chatbots'),
    ('content_creation', 'Content Creation (AI-generated)'),
    ('image_video', 'Image & Video Generation'),
    ('blog_writing', 'Blog Writing'),
    ('lead_generation', 'Lead Generation'),
    ('meta_ads', 'Meta Ads'),
    ('landing_page', 'Landing Page Optimization'),
    ('social_media', 'Social Media Marketing'),
]

LEAD_STATUS_CHOICES = [
    ('new', 'New'),
    ('contacted', 'Contacted'),
    ('qualified', 'Qualified'),
    ('proposal_sent', 'Proposal Sent'),
    ('closed_won', 'Closed Won'),
    ('closed_lost', 'Closed Lost'),
]


class ConsultationBooking(TimeStampedModel):
    """
    Stores every lead/booking from the Contact page form.
    This is the most important model — every form submission lands here.
    """
    # Required fields (match the frontend form exactly)
    name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Optional fields
    website = models.URLField(blank=True, null=True)
    service_interested = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        default='aeo'
    )
    message = models.TextField(blank=True, null=True)

    # CRM / Admin tracking
    status = models.CharField(
        max_length=20,
        choices=LEAD_STATUS_CHOICES,
        default='new'
    )
    admin_notes = models.TextField(blank=True, null=True)
    is_consultation_scheduled = models.BooleanField(default=False)
    consultation_datetime = models.DateTimeField(blank=True, null=True)

    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    referrer_url = models.URLField(blank=True, null=True)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consultation Booking'
        verbose_name_plural = 'Consultation Bookings'

    def __str__(self):
        return f"{self.name} — {self.business_name} ({self.get_status_display()})"


class NewsletterSubscriber(TimeStampedModel):
    """
    Email capture from the blog sidebar, CTAs, footer.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    source = models.CharField(
        max_length=50,
        blank=True,
        help_text="Where they subscribed from (blog, footer, hero, etc.)"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email
