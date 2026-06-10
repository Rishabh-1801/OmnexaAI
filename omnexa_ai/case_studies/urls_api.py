"""
URL configuration for case_studies app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'case_studies_api'

urlpatterns = [
    path('', views.CaseStudyListAPIView.as_view(), name='case-study-list'),
    path('<slug:slug>/', views.CaseStudyDetailAPIView.as_view(), name='case-study-detail'),
]
