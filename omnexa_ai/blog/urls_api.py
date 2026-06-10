"""
URL configuration for blog app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'blog_api'

urlpatterns = [
    path('', views.BlogListAPIView.as_view(), name='blog-list'),
    path('<slug:slug>/', views.BlogDetailAPIView.as_view(), name='blog-detail'),
]
