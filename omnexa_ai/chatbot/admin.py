"""
Admin configuration for chatbot app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ChatSession, ChatMessage, ChatbotKnowledgeBase, ChatbotAnalytics


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'page_url', 'ip_address', 'message_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['session_key', 'page_url', 'ip_address']
    readonly_fields = ['session_key', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Session Info', {
            'fields': ('session_key', 'page_url', 'user_agent', 'ip_address', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'is_read', 'created_at']
    list_filter = ['role', 'is_read', 'created_at']
    search_fields = ['content', 'session__session_key']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'

    fieldsets = (
        ('Message Info', {
            'fields': ('session', 'role', 'content', 'is_read')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


@admin.register(ChatbotKnowledgeBase)
class ChatbotKnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'priority', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer', 'keywords']
    list_editable = ['priority', 'is_active']
    ordering = ['-priority', 'created_at']

    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'

    fieldsets = (
        ('Basic Info', {
            'fields': ('question', 'answer', 'category', 'priority', 'is_active')
        }),
        ('Keywords', {
            'fields': ('keywords',)
        }),
    )


@admin.register(ChatbotAnalytics)
class ChatbotAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sessions', 'total_messages', 'unique_users', 'avg_session_duration']
    list_filter = ['date']
    readonly_fields = ['date', 'total_sessions', 'total_messages', 'unique_users', 'avg_session_duration']
    ordering = ['-date']

    fieldsets = (
        ('Analytics Info', {
            'fields': ('date', 'total_sessions', 'total_messages', 'unique_users', 'avg_session_duration')
        }),
        ('Conversation Stats', {
            'fields': ('successful_conversations', 'failed_conversations')
        }),
    )

    def has_add_permission(self, request):
        # Prevent manual creation - analytics are auto-generated
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of analytics
        return False
