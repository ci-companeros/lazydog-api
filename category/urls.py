from django.urls import path
from .views import CategoryViewSet

urlpatterns = [
    path('', CategoryViewSet.as_view({'get': 'list'})),
]
