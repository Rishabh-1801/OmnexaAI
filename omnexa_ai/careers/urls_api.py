"""
URL configuration for careers app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'careers_api'

urlpatterns = [
    path('', views.CareersPageContentAPIView.as_view(), name='careers-content'),
    path('jobs/', views.JobOpeningListAPIView.as_view(), name='job-list'),
    path('jobs/<slug:slug>/', views.JobOpeningDetailAPIView.as_view(), name='job-detail'),
    path('apply/', views.JobApplicationCreateAPIView.as_view(), name='job-apply'),
    path('benefits/', views.CompanyBenefitListAPIView.as_view(), name='benefits-list'),
    path('categories/', views.JobCategoriesAPIView.as_view(), name='job-categories'),
    path('job-types/', views.JobTypesAPIView.as_view(), name='job-types'),
    path('experience-levels/', views.ExperienceLevelsAPIView.as_view(), name='experience-levels'),
]
