"""
URL configuration for case_studies app - template views.
"""

from django.urls import path
from . import views

app_name = 'case_studies'

urlpatterns = [
    path('', views.case_studies_page, name='case-studies'),
    path('<slug:slug>/', views.case_study_detail_page, name='case-study-detail'),
]
