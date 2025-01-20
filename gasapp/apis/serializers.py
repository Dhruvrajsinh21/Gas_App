from rest_framework import serializers
from .models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'customer', 'type_of_service', 'details', 'file', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer', 'status', 'created_at', 'updated_at']
