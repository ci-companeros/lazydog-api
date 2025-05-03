from django.db import models
from django.contrib.auth.models import User
from resource_item.models import ResourceItem


class Bookmark(models.Model):
    """
    Model to represent a bookmark linking a user to a resource item.
    Ensures each user can only bookmark a resource once.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey(
        ResourceItem, on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')  # Prevent duplicate bookmarks
        ordering = ['-created_at']
        verbose_name = 'Bookmark'
        indexes = [
            models.Index(
                fields=['user', 'resource']
            ),  # Optimize lookup
        ]

    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"
