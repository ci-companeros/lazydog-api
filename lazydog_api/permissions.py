from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner/author of an item to delete it.
    Read-only access (GET, HEAD, OPTIONS) is allowed to everyone.
    """

    def has_permission(self, request, view):
        # Allow anyone to read, but only authenticated users can create/delete

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read access to everyone, write/delete only to the owner/author
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class AdminOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to modify the model.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAdminOrOwner(permissions.BasePermission):
    """
    Allow read access to all, creation by authenticated users,
    and edit/review only allowed for staff/admins.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff
        return False