from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import


"""
This file defines the available API endpoints for the comment model.
Provides standard CRUD operations through DRF's DefaultRouter.
"""

router = DefaultRouter()
router.register(r'', )

urlpatterns = [
    path('', include(router.urls)),
]
