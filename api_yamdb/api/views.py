from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsUser
from api.serializers import UserSerializer
from reviews.models import User



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    def get_permissions(self):
        if self.request.user == self.kwargs.get("username"):
            return (IsAuthenticated(),)
        return (IsAdminUser(),)

