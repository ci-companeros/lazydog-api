from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ResourceItem
from .serializers import ResourceItemSerializer


class ResourceItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ResourceItem model.
    """
    serializer_class = ResourceItemSerializer
    queryset = ResourceItem.objects.all()
    permission_classes = [IsAuthenticated]
