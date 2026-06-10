"""
Admin configuration for careers app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    JobOpening, JobApplication, CareersPageContent,
    CompanyBenefit
)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'job_type', 'experience_level', 'category',
        'location', 'is_remote', 'featured', 'is_published', 'created_at'
    ]
    list_filter = [
        'job_type', 'experience_level', 'category',
        'is_remote', 'featured', 'is_published'
    ]
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured', 'is_published']
    ordering = ['order', '-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title', 'slug', 'job_type', 'experience_level',
                'category', 'location', 'is_remote', 'order',
                'featured', 'is_published', 'published_at'
            )
        }),
        ('Job Details', {
            'fields': ('description', 'responsibilities', 'requirements', 'benefits')
        }),
        ('Salary', {
            'fields': ('salary_min', 'salary_max', 'salary_currency', 'salary_period')
        }),
        ('Application Settings', {
            'fields': ('application_deadline', 'application_email', 'application_url')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'email', 'phone', 'status', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'created_at'
    ]
    search_fields = [
        'name', 'email', 'phone', 'category'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'ip_address'
    ]
    list_editable = ['status']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Application Info', {
            'fields': ('status', 'interview_date')
        }),
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('category', 'address')
        }),
        ('Application Materials', {
            'fields': ('resume',)
        }),
        ('Tracking', {
            'fields': ('ip_address',)
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(CareersPageContent)
class CareersPageContentAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['hero_title', 'hero_subtitle', 'culture_title']
    list_editable = ['is_active']

    fieldsets = (
        ('Hero Section', {
            'fields': (
                'hero_title', 'hero_subtitle', 'hero_description',
                'hero_image', 'is_active'
            )
        }),
        ('Company Culture Section', {
            'fields': ('culture_title', 'culture_description')
        }),
        ('Benefits Section', {
            'fields': ('benefits_title', 'benefits_description')
        }),
        ('CTA Section', {
            'fields': (
                'cta_title', 'cta_description',
                'cta_button_text', 'cta_button_link'
            )
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )


@admin.register(CompanyBenefit)
class CompanyBenefitAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon_class', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'icon_class', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('description',)
        }),
    )
