"""
Serializers for careers app.
"""

from rest_framework import serializers
from .models import (
    JobOpening, JobApplication, CareersPageContent,
    CompanyBenefit
)


class JobOpeningSerializer(serializers.ModelSerializer):
    """Full serializer for job opening."""
    job_type_display = serializers.CharField(
        source='get_job_type_display', read_only=True
    )
    experience_level_display = serializers.CharField(
        source='get_experience_level_display', read_only=True
    )
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = JobOpening
        fields = '__all__'


class JobOpeningListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for job opening listing."""
    job_type_display = serializers.CharField(
        source='get_job_type_display', read_only=True
    )
    experience_level_display = serializers.CharField(
        source='get_experience_level_display', read_only=True
    )
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = JobOpening
        fields = [
            'id', 'title', 'slug', 'job_type', 'job_type_display',
            'experience_level', 'experience_level_display', 'category',
            'category_display', 'location', 'is_remote', 'order',
            'featured', 'is_published', 'published_at'
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for job application."""
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = JobApplication
        fields = '__all__'


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new job application."""
    class Meta:
        model = JobApplication
        fields = [
            'name', 'email', 'phone', 'category', 'address', 'resume'
        ]

    def validate_resume(self, value):
        """Validate resume file."""
        # Check file size (max 5MB)
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                "Resume file size must be less than 5MB."
            )

        # Check file type
        allowed_extensions = ['.pdf', '.doc', '.docx']
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                "Resume must be a PDF, DOC, or DOCX file."
            )

        return value


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    """Full serializer for job application (admin use)."""
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = JobApplication
        fields = '__all__'


class CareersPageContentSerializer(serializers.ModelSerializer):
    """Full serializer for careers page content."""
    company_benefits = serializers.SerializerMethodField()

    class Meta:
        model = CareersPageContent
        fields = '__all__'

    def get_company_benefits(self, obj):
        benefits = CompanyBenefit.objects.filter(is_active=True).order_by('order')
        return CompanyBenefitSerializer(benefits, many=True).data


class CompanyBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBenefit
        fields = [
            'id', 'title', 'icon_class', 'description', 'order', 'is_active'
        ]
