# flag/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Flag
from .serializers import FlagSerializer
from .permissions import IsAdminOrOwner


class FlagViewSet(viewsets.ModelViewSet):
    queryset = Flag.objects.all()
    serializers_class = FlagSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrOwner,
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ['resource_item', 'user', 'comment', 'status']
    search_fields = ['reason']
    ordering_fields = ['created_at', 'status']
    ordering = ['_created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
