from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role",)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["username", "email"]
            ),
        ]


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        read_only_fields = ("role",)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Это имя недопустимо"
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(
        regex=r"^[-a-zA-Z0-9_]+$",
        required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"
        extra_kwargs = {
            "url": {"lookup_field": "slug"}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"
        extra_kwargs = {
            "url": {"lookup_field": "slug"}
        }


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug",
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field="slug",
                                         many=True,
                                         queryset=Genre.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = "__all__"

    def get_rating(self, obj):
        reviews = list(Review.objects.filter(title_id=obj.id).values_list(
            "score", flat=True))
        if reviews:
            return round(sum(reviews) / len(reviews))
        return None

    def validate_genre(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Должен быть указан"
                                              " хотя бы один жанр")
        return value

    def validate_year(self, value):
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError("Год публикации должен быть "
                                              "не больше текущего!")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category = Category.objects.get(slug=data["category"])
        data["category"] = CategorySerializer(category).data
        genres = []
        for item in data["genre"]:
            genre = Genre.objects.get(slug=item)
            genres.append(GenreSerializer(genre).data)
        data["genre"] = genres
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError('Отзыв уже оставлен!')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
