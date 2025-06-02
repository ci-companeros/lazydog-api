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
        Ensure category names are unique (case-insensitive) except for the current instance.
        Normalize the name to title case.
        """
        normalized_value = value.strip().title()
        instance = getattr(self, "instance", None)

        qs = Category.objects.filter(name__iexact=normalized_value)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A category with this name already exists.")

        return normalized_value
