#<<<<<<< HEAD
from api.views import UserViewSet, get_token_for_users, register_user
from django.urls import include, path
from rest_framework.routers import SimpleRouter
#=======
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import (UserViewSet,
                       CategoryViewSet,
                       GenreViewSet,
                       TitlesViewSet,
                       ReviewViewSet,
                       CommentViewSet)
#>>>>>>> origin/categories-genres-service

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitlesViewSet, basename="titles")
router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
#<<<<<<< HEAD
    path("v1/auth/token/", get_token_for_users),
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", register_user),
#=======
    path('v1/auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path("v1/", include(router.urls)),
    path('v1/', include(router_v1.urls)),
#>>>>>>> origin/categories-genres-service
]
