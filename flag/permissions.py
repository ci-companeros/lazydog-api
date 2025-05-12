# flag/permissions.py
from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Allow read access to all, flag creation by authenticated users,
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

