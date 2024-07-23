from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (SignUpApiView,
                    LogInApiView,
                    LogOutApiView,
                    UserInfoApiView
                    )


urlpatterns = [
    path('sign-up/', SignUpApiView.as_view()),
    path('login/', LogInApiView.as_view()),
    path('logout/', LogOutApiView.as_view()),
    path('info/', UserInfoApiView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]
