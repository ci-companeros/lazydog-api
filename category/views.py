from rest_framework import viewsets, permissions, filters
from .models import Category
from .serializers import CategorySerializer
from .permissions import IsOwnerOrReadOnly  # 👈 Lägg till denna import


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions for the Category model.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'name']
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        """
        Set the user to the authenticated user when creating a category.
        """
        serializer.save(user=self.request.user)
