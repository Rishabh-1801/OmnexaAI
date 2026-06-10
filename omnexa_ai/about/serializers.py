"""
Serializers for about app.
"""

from rest_framework import serializers
from .models import TeamMember, CompanyValue, CompanyMilestone, AboutPageContent


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'slug', 'title', 'bio', 'image',
            'linkedin_url', 'twitter_url', 'order', 'is_active'
        ]


class CompanyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyValue
        fields = [
            'id', 'title', 'icon_class', 'description', 'order', 'is_active'
        ]


class CompanyMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMilestone
        fields = [
            'id', 'year', 'title', 'description', 'order', 'is_active'
        ]


class AboutPageContentSerializer(serializers.ModelSerializer):
    team_members = TeamMemberSerializer(many=True, read_only=True, source='teammember_set')
    company_values = CompanyValueSerializer(many=True, read_only=True, source='companyvalue_set')
    company_milestones = CompanyMilestoneSerializer(many=True, read_only=True, source='companymilestone_set')

    class Meta:
        model = AboutPageContent
        fields = '__all__'


class AboutPageContentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for about page listing."""
    class Meta:
        model = AboutPageContent
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'mission_statement',
            'vision_statement', 'stats_clients', 'stats_projects',
            'stats_years', 'stats_team', 'cta_title', 'cta_button_text',
            'cta_button_link', 'is_active'
        ]
