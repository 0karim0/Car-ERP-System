"""
Vehicle serializers for Car ERP System.
"""
from rest_framework import serializers
from .models import Vehicle, VehicleDocument, VehiclePhoto, VehicleHistory
from customers.serializers import CustomerSerializer
from authentication.serializers import UserSerializer


class VehicleSerializer(serializers.ModelSerializer):
    """
    Vehicle serializer.
    """
    full_description = serializers.ReadOnlyField()
    customer_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class VehicleDocumentSerializer(serializers.ModelSerializer):
    """
    Vehicle document serializer.
    """
    vehicle_description = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VehicleDocument
        fields = '__all__'
        read_only_fields = ['uploaded_at']
    
    def get_vehicle_description(self, obj):
        return obj.vehicle.full_description
    
    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name()
        return None


class VehiclePhotoSerializer(serializers.ModelSerializer):
    """
    Vehicle photo serializer.
    """
    vehicle_description = serializers.SerializerMethodField()
    taken_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VehiclePhoto
        fields = '__all__'
        read_only_fields = ['taken_at']
    
    def get_vehicle_description(self, obj):
        return obj.vehicle.full_description
    
    def get_taken_by_name(self, obj):
        if obj.taken_by:
            return obj.taken_by.get_full_name()
        return None


class VehicleHistorySerializer(serializers.ModelSerializer):
    """
    Vehicle history serializer.
    """
    vehicle_description = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VehicleHistory
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_vehicle_description(self, obj):
        return obj.vehicle.full_description
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class VehicleDetailSerializer(VehicleSerializer):
    """
    Detailed vehicle serializer with related data.
    """
    customer = CustomerSerializer(read_only=True)
    documents = VehicleDocumentSerializer(many=True, read_only=True)
    photos = VehiclePhotoSerializer(many=True, read_only=True)
    history = VehicleHistorySerializer(many=True, read_only=True)
    
    class Meta(VehicleSerializer.Meta):
        fields = VehicleSerializer.Meta.fields + ['customer', 'documents', 'photos', 'history']
