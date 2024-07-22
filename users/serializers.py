from rest_framework import serializers
from .models import CustomUser


class UserSerializerSignUp(serializers.ModelSerializer):
    """Sign-up serializer class"""
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializerInfo(serializers.ModelSerializer):
    """Represent inforamation about system users"""
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'email', 'date_joined','last_login', 'is_superuser']