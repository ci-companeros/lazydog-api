from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a rating to edit or delete it.
    """

    def has_permission(self, request, view):
        """
        Allow authenticated users to create new ratings.
        Everyone can read.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow read access to all, but write/delete only for the owner.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
