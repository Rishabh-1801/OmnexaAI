"""
Utility functions for OMNEXA AI project.
"""

import re
from django.core.mail import send_mail
from django.conf import settings


def get_client_ip(request):
    """
    Extract real IP address from request, accounting for proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def sanitize_phone_number(phone):
    """
    Sanitize phone number by keeping only digits and +.
    """
    return re.sub(r'[^\d+]', '', phone)


def validate_phone_number(phone):
    """
    Validate phone number - must be at least 10 digits.
    """
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 10


import threading

def send_mail_async(subject, message, from_email, recipient_list, fail_silently=True):
    """
    Send email asynchronously using a background thread to prevent SMTP connection timeouts
    from blocking the main request-response cycle.
    """
    thread = threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list),
        kwargs={'fail_silently': fail_silently}
    )
    thread.start()


def send_admin_email(subject, message, recipient_list=None):
    """
    Send email to admin(s) asynchronously.
    """
    if recipient_list is None:
        recipient_list = [settings.ADMIN_EMAIL]

    send_mail_async(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True,
    )


def send_user_email(subject, message, recipient_email):
    """
    Send email to a user asynchronously.
    """
    send_mail_async(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=True,
    )


def truncate_words(text, num_words):
    """
    Truncate text to a specified number of words.
    """
    words = text.split()
    if len(words) <= num_words:
        return text
    return ' '.join(words[:num_words]) + '...'


def generate_slug(text):
    """
    Generate a URL-friendly slug from text.
    """
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')
