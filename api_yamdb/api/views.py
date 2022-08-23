
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from api.permissions import IsAdmin, IsUser
from api.serializers import UserSerializer
from api.users_pagination import UsersPagination

from reviews.models import User




class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    permission_classes = (IsAdmin|IsAdminUser, )

    pagination_class = UsersPagination
    @action(methods=["GET", "PATCH"],url_path="me", detail=False,
            permission_classes=((IsAuthenticated,))
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        print(super().permission_classes)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                self.request.user,
                data=request.data,
                partial=True)
            serializer.is_valid()
            serializer.save()

        return Response(serializer.data)






