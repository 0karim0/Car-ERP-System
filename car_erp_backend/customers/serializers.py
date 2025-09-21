"""
Customer serializers for Car ERP System.
"""
from rest_framework import serializers
from .models import Customer, CustomerDocument, CustomerCommunication, Appointment
from authentication.serializers import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer serializer.
    """
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class CustomerDocumentSerializer(serializers.ModelSerializer):
    """
    Customer document serializer.
    """
    customer_name = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerDocument
        fields = '__all__'
        read_only_fields = ['uploaded_at']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name()
        return None


class CustomerCommunicationSerializer(serializers.ModelSerializer):
    """
    Customer communication serializer.
    """
    customer_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerCommunication
        fields = '__all__'
        read_only_fields = ['communication_date']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Appointment serializer.
    """
    customer_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    assigned_to_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None
    
    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name()
        return None


class CustomerDetailSerializer(CustomerSerializer):
    """
    Detailed customer serializer with related data.
    """
    documents = CustomerDocumentSerializer(many=True, read_only=True)
    communications = CustomerCommunicationSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    
    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields + ['documents', 'communications', 'appointments']

