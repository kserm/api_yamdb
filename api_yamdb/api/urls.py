from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserViewSet, CategoryViewSet, GenreViewSet, TitlesViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitlesViewSet, basename="titles")


urlpatterns = [
    path('v1/auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path("v1/", include(router.urls))
]
