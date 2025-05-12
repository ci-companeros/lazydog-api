# Comment model for resource_item app
# Each comment is associated with a resource item,
# and each resource item can have multiple comments.
from django.contrib.auth.models import User
from django.db import models
from resource_item.models import ResourceItem

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_item = models.ForeignKey(
        ResourceItem, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
