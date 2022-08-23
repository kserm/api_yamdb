
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, generics, serializers, status

from api.permissions import IsAdmin
from api.serializers import UserSerializer

from reviews.models import User



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    permission_classes = (IsAdmin|IsAdminUser,)
    pagination_class = LimitOffsetPagination
    @action(url_path="me", detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)






