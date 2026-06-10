"""
Views for services page — both SSR template and REST API.
"""

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Service
from .serializers import ServiceSerializer


# --- Template Views (SSR) ---
def services_page(request):
    """Renders services.html with all active services."""
    services = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'services.html', {'services': services})


def service_detail_page(request, slug):
    """Individual service detail page."""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'service_detail.html', {'service': service})


# --- REST API Views ---
class ServiceListAPIView(ListAPIView):
    """
    GET /api/v1/services/
    Returns all active services. Used by frontend JS to populate cards.
    """
    queryset = Service.objects.filter(is_active=True).order_by('order')
    serializer_class = ServiceSerializer


class ServiceDetailAPIView(RetrieveAPIView):
    """
    GET /api/v1/services/<slug>/
    Returns a single service's full 6-part detail.
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
