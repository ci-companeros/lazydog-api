from rest_framework import viewsets, permissions, filters
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be
    created, viewed, edited, or deleted.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,]
    filter_backends = [filters.OrderingFilter,]
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
