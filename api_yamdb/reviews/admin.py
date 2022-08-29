from django.contrib import admin
from import_export.admin import ImportMixin

from .resourseces import (
    ReviewResource, CommentResource, TitleResource,
    UserResource, CategoryResource, GenreResource,
    GenresTitleResource)
from .models import (
    Review, Comment, Title, User,
    Category, Genre, Genres)


class ReviewAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ReviewResource


class CommentAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = CommentResource


class TitleAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = TitleResource


class UserAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = UserResource


class CategoryAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = CategoryResource


class GenreAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = GenreResource


class GenresTitleAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = GenresTitleResource


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Genres, GenresTitleAdmin)
