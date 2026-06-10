"""
Models for solutions app.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel


INDUSTRY_CHOICES = [
    ('real_estate', 'Real Estate'),
    ('healthcare', 'Healthcare / Clinics'),
    ('ecommerce', 'E-commerce'),
    ('coaches', 'Coaches / Consultants'),
    ('local_business', 'Local Businesses'),
    ('startups_saas', 'Startups / SaaS'),
    ('education', 'Education Institutes'),
]


class IndustrySolution(TimeStampedModel):
    """
    Each industry solution block shown on solutions.html.
    """
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
        unique=True
    )
    icon_class = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    # 6-part structure matching frontend spec
    problems = models.TextField(
        help_text="Bullet-separated list of problems (one per line)"
    )
    solution_overview = models.TextField(
        help_text="One-paragraph AI solution description"
    )
    what_we_implement = models.TextField(
        help_text="Bullet list of AI tools/services used (one per line)"
    )
    how_it_works = models.TextField(
        help_text="5 numbered steps, one per line"
    )
    expected_results = models.TextField(
        help_text="Bullet list of expected results"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Industry Solution'
        verbose_name_plural = 'Industry Solutions'

    def __str__(self):
        return self.get_industry_display()
