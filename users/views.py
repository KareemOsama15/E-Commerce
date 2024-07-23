from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializerSignUp, UserSerializerInfo
from .services import SignUpService, LogInService
from .models import CustomUser


class SignUpApiView(GenericAPIView):
    """"""
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerSignUp

    def post(self, request):
        """"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            SignUpService.validate(serializer.validated_data)
            user = SignUpService.create_user(serializer.validated_data)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data['tokens'] = {
                'access': str(token.access_token),
                'refresh': str(token)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogInApiView(GenericAPIView):
    """"""
    permission_classes = (AllowAny,)

    def post(self, request):
        """"""
        user = LogInService.check_user_authenticated(request)
        if user:
            token = RefreshToken.for_user(user)
            data = {
                'username': user.username,
                'tokens': {
                    'access': str(token.access_token),
                    'refresh': str(token)
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogOutApiView(GenericAPIView):
    """"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """"""
        try:
            refreshToken = request.data.get('refresh')
            refresh = RefreshToken(refreshToken)
            refresh.blacklist()
            return Response({'message': 'Logout Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoApiView(ListAPIView):
    """"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerInfo
    permission_classes = (IsAdminUser,)
