from django.db import models
from users.models import CustomUser
from products.models import Product, Coupon


class Cart(models.Model):
    """
    Cart model class
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Cart'

    @property
    def get_total_price(self):
        """
        Method return total price for all products
        """
        totalPrice = 0
        products = self.items.all()

        for productItem in products:
            productPrice = productItem.product.price

            coupon = Coupon.objects.filter(product=productItem.product).first()
            if coupon:
                discount = (productPrice * coupon.discount) / 100
                productPrice -= discount

            totalPrice += productPrice * productItem.quantity
        return totalPrice


class CartItem(models.Model):
    """
    CartItem model class
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.product.name} - {self.quantity}'


class Order(models.Model):
    """
    Order model class
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.status}'


class OrderItem(models.Model):
    """
    OrderItem model class
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.Product.name} - {self.quantity} for order {self.order.id}'
