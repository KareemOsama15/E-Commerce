from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    CartItem serializer class
    """
    name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'name', 'price', 'quantity']

    def get_name(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.price

class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer class
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'username', 'items', 'total_price', 'created', 'updated']

    def get_total_price(self, obj):
        return obj.get_total_price

    def get_username(self, obj):
        return obj.user.username


class OrderItemSerializer(serializers.ModelSerializer):
    """
    OrderItem serializer class
    """
    name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'name', 'price', 'quantity']

    def get_name(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.price


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer class
    """
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'items', 'total_price', 'status', 'created']

    def get_username(self, obj):
        return obj.user.username
