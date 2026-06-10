"""
URL configuration for chatbot app.
"""

from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Chat endpoints
    path('message/', views.chat_message, name='chat-message'),
    path('history/', views.chat_history, name='chat-history'),
    path('clear/', views.clear_chat, name='clear-chat'),

    # REST API endpoints
    path('sessions/', views.ChatSessionListAPIView.as_view(), name='session-list'),
    path('sessions/<str:session_key>/', views.ChatSessionDetailAPIView.as_view(), name='session-detail'),
    path('knowledge/', views.ChatbotKnowledgeBaseListAPIView.as_view(), name='knowledge-list'),
    path('analytics/', views.ChatbotAnalyticsAPIView.as_view(), name='analytics'),
]
