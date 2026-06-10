"""
Views for home page — both SSR template and REST API.
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import (
    HomePageContent, Testimonial, Partner,
    FeatureHighlight, GoogleBusinessReviewConfig
)
from .serializers import (
    HomePageContentSerializer, TestimonialSerializer,
    PartnerSerializer, FeatureHighlightSerializer,
    GoogleBusinessReviewConfigSerializer
)
from omnexa_ai.blog.models import BlogPost
from omnexa_ai.case_studies.models import CaseStudy
from omnexa_ai.services.models import Service


# --- Template Views (SSR) ---
def home_page(request):
    """
    Renders index.html with all home page content.
    """
    # Get active home page content
    home_content = HomePageContent.objects.filter(is_active=True).first()

    # Get all active related content
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    partners = Partner.objects.filter(is_active=True).order_by('order')
    feature_highlights = FeatureHighlight.objects.filter(is_active=True).order_by('order')

    # Get preview content from other apps
    recent_blog_posts = BlogPost.objects.filter(
        is_published=True
    ).order_by('-published_at')[:3]

    featured_case_studies = CaseStudy.objects.filter(
        is_published=True
    ).order_by('order', '-created_at')[:3]

    featured_services = Service.objects.filter(
        is_active=True
    ).order_by('order')[:6]

    context = {
        'home_content': home_content,
        'testimonials': testimonials,
        'partners': partners,
        'feature_highlights': feature_highlights,
        'recent_blog_posts': recent_blog_posts,
        'featured_case_studies': featured_case_studies,
        'featured_services': featured_services,
    }

    return render(request, 'index.html', context)


# --- REST API Views ---
class HomePageContentAPIView(RetrieveAPIView):
    """
    GET /api/v1/home/
    Returns the active home page content with all related data.
    """
    queryset = HomePageContent.objects.filter(is_active=True)
    serializer_class = HomePageContentSerializer

    def get_object(self):
        # Return the first active home page content
        return get_object_or_404(self.queryset)


class TestimonialListAPIView(ListAPIView):
    """
    GET /api/v1/home/testimonials/
    Returns all active testimonials.
    """
    queryset = Testimonial.objects.filter(is_active=True).order_by('order')
    serializer_class = TestimonialSerializer


class PartnerListAPIView(ListAPIView):
    """
    GET /api/v1/home/partners/
    Returns all active partners.
    """
    queryset = Partner.objects.filter(is_active=True).order_by('order')
    serializer_class = PartnerSerializer


class FeatureHighlightListAPIView(ListAPIView):
    """
    GET /api/v1/home/features/
    Returns all active feature highlights.
    """
    queryset = FeatureHighlight.objects.filter(is_active=True).order_by('order')
    serializer_class = FeatureHighlightSerializer


class HomeStatsAPIView(APIView):
    """
    GET /api/v1/home/stats/
    Returns home page statistics.
    """

    def get(self, request):
        home_content = HomePageContent.objects.filter(is_active=True).first()

        if home_content:
            stats = {
                'stat_1': {
                    'label': home_content.stat_1_label,
                    'value': home_content.stat_1_value,
                },
                'stat_2': {
                    'label': home_content.stat_2_label,
                    'value': home_content.stat_2_value,
                },
                'stat_3': {
                    'label': home_content.stat_3_label,
                    'value': home_content.stat_3_value,
                },
                'stat_4': {
                    'label': home_content.stat_4_label,
                    'value': home_content.stat_4_value,
                },
            }
        else:
            stats = {
                'stat_1': {'label': 'Clients Served', 'value': '500+'},
                'stat_2': {'label': 'Projects Completed', 'value': '1000+'},
                'stat_3': {'label': 'Years Experience', 'value': '5+'},
                'stat_4': {'label': 'Team Members', 'value': '50+'},
            }

        return Response(stats)


class HomePreviewAPIView(APIView):
    """
    GET /api/v1/home/preview/
    Returns preview content for home page (blog, case studies, services).
    """

    def get(self, request):
        # Get recent blog posts
        recent_blog_posts = BlogPost.objects.filter(
            is_published=True
        ).order_by('-published_at')[:3]

        # Get featured case studies
        featured_case_studies = CaseStudy.objects.filter(
            is_published=True
        ).order_by('order', '-created_at')[:3]

        # Get featured services
        featured_services = Service.objects.filter(
            is_active=True
        ).order_by('order')[:6]

        from blog.serializers import BlogPostListSerializer
        from case_studies.serializers import CaseStudySerializer
        from services.serializers import ServiceListSerializer

        return Response({
            'recent_blog_posts': BlogPostListSerializer(recent_blog_posts, many=True).data,
            'featured_case_studies': CaseStudySerializer(featured_case_studies, many=True).data,
            'featured_services': ServiceListSerializer(featured_services, many=True).data,
        })


# --- Google Business Reviews API ---

class GoogleBusinessConfigAPIView(APIView):
    """
    GET  /api/v1/home/google-reviews/config/
    POST /api/v1/home/google-reviews/sync/
    Manages Google Business review integration.
    """

    def get(self, request):
        """Get Google Business review config and status."""
        config = GoogleBusinessReviewConfig.objects.filter(is_active=True).first()
        if not config:
            return Response(
                {'detail': 'Google Business configuration not set up.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = GoogleBusinessReviewConfigSerializer(config)
        return Response(serializer.data)

    def post(self, request):
        """Update Google Business configuration."""
        config = GoogleBusinessReviewConfig.objects.filter(is_active=True).first()
        if not config:
            return Response(
                {'detail': 'Google Business configuration not set up.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = GoogleBusinessReviewConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleBusinessSyncAPIView(APIView):
    """
    POST /api/v1/home/google-reviews/sync/
    Triggers a sync of reviews from Google Business.
    """

    def post(self, request):
        config = GoogleBusinessReviewConfig.objects.filter(is_active=True).first()
        if not config:
            return Response(
                {'detail': 'Google Business configuration not set up.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not config.sync_enabled:
            return Response(
                {'detail': 'Sync is disabled. Enable it in the admin panel.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not config.place_id or not config.api_key:
            return Response(
                {'detail': 'Place ID or API key is missing. Configure in admin panel.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from .google_reviews_service import sync_google_reviews_to_testimonials
        result = sync_google_reviews_to_testimonials(config)

        return Response({
            'success': True,
            'created': result['created'],
            'updated': result['updated'],
            'skipped': result['skipped'],
            'errors': result['errors'],
        })


class GoogleBusinessReviewsAPIView(APIView):
    """
    GET /api/v1/home/google-reviews/
    Fetches Google reviews directly without saving to DB.
    """

    def get(self, request):
        config = GoogleBusinessReviewConfig.objects.filter(is_active=True).first()
        if not config:
            return Response(
                {'detail': 'Google Business configuration not set up.'},
                status=status.HTTP_404_NOT_FOUND
            )

        from .google_reviews_service import fetch_google_reviews
        reviews = fetch_google_reviews(config.place_id, config.api_key)

        return Response({
            'count': len(reviews),
            'reviews': reviews,
        })


class GoogleBusinessTestimonialsAPIView(ListAPIView):
    """
    GET /api/v1/home/google-reviews/testimonials/
    Returns testimonials that came from Google Business.
    """
    queryset = Testimonial.objects.filter(is_from_google=True, is_active=True).order_by('order')
    serializer_class = TestimonialSerializer
