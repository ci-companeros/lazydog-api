from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import ResourceItem
from .serializers import ResourceItemSerializer
from .permissions import IsOwnerOrReadOnly


class ResourceItemViewSet(viewsets.ModelViewSet):
    """
    This ViewSet provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions for the ResourceItem model.
    You can add more fields to the search and filter options
    """
    serializer_class = ResourceItemSerializer
    queryset = ResourceItem.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'title']
    search_fields = ['title', 'description']
