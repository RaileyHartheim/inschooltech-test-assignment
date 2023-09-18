from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Overridden user class. """

    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Email",
        help_text="Enter your email",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
