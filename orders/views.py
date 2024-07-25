from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .serializers import (CartItemSerializer,
                          CartSerializer,
                          OrderItemSerializer,
                          OrderSerializer)
from django.shortcuts import get_object_or_404
from .services import OrderServices


# order >> create, retrieve, list,
# cart >> retrieve, create, delete, update
class OrderCreateApiView(generics.CreateAPIView):
    """
    API view to create an order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)

        order = Order.objects.create(user=user, total_price=cart.get_total_price())

        for item in cart.items.all():
            product = item.product
            OrderItem.objects.create(order=order, product=product, quantity=item.quantity)
        cart.items.all().delete()

        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderRetrieveApiView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class OrderListApiView(generics.ListAPIView):
    """
    API view to list all orders of the user.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        orders = OrderServices.get_cached_orders_list(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartRetrieveApiView(generics.RetrieveAPIView):
    """
    API view to retrieve the user's cart.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart


class CartItemAddApiView(generics.CreateAPIView):
    """
    API view to add an item to the cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        # check product quantity in stock
        print(f'first quantity = {quantity}')
        response = OrderServices.check_product_quantity(quantity, product_id)
        if response:
            return response

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
            # check the updated quantity in stock
            print(f'updated quantity = {cart_item.quantity}')
            response = OrderServices.check_product_quantity(cart_item.quantity, product_id)
            if response:
                return response
        cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class CartItemRemoveApiView(generics.DestroyAPIView):
    """
    API view to remove an item from the cart.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart = get_object_or_404(Cart, user=user)
        item_id = self.kwargs['pk']
        return get_object_or_404(CartItem, cart=cart, pk=item_id)


class CartItemUpdateApiView(generics.UpdateAPIView):
    """
    API view to update the quantity of an item in the cart.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart = get_object_or_404(Cart, user=user)
        item_id = self.kwargs['pk']
        return get_object_or_404(CartItem, cart=cart, pk=item_id)
