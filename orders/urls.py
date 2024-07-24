from django.urls import path
from .views import (OrderCreateApiView,
                    OrderRetrieveApiView,
                    OrderListApiView,
                    CartRetrieveApiView,
                    CartItemAddApiView,
                    CartItemRemoveApiView,
                    CartItemUpdateApiView)

urlpatterns = [
    # Order URLs
    path('orders/create/', OrderCreateApiView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderRetrieveApiView.as_view(), name='order-retrieve'),
    path('orders/', OrderListApiView.as_view(), name='order-list'),
    
    # Cart URLs
    path('cart/', CartRetrieveApiView.as_view(), name='cart-retrieve'),
    path('cart/add/', CartItemAddApiView.as_view(), name='cart-item-add'),
    path('cart/<int:pk>/delete/', CartItemRemoveApiView.as_view(), name='cart-item-remove'),
    path('cart/<int:pk>/update/', CartItemUpdateApiView.as_view(), name='cart-item-update'),
]
