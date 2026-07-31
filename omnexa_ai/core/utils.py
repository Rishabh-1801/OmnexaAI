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
import logging

logger = logging.getLogger(__name__)

def _send_mail_in_thread(subject, message, from_email, recipient_list):
    """
    Internal wrapper to send mail inside a thread with error logging.
    Errors are logged but never raised (so the thread won't crash silently).
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
    except Exception as e:
        logger.error(f"EMAIL SEND FAILED to {recipient_list} | Subject: {subject} | Error: {type(e).__name__}: {e}")


def send_mail_async(subject, message, from_email, recipient_list, fail_silently=True):
    """
    Send email asynchronously using a background thread.
    Prevents SMTP timeouts from blocking the HTTP response (avoids 502 errors).
    Errors are logged to Render logs for debugging.
    """
    thread = threading.Thread(
        target=_send_mail_in_thread,
        args=(subject, message, from_email, recipient_list),
        daemon=True,
    )
    thread.start()
    logger.info(f"Email queued for async delivery to {recipient_list}")


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
