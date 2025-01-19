from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResourceItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,
                                    related_name="resource item")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="created by")
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
