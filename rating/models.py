from django.db import models
from django.contrib.auth.models import User
from resource_item.models import ResourceItem


class Rating(models.Model):
    """Rating model for resource items.
    Each user can only give one rating per resource item.
    Score must be between 1 and 5 stars.
    """
    SCORE_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_item = models.ForeignKey(
        ResourceItem,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    score = models.IntegerField(
        choices=SCORE_CHOICES,
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'resource_item'],
                name='unique_rating_per_user_item'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} rated {self.resource_item} with {self.get_score_display()}'
