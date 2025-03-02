from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to modify the model.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
