from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookmarkViewSet

"""
This file defines the available API endpoints for the Bookmark model.
Provides standard CRUD operations through DRF's DefaultRouter.
"""

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]