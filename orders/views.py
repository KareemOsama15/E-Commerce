from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (CartItemSerializer,
                          CartSerializer,
                          OrderItemSerializer,
                          OrderSerializer)
from django.shortcuts import get_object_or_404


# order >> create, retrieve, list,
# cart >> retrieve, create, delete, update
class OrderCreateApiView(generics.CreateAPIView):
    """
    API view to create an order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        order = Order.objects.create(user=request.user, 
                                     total_price=cart.get_total_price())

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product,
                                     quantity=item.quantity)
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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


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
        quantity = int(request.data.get('quantity', 1))  # Ensure quantity is an integer
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
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
