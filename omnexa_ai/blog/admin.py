"""
Admin configuration for blog app.
"""

from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'views_count', 'published_at']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    date_hierarchy = 'published_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'author', 'is_published', 'published_at')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
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

    class Media:
        js = (
            'https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js',
            'js/admin_ckeditor.js',
        )

