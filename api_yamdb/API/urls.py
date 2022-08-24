from rest_framework import routers
from django.urls import include, path
from api import views


router = routers.DefaultRouter()
router.register(r"titles", views.TitlesViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"genre", views.GenreViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
]
