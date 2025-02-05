from rest_framework import viewsets, permissions, filters
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions for the Category model.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'name']
    search_fields = ['name', 'description']
