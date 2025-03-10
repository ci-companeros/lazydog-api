from rest_framework import viewsets, permissions
from .models import Tag
from .serializers import TagSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Read access for everyone.
    - Only admins and superusers can create, update, and delete tags.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access
        return request.user and request.user.is_staff  # Only admins can modify


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage tags.
    - Unauthenticated users: Can view tags.
    - Authenticated users: Can assign/remove predefined tags but cannot
      create new ones.
    - Admins/superusers: Full CRUD permissions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
