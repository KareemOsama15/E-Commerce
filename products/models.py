from django.db import models
from users.models import CustomUser


class Category(models.Model):
    """"""
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=False, upload_to='product_images/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Coupon(models.Model):
    """"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='copoun')
    code = models.CharField(max_length='25')
    models.PositiveSmallIntegerField(help_text="Discount percentage (0-100).")

    def __str__(self) -> str:
        return f'{self.code} - {self.product}'