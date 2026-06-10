"""
Serializers for solutions app.
"""

from rest_framework import serializers
from .models import IndustrySolution


class IndustrySolutionSerializer(serializers.ModelSerializer):
    industry_display = serializers.CharField(
        source='get_industry_display', read_only=True
    )

    class Meta:
        model = IndustrySolution
        fields = [
            'id', 'industry', 'industry_display', 'icon_class', 'order',
            'problems', 'solution_overview', 'what_we_implement',
            'how_it_works', 'expected_results', 'is_active'
        ]
