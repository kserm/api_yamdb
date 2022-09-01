from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return(request.user.is_authenticated
               and request.user.role == "admin"
               or request.user.is_staff)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == "admin"
                or request.user.is_staff)


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or obj.author == request.user
            or request.user.role == "admin"
            or request.user.role == "moderator"
        )
