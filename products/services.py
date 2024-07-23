from .models import Product, Coupon, Category
from django.shortcuts import get_object_or_404

class ProductAppServices():
    """"""
    @staticmethod
    def get_categories_ids(data):
        """"""
        category_ids = data['categories']
        category_list = []
        for id in category_ids:
            category = get_object_or_404(Category, pk=id)
            category_list.append(category)
        return category_list

    @staticmethod
    def create_product(serializer, categories, user):
        """"""
        product = serializer.save(user=user)
        product.categories.set(categories)
        return product

    @staticmethod
    def create_coupon(data):
        """"""
        product_id = data['product_id']
        product = get_object_or_404(Product, pk=product_id)
        return product

    @staticmethod
    def search_by_category(category_id):
        """"""
        category = get_object_or_404(Category, pk=category_id)
        products = category.products.all()
        return products