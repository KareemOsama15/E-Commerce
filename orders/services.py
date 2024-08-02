from django.shortcuts import get_object_or_404
from products.models import Product
from django.core.cache import cache
from .models import Order, Cart, CartItem, OrderItem
from django.core.exceptions import ValidationError


class OrderServices():
    """
    Order service class
    """
    @staticmethod
    def create_order(user):
        """
        method creates new order and add user cart items to order items
        """
        cart, created = Cart.objects.get_or_create(user=user)
        cartItems = cart.items.all()

        if not cartItems.exists():
            raise ValidationError("Cart is empty, please add items to your cart first")

        order = Order.objects.create(user=user, total_price=cart.get_total_price)
        for item in cartItems:
            product = item.product
            OrderItem.objects.create(order=order, product=product, quantity=item.quantity)
            product.stock -= item.quantity
            product.save()
        cart.items.all().delete()
        return order

    @staticmethod
    def get_cached_orders_list(user):
        """
        Method returns cached products list
        """
        orders = cache.get('orders')
        if not orders:
            orders = Order.objects.filter(user=user)
            cache.set('orders', orders, timeout=60*15)
        return orders

    @staticmethod
    def get_cached_order_retrieve(user, pk):
        """
        Method returns cached product detail
        """
        cache_key = f'order_{pk}'
        order = cache.get(cache_key)
        if not order:
            order = get_object_or_404(Order, pk=pk, user=user)
            cache.set(cache_key, order, timeout=60*15)
        return order


class CartServices():
    """
    CartServices class that manages Cart and CartItem operations
    """
    @staticmethod
    def validate_quantity(quantity, product_id):
        """ Method checks product available quantity in stock """
        product = get_object_or_404(Product, id=product_id)
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0")
        elif quantity > product.stock:
            raise ValidationError(f"Not enough stock for {product.name}")

    @staticmethod
    def get_cart_object(user):
        """
        Method returns cart object
        """
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get_cartItem_object(user, item_id):
        """
        Method returns cart item object
        """
        cart = get_object_or_404(Cart, user=user)
        cartItem = get_object_or_404(CartItem, cart=cart, pk=item_id)
        return cartItem

    @staticmethod
    def addCartItems(requset):
        """
        Method adds new items to user cart
        """
        user = requset.user
        product_id = requset.data.get('product_id')
        quantity = int(requset.data.get('quantity'))

        # validate quantity before creating or getting Cart, CartItem
        # , because if they created and then we checked quantity
        # , it will be saved as item even it is not validated with product stock
        CartServices.validate_quantity(quantity, product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cartItem, created = CartItem.objects.get_or_create(cart=cart,
                                                           product_id=product_id)
        if created:
            cartItem.quantity = quantity
        else:
            cartItem.quantity += quantity
            # validate quantity here in case of user wants to add more quantity to same product
            CartServices.validate_quantity(cartItem.quantity, product_id)
        cartItem.save()
        return cartItem
