from rest_framework import serializers
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializers for the Bookmark model.
    Ensures that user is set from the request and fields are validated.
    The user is not allowed to bookmark the same resource item multiple times.
    """

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'resource', 'created_at']
        read_only_fields = ['user', 'created_at']
        # Prevent mass assignment of user

    def validate(self, data):
        user = self.context['request'].user
        resource = data.get('resource')

        if Bookmark.objects.filter(user=user, resource=resource).exists():
            raise serializers.ValidationError(
                "You have already bookmarked this resource."
            )

        return data

    def create(self, validated_data):
        """
        Assign the currently authenticated user automatically.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
