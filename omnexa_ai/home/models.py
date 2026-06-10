"""
Models for home app.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel, MetaTagModel


class HomePageContent(TimeStampedModel, MetaTagModel):
    """
    Main content for the home page.
    """
    # Hero Section
    hero_title = models.CharField(max_length=300)
    hero_subtitle = models.TextField()
    hero_description = models.TextField()
    hero_primary_button_text = models.CharField(max_length=100, default="Book Free Strategy")
    hero_primary_button_link = models.CharField(max_length=200, default="/contact/")
    hero_secondary_button_text = models.CharField(max_length=100, default="View Services")
    hero_secondary_button_link = models.CharField(max_length=200, default="/services/")
    hero_image = models.ImageField(upload_to='home/hero/', blank=True, null=True)

    # Stats Section
    stat_1_label = models.CharField(max_length=100, default="Clients Served")
    stat_1_value = models.CharField(max_length=50, default="500+")
    stat_2_label = models.CharField(max_length=100, default="Projects Completed")
    stat_2_value = models.CharField(max_length=50, default="1000+")
    stat_3_label = models.CharField(max_length=100, default="Years Experience")
    stat_3_value = models.CharField(max_length=50, default="5+")
    stat_4_label = models.CharField(max_length=100, default="Team Members")
    stat_4_value = models.CharField(max_length=50, default="50+")

    # Services Preview Section
    services_section_title = models.CharField(max_length=200, default="Our AI Services")
    services_section_subtitle = models.TextField(default="Transform your business with cutting-edge AI solutions")
    services_button_text = models.CharField(max_length=100, default="View All Services")
    services_button_link = models.CharField(max_length=200, default="/services/")

    # Solutions Preview Section
    solutions_section_title = models.CharField(max_length=200, default="Industry Solutions")
    solutions_section_subtitle = models.TextField(default="Tailored AI solutions for every industry")
    solutions_button_text = models.CharField(max_length=100, default="Explore Solutions")
    solutions_button_link = models.CharField(max_length=200, default="/solutions/")

    # Case Studies Preview Section
    case_studies_section_title = models.CharField(max_length=200, default="Success Stories")
    case_studies_section_subtitle = models.TextField(default="See how we've helped businesses grow with AI")
    case_studies_button_text = models.CharField(max_length=100, default="View All Case Studies")
    case_studies_button_link = models.CharField(max_length=200, default="/case-studies/")

    # Blog Preview Section
    blog_section_title = models.CharField(max_length=200, default="Latest Insights")
    blog_section_subtitle = models.TextField(default="Stay updated with AI trends and best practices")
    blog_button_text = models.CharField(max_length=100, default="Read All Articles")
    blog_button_link = models.CharField(max_length=200, default="/blog/")

    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Transform Your Business?")
    cta_description = models.TextField(default="Get a free AI strategy consultation and discover how we can help you grow.")
    cta_button_text = models.CharField(max_length=100, default="Get Started")
    cta_button_link = models.CharField(max_length=200, default="/contact/")

    # Testimonials Section
    testimonials_section_title = models.CharField(max_length=200, default="What Our Clients Say")
    testimonials_section_subtitle = models.TextField(default="Real results from real businesses")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Home Page Content'
        verbose_name_plural = 'Home Page Content'

    def __str__(self):
        return "Home Page Content"


class Testimonial(TimeStampedModel):
    """
    Client testimonials for home page.
    """
    client_name = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200, blank=True)
    client_title = models.CharField(max_length=200, blank=True)
    quote = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")
    image = models.ImageField(upload_to='testimonials/images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Google Business integration
    is_from_google = models.BooleanField(default=False, help_text="If True, this review was fetched from Google Business")
    google_review_id = models.CharField(max_length=255, blank=True, help_text="Original Google review ID (used to prevent duplicates)")
    google_star_rating = models.PositiveIntegerField(default=0, help_text="Original Google star rating (if available)")
    google_review_date = models.DateTimeField(blank=True, null=True, help_text="Original Google review publish time")

    class Meta:
        ordering = ['order']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.client_name} — {self.client_company or 'Individual'}"


class Partner(TimeStampedModel):
    """
    Partner/Client logos for home page.
    """
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/logos/')
    website_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.name


class FeatureHighlight(TimeStampedModel):
    """
    Feature highlights for home page.
    """
    title = models.CharField(max_length=200)
    icon_class = models.CharField(
        max_length=100,
        help_text="Font Awesome icon class, e.g. 'fa-solid fa-rocket'"
    )
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Feature Highlight'
        verbose_name_plural = 'Feature Highlights'

    def __str__(self):
        return self.title


class GoogleBusinessReviewConfig(TimeStampedModel):
    """
    Configuration for Google Business / Google Places API.
    Stores the Place ID and API key to fetch reviews.
    """
    place_name = models.CharField(max_length=255, default="OMNEXA AI")
    place_id = models.CharField(max_length=255, blank=True, help_text="Google Place ID (e.g., ChIJN1t_tQuEmsT1o...)")
    api_key = models.CharField(max_length=255, blank=True, help_text="Google Cloud API Key with Places API enabled")
    is_active = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(blank=True, null=True, help_text="Last time reviews were synced from Google")
    sync_enabled = models.BooleanField(default=False, help_text="Enable automatic fetching of reviews from Google")

    class Meta:
        verbose_name = 'Google Business Review Config'
        verbose_name_plural = 'Google Business Review Configs'

    def __str__(self):
        return f"{self.place_name} ({self.place_id})"

    def clean(self):
        super().clean()
        # Only one config should be active at a time
        if self.is_active:
            GoogleBusinessReviewConfig.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
