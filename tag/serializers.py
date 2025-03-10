from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Converts Tag model instances to JSON format for API responses.
    Ensures users can only use existing tags.
    """
    class Meta:
        model = Tag
        fields = [
            'tag_id',
            'name',
            'description',
            'slug',
            'created_at',
            'updated_at'
        ]
