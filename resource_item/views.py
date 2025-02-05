from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import ResourceItem
from .serializers import ResourceItemSerializer


class ResourceItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ResourceItem model.

    This ViewSet supports ordering and searching.
    
    - Ordering is available on the following fields: 'created_at', 'title'.
    - Searching is available on the following fields: 'title', 'description'.

    You can extend the search fields by adding more fields to the 'search_fields' list.
    """
    serializer_class = ResourceItemSerializer
    queryset = ResourceItem.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'title']
    search_fields = ['title', 'description']
