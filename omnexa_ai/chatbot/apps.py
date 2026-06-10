"""
Chatbot app configuration.
"""

from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omnexa_ai.chatbot'
    verbose_name = 'Chatbot'
