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
    image = models.ImageField(null=True, blank=True, upload_to='product_images/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Coupon(models.Model):
    """"""
    code = models.CharField(max_length=25)
    discount = models.PositiveSmallIntegerField(help_text="Discount percentage (0-100).",
                                                default=0)
    product = models.OneToOneField(Product, on_delete=models.CASCADE,
                                  related_name='coupon')

    def __str__(self) -> str:
        return self.code