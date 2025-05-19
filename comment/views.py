from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed, created, edited,
    or deleted.

    Filtering:
    - Filter by resource_item and user
    - Search by comment content
    - Order by created_at
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
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
    search_fields = ['content', 'resource_item__title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
