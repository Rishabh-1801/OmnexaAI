"""
Admin configuration for solutions app.
"""

from django.contrib import admin
from .models import IndustrySolution


@admin.register(IndustrySolution)
class IndustrySolutionAdmin(admin.ModelAdmin):
    list_display = ['industry', 'icon_class', 'order', 'is_active']
    list_filter = ['industry', 'is_active']
    search_fields = ['industry', 'solution_overview']
    list_editable = ['order', 'is_active']
    ordering = ['order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('industry', 'icon_class', 'order', 'is_active')
        }),
        ('Solution Details', {
            'fields': ('problems', 'solution_overview', 'what_we_implement', 'how_it_works', 'expected_results')
        }),
    )
