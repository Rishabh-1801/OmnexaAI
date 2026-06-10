"""
Serializers for chatbot app.
"""

from rest_framework import serializers
from .models import ChatSession, ChatMessage, ChatbotKnowledgeBase


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'is_read', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.ReadOnlyField()

    class Meta:
        model = ChatSession
        fields = [
            'id', 'session_key', 'page_url', 'user_agent',
            'ip_address', 'is_active', 'message_count',
            'created_at', 'updated_at'
        ]


class ChatSessionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new chat session."""
    class Meta:
        model = ChatSession
        fields = ['session_key', 'page_url', 'user_agent']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new chat message."""
    class Meta:
        model = ChatMessage
        fields = ['session', 'role', 'content']


class ChatbotKnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotKnowledgeBase
        fields = [
            'id', 'question', 'answer', 'keywords', 'category',
            'priority', 'is_active', 'created_at'
        ]


class ChatbotResponseSerializer(serializers.Serializer):
    """Serializer for chatbot response."""
    success = serializers.BooleanField()
    session_key = serializers.CharField()
    reply = serializers.CharField()
    message_id = serializers.IntegerField(required=False)
