"""
Serializers for contact app.
"""

from rest_framework import serializers
from .models import ConsultationBooking, NewsletterSubscriber


class ConsultationBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBooking
        fields = [
            'name', 'business_name', 'phone', 'email',
            'website', 'service_interested', 'message'
        ]
        extra_kwargs = {
            'name': {'required': True},
            'business_name': {'required': True},
            'phone': {'required': True},
            'email': {'required': True},
            'website': {'required': False},
            'message': {'required': False},
        }

    def validate_phone(self, value):
        """Basic phone validation — must be at least 10 digits."""
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 10:
            raise serializers.ValidationError(
                "Please enter a valid phone number with at least 10 digits."
            )
        return value


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']


class ConsultationBookingDetailSerializer(serializers.ModelSerializer):
    """Full serializer for admin use."""
    service_display = serializers.CharField(
        source='get_service_interested_display', read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = ConsultationBooking
        fields = '__all__'
