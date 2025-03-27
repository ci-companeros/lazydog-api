from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from .models import Rating
from .serializers import RatingSerializer
from .permissions import IsOwnerOrReadOnly


class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed, created, edited, or deleted.
    
    Filtering:
    - Filter by resource_item and user
    - Search by resource title
    - Order by created_at
    """
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['resource_item', 'user']
    search_fields = ['resource_item__title']
    ordering_fields = ['created_at', 'score']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
