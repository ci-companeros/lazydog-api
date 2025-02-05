from rest_framework import serializers
from .models import ResourceItem


class ResourceItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ResourceItem model.
    """

    class Meta:
        """
        Metadata for the ResourceItem serializer.
        """
        model = ResourceItem
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

    def validate_name(self, value):
        """
        Validate the name field to ensure uniqueness.
        """
        if ResourceItem.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "An item with this name already exists.")
        return value
