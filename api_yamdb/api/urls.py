from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path('v1/auth/token/',
    TokenObtainPairView.as_view(),
    name='token_obtain_pair'
         ),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("v1/", include(router.urls))
]
