from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ( "username", "email", "first_name", "last_name",
                  "bio", "role",)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["username", "email"]
            ),
        ]





