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
        Validate the serializer data.
        """
        # Check if the user is the same as the current user
        if self.context['request'].user != data['user']:
            raise serializers.ValidationError(
                "You can only create comments for yourself.")

        return data