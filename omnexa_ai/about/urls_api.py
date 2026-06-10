"""
URL configuration for about app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'about_api'

urlpatterns = [
    path('', views.AboutPageContentAPIView.as_view(), name='about-content'),
    path('team/', views.TeamMemberListAPIView.as_view(), name='team-list'),
    path('team/<slug:slug>/', views.TeamMemberDetailAPIView.as_view(), name='team-detail'),
    path('values/', views.CompanyValueListAPIView.as_view(), name='values-list'),
    path('milestones/', views.CompanyMilestoneListAPIView.as_view(), name='milestones-list'),
    path('stats/', views.AboutStatsAPIView.as_view(), name='about-stats'),
]
