"""
URL configuration for solutions app - template views.
"""

from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    path('', views.solutions_page, name='solutions'),
    path('<str:industry>/', views.solution_detail_page, name='solution-detail'),
]
