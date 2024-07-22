from .models import CustomUser
from django.contrib.auth import authenticate


class SignUpService():
    """"""
    @staticmethod
    def create_user(validated_data):
        """"""
        user = CustomUser.objects.create_user(**validated_data)
        return user

    @staticmethod
    def validate(validated_data):
        """"""
        password = validated_data.get('password', '')
        print(f"password = {password}, len = {len(password)}")
        if len(password) >= 8:
            return True
        raise ValueError("Your Password must contains of 8 characters at least")

class LogInService():
    """"""
    @staticmethod
    def check_user_authenticated(request):
        """"""
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        return user