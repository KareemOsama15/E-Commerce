from django.shortcuts import get_object_or_404
from products.models import Product
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Order


class OrderServices():
    """
    Order service class
    """
    @staticmethod
    def check_product_quantity(quantity, product_id):
        """ Method checks product available quantity in stock """
        product = get_object_or_404(Product, id=product_id)
        print(f'product = {product}, quant = {quantity}, stock = {product.stock}')
        if quantity > product.stock:
                print('quantit bigger than stock')
                return Response(
                    {
                        'error': f"Not enough stock for {product.name}. Available: {product.stock}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return None

    @staticmethod
    def get_cached_orders_list(user):
        """
        Method returns cached products list
        """
        orders = cache.get('orders')
        if not orders:
            print("orders not cached yet")
            orders = Order.objects.filter(user=user)
            cache.set('orders', orders, timeout=60*15)
        print("orders retrieved from redis")
        return orders