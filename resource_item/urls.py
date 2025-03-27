from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceItemViewSet

router = DefaultRouter()
router.register(r'', ResourceItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
