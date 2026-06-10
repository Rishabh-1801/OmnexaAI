"""
Serializers for home app.
"""

from rest_framework import serializers
from .models import (
    HomePageContent, Testimonial, Partner,
    FeatureHighlight, GoogleBusinessReviewConfig
)


class HomePageContentSerializer(serializers.ModelSerializer):
    """Full serializer for home page content."""
    testimonials = serializers.SerializerMethodField()
    partners = serializers.SerializerMethodField()
    feature_highlights = serializers.SerializerMethodField()

    class Meta:
        model = HomePageContent
        fields = '__all__'

    def get_testimonials(self, obj):
        from .serializers import TestimonialSerializer
        testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
        return TestimonialSerializer(testimonials, many=True).data

    def get_partners(self, obj):
        from .serializers import PartnerSerializer
        partners = Partner.objects.filter(is_active=True).order_by('order')
        return PartnerSerializer(partners, many=True).data

    def get_feature_highlights(self, obj):
        from .serializers import FeatureHighlightSerializer
        features = FeatureHighlight.objects.filter(is_active=True).order_by('order')
        return FeatureHighlightSerializer(features, many=True).data


class HomePageContentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for home page listing."""
    class Meta:
        model = HomePageContent
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'hero_description',
            'stat_1_label', 'stat_1_value', 'stat_2_label', 'stat_2_value',
            'stat_3_label', 'stat_3_value', 'stat_4_label', 'stat_4_value',
            'services_section_title', 'solutions_section_title',
            'case_studies_section_title', 'blog_section_title',
            'cta_title', 'cta_description', 'testimonials_section_title',
            'is_active'
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_company', 'client_title',
            'quote', 'rating', 'image', 'order', 'is_active',
            'is_from_google', 'google_review_id', 'google_star_rating',
            'google_review_date'
        ]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = [
            'id', 'name', 'logo', 'website_url', 'order', 'is_active'
        ]


class FeatureHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureHighlight
        fields = [
            'id', 'title', 'icon_class', 'description', 'order', 'is_active'
        ]


class GoogleBusinessReviewConfigSerializer(serializers.ModelSerializer):
    """Serializer for Google Business review config."""
    class Meta:
        model = GoogleBusinessReviewConfig
        fields = [
            'id', 'place_name', 'place_id', 'is_active',
            'sync_enabled', 'last_synced_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_synced_at', 'created_at', 'updated_at']
