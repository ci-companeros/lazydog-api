from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

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
