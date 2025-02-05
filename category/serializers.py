from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'user',
                  'created_at', 'updated_at']
        read_only_fields = ['user']

    def validate_name(self, value):
        """
        Validate the name field, except for the current instance.
        """
        instance = getattr(self, "instance", None)

        if instance is None or instance.name != value:
            if Category.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    "A category with this name already exists."
                )

        return value

    def create(self, validated_data):
        """
        Set the user to the authenticated user when creating a category.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
