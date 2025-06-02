from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category


# Create your tests here.
class CategoryAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create all test data once for all tests"""
        cls.admin_user = User.objects.create_user(
            username="adminuser", password="adminpassword", is_staff=True
        )
        cls.normal_user = User.objects.create_user(
            username="normaluser", password="testpassword"
        )
        cls.category = Category.objects.create(
            name="Test Category", description="This is a test category."
        )
        cls.url = reverse("category-list")
        cls.url_detail = reverse("category-detail", args=[cls.category.id])

    def test_create_category_authenticated_admin(self):
        """
        Ensure an admin user can successfully create a category.
        Tests POST /categories/ with valid data and expects HTTP 201 Created.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(
            self.url, {"name": "New Category", "description": "This is a new category."}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Category")
        self.assertEqual(response.data["description"], "This is a new category.")

    def test_create_category_invalid_name(self):
        """
        Ensure category creation fails with invalid data.
        Tests POST /categories/ with missing name and expects HTTP 400 Bad Request.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(self.url, {"description": "Missing name."})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_create_category_invalid_description(self):
        """
        Ensure category creation fails with invalid description.
        Tests POST /categories/ with empty description and expects HTTP 400 Bad Request.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(self.url, {"name": "Invalid Category", "description": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)

    def test_create_category_unauthenticated_forbidden(self):
        """
        Ensure unauthenticated users cannot create categories.
        Tests POST /categories/ without login and expects HTTP 403 Forbidden.
        """
        response = self.client.post(
            self.url,
            {"name": "Unauthenticated Category", "description": "This should fail."},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_as_normal_user_forbidden(self):
        """
        Ensure normal users cannot create categories.
        Tests POST /categories/ as a normal user and expects HTTP 403 Forbidden.
        """
        self.client.login(username="normaluser", password="testpassword")
        response = self.client.post(
            self.url,
            {"name": "Unauthorized Category", "description": "This should fail."},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_categories(self):
        """
        Ensure all users can list categories.
        Tests GET /categories/ and expects HTTP 200 OK with category data.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_category(self):
        """
        Ensure all users can retrieve a specific category.
        Tests GET /categories/{id}/ and expects HTTP 200 OK with category data.
        """
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)
        self.assertEqual(response.data["description"], self.category.description)

    def test_update_category_authenticated_admin(self):
        """
        Ensure an admin user can update a category.
        Tests PATCH /categories/{id}/ with valid data and expects HTTP 200 OK.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.patch(
            self.url_detail,
            {"name": "Updated Category", "description": "Updated description."},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Category")
        self.assertEqual(self.category.description, "Updated description.")

    def test_partial_update_category_authenticated_admin(self):
        """
        Ensure an admin user can partially update a category.
        Tests PATCH /categories/{id}/ with partial data and expects HTTP 200 OK.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.patch(
            self.url_detail, {"description": "Partially updated description."}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.description, "Partially updated description.")

    def test_update_category_as_normal_user_forbidden(self):
        """
        Ensure normal users cannot update categories.
        Tests PATCH /categories/{id}/ as a normal user and expects HTTP 403 Forbidden.
        """
        self.client.login(username="normaluser", password="testpassword")
        response = self.client.patch(
            self.url_detail,
            {"name": "Unauthorized Update", "description": "This should fail."},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_unauthenticated(self):
        """
        Ensure unauthenticated users cannot update categories.
        Tests PATCH /categories/{id}/ without login and expects HTTP 403 Forbidden.
        """
        response = self.client.patch(
            self.url_detail,
            {"name": "Unauthenticated Update", "description": "This should fail."},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_nonexistent_category(self):
        """
        Ensure updating a nonexistent category returns 404 Not Found.
        Tests PATCH /categories/{id}/ with an invalid ID and expects HTTP 404 Not Found.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.patch(reverse("category-detail", args=[99999]), {"name": "Nonexistent"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_category_authenticated_admin(self):
        """
        Ensure an admin user can delete a category.
        Tests DELETE /categories/{id}/ and expects HTTP 204 No Content.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_delete_category_as_normal_user_forbidden(self):
        """
        Ensure normal users cannot delete categories.
        Tests DELETE /categories/{id}/ as a normal user and expects HTTP 403 Forbidden.
        """
        self.client.login(username="normaluser", password="testpassword")
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

    def test_delete_category_unauthenticated(self):
        """
        Ensure unauthenticated users cannot delete categories.
        Tests DELETE /categories/{id}/ without login and expects HTTP 403 Forbidden.
        """
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

    def test_category_name_uniqueness(self):
        """
        Ensure category names are unique.
        Tests POST /categories/ with a duplicate name and expects HTTP 400 Bad Request.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(
            self.url, {"name": "Test Category", "description": "Duplicate name test."}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name already exists.", str(response.data))

    def test_category_name_update_uniqueness(self):
        """
        Ensure category name can be updated to a unique name.
        Tests PATCH /categories/{id}/ with a new unique name and expects HTTP 200 OK.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.patch(self.url_detail, {"name": "Unique Category Name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Unique Category Name")

    def test_category_name_update_to_duplicate(self):
        """
        Ensure category name cannot be updated to a duplicate name.
        Tests PATCH /categories/{id}/ with a duplicate name and expects HTTP 400 Bad Request.
        """
        self.client.login(username="adminuser", password="adminpassword")
        Category.objects.create(
            name="Another Category", description="This is another category."
        )
        response = self.client.patch(self.url_detail, {"name": "Another Category"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name already exists.", str(response.data))

    def test_case_sensitivity_in_category_names(self):
        """
        Ensure category names are case-insensitive.
        Tests POST /categories/ with a name that differs only in case
        and expects HTTP 400 Bad Request.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(
            self.url, {"name": "test category", "description": "Case sensitivity test."}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name already exists.", str(response.data))

    def test_white_space_in_category_names(self):
        """
        Ensure category names with leading/trailing whitespace are trimmed.
        Tests POST /categories/ with a name that has leading/trailing whitespace
        and expects HTTP 201 Created with trimmed name.
        """
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.post(
            self.url,
            {"name": "  Trimmed Category  ", "description": "Whitespace test."},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Trimmed Category")
