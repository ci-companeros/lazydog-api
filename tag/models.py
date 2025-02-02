from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    """
    Represents a tag that can be used to categorize resources
    
    Tags provide a way to add additional metadata to resources, 
    allowing for greater flexibility in resource categorization. 
    Tags can be associated with many resources, enabling users to find 
    content based on specific keywords. 
    """
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        """
        Automatically generates a unique slug from the name.
        If a duplicate slug exists, appends a number to make it unique.
        """
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

# Create your models here.
