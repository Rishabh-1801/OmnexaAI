"""
Admin configuration for about app.
"""

from django.contrib import admin
from .models import TeamMember, CompanyValue, CompanyMilestone, AboutPageContent


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'title', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'title', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('bio', 'image')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'twitter_url')
        }),
    )


@admin.register(CompanyValue)
class CompanyValueAdmin(admin.ModelAdmin):
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


@admin.register(CompanyMilestone)
class CompanyMilestoneAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order', 'is_active']
    list_filter = ['is_active', 'year']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('year', 'title', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('description',)
        }),
    )


@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['hero_title', 'mission_statement', 'vision_statement']
    list_editable = ['is_active']

    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image', 'is_active')
        }),
        ('Mission & Vision', {
            'fields': ('mission_statement', 'vision_statement')
        }),
        ('About Us Content', {
            'fields': ('about_us_content',)
        }),
        ('Statistics', {
            'fields': ('stats_clients', 'stats_projects', 'stats_years', 'stats_team')
        }),
        ('Call to Action', {
            'fields': ('cta_title', 'cta_description', 'cta_button_text', 'cta_button_link')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
