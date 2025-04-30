from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a bookmark to delete it.
    Read-only access (GET, HEAD, OPTIONS) is allowed to everyone.
    """

    def has_permission(self, request, view):
        # Allow anyone to read, but only authenticated users can create/delete

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read access to everyone, write/delete only to the owner
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
