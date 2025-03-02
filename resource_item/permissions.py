from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a resource to edit or delete it.
    """

    def has_permission(self, request, view):
        """
        Allow authenticated users to create new objects.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow read access to all, but write access only to the owner.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
