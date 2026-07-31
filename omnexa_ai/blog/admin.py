"""
Admin configuration for blog app.
"""

from django.contrib import admin
from django.utils import timezone
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'views_count', 'published_at']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    date_hierarchy = 'published_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'author', 'is_published', 'published_at')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),

        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('Stats', {
            'fields': ('views_count',),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Auto-set published_at to now if is_published is True but published_at is blank.
        This ensures blog posts always appear on the frontend after ticking is_published.
        """
        if obj.is_published and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """
        Also handle bulk is_published toggle from list_editable.
        """
        super().save_related(request, form, formsets, change)

    class Media:
        js = (
            'https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js',
            'js/admin_ckeditor.js',
        )
