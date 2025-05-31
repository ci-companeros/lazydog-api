"""
Unit tests for the Tag serializer.

This test suite ensures correct serialization, deserialization, and validation
of Tag instances when using the TagSerializer class.

Focus areas:
- Correct output format and field presence in serialized data
- Validation of required and unique fields
- Behavior with valid and invalid input data
- Slug and default handling
"""
from rest_framework.test import APITestCase
from tag.serializers import TagSerializer
from tag.models import Tag


class TagSerializerTestCase(APITestCase):
    def test_serialized_fields(self):
        """
        Test that all required fields are included in serialized output.
        Ensures completeness of API response data.
        Expected: All defined fields present in serializer output.

        Confirms that clients receive all relevant metadata required
        to render or interact with Tag resources.
        """
        tag = Tag.objects.create(name="API")
        serializer = TagSerializer(tag)
        data = serializer.data
        self.assertIn("tag_id", data)
        self.assertIn("name", data)
        self.assertIn("slug", data)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_name_required(self):
        """
        Test that the name field is required for serializer input.
        Expected: Serializer is invalid without name.

        Validates serializer's safeguard against incomplete submissions
        which could otherwise break business logic or cause DB errors.
        """
        serializer = TagSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_unique_validation(self):
        """
        Test that serializer validates name uniqueness.
        Expected: Second tag with same name is rejected as invalid.

        Serializer should mirror model-level uniqueness logic to prevent
        early
        """
        Tag.objects.create(name="Unique")
        serializer = TagSerializer(data={"name": "Unique"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
