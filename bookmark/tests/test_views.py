"""
Unit tests for the Bookmark views (API endpoints).

Covers:
- List view access and response for authenticated users
- Rejection of unauthenticated actions
- Creation and deletion of bookmarks through API
- Permission handling (only owner can delete)
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from resource_item.models import ResourceItem
from bookmark.models import Bookmark


# SETUP
class BookmarkViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.testuser1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        cls.testuser2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )

        cls.resource1 = ResourceItem.objects.create(
            title="Resource 1",
            user=cls.testuser2,
            url="https://example.com/view-1"
        )

        cls.resource2 = ResourceItem.objects.create(
            title="Resource 2",
            user=cls.testuser1,
            url="https://example.com/view-2"
        )

        cls.bookmark = Bookmark.objects.create(
            user=cls.testuser1, resource=cls.resource1
        )

        cls.list_url = reverse("bookmark-list")
        cls.detail_url = reverse(
            "bookmark-detail",
            args=[cls.bookmark.id]  # type: ignore[attr-defined]
        )

    # GET
    def test_list_bookmarks_authenticated(self):
        """
        Authenticated users should be able to list their bookmarks.
        """
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # type: ignore[attr-defined]
        self.assertEqual(
            response.data[0]["user"],  # type: ignore[attr-defined]
            self.testuser1.id  # type: ignore[attr-defined]
        )

    def test_retrieve_single_bookmark(self):
        """
        Authenticated users should be able to retrieve a specific bookmark
        by ID.
        """
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["id"],  # type: ignore[attr-defined]
            self.bookmark.id  # type: ignore[attr-defined]
        )

    def test_retrieve_bookmark_unauthenticated(self):
        """
        Unauthenticated users should not be able to retrieve a
        specific bookmark.
        """
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_bookmark_by_non_owner(self):
        """
        Non-owners should not be able to retrieve bookmarks they do not own.
        """
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # POST
    def test_create_bookmark_authenticated(self):
        """
        Authenticated users should be able to create a new bookmark.
        """
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.post(
            self.list_url,
            {"resource": self.resource2.id}  # type: ignore[attr-defined]
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["user"],  # type: ignore[attr-defined]
            self.testuser2.id  # type: ignore[attr-defined]
        )
        self.assertEqual(
            response.data["resource"],  # type: ignore[attr-defined]
            self.resource2.id  # type: ignore[attr-defined]
        )

    def test_create_bookmark_unauthenticated(self):
        """
        Unauthenticated users should not be able to create bookmarks.
        """
        self.client.logout()
        response = self.client.post(
            self.list_url,
            {"resource": self.resource2.id}  # type: ignore[attr-defined]
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_prevent_duplicate_bookmark_api(self):
        """
        API should prevent a user from bookmarking the same resource twice.
        """
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.post(
            self.list_url,
            {"resource": self.resource1.id}  # type: ignore[attr-defined]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "already bookmarked",
            str(response.data)  # type: ignore[attr-defined]
        )

    # DELETE
    def test_delete_bookmark_by_owner(self):
        """
        The owner of a bookmark should be able to delete it.
        """
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Bookmark.objects.filter(id=self.bookmark.id).exists()  # type: ignore[attr-defined]
        )

    def test_delete_bookmark_by_non_owner(self):
        """
        Non-owners should not be able to delete bookmarks they do not own.
        """
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Bookmark.objects.filter(id=self.bookmark.id).exists()  # type: ignore[attr-defined]
        )

    def test_delete_bookmark_unauthenticated(self):
        """
        Unauthenticated users should not be able to delete any bookmarks.
        """
        self.client.logout() 
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Bookmark.objects.filter(id=self.bookmark.id).exists()  # type: ignore[attr-defined]
        )
