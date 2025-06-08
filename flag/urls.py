# flag/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlagViewSet

router = DefaultRouter()
router.register(r'', FlagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
