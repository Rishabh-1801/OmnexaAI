"""
URL configuration for services app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'services_api'

urlpatterns = [
    path('', views.ServiceListAPIView.as_view(), name='service-list'),
    path('<slug:slug>/', views.ServiceDetailAPIView.as_view(), name='service-detail'),
]
