from .models import Product, Coupon, Category
from django.shortcuts import get_object_or_404
from django.core.cache import cache

class ProductAppServices():
    """
    Produc Services class
    """
    @staticmethod
    def get_categories_list(data):
        """
        Method return list of categories applied to product
        """
        category_ids = data['categories']
        category_list = []
        for id in category_ids:
            category = get_object_or_404(Category, pk=id)
            category_list.append(category)
        return category_list

    @staticmethod
    def create_product(serializer, categories, user):
        """
        Method creates a new product object
        """
        product = serializer.save(user=user)
        product.categories.set(categories)
        return product

    @staticmethod
    def get_coupon_product(data):
        """
        Method creates a new coupon 
        """
        product_id = data['product_id']
        product = get_object_or_404(Product, pk=product_id)
        return product

    @staticmethod
    def search_by_category(category_id):
        """
        Method get all procducts for one category
        """
        category = get_object_or_404(Category, pk=category_id)
        products = category.products.all()
        return products

    @staticmethod
    def get_cached_products_list():
        """
        Method returns cached products list
        """
        products = cache.get('products')
        if not products:
            products = Product.objects.all()
            cache.set('products', products, timeout=60*15)
        return products

    @staticmethod
    def get_cached_product_detail(id):
        """
        Method return cached product detail
        """
        product = cache.get(f'product_{id}')
        if not product:
            product = Product.objects.get(pk=id)
            cache.set(f'product_{id}', product, timeout=60*15)
        return product