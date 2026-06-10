"""
Views for careers page — both SSR template and REST API.
"""

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    JobOpening, JobApplication, CareersPageContent,
    CompanyBenefit
)
from .serializers import (
    JobOpeningSerializer, JobOpeningListSerializer,
    JobApplicationCreateSerializer, JobApplicationDetailSerializer,
    CareersPageContentSerializer, CompanyBenefitSerializer
)
from omnexa_ai.core.utils import get_client_ip


# --- Template Views (SSR) ---
def careers_page(request):
    """
    Renders careers.html with all careers page content.
    """
    # Get active careers page content
    careers_content = CareersPageContent.objects.filter(is_active=True).first()

    # Get all active job openings
    job_openings = JobOpening.objects.filter(is_published=True).order_by('order', '-created_at')

    # Get company benefits
    company_benefits = CompanyBenefit.objects.filter(is_active=True).order_by('order')

    context = {
        'careers_content': careers_content,
        'job_openings': job_openings,
        'company_benefits': company_benefits,
    }

    return render(request, 'careers.html', context)


def job_detail_page(request, slug):
    """
    Individual job opening detail page.
    """
    job = get_object_or_404(JobOpening, slug=slug, is_published=True)
    return render(request, 'job_detail.html', {'job': job})


# --- REST API Views ---
class CareersPageContentAPIView(APIView):
    """
    GET /api/v1/careers/
    Returns the active careers page content with all related data.
    """

    def get(self, request):
        careers_content = CareersPageContent.objects.filter(is_active=True).first()

        if careers_content:
            serializer = CareersPageContentSerializer(careers_content)
            return Response(serializer.data)

        return Response(
            {'error': 'Careers page content not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class JobOpeningListAPIView(ListAPIView):
    """
    GET /api/v1/careers/jobs/
    Returns all published job openings.
    Supports filtering by category, job_type, experience_level.
    """
    serializer_class = JobOpeningListSerializer

    def get_queryset(self):
        qs = JobOpening.objects.filter(is_published=True).order_by('order', '-created_at')

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)

        # Filter by job type
        job_type = self.request.query_params.get('job_type')
        if job_type:
            qs = qs.filter(job_type=job_type)

        # Filter by experience level
        experience_level = self.request.query_params.get('experience_level')
        if experience_level:
            qs = qs.filter(experience_level=experience_level)

        # Filter by remote
        is_remote = self.request.query_params.get('is_remote')
        if is_remote:
            qs = qs.filter(is_remote=is_remote.lower() == 'true')

        # Filter by featured
        featured = self.request.query_params.get('featured')
        if featured:
            qs = qs.filter(featured=featured.lower() == 'true')

        return qs


class JobOpeningDetailAPIView(RetrieveAPIView):
    """
    GET /api/v1/careers/jobs/<slug>/
    Returns a single job opening's full detail.
    """
    queryset = JobOpening.objects.filter(is_published=True)
    serializer_class = JobOpeningSerializer
    lookup_field = 'slug'


class JobApplicationCreateAPIView(CreateAPIView):
    """
    POST /api/v1/careers/apply/
    Submit a job application.

    Steps:
      1. Validate application data
      2. Save application to database
      3. Send confirmation email to applicant
      4. Send notification email to HR
      5. Return success response
    """
    serializer_class = JobApplicationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Save application with IP address
            application = serializer.save(
                ip_address=get_client_ip(request)
            )

            # Send confirmation email to applicant
            send_mail(
                subject=f"Application Received — OMNEXA AI",
                message=f"""
Dear {application.name},

Thank you for applying to OMNEXA AI!

We have received your application and our team will review it shortly.
If your qualifications match our requirements, we will contact you within 7-10 business days
to schedule an interview.

Here's a summary of your application:
- Category: {application.category}
- Applied on: {application.created_at.strftime('%B %d, %Y')}

We appreciate your interest in joining OMNEXA AI and wish you the best of luck!

Best regards,
OMNEXA AI Hiring Team
📍 210, Sarthak Pulse Mall, Gandhinagar
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=True,
            )

            # Send notification email to HR
            send_mail(
                subject=f"📋 New Application: {application.name} — {application.category}",
                message=f"""
New job application received!

Applicant: {application.name}
Email: {application.email}
Phone: {application.phone}
Category: {application.category}
Address: {application.address}

View application in admin: https://omnexa.ai/admin/careers/jobapplication/{application.id}/
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            # Return success response
            return Response(
                {
                    "success": True,
                    "message": "Application submitted successfully! We'll review it and get back to you soon.",
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class CompanyBenefitListAPIView(ListAPIView):
    """
    GET /api/v1/careers/benefits/
    Returns all active company benefits.
    """
    queryset = CompanyBenefit.objects.filter(is_active=True).order_by('order')
    serializer_class = CompanyBenefitSerializer


class JobCategoriesAPIView(APIView):
    """
    GET /api/v1/careers/categories/
    Returns available job categories with counts.
    """

    def get(self, request):
        from .models import JOB_CATEGORY_CHOICES

        categories = []
        for value, label in JOB_CATEGORY_CHOICES:
            count = JobOpening.objects.filter(
                category=value,
                is_published=True
            ).count()
            categories.append({
                'value': value,
                'label': label,
                'count': count,
            })

        return Response(categories)


class JobTypesAPIView(APIView):
    """
    GET /api/v1/careers/job-types/
    Returns available job types with counts.
    """

    def get(self, request):
        from .models import JOB_TYPE_CHOICES

        job_types = []
        for value, label in JOB_TYPE_CHOICES:
            count = JobOpening.objects.filter(
                job_type=value,
                is_published=True
            ).count()
            job_types.append({
                'value': value,
                'label': label,
                'count': count,
            })

        return Response(job_types)


class ExperienceLevelsAPIView(APIView):
    """
    GET /api/v1/careers/experience-levels/
    Returns available experience levels with counts.
    """

    def get(self, request):
        from .models import EXPERIENCE_LEVEL_CHOICES

        levels = []
        for value, label in EXPERIENCE_LEVEL_CHOICES:
            count = JobOpening.objects.filter(
                experience_level=value,
                is_published=True
            ).count()
            levels.append({
                'value': value,
                'label': label,
                'count': count,
            })

        return Response(levels)
