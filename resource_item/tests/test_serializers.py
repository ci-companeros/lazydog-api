"""
Unit tests for the ResourceItemSerializer.

This suite validates custom field validation and constraints for the ResourceItemSerializer.
Covers:
- Min/max length for description
- Valid/invalid URL
- Unique title per user
- Required fields
- Valid and invalid category
"""

from django.test import TestCase
from django.contrib.auth.models import User
from category.models import Category
from tag.models import Tag
from resource_item.models import ResourceItem
from resource_item.serializers import ResourceItemSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError


class ResourceItemSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up users, category, and tag for tests."""
        cls.user = User.objects.create_user(username="testuser", password="pw")
        cls.other_user = User.objects.create_user(username="other", password="pw")
        cls.category_html = Category.objects.create(name="HTML")
        cls.tag_python = Tag.objects.create(name="python")

    def get_context(self, user=None):
        """Return serializer context with a fake request and user."""
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user or self.user
        return {"request": request}

    def test_valid_serializer(self):
        """Serializer should be valid with correct data."""
        data = {
            "title": "HTML Guide",
            "description": "A great resource for HTML.",
            "category": self.category_html.pk,
            "tags": [self.tag_python.pk],
            "url": "https://html.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_description_too_short(self):
        """Should error if description is too short."""
        data = {
            "title": "Short desc",
            "description": "short",
            "category": self.category_html.pk,
            "tags": [],
            "url": "https://html.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)
        self.assertIn("at least 10 characters", serializer.errors["description"][0])

    def test_description_too_long(self):
        """Should error if description is too long."""
        data = {
            "title": "Long desc",
            "description": "x" * 501,
            "category": self.category_html.pk,
            "tags": [],
            "url": "https://html.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)
        self.assertIn("500", serializer.errors["description"][0])

    def test_invalid_url(self):
        """Should error if URL is not valid."""
        data = {
            "title": "Invalid url",
            "description": "Valid description for resource.",
            "category": self.category_html.pk,
            "tags": [],
            "url": "not-a-url"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("url", serializer.errors)
        self.assertIn("Enter a valid URL", serializer.errors["url"][0])

    def test_duplicate_title_for_same_user(self):
        """Should error if same user tries to create resource with same title."""
        ResourceItem.objects.create(
            title="Duplicate",
            description="Desc",
            category=self.category_html,
            user=self.user,
            url="https://unique1.com"
        )
        data = {
            "title": "Duplicate",
            "description": "Some new desc",
            "category": self.category_html.pk,
            "tags": [],
            "url": "https://unique2.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("already have a resource with this title", serializer.errors["title"][0])

    def test_duplicate_title_for_other_user_ok(self):
        """Should allow same title for different users."""
        ResourceItem.objects.create(
            title="Duplicate",
            description="Descriptions",
            category=self.category_html,
            user=self.other_user,
            url="https://unique3.com"
        )
        data = {
            "title": "Duplicate",
            "description": "Some description",
            "category": self.category_html.pk,
            "tags": [],
            "url": "https://unique4.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_category_required(self):
        """Should fail if category is not provided."""
        data = {
            "title": "No category",
            "description": "Valid description.",
            # "category": missing
            "tags": [],
            "url": "https://some.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)

    def test_tags_optional(self):
        """Should allow tags to be omitted (empty list)."""
        data = {
            "title": "No tags",
            "description": "Valid description.",
            "category": self.category_html.pk,
            "url": "https://some.com"
        }
        serializer = ResourceItemSerializer(
            data=data, context=self.get_context(self.user)
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
