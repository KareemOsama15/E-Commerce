from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    CartItem serializer class
    """
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer class
    """
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created', 'updated']


class OrderItemSerializer(serializers.ModelSerializer):
    """
    OrderItem serializer class
    """
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer class
    """
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status', 'created']