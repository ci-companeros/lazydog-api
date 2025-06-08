from rest_framework import viewsets, permissions, filters
from .models import Category
from .serializers import CategorySerializer
from lazydog_api.permissions import AdminOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset allows only admin users to create, update,
    and delete categories.
    All users can list and retrieve categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'name']
    search_fields = ['name', 'description']

