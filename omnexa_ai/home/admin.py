"""
Admin configuration for home app.
"""

from django.contrib import admin
from .models import (
    HomePageContent, Testimonial, Partner,
    FeatureHighlight, GoogleBusinessReviewConfig
)


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['hero_title', 'hero_subtitle', 'cta_title']
    list_editable = ['is_active']

    fieldsets = (
        ('Hero Section', {
            'fields': (
                'hero_title', 'hero_subtitle', 'hero_description',
                'hero_primary_button_text', 'hero_primary_button_link',
                'hero_secondary_button_text', 'hero_secondary_button_link',
                'hero_image', 'is_active'
            )
        }),
        ('Statistics Section', {
            'fields': (
                'stat_1_label', 'stat_1_value',
                'stat_2_label', 'stat_2_value',
                'stat_3_label', 'stat_3_value',
                'stat_4_label', 'stat_4_value',
            )
        }),
        ('Services Preview Section', {
            'fields': (
                'services_section_title', 'services_section_subtitle',
                'services_button_text', 'services_button_link',
            )
        }),
        ('Solutions Preview Section', {
            'fields': (
                'solutions_section_title', 'solutions_section_subtitle',
                'solutions_button_text', 'solutions_button_link',
            )
        }),
        ('Case Studies Preview Section', {
            'fields': (
                'case_studies_section_title', 'case_studies_section_subtitle',
                'case_studies_button_text', 'case_studies_button_link',
            )
        }),
        ('Blog Preview Section', {
            'fields': (
                'blog_section_title', 'blog_section_subtitle',
                'blog_button_text', 'blog_button_link',
            )
        }),
        ('Testimonials Section', {
            'fields': (
                'testimonials_section_title', 'testimonials_section_subtitle',
            )
        }),
        ('CTA Section', {
            'fields': (
                'cta_title', 'cta_description',
                'cta_button_text', 'cta_button_link',
            )
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'order', 'is_active', 'is_from_google']
    list_filter = ['is_active', 'rating', 'is_from_google']
    search_fields = ['client_name', 'client_company', 'quote']
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('client_name', 'client_company', 'client_title', 'rating', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('quote', 'image')
        }),
        ('Google Integration', {
            'fields': ('is_from_google', 'google_review_id', 'google_star_rating', 'google_review_date'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_url', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'website_url']
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'logo', 'website_url', 'order', 'is_active')
        }),
    )


@admin.register(FeatureHighlight)
class FeatureHighlightAdmin(admin.ModelAdmin):
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


class GoogleBusinessReviewConfigAdmin(admin.ModelAdmin):
    list_display = ['place_name', 'place_id', 'is_active', 'sync_enabled', 'last_synced_at']
    list_filter = ['is_active', 'sync_enabled']
    fieldsets = (
        ('Place Details', {
            'fields': ('place_name', 'place_id')
        }),
        ('API Configuration', {
            'fields': ('api_key',),
            'description': 'Enter your Google Cloud API Key with Places API enabled. Keep this secure.'
        }),
        ('Sync Settings', {
            'fields': ('sync_enabled', 'is_active')
        }),
        ('Sync Status', {
            'fields': ('last_synced_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['last_synced_at']

    actions = ['sync_reviews_action']

    def sync_reviews_action(self, request, queryset):
        """Admin action to sync Google reviews."""
        from .google_reviews_service import sync_google_reviews_to_testimonials
        for config in queryset.filter(is_active=True):
            result = sync_google_reviews_to_testimonials(config)
            self.message_user(
                request,
                f"Sync complete: {result['created']} created, {result['updated']} updated, {result['skipped']} skipped."
            )
    sync_reviews_action.short_description = 'Sync reviews from Google Business'


admin.site.register(GoogleBusinessReviewConfig, GoogleBusinessReviewConfigAdmin)
