"""
Serializers for services app.
"""

from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'tagline', 'icon_class',
            'problem', 'ai_solution', 'what_we_do',
            'process', 'result', 'order', 'is_active'
        ]


class ServiceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for service listing cards."""
    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'tagline', 'icon_class', 'order']
