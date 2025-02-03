from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes the Tag model fields to be used in API responses.
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

    def validate_name(self, value):
        """Ensure tag name is unique before saving."""
        if Tag.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "A tag with this name already exists."
            )
        return value
