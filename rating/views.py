from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from django.db.models import Avg
from .models import Rating
from .serializers import RatingSerializer
from lazydog_api.permissions import IsOwnerOrReadOnly


class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed, created, edited, or deleted.

    When a rating is created, updated, or deleted, the average rating
    and rating count fields on the related ResourceItem are automatically
    recalculated and updated.

    Filtering:
    - Filter by resource_item and user
    - Search by resource title
    - Order by created_at and score
    """

    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["resource_item", "user"]
    search_fields = ["resource_item__title"]
    ordering_fields = ["created_at", "score"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        rating = serializer.save(user=self.request.user)
        self.update_resource_ratings(rating.resource_item)

    def perform_update(self, serializer):
        rating = serializer.save()
        self.update_resource_ratings(rating.resource_item)

    def perform_destroy(self, instance):
        resource_item = instance.resource_item
        instance.delete()
        self.update_resource_ratings(resource_item)

    def update_resource_ratings(self, resource_item):
        ratings = resource_item.ratings.all()
        count = ratings.count()
        avg = ratings.aggregate(Avg('score'))['score__avg'] or 0.0
        resource_item.average_rating = round(avg, 1)
        resource_item.rating_count = count
        resource_item.save()
