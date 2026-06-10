"""
URL configuration for careers app - template views.
"""

from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.careers_page, name='careers'),
    path('job/<slug:slug>/', views.job_detail_page, name='job-detail'),
]
