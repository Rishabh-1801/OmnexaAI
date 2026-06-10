"""
Models for chatbot app.
"""

from django.db import models
from omnexa_ai.core.models import TimeStampedModel


class ChatSession(TimeStampedModel):
    """
    Stores chatbot sessions from the floating widget on all pages.
    """
    session_key = models.CharField(max_length=100, unique=True)
    page_url = models.URLField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'

    def __str__(self):
        return f"Chat {self.session_key} — {self.created_at.date()}"

    @property
    def message_count(self):
        return self.messages.count()


class ChatMessage(TimeStampedModel):
    """
    Individual messages within a chat session.
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'

    def __str__(self):
        return f"[{self.role}] {self.content[:60]}"


class ChatbotKnowledgeBase(TimeStampedModel):
    """
    Knowledge base for chatbot responses.
    Can be used for rule-based responses or training data.
    """
    question = models.CharField(max_length=500, help_text="User question or keyword")
    answer = models.TextField(help_text="Bot response")
    keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated keywords for matching"
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category for organizing responses"
    )
    priority = models.PositiveIntegerField(default=0, help_text="Higher priority matches first")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-priority', 'created_at']
        verbose_name = 'Chatbot Knowledge Base'
        verbose_name_plural = 'Chatbot Knowledge Base'

    def __str__(self):
        return f"{self.question[:50]}..."


class ChatbotAnalytics(TimeStampedModel):
    """
    Analytics for chatbot usage.
    """
    date = models.DateField(unique=True)
    total_sessions = models.PositiveIntegerField(default=0)
    total_messages = models.PositiveIntegerField(default=0)
    unique_users = models.PositiveIntegerField(default=0)
    avg_session_duration = models.FloatField(default=0, help_text="Average session duration in seconds")
    successful_conversations = models.PositiveIntegerField(default=0)
    failed_conversations = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Chatbot Analytics'
        verbose_name_plural = 'Chatbot Analytics'

    def __str__(self):
        return f"Analytics for {self.date}"
