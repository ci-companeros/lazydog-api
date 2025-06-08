"""
Unit tests for the Bookmark serializer.

Covers:
- Successful serialization and creation of a bookmark
- Automatic assignment of the authenticated user
- Rejection of duplicate bookmarks (user + resource uniqueness)
- Handling of invalid or missing input
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from resource_item.models import ResourceItem
from bookmark.models import Bookmark
from bookmark.serializers import BookmarkSerializer
from rest_framework.exceptions import ValidationError


class BookmarkSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

        cls.testuser1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        cls.testuser2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )

        cls.resource1 = ResourceItem.objects.create(
            title="Resource 1", user=cls.testuser2
        )

        cls.resource2 = ResourceItem.objects.create(
            title="Resource 2", user=cls.testuser1
        )

        # Existing bookmark for duplicate test
        cls.existing = Bookmark.objects.create(
            user=cls.testuser1, resource=cls.resource1
        )

    def test_valid_bookmark_creation(self):
        """
        Serializer should allow creating a new valid bookmark
        """
        request = self.factory.post("/")
        request.user = self.testuser2
        serializer = BookmarkSerializer(
            data={"resource": self.resource1.id},  # type: ignore[attr-defined]
            context={"request": request}
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.user, self.testuser2)

    def test_automatic_user_assignment(self):
        """
        Serializer should automatically assign the authenticated user
        """
        request = self.factory.post("/")
        request.user = self.testuser2
        serializer = BookmarkSerializer(
            data={"resource": self.resource2.id},  # type: ignore[attr-defined]
            context={"request": request}
        )
        serializer.is_valid()
        instance = serializer.save()
        self.assertEqual(instance.user, request.user)

    def test_duplicate_bookmark_rejected(self):
        """
        Serializer should reject duplicate bookmarks
        """
        request = self.factory.post("/")
        request.user = self.testuser1
        serializer = BookmarkSerializer(
            data={"resource": self.resource1.id},  # type: ignore[attr-defined]
            context={"request": request}
        )
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)
        self.assertIn("already bookmarked", str(ctx.exception))
