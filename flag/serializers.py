from rest_framework import serializers
from .models import Flag

class FlagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Flag model.
    Handles validation and serialization of flag data.
    """

    class Meta:
        model = Flag
        fields = '__all__'
        read_only_fields = [
            'user', 'created_at', 'updated_at',
            'status', 'reviewed_by', 'reviewed_at'
        ]

    def validate(self, data):
        """
        Custom validation to ensure:
        - The user creating the flag matches the request user.
        - Either a resource or comment is flagged, but not both or neither.
        - A user cannot flag the same resource or comment more than once.
        """
        user = self.context['request'].user

        # Ensure the user creating the flag is the request user.
        if user != data['user']:
            raise serializers.ValidationError(
                "You can only create flags for yourself."
            )

        resource = data.get('resource')
        comment = data.get('comment')

        # Must flag either a resource or a comment, not both, not neither.
        if not resource and not comment:
            raise serializers.ValidationError(
                "You must flag either a resource or a comment."
            )
        if resource and comment:
            raise serializers.ValidationError(
                "You can only flag a resource or a comment, not both."
            )

        # Prevent duplicate flagging of the same resource or comment.
        if resource:
            exists = Flag.objects.filter(user=user, resource=resource).exists()
            if exists:
                raise serializers.ValidationError(
                    "You have already flagged this resource. Please wait for review."
                )

        if comment:
            exists = Flag.objects.filter(user=user, comment=comment).exists()
            if exists:
                raise serializers.ValidationError(
                    "You have already flagged this comment. Please wait for review."
                )

        return data

    def create(self, validated_data):
        """
        Custom create method to set the user automatically based on the request context.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
