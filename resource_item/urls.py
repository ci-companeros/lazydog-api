from django.urls import path
from . import views

urlpatterns = [
    path('', views.resource_item, name='resource_item'),
]
