from rest_framework import viewsets, permissions, filters
from .models import Category
from .serializers import CategorySerializer
from .permissions import AdminOnly  # Importera din custom permission


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset allows only admin users to create, update, 
    and delete categories.
    All users can list and retrieve categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'name']
    search_fields = ['name', 'description']

    def get_permissions(self):
        """
        Allow read-only access for all users, 
        but restrict modifications to admins.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [AdminOnly()]
