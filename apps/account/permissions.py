from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrGuardian(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin or request.user.is_guardian)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsGuardian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_guardian or request.user.is_admin
        )


class IsAuxiliary(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_auxiliary or request.user.is_guardian or request.user.is_admin
        )