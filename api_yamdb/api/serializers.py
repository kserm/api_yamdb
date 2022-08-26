from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import User, Category, Genre, Titles


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())])

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


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        read_only_fields = ("role",)


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(regex=r"^[-a-zA-Z0-9_]+$",
                                  required=True,
                                  validators=[UniqueValidator(
                                      queryset=Category.objects.all())]
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
        model = Titles
        fields = "__all__"

    def get_rating(self, obj):
        # здесь будет расчет рейтинга
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
