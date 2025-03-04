from rest_framework import serializers
from .models import Flag


class FlagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Flag model.
    """

    class Meta:
        """
        Metadata for the Flag serializer.
        """
        model = Flag
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'status', 'reviewed_by', 'reviewed_at']

    def validate(self, data):
        """
        Validate the serializer data.
        """
        # Check if the user is the same as the current user
        if self.context['request'].user != data['user']:
            raise serializers.ValidationError(
                "You can only create flags for yourself.")
        
        # Ensure at least one of resource or comment is provided
        if not data.get('resource') and not data.get('comment'):
            raise serializers.ValidationError(
                "You must flag either a resource or a comment.")

        return data