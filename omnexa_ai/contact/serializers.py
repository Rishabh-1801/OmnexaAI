"""
Serializers for contact app.
"""

from rest_framework import serializers
from .models import ConsultationBooking, NewsletterSubscriber


class ConsultationBookingSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, allow_null=True)

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

    def validate_website(self, value):
        """Clean and validate website URL."""
        if not value:
            return ''
        
        value = value.strip()
        # Clean placeholders like N/A, None, etc.
        if value.lower() in ['n/a', 'na', 'none', 'no', 'nil', 'null']:
            return ''
            
        # Prepend https:// if it does not have a protocol scheme
        import re
        if not re.match(r'^https?://', value, re.IGNORECASE):
            value = 'https://' + value
            
        # Validate it using Django's URLValidator
        from django.core.validators import URLValidator
        from django.core.exceptions import ValidationError
        val = URLValidator()
        try:
            val(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid URL.")
            
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
