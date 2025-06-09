from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer
from lazydog_api.permissions import AdminOnly


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
    permission_classes = [AdminOnly]
