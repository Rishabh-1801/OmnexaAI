"""
Views for case_studies page — both SSR template and REST API.
"""

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import CaseStudy
from .serializers import CaseStudySerializer


# --- Template Views (SSR) ---
def case_studies_page(request):
    """Renders case-studies.html with all published case studies."""
    case_studies = CaseStudy.objects.filter(is_published=True).order_by('order', '-created_at')
    return render(request, 'case-studies.html', {'case_studies': case_studies})


def case_study_detail_page(request, slug):
    """Individual case study detail page."""
    case_study = get_object_or_404(CaseStudy, slug=slug, is_published=True)
    return render(request, 'case-study_detail.html', {'case_study': case_study})


# --- REST API Views ---
class CaseStudyListAPIView(ListAPIView):
    """
    GET /api/v1/case-studies/
    Returns all published case studies.
    """
    queryset = CaseStudy.objects.filter(is_published=True).order_by('order', '-created_at')
    serializer_class = CaseStudySerializer


class CaseStudyDetailAPIView(RetrieveAPIView):
    """
    GET /api/v1/case-studies/<slug>/
    Returns a single case study's full detail.
    """
    queryset = CaseStudy.objects.filter(is_published=True)
    serializer_class = CaseStudySerializer
    lookup_field = 'slug'
