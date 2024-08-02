from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import CartItem
from .serializers import (CartItemSerializer,
                          CartSerializer,
                          OrderSerializer)
from .services import OrderServices, CartServices
from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied


class OrderCreateApiView(generics.CreateAPIView):
    """
    API view to create an order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            order = OrderServices.create_order(request.user)
            serializer = self.get_serializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        except ValidationError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderRetrieveApiView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """"""
        user = self.request.user
        pk = self.kwargs.get('pk')
        order = OrderServices.get_cached_order_retrieve(user, pk)
        return order
        

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


class CartItemAddApiView(generics.CreateAPIView):
    """
    API view to add an item to the cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            cart_item = CartServices.addCartItems(request)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(cart_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartRetrieveApiView(generics.RetrieveAPIView):
    """
    API view to retrieve the user's cart.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CartServices.get_cart_object(self.request.user)


class CartItemRemoveApiView(generics.DestroyAPIView):
    """
    API view to remove an item from the cart.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CartServices.get_cartItem_object(self.request.user,
                                                self.kwargs.get('pk'))


class CartItemUpdateApiView(generics.UpdateAPIView):
    """
    API view to update the quantity of an item in the cart.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CartServices.get_cartItem_object(self.request.user,
                                                self.kwargs.get('pk'))

    def patch(self, request, *args, **kwargs):
        product_id = self.get_object().product.id
        try:
            CartServices.validate_quantity(request.data['quantity'], product_id)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return self.partial_update(request, *args, **kwargs)
