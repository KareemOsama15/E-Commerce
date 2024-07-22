from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """"""
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username