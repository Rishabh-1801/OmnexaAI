"""
Admin configuration for services app.
"""

from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'tagline', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'tagline', 'problem']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'tagline', 'icon_class', 'order', 'is_active')
        }),
        ('Service Details', {
            'fields': ('problem', 'ai_solution', 'what_we_do', 'process', 'result')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
