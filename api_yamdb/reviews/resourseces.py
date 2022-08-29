from import_export import resources

from reviews.models import Review, Title, Comment, User, Genres, Category, Genre


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        #fields= ("id", "score", "title", "author", "text", "pub_date")

class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre")


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment



class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ("id","username", "email","role","bio","first_name","last_name")


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre


class GenresTitleResource(resources.ModelResource):
    class Meta:
        model = Genres
