from django.db import models
from users.models import CustomUser
from products.models import Product


class Cart(models.Model):
    """"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Cart'

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    """"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.Product.name} - {self.quantity}'


class Order(models.Model):
    """"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.name} - {self.status}'


class OrderItem(models.Model):
    """"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.Product.name} - {self.quantity} for order {self.order.id}'
