from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated \
        and request.user.role == "admin":
            return True
        return False

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return False
