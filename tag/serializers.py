from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Converts Tag model instances to JSON format for API responses.
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
        """
        EValidates uniqueness of the tag name.
        Prevents duplicate tags from being created.
        """
        if Tag.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "A tag with this name already exists."
            )
        return value
