from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """

    class Meta:
        """
        Metadata for the Comment serializer.
        """
        model = Comment
        fields = ['id', 'user', 'resource_item', 'content',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Perform object-level validation for Comment updates.

        Prevents modification of the 'user' and 'resource_item' fields after creation
        by raising a ValidationError if either field is present in the update request.
        Allows normal validation during creation.
        """
        if self.instance:
            if 'user' in self.initial_data:
                raise serializers.ValidationError('User cannot be modified.')
            if 'resource_item' in self.initial_data:
                raise serializers.ValidationError('Resource item cannot be modified.')
        return data

    def create(self, validated_data):
        """Set the user from the request when creating a new comment."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
