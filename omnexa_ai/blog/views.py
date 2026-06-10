"""
Views for blog app - listing with category filtering, pagination, and view count tracking.
"""

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer


# --- Template Views (SSR) ---
def blog_list(request):
    """
    Renders blog.html.
    Supports ?category= filter from the category tab buttons.
    """
    category = request.GET.get('category', None)
    posts = BlogPost.objects.filter(is_published=True)

    if category:
        posts = posts.filter(category=category)

    posts = posts.order_by('-published_at')

    # Recent posts for sidebar
    recent_posts = BlogPost.objects.filter(
        is_published=True
    ).order_by('-published_at')[:5]

    return render(request, 'blog.html', {
        'posts': posts,
        'recent_posts': recent_posts,
        'active_category': category,
        'categories': BlogPost._meta.get_field('category').choices,
    })


def blog_detail(request, slug):
    """
    Individual blog post page.
    Increments view count on every visit.
    """
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.increment_views()

    # Related posts (same category, exclude current)
    related = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id).order_by('-published_at')[:3]

    return render(request, 'blog_detail.html', {
        'post': post,
        'related_posts': related,
    })


# --- REST API Views ---
class BlogListAPIView(ListAPIView):
    """
    GET /api/v1/blog/?category=aeo
    List all published blog posts. Supports ?category= and ?search= filters.
    """
    serializer_class = BlogPostListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'excerpt']

    def get_queryset(self):
        qs = BlogPost.objects.filter(is_published=True).order_by('-published_at')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


class BlogDetailAPIView(RetrieveAPIView):
    """
    GET /api/v1/blog/<slug>/
    Single blog post detail.
    """
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'
