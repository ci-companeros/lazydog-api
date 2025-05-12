from django.db import models
from django.contrib.auth.models import User
from resource_item.models import ResourceItem
from django.core.exceptions import ValidationError


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    resource_item = models.ForeignKey(
        ResourceItem,
        on_delete=models.CASCADE,
        related_name='ratings',
        db_index=True¢
    )
    score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'resource_item'],
                name='unique_rating_per_user_item'
            )
        ]
        ordering = ['-created_at']

    def clean(self):
        if not (1 <= self.score <= 5):
            raise ValidationError('Score must be between 1 and 5.')

    def get_score_display(self):
        """Return the display value for the score."""
        return dict(self.SCORE_CHOICES).get(self.score, 'Unknown score')

    def __str__(self):
        return (
            f'{self.user.username} rated '
            f'{self.resource_item} with {self.get_score_display()}'
        )
