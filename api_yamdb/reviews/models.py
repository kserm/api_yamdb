from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["slug"]


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["slug"]


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre,
                                   through="Genres",
                                   related_name="genre")
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name="category")


class Genres(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              null=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE)



class User(AbstractUser):
    bio = models.TextField(
        "Биография",
        blank=True
    )
    ROLE_CHOICES = (
        ("user", "user"),
        ("admin", "admin"),
        ("moderator", "moderator"),
    )

    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
        default="user")


class Review(models.Model):
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )
