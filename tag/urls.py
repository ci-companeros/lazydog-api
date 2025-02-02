from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet


"""
This file defines the available API endpoints for the Tag model.
"""

# Using Django REST Framework's router to automatically generate URL patterns
router = DefaultRouter()
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
