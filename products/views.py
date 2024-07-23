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
    """"""
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        categories = ProductAppServices.get_categories_ids(self.request.data)
        ProductAppServices.create_product(serializer, categories, self.request.user)
        


class ProductUpdateDestroyApiView(UpdateAPIView, DestroyAPIView):
    """"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)


class ProductListRetrieveApiView(RetrieveAPIView, ListAPIView):
    """"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class CouponCreateApiView(CreateAPIView):
    """"""
    serializer_class = CouponSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        product = ProductAppServices.create_coupon(self.request.data)
        serializer.save(product=product)

class CouponUpdateDeleteApiView(UpdateAPIView, DestroyAPIView):
    """"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)


class CategoryCreateApiView(CreateAPIView):
    """"""
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class CategoryUpdateDeleteApiView(UpdateAPIView, DestroyAPIView):
    """"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)

class CategoryListApiView(ListAPIView):
    """"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CategorySearchApiView(ListAPIView):
    """"""
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        products = ProductAppServices.search_by_category(kwargs.get('pk'))
        product_data = self.serializer_class(products, many=True).data       
        return Response({'products': product_data}, status=status.HTTP_200_OK)
