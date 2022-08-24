from datetime import datetime
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField(blank=True)
    rating = models.IntegerField()
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name="titles")
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name="titles")

    class Meta:
        models.CheckConstraint(
            check=models.Q(year__lte=datetime.now().year),
            name="title_year_constraint"
        )
