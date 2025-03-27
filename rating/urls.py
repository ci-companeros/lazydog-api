from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet

"""
This file defines the available API endpoints for the Rating model.
Provides standard CRUD operations through DRF's DefaultRouter.
"""

router = DefaultRouter()
router.register(r'', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
