"""
URL configuration for solutions app - API endpoints.
"""

from django.urls import path
from . import views

app_name = 'solutions_api'

urlpatterns = [
    path('', views.IndustrySolutionListAPIView.as_view(), name='solution-list'),
    path('<str:industry>/', views.IndustrySolutionDetailAPIView.as_view(), name='solution-detail'),
]
