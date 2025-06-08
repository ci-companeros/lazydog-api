from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ResourceItem
from .serializers import ResourceItemSerializer
from lazydog_api.permissions import IsOwnerOrAdminOrReadOnly


class ResourceItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows resource items to be viewed, created,
    edited, or deleted.

    Filtering:
    - Filter by category and tags
    - Search by title and description
    - Order by created_at and title

    Permissions:
    - Anyone can view resources
    - Only authenticated users can create resources
    - Only owners can edit/delete their resources
    """

    serializer_class = ResourceItemSerializer
    queryset = ResourceItem.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "tags", "user"]
    ordering_fields = ["created_at", "title"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
