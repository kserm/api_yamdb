from import_export import resources

from reviews.models import (Review, Title, Comment,
                            User, Genres, Category, Genre)


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre


class GenresTitleResource(resources.ModelResource):
    class Meta:
        model = Genres
