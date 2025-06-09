from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from category.models import Category
from tag.models import Tag


class ResourceItem(models.Model):
    """
    Represents a resource shared by a user, such as a tutorial, guide, or
    reference link.

    Fields:
        title (str): The title of the resource (max 200 characters).
        description (str): A short description of the resource
            (max 500 characters).
        category (Category): Optional foreign key to the Category model;
            groups resources by topic.
        user (User): Foreign key to the user who created/uploaded the resource.
        url (str): The (unique) URL to the resource.
        created_at (datetime): Timestamp when the resource was created.
        updated_at (datetime): Timestamp when the resource was last updated.
        tags (Tag): Many-to-many field for categorizing resources by multiple
            tags.
    """
    title = models.CharField(
        max_length=200,
        help_text="The title of the resource (max 200 characters)."
    )
    description = models.TextField(
        max_length=500,
        help_text="A short description of the resource (max 500 characters)."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="resource_items",
        null=True,
        blank=True,
        help_text="Optional. The main topic/category for this resource."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resources",
        help_text="The user who uploaded this resource."
    )
    url = models.URLField(
        unique=True,
        help_text="A unique URL pointing to the resource."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when this resource was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this resource was last updated."
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="resources",
        help_text="Optional. One or more tags for this resource."
    )

    def clean(self):
        """
        Custom validation for the ResourceItem model.
        """
        super().clean()
        
        # Enforce description max length constraint
        if self.description and len(self.description) > 500:
            raise ValidationError({
                'description': 'Ensure this value has at most 500 characters '
                              f'(it has {len(self.description)}).'
            })

    def __str__(self):
        """
        Returns the string representation of the resource, which is its title.
        """
        return self.title

    class Meta:
        """
        Metadata for the ResourceItem model.
        Orders items by descending creation date (newest first).
        """
        ordering = ["-created_at"]
