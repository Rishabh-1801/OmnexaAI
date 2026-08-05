"""
URL configuration for contact app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'contact_api'

urlpatterns = [
    path('book/', views.ConsultationBookingCreateView.as_view(), name='booking-create'),
    path('newsletter/', views.NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('email-test/', views.EmailTestView.as_view(), name='email-test'),  # TEMP: debug only
]
