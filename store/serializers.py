from django.db import transaction
from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product"""
    class Meta:
        model = Product
        fields = ('url', 'id', 'name', 'description', 'manufacturer')


class AttributeSerializerForAttributeType(serializers.ModelSerializer):
    """Serializer for Attribute under AttributeType"""
    class Meta:
        model = Attribute
        fields = ('id', 'name', 'description')


class AttributeTypeSerializer(serializers.ModelSerializer):
    """Serializer for AttributeType"""
    attribute_set = AttributeSerializerForAttributeType(
        many=True, read_only=True)

    class Meta:
        model = AttributeType
        fields = ('id', 'name', 'description', 'attribute_set')


class AttributeSerializer(serializers.ModelSerializer):
    """Serializer for Attribute"""
    type = AttributeTypeSerializer()

    class Meta:
        model = Attribute
        fields = ('id', 'name', 'type', 'description')


class AttributeTypeSerializerForSKU(serializers.ModelSerializer):
    """Serializer for AttributeType under SKU"""
    class Meta:
        model = AttributeType
        fields = ('id', 'name',)


class SKUSerializer(serializers.ModelSerializer):
    """Serializer for SKU"""
    product = ProductSerializer()
    attributes = AttributeTypeSerializerForSKU(read_only=True, many=True)

    class Meta:
        model = SKU
        fields = ('url', 'id', 'number', 'product', 'price', 'currency',
                  'attributes')


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address"""
    class Meta:
        model = Address
        fields = ('id', 'country', 'street', 'city', 'state', 'postal_code')


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact"""
    class Meta:
        model = Contact
        fields = ('id', 'full_name', 'email')


class OrderLineSerializer(serializers.ModelSerializer):
    """Serializer for OrderLine"""
    class Meta:
        model = OrderLine
        fields = ('id', 'sku', 'price', 'currency', 'quantity', 'ordering',)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    ship_to = AddressSerializer(required=True)
    bill_to = AddressSerializer(required=True)
    contact = ContactSerializer(required=True)
    order_line_set = OrderLineSerializer(required=True, many=True)

    class Meta:
        model = Order
        fields = (
            'id', 'status', 'ship_to', 'bill_to', 'contact', 'order_line_set')

    @transaction.atomic  # Run in single Database transaction
    def create(self, validated_data):
        """
        Validate and create order instance.
        """

        # Pop related data
        ship_to_data = validated_data.pop('ship_to')
        bill_to_data = validated_data.pop('bill_to')
        contact_data = validated_data.pop('contact')
        order_lines_data = validated_data.pop('order_line_set')

        # Create FK instances
        ship_to = AddressSerializer.create(
            AddressSerializer(), validated_data=ship_to_data)
        bill_to = AddressSerializer.create(
            AddressSerializer(), validated_data=bill_to_data)
        contact = ContactSerializer.create(
            ContactSerializer(), validated_data=contact_data
        )

        # Create order
        order, created = Order.objects.update_or_create(
            ship_to=ship_to, bill_to=bill_to, contact=contact,
            **validated_data)

        # Create Reverse related OrderLines
        for order_line_data in order_lines_data:
            order_line_data['order'] = order
            order_line = OrderLineSerializer.create(
                OrderLineSerializer(),
                validated_data=order_line_data)

            # Update the available quantity for this SKU
            order_line.sku.quantity = (
                order_line.sku.quantity - order_line.quantity)
            order_line.sku.save()

        return order
