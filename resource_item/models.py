from django.db import models
from django.contrib.auth.models import User
from category.models import Category
from tag.models import Tag

# Create your models here.


class ResourceItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="resource_items",
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_by"
    )
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True,  db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="resources") 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
