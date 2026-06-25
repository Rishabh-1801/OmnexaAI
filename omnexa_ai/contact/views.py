"""
Views for contact app - lead capture and consultation booking.
"""

from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import ConsultationBooking, NewsletterSubscriber
from .serializers import ConsultationBookingSerializer, NewsletterSerializer
from omnexa_ai.core.utils import get_client_ip, send_mail_async
 
 
class ConsultationBookingCreateView(APIView):
    """
    POST /api/v1/contact/book/

    Handles form submission from contact.html.
    Steps:
      1. Validate form data with serializer
      2. Save lead to database
      3. Capture UTM params and IP from request
      4. Send confirmation email to the lead
      5. Send notification email to OMNEXA AI admin
      6. Return success JSON response
    """

    def post(self, request):
        serializer = ConsultationBookingSerializer(data=request.data)

        if serializer.is_valid():
            # Save lead with metadata
            booking = serializer.save(
                ip_address=get_client_ip(request),
                referrer_url=request.META.get('HTTP_REFERER', ''),
                utm_source=request.data.get('utm_source', ''),
                utm_medium=request.data.get('utm_medium', ''),
                utm_campaign=request.data.get('utm_campaign', ''),
            )

            # Send confirmation email to lead
            send_mail_async(
                subject="✅ Your Free AI Strategy Consultation is Booked — OMNEXA AI",
                message=f"""
Hi {booking.name},

Thank you for booking a free AI strategy consultation with OMNEXA AI!

Here's what happens next:
1. Our team will review your business within 24 hours
2. We'll prepare a custom AI growth plan for {booking.business_name}
3. We'll reach out to schedule your consultation call
4. You'll receive your personalized AI strategy

We're excited to show you how AI can transform your business!

Best,
OMNEXA AI Team
📍 210, Sarthak Pulse Mall, Gandhinagar
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=True,
            )

            # Notify admin
            send_mail_async(
                subject=f"🔥 New Lead: {booking.name} — {booking.business_name}",
                message=f"""
New consultation booking received!

Name: {booking.name}
Business: {booking.business_name}
Phone: {booking.phone}
Email: {booking.email}
Website: {booking.website or 'N/A'}
Service: {booking.get_service_interested_display()}
Message: {booking.message or 'N/A'}

UTM Source: {booking.utm_source}
Referrer: {booking.referrer_url}
IP: {booking.ip_address}

Login to admin to view: https://omnexa.ai/admin/contact/consultationbooking/{booking.id}/
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            return Response(
                {
                    "success": True,
                    "message": "Booking confirmed! We'll contact you within 24 hours.",
                    "booking_id": booking.id,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class NewsletterSubscribeView(APIView):
    """
    POST /api/v1/contact/newsletter/

    Handles newsletter signups from blog sidebar, footer, hero CTA.
    """

    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=serializer.validated_data['email'],
                defaults={
                    'name': serializer.validated_data.get('name', ''),
                    'source': request.data.get('source', 'unknown'),
                }
            )
            if created:
                return Response(
                    {"success": True, "message": "Subscribed successfully!"},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"success": True, "message": "You're already subscribed!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


# Template Views
def contact_page(request):
    """Renders contact.html."""
    return render(request, 'contact.html')
