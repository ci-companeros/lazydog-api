from django.contrib.auth.models import User
from django.db import models
from resource_item.models import ResourceItem


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_item = models.ForeignKey(
        ResourceItem, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
