from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
<<<<<<< HEAD
        if (request.user.is_authenticated
                and request.user.role == "admin"):
            return True
        return False
=======
        if request.user.is_authenticated and request.user.role == "admin":
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == "admin")


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
>>>>>>> origin/categories-genres-service
