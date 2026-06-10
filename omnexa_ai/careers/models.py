"""
Models for careers app.
"""

from django.db import models
from django.contrib.auth.models import User
from omnexa_ai.core.models import TimeStampedModel, MetaTagModel, PublishableModel


JOB_TYPE_CHOICES = [
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
    ('remote', 'Remote'),
]

EXPERIENCE_LEVEL_CHOICES = [
    ('entry', 'Entry Level'),
    ('mid', 'Mid Level'),
    ('senior', 'Senior Level'),
    ('lead', 'Lead / Manager'),
    ('executive', 'Executive'),
]

JOB_CATEGORY_CHOICES = [
    ('engineering', 'Engineering'),
    ('design', 'Design'),
    ('marketing', 'Marketing'),
    ('sales', 'Sales'),
    ('operations', 'Operations'),
    ('hr', 'Human Resources'),
    ('finance', 'Finance'),
    ('ai_ml', 'AI / Machine Learning'),
    ('data_science', 'Data Science'),
    ('product', 'Product'),
]


class JobOpening(TimeStampedModel, MetaTagModel, PublishableModel):
    """
    Job openings displayed on the careers page.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='mid')
    category = models.CharField(max_length=50, choices=JOB_CATEGORY_CHOICES, default='engineering')

    # Location
    location = models.CharField(max_length=200, help_text="e.g., 'Gandhinagar, India' or 'Remote'")
    is_remote = models.BooleanField(default=False, help_text="Is this position remote?")

    # Job Details
    description = models.TextField(help_text="Job description")
    responsibilities = models.TextField(help_text="Key responsibilities (one per line)")
    requirements = models.TextField(help_text="Requirements and qualifications (one per line)")
    benefits = models.TextField(blank=True, help_text="Benefits offered (one per line)")

    # Salary
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Minimum salary (optional)"
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Maximum salary (optional)"
    )
    salary_currency = models.CharField(max_length=10, default='INR', help_text="e.g., INR, USD")
    salary_period = models.CharField(
        max_length=20,
        default='annual',
        help_text="e.g., annual, monthly, hourly"
    )

    # Application Settings
    application_deadline = models.DateTimeField(blank=True, null=True)
    application_email = models.EmailField(
        blank=True,
        help_text="Email to receive applications (if not using form)"
    )
    application_url = models.URLField(
        blank=True,
        help_text="External application URL (if not using form)"
    )

    # Additional Info
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False, help_text="Feature this job opening")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Job Opening'
        verbose_name_plural = 'Job Openings'

    def __str__(self):
        return f"{self.title} — {self.get_job_type_display()}"


class JobApplication(TimeStampedModel):
    """
    Job applications submitted through the careers page.
    """
    # Personal Information
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Professional Information
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Interested category (e.g., AI Developer, ML Engineer, etc.)"
    )
    address = models.TextField(blank=True, help_text="Candidate's address")

    # Resume
    resume = models.FileField(upload_to='careers/resumes/')

    # Application Status
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offer Extended'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='received'
    )

    # Admin Notes
    admin_notes = models.TextField(blank=True)
    interview_date = models.DateTimeField(blank=True, null=True)

    # Tracking
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return f"{self.name} — {self.category}"


class CareersPageContent(TimeStampedModel, MetaTagModel):
    """
    Main content for the careers page.
    """
    hero_title = models.CharField(max_length=300, default="Join Our Team")
    hero_subtitle = models.TextField(default="Build the future of AI with us")
    hero_description = models.TextField(
        default="We're looking for talented individuals who are passionate about AI and innovation. "
                "Join our team and help transform businesses with cutting-edge AI solutions."
    )
    hero_image = models.ImageField(upload_to='careers/hero/', blank=True, null=True)

    # Company Culture Section
    culture_title = models.CharField(max_length=200, default="Our Culture")
    culture_description = models.TextField(
        default="At OMNEXA AI, we believe in fostering a culture of innovation, collaboration, "
                "and continuous learning. We're committed to creating an inclusive environment "
                "where everyone can thrive and contribute to our mission."
    )

    # Benefits Section
    benefits_title = models.CharField(max_length=200, default="Benefits & Perks")
    benefits_description = models.TextField(
        default="We offer competitive compensation and a comprehensive benefits package "
                "to support our team members."
    )

    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Make an Impact?")
    cta_description = models.TextField(
        default="Browse our open positions and find your next career opportunity."
    )
    cta_button_text = models.CharField(max_length=100, default="View Open Positions")
    cta_button_link = models.CharField(max_length=200, default="#openings")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Careers Page Content'
        verbose_name_plural = 'Careers Page Content'

    def __str__(self):
        return "Careers Page Content"


class CompanyBenefit(TimeStampedModel):
    """
    Company benefits displayed on the careers page.
    """
    title = models.CharField(max_length=200)
    icon_class = models.CharField(
        max_length=100,
        help_text="Font Awesome icon class, e.g. 'fa-solid fa-heart'"
    )
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Company Benefit'
        verbose_name_plural = 'Company Benefits'

    def __str__(self):
        return self.title
