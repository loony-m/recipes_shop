from rest_framework.permissions import SAFE_METHODS, BasePermission


class OnlyAdminOrRead(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)
