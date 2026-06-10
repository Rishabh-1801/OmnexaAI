"""
API URL configuration for home app.
"""

from django.urls import path
from . import views

app_name = 'home_api'

urlpatterns = [
    # Google Business Reviews
    path('google-reviews/', views.GoogleBusinessReviewsAPIView.as_view(), name='google-reviews'),
    path('google-reviews/config/', views.GoogleBusinessConfigAPIView.as_view(), name='google-reviews-config'),
    path('google-reviews/sync/', views.GoogleBusinessSyncAPIView.as_view(), name='google-reviews-sync'),
    path('google-reviews/testimonials/', views.GoogleBusinessTestimonialsAPIView.as_view(), name='google-reviews-testimonials'),
]
