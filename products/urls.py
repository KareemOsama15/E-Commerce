from django.urls import path
from .views import (ProductCreateApiView,
                    ProductUpdateDestroyApiView,
                    ProductRetrieveApiView,
                    ProductListApiView,
                    CouponCreateApiView,
                    CouponUpdateDeleteApiView,
                    CategoryCreateApiView,
                    CategoryUpdateDeleteApiView,
                    CategorySearchApiView,
                    CategoryListApiView
                    )

urlpatterns = [
     # Product urls
     path('product/create/', ProductCreateApiView.as_view(), name='create-product'),
     path('product/<int:pk>/update/', ProductUpdateDestroyApiView.as_view(),
          name='update-product'),
     path('product/<int:pk>/delete/', ProductUpdateDestroyApiView.as_view(),
          name='delete-product'),
     path('product/<int:pk>/', ProductRetrieveApiView.as_view(),
          name='retrieve-product'),
     path('products/', ProductListApiView.as_view(),
         name='list-products'),

     # Category urls
     path('category/', CategoryCreateApiView.as_view(), name='create-category'),
     path('category/<int:pk>/', CategorySearchApiView.as_view(),
          name='search-category'),
     path('categories/', CategoryListApiView.as_view(), name='list-categories'),
     path('category/<int:pk>/update/', CategoryUpdateDeleteApiView.as_view(),
          name='update-category'),
     path('category/<int:pk>/delete/', CategoryUpdateDeleteApiView.as_view(),
          name='delete-category'),

     # Coupon URLs
     path('coupon/', CouponCreateApiView.as_view(), name='create-coupon'),
     path('coupon/<int:pk>/update/', CouponUpdateDeleteApiView.as_view(),
          name='update-coupon-'),
     path('coupon/<int:pk>/delete/', CouponUpdateDeleteApiView.as_view(),
          name='delete-coupon-'),
]
