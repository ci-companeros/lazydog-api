"""
Unit tests for the Tag API enpoints.

This test suite verifies the full CRUD behaviour of the Tag model under
different user roles using Djange REST Framework and APITestCase. Each test
targets one of the following access levels:

Recommended test user structure:
- Regular user (is_staff=False)
    - Used to validate that POST, PATCH & DELETE actions ar blocked
    - Test users; user1, user 2
- Unauthentcated user
    - Used to validate thet POST is forbidden and GET is allowed
    - No login used
- Admin user (is_staff=True)
    - Has full access to  all CRUD operations
    - Tst user: admin_user
"""
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from tag.models import Tag


# SETUP
class TagAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create test data: admin user, two regular users, one tag,
        and URL endpoints
        """
        # Create an admin user
        cls.admin_user = User.objects.create_user(
            username='adminuser', password='adminpassword', is_staff=True
            )
        # Create a regular user
        cls.user1 = User.objects.create_user(
            username='testuser1', password='testpassword1', is_staff=False
            )
        cls.user2 = User.objects.create_user(
            username='testuser2', password='testpassword2', is_staff=False
            )
        # Create a tag instance for testing
        cls.tag = Tag.objects.create(name='Test Tag')
        cls.url = reverse("tag-list")
        cls.url_detail = reverse("tag-detail", args=[cls.tag.tag_id])

    # CREATE
    def test_create_tag_authenticated_asmin(self):
        """
        Ensure an admin user can successfully create a tag.
        Tests POST /tags/ with valid data and expects HTTP 201 Created.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(self.url, {"name": "django"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "django")

    def test_create_tag_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create tags.
        Tests POST /tags/ without login and expects HTTP 403 Forbidden.
        """
        respons = self.client.post(self.url, {"name": "unauth"})
        self.assertEqual(respons.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_tag_as_regular_user_forbidden(self):
        """
        Ensure regular users cannot create tags.
        Tests POST /tags/ as is_staff=False and expects HTTP 403 Forbidden.
        """
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(self.url, {"name": "unauthorized-tag"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_slug_is_generated_on_create(self):
        """
        Ensure slug is automatically generated based on name.
        Tests POST /tags/ and verifies slug begins with slugified name.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(
            self.url, {"name": "My Supercalifragilisticexpialidocious Tag"}
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["slug"].startswith(
            "my-supercalifragilisticexpialidocious-tag"
            )
        )

    # READ
    def test_list_tags(self):
        """
        Ensure tags can be listed without authentication.
        Tests GET /tags/ and expects HTTP 200 OK and at least one result.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_tag(self):
        """
        Ensure a specific tag can be retrieved by a logged-in user.
        Tests GET /tags/<id>/ and expects correct tag data returned.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Tag")

    # UPDATE
    def test_update_tag_as_admin(self):
        """
        Ensure a tag can be updated by an admin.
        Tests PATCH /tags/<id>/ and expects updated name in response.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.patch(self.url_detail, {"name": "Updated Tag"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Tag")

    def test_update_tag_as_non_admin_forbidden(self):
        """
        Ensure regular users cannot update tags.
        Tests PATCH /tags/<id>/ as is_staff=False and expects
        HTTP 403 Forbidden.
        """
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.patch(
            self.url_detail, {"name": "Unauthorized Update"}
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE
    def test_delete_tag_as_admin(self):
        """
        Ensure a tag can be deleted by an admin.
        Tests DELETE /tags/<id>/ and verifies tag is removed from database
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(tag_id=self.tag.tag_id).exists())

    def test_delete_tag_as_non_admin_forbidden(self):
        """
        Ensure regular users cannot delete tags.
        Tests DELETE /tags/<id>/ as is_staff=False and expects
        HTTP 403 Forbidden.
        """
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
