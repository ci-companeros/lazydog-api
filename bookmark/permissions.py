from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow access to objects owned by the requesting user
        return obj.user == request.user
