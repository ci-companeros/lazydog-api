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
        Validate the comment data.
        Ensures resource item exists.
        """
        resource_item = data.get('resource_item')

        # Check that resource_item is provided
        if not resource_item:
            raise serializers.ValidationError('Resource item is required.')

        return data

    def create(self, validated_data):
        """Create a new comment, setting the user from the request"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
