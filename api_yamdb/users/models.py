from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import (
    UsernameSimbolsValidator, validate_name_me)


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE_CHOICES = (
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
    )
    username_simbols_validator = UsernameSimbolsValidator()

    username = models.CharField(
        validators=(
            username_simbols_validator,
            validate_name_me
        ),
        unique=True,
        max_length=150
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        blank=True
    )
    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
        default="user")

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
