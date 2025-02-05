from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet


router = DefaultRouter()
"""
router
  - A Django Rest Framework SimpleRouter instance that maps URLs to views.
  - Automatically determines the URL conf based on the registered viewsets.
"""
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
