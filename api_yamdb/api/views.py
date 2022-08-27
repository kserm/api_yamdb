from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api.serializers import (SignUpSerializer, TokenSerializer,
                             UserMeSerializer, UserSerializer)
from api.utils import send_mail_function
from reviews.models import User


@api_view(["POST"])
def register_user(request):
    """Регистрация нового пользователя """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail_function(user, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token_for_users(request):
    """Получить токен"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
            user,
            serializer.validated_data["confirmation_code"]):
        token = AccessToken.for_user(user)
        return Response({"token": token},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """Логика работы с пользователями"""
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    permission_classes = (IsAdmin | IsAdminUser,)

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости
        от роли пользователя
        """
        if self.request.user.role == "user":
            return UserMeSerializer
        return UserSerializer

    @action(methods=["GET", "PATCH"], url_path="me", detail=False,
            permission_classes=(IsAuthenticated,))
    def users_profile(self, request):
        """Метод обрабатывает запрос users/me"""
        serializer = self.get_serializer(self.request.user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                self.request.user,
                data=request.data,
                partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)
