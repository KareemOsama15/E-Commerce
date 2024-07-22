from django.urls import path
from .views import SignUpApiView, LogInApiView


urlpatterns = [
    path('sign-up/', SignUpApiView.as_view()),
    path('log-in/', LogInApiView.as_view()),
]

