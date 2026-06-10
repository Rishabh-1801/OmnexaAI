"""
URL configuration for home app - template views.
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home'),
]
