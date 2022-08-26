from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import (IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from api.permissions import (IsAdmin,
                             IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (
    UserSerializer,
    UserMeSerializer,
    CategorySerializer,
    GenreSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api.users_pagination import UsersPagination
from api.filters import TitlesFilter

from reviews.models import User, Category, Genre, Title, Review


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    permission_classes = (IsAdmin | IsAdminUser,)
    pagination_class = UsersPagination

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости
        от роли пользователя
        """
        if self.request.user.role == "user":
            return UserMeSerializer
        return UserSerializer

    @action(methods=["GET", "PATCH"],
            url_path="me", detail=False,
            permission_classes=(IsAuthenticated,),
            )
    def users_profile(self, request):
        serializer = self.get_serializer(self.request.user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                self.request.user,
                data=request.data,
                partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
