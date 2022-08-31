from django.contrib import admin

from .models import (Review, Category,
                     Genre, Title, Genres, Comment)


admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Genres)
