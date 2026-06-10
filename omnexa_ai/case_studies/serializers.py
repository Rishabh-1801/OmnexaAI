"""
Serializers for case_studies app.
"""

from rest_framework import serializers
from .models import CaseStudy


class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'


class CaseStudyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for case study listing cards."""
    class Meta:
        model = CaseStudy
        fields = [
            'id', 'client_type', 'industry', 'slug', 'order',
            'excerpt', 'stat_1_label', 'stat_1_value',
            'stat_2_label', 'stat_2_value',
            'stat_3_label', 'stat_3_value', 'is_published'
        ]
