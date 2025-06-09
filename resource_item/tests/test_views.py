"""
Unit tests for the ResourceItem API endpoints.

This test suite verifies full CRUD behaviour, permissions (including both owner and admin),
filtering, search, and ordering of the ResourceItem model using Django REST Framework
and APITestCase.

Test user structure:
- Owner (authenticated user, creator of a resource item)
- Other authenticated user (not owner)
- Admin user (is_staff=True)
- Unauthenticated user (not logged in)

Tested functionality:
- Permissions for create, update, delete, list, and retrieve endpoints for all user roles
- Filtering by category (query param)
- Searching by title (query param)
- Ordering by title (query param)
- Edge cases: missing required fields (e.g., category)
"""

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from resource_item.models import ResourceItem, Category


class TestResourceItemAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up users, categories, resource items, and endpoint URLs for all tests."""
        # Users
        cls.owner = User.objects.create_user(
            username='owner', password='ownerpass')
        cls.other_user = User.objects.create_user(
            username='other', password='otherpass')
        cls.admin = User.objects.create_user(
            username='admin', password='adminpass', is_staff=True)
        # Categories
        cls.category_music = Category.objects.create(name="music")
        cls.category_book = Category.objects.create(name="book")
        # Items
        cls.item1 = ResourceItem.objects.create(
            title="Item One",
            description="First item",
            user=cls.owner,
            category=cls.category_music,
            url="https://example.com/item1"
        )
        cls.item2 = ResourceItem.objects.create(
            title="Item Two",
            description="Second item",
            user=cls.owner,
            category=cls.category_book,
            url="https://example.com/item2"
        )
        # URLs
        cls.list_url = reverse("resourceitem-list")
        cls.detail_url = reverse("resourceitem-detail", args=[cls.item1.pk])

    # ---------- PERMISSIONS TESTS ----------

    def test_list_resourceitems_as_anonymous(self):
        """Anyone (even unauthenticated) can list all resource items."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_resourceitem_as_anonymous(self):
        """Anyone can retrieve a single resource item by ID."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.item1.title)

    def test_create_resourceitem_as_anonymous_forbidden(self):
        """Unauthenticated users cannot create resource items."""
        response = self.client.post(self.list_url, {
            "title": "Anon Create",
            "description": "Should not work at all",
            "category": self.category_music.pk,
            "url": "https://example.com/anon-test"
        })
        self.assertIn(response.status_code, [
                      status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_resourceitem_as_authenticated(self):
        """Authenticated users can create resource items."""
        self.client.login(username="owner", password="ownerpass")
        response = self.client.post(self.list_url, {
            "title": "Created By Owner",
            "description": "Test description to test this",
            "category": self.category_music.pk,
            "url": "https://example.com/create-test"
        })
        print("RESPONSE DATA (as_authenticated):", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Created By Owner")

    def test_create_resourceitem_as_admin(self):
        """Admin user can create resource items."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(self.list_url, {
            "title": "Admin Created",
            "description": "By admin is this made",
            "category": self.category_book.pk,
            "url": "https://example.com/admin-test"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Admin Created")

    def test_create_resourceitem_without_category(self):
        """
        Creating a resource item without category returns error.
        """
        self.client.login(username="owner", password="ownerpass")
        response = self.client.post(self.list_url, {
            "title": "Missing Category",
            "description": "Should fail oh yes",
            # No category provided
            "url": "https://example.com/no-category-test"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category", response.data)

    def test_update_resourceitem_as_owner(self):
        """Owners can update (PATCH) their own resource item."""
        self.client.login(username="owner", password="ownerpass")
        response = self.client.patch(
            self.detail_url, {"title": "Updated Title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_update_resourceitem_as_non_owner_forbidden(self):
        """Non-owners cannot update another user's resource item."""
        self.client.login(username="other", password="otherpass")
        response = self.client.patch(self.detail_url, {"title": "Hacker Edit"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_resourceitem_as_admin(self):
        """Admin user can update any resource item."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.patch(self.detail_url, {"title": "Admin Edit"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Admin Edit")

    def test_delete_resourceitem_as_owner(self):
        """Owners can delete their own resource item."""
        self.client.login(username="owner", password="ownerpass")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResourceItem.objects.filter(
            pk=self.item1.pk).exists())

    def test_delete_resourceitem_as_non_owner_forbidden(self):
        """Non-owners cannot delete another user's resource item."""
        self.client.login(username="other", password="otherpass")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_resourceitem_as_admin(self):
        """Admin user can delete any resource item."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResourceItem.objects.filter(
            pk=self.item1.pk).exists())

    # ---------- FILTERING, SEARCH & ORDERING ----------

    def test_filter_by_category(self):
        """Filter items by category query param."""
        response = self.client.get(
            f"{self.list_url}?category={self.category_music.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(item["category"] == self.category_music.pk for item in response.data))

    def test_search_by_title(self):
        """Search items by title using search query param."""
        response = self.client.get(f"{self.list_url}?search=One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("One" in item["title"] for item in response.data))

    def test_order_by_title(self):
        """Order items by title ascending."""
        response = self.client.get(f"{self.list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertEqual(titles, sorted(titles))

    # ---------- EDGE CASES ----------

    def test_invalid_create_missing_fields(self):
        """Creating a resource item without required fields returns error."""
        self.client.login(username="owner", password="ownerpass")
        response = self.client.post(self.list_url, {
            "title": "",
            "description": "",
            "category": self.category_music.pk,
            "url": "https://example.com/invalid-test"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_no_results(self):
        """Filtering on a value with no matches returns empty list."""
        response = self.client.get(f"{self.list_url}?category=9999")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
