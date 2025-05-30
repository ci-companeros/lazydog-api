from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

"""
This file defines the available API endpoints for the Category model.
Provides standard CRUD operations through DRF's DefaultRouter.
"""

router = DefaultRouter()
router.register(r'', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
