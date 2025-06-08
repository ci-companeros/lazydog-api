"""
Unit tests for the Bookmark model.

Covers:
- Creation of valid bookmarks.
- Prevention of duplicate bookmarks for same user and resource.
- String representation of bookmark objects.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from resource_item.models import ResourceItem
from bookmark.models import Bookmark
from django.db import IntegrityError


class BookmarkModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        cls.testuser2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        cls.adminuser = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword"
        )

        cls.resource1 = ResourceItem.objects.create(
            title="Test Resource 1", user=cls.testuser1
        )
        cls.resource2 = ResourceItem.objects.create(
            title="Test Resource 2", user=cls.testuser2
        )

        cls.bookmark1 = Bookmark.objects.create(
            user=cls.testuser1, resource=cls.resource1
            )
        cls.bookmark2 = Bookmark.objects.create(
            user=cls.testuser2, resource=cls.resource2
            )

    def test_create_valid_bookmark(self):
        """
        Test that a bookmark is created with correct fields.
        """
        self.assertEqual(self.bookmark1.user.username, "testuser1")
        self.assertEqual(self.bookmark1.resource.title, "Test Resource 1")
        self.assertIsNotNone(self.bookmark1.created_at)

    def test_str_representation(self):
        """
        Test string output of bookmark
        """
        expected = "testuser1 bookmarked Test Resource 1"
        self.assertEqual(str(self.bookmark1), expected)

    def test_duplicate_bookmark_not_allowed(self):
        """
        User should not be able to bookmark same resource twice.
        """
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(
                user=self.testuser1,
                resource=self.resource1
            )

    def test_cascade_delete_user(self):
        """
        When a user is deleted, their bookmarks should also be
        deleted (CASCADE).
        """
        self.testuser1.delete()
        remaining = Bookmark.objects.filter(user__username="testuser1")
        self.assertEqual(remaining.count(), 0)

    def test_cascade_delete_resource(self):
        """
        When a resource is deleted, related bookmarks should
        also be deleted (CASCADE).
        """
        self.resource1.delete()
        remaining = Bookmark.objects.filter(resource__title="Test Resource 1")
        self.assertEqual(remaining.count(), 0)

    def test_bookmark_ordering(self):
        """
        Bookmarks should be ordered by created_at descending (newest first).
        """
        bookmarks = Bookmark.objects.all()
        timestamps = [b.created_at for b in bookmarks]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))
