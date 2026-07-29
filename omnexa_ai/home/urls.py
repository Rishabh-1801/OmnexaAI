"""
URL configuration for home app - template views.
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('enter-password/', views.enter_password, name='enter_password'),
    path('exit-password/', views.exit_password, name='exit_password'),
]
