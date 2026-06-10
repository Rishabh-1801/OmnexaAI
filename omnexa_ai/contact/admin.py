"""
Admin configuration for contact app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ConsultationBooking, NewsletterSubscriber


@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'business_name', 'phone', 'email',
        'service_interested', 'status', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'service_interested', 'created_at']
    search_fields = ['name', 'business_name', 'email', 'phone']
    readonly_fields = [
        'ip_address', 'referrer_url', 'utm_source', 'utm_medium',
        'utm_campaign', 'created_at', 'updated_at'
    ]
    list_editable = ['status']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Lead Info', {
            'fields': ('name', 'business_name', 'phone', 'email', 'website', 'service_interested', 'message')
        }),
        ('CRM', {
            'fields': ('status', 'is_consultation_scheduled', 'consultation_datetime', 'admin_notes')
        }),
        ('Tracking', {
            'fields': ('ip_address', 'referrer_url', 'utm_source', 'utm_medium', 'utm_campaign', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        """Show colored badge for lead status in list view."""
        colors = {
            'new': '#22C55E',
            'contacted': '#1A6DFF',
            'qualified': '#7B2FD4',
            'proposal_sent': '#FF6B00',
            'closed_won': '#16A34A',
            'closed_lost': '#DC2626',
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;'
            'border-radius:12px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'source', 'is_active', 'created_at']
    list_filter = ['is_active', 'source']
    search_fields = ['email', 'name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
