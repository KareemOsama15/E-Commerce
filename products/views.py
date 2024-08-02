from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     UpdateAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView)
from .serializers import CategorySerializer, ProductSerializer, CouponSerializer
from .services import ProductAppServices
from .models import Product, Coupon, Category


class ProductCreateApiView(CreateAPIView):
    """
    Api view to craete a new product by admin user
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        product = serializer.save(user=self.request.user)
        ProductAppServices.create_product_categories(product,
                                          self.request.data)


class ProductUpdateDestroyApiView(UpdateAPIView, DestroyAPIView):
    """
    Api view to update a product by admin user
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)

    def perform_update(self, serializer):
        product = serializer.save()
        ProductAppServices.update_product_categories(product, self.request.data)


class ProductRetrieveApiView(RetrieveAPIView):
    """
    Api view to retrieve specific product details
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        product_id = self.kwargs.get('pk')
        product = ProductAppServices.get_cached_product_detail(product_id)
        return product


class ProductListApiView(ListAPIView):
    """
    Api view to list all products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        products = ProductAppServices.get_cached_products_list()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CouponCreateApiView(CreateAPIView):
    """
    Api view to create a coupon for existing product
    """
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        product = ProductAppServices.get_coupon_product(self.request.data)
        serializer.save(product=product)

class CouponUpdateDeleteApiView(UpdateAPIView, DestroyAPIView):
    """
    Api view to delete or update a coupon
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)


class CategoryCreateApiView(CreateAPIView):
    """
    Api view to create a category
    """
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class CategoryUpdateDeleteApiView(UpdateAPIView, DestroyAPIView):
    """
    Api view to update or delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)

class CategoryListApiView(ListAPIView):
    """
    Api view to list all categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CategorySearchApiView(ListAPIView):
    """
    Api view to search on products by category
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        products = ProductAppServices.search_by_category(kwargs.get('pk'))
        product_data = self.serializer_class(products, many=True).data
        return Response({'products': product_data}, status=status.HTTP_200_OK)
