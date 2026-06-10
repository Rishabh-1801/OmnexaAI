"""
Admin configuration for case_studies app.
"""

from django.contrib import admin
from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ['client_type', 'industry', 'order', 'is_published', 'created_at']
    list_filter = ['industry', 'is_published']
    search_fields = ['client_type', 'industry', 'problem']
    prepopulated_fields = {'slug': ('client_type',)}
    list_editable = ['order', 'is_published']
    ordering = ['order', '-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('client_type', 'industry', 'slug', 'order', 'is_published')
        }),
        ('Case Study Details', {
            'fields': ('problem', 'services_used', 'ai_strategy', 'process_timeline', 'results')
        }),
        ('Before/After Data', {
            'fields': ('before_after_data',)
        }),
        ('Testimonial', {
            'fields': ('testimonial_quote', 'testimonial_client_name', 'testimonial_client_title')
        }),
        ('Stats', {
            'fields': ('stat_1_label', 'stat_1_value', 'stat_2_label', 'stat_2_value', 'stat_3_label', 'stat_3_value')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
