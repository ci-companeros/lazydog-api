from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model.
    Handles validation of ratings and ensures
    users can only rate once per resource.
    """
    class Meta:
        model = Rating
        fields = ['id', 'user', 'resource_item', 'score',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_score(self, value):
        """Validate that score is between 1 and 5"""
        if value not in [choice[0] for choice in Rating.SCORE_CHOICES]:
            raise ValidationError('Score must be between 1 and 5')
        return value

    def validate(self, data):
        """Validate that user hasn't already rated
        this resource and doesn't own it"""
        user = self.context['request'].user
        resource_item = data.get('resource_item')

        # Check that resource_item is provided
        if not resource_item:
            raise ValidationError('Resource item is required.')

        # ⛔ Prevent user from rating their own resource
        if resource_item.user == user:
            raise ValidationError('You cannot rate your own resource item.')

        # ✅ Check for existing rating
        if self.instance is None:
            existing_rating = Rating.objects.filter(
                user=user,
                resource_item=resource_item
            ).exists()
            if existing_rating:
                raise ValidationError(
                    'You have already rated this resource item.')

        return data

    def create(self, validated_data):
        """Create a new rating, setting the user from the request"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
