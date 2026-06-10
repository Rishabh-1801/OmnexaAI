"""
URL configuration for about app - template views.
"""

from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.about_page, name='about'),
    path('team/<slug:slug>/', views.team_member_detail, name='team-member-detail'),
]
