from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Validates the name to ensure that no two categories have the same name.
    """

    class Meta:
        """
        Metadata for the serializer.
        """
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

    def validate_name(self, value):
        """
        Validate the name field.

        Check if a category with the given name already exists.
        If it does, raise a Validation Error.
        """
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )
        return value
