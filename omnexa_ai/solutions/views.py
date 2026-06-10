"""
Views for solutions page — both SSR template and REST API.
"""

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import IndustrySolution
from .serializers import IndustrySolutionSerializer


# --- Template Views (SSR) ---
def solutions_page(request):
    """Renders solutions.html with all active industry solutions."""
    solutions = IndustrySolution.objects.filter(is_active=True).order_by('order')
    return render(request, 'solutions.html', {'solutions': solutions})


def solution_detail_page(request, industry):
    """Individual industry solution detail page."""
    solution = get_object_or_404(IndustrySolution, industry=industry, is_active=True)
    return render(request, 'solution_detail.html', {'solution': solution})


# --- REST API Views ---
class IndustrySolutionListAPIView(ListAPIView):
    """
    GET /api/v1/solutions/
    Returns all active industry solutions.
    """
    queryset = IndustrySolution.objects.filter(is_active=True).order_by('order')
    serializer_class = IndustrySolutionSerializer


class IndustrySolutionDetailAPIView(RetrieveAPIView):
    """
    GET /api/v1/solutions/<industry>/
    Returns a single industry solution's full detail.
    """
    queryset = IndustrySolution.objects.filter(is_active=True)
    serializer_class = IndustrySolutionSerializer
    lookup_field = 'industry'
