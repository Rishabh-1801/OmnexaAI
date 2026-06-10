"""
Serializers for blog app.
"""

from rest_framework import serializers
from .models import BlogPost


class BlogPostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for blog listing cards."""
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'category', 'category_display',
            'excerpt', 'featured_image', 'published_at', 'views_count'
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Full serializer for single blog post page."""
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )
    author_name = serializers.CharField(
        source='author.get_full_name', read_only=True
    )

    class Meta:
        model = BlogPost
        fields = '__all__'
