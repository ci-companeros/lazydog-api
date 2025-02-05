from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceItemViewSet


"""
This file defines the available API endpoints for the ResourceItem model.
Provides standard CRUD operations through DRF's DefaultRouter.
"""

router = DefaultRouter()
router.register(r'', ResourceItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
