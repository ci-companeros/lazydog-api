# bookmark/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bookmark
from .serializers import BookmarkSerializer
from lazydog_api.permissions import IsOwnerOrReadOnly


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to create, view, delete their bookmarks.
    Provides filtering and sorting capabilities.
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_fields = ['user', 'resource']
    # Allow filtering by user or resource
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Default ordering by creation date
    
    def get_queryset(self):
        """
        Return only the bookmarks belonging to the currently authenticated 
        user. Prevents users from seeing others' bookmarks.
        """
        user = self.request.user
        if user.is_authenticated:
            return Bookmark.objects.filter(user=user)
        return Bookmark.objects.none()

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user as the owner when creating a bookmark.
        Prevents spoofing another user in the POST payload.
        """
        serializer.save(user=self.request.user)
