from api.views import UserViewSet, get_token_for_users, register_user
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path('v1/auth/token/', get_token_for_users),
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", register_user),
]
