from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Rating

"""
Signals for the Rating app.

Automatically updates the average_rating and rating_count fields
on the related ResourceItem whenever a Rating is created, updated, or deleted.
This ensures that rating statistics are always accurate, regardless of
whether changes are made through the API, Django admin, or elsewhere.
"""


@receiver([post_save, post_delete], sender=Rating)
def update_resource_rating(sender, instance, **kwargs):
    resource = instance.resource_item
    ratings = resource.ratings.all()
    count = ratings.count()
    avg = ratings.aggregate(Avg('score'))['score__avg'] or 0.0
    resource.average_rating = round(avg, 1)
    resource.rating_count = count
    resource.save()
