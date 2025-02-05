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
        fields = ['id', 'title', 'description',
                  'category', 'user', 'url', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Validate the title field to ensure uniqueness,
        except for the current instance.
        """
        instance = getattr(self, "instance", None)

        # Check if the title is unique, except for the current instance
        if instance is None or instance.title != value:
            if ResourceItem.objects.filter(title=value).exists():
                raise serializers.ValidationError(
                    "An item with this title already exists.")

        return value
