from rest_framework import serializers
from .models import ResourceItem
from category.models import Category
import validators


class ResourceItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ResourceItem model.
    """

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

    class Meta:
        """
        Metadata for the ResourceItem serializer.
        """
        model = ResourceItem
        fields = ['id', 'title', 'description',
                  'category', 'user', 'url', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Ensure that title is unique per user.
        """
        user = self.context['request'].user
        # Check if the title already exists for this user
        if ResourceItem.objects.filter(title=value, user=user).exists():
            raise serializers.ValidationError(
                "You already have a resource with this title."
            )

        return value

    def validate_url(self, value):
        """
        Ensure the provided URL is valid.
        """
        if not validators.url(value):
            raise serializers.ValidationError("Enter a valid URL.")
        return value

    def validate_description(self, value):
        """
        Ensure the description has a reasonable length.
        """
        min_length = 10
        max_length = 500

        if len(value) < min_length:
            raise serializers.ValidationError(
                f"Description must be at least {min_length} characters long."
            )

        if len(value) > max_length:
            raise serializers.ValidationError(
                f"Description cannot exceed {max_length} characters."
            )

        return value

    def create(self, validated_data):
        """
        Set the user to the authenticated user when creating a ResourceItem.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
