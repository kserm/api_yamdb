from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint


class User(AbstractUser):
    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username="me"),
                name="not_me"),
            UniqueConstraint(
                fields=("email",),
                name="email_constraint"
            )
        ]

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE_CHOICES = (
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
    )

    username = models.CharField(
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
    last_name = models.CharField(
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
