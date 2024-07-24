from rest_framework import serializers
from .models import Category, Product, Coupon


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer class
    """
    id = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'description', 
                  'price',
                  'stock',
                  'image',
                  'categories',
                  'discount'
                  ]

    def get_id(self, obj):
        """ Return object id """
        return obj.id

    def get_categories(self, obj):
        """ Return categories related to that object """
        return [category.name for category in obj.categories.all()]

    def get_discount(self, obj):
        """ Return if there any coupon available to that object """
        coupon = Coupon.objects.filter(product=obj).first()
        return coupon.discount if coupon else None

class CouponSerializer(serializers.ModelSerializer):
    """
    Coupon serializer class
    """
    id = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount', 'product_id']

    def validate(self, attrs):
        """ Validta discount field value """
        discount = attrs.get('discount', '')
        if not (0 <= discount <= 100):
            raise serializers.ValidationError("Discount must be between 0 and 100.")
        return attrs

    def get_id(self, obj):
        return obj.id


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer class
    """
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name']

    def get_id(self, obj):
        """ Return object id """
        return obj.id