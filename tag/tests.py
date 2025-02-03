from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tag


class TagModelTest(TestCase):
    """
    Tests for the Tag model.
    """

    def test_create_tag(self):
        """Test that a Tag object can be created successfully."""
        tag = Tag.objects.create(
            name="Python",
            description="A programming language"
        )
        self.assertEqual(tag.name, "Python")
        self.assertEqual(tag.slug, slugify("Python"))  # Ensure slug is auto-generated

    def test_slug_auto_generation(self):
        """Test that a slug is automatically generated if not provided."""
        tag = Tag.objects.create(name="Django Framework")
        self.assertEqual(tag.slug, "django-framework")

    def test_slug_uniqueness(self):
        """Ensure slugs are unique, even for similar tag names."""
        tag1 = Tag.objects.create(name="React")
        tag2 = Tag.objects.create(name="React Unique")  # Force unique name
        self.assertNotEqual(tag1.slug, tag2.slug)  # Slugs should be different

    def test_empty_description(self):
        """Test that description can be empty."""
        tag = Tag.objects.create(name="JavaScript")
        self.assertEqual(tag.description, "")


class TagAPITest(TestCase):
    """
    Tests for the Tag API endpoints.
    """

    def setUp(self):
        """Set up test client and create a user for authentication."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_authenticate(user=self.user)  # Ensure authentication

        # Ensure tag object is fully saved and has an ID
        self.tag = Tag.objects.create(
            name="HTML",
            description="Markup language"
        )
        self.tag.refresh_from_db()  # Ensure ID is available

    def test_get_tags(self):
        """Test retrieving all tags."""
        response = self.client.get("/api/tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "HTML")

    def test_create_tag(self):
        """Test creating a tag via API."""
        data = {"name": "CSS", "description": "Stylesheet language"}
        response = self.client.post("/api/tags/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "CSS")
        self.assertEqual(response.data["slug"], "css")  # Slug should be auto-generated

    def test_duplicate_tag_name(self):
        """Test that creating a tag with the same name returns an error."""
        # Create initial tag in the API instead of directly in the database
        data = {"name": "HTML", "description": "Original Tag"}
        self.client.post("/api/tags/", data, format="json")

        # Try creating a duplicate via API
        response = self.client.post("/api/tags/", data, format="json")

        # Ensure API returns 400 instead of crashing with IntegrityError
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  # ✅ Ensure error is on the "name" field

    def test_update_tag(self):
        """Test updating an existing tag."""
        data = {"name": "Updated HTML", "description": "Updated description"}
        response = self.client.patch(
            f"/api/tags/{self.tag.tag_id}/", data, format="json"
        )  # Use `tag_id`
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated HTML")

    def test_delete_tag(self):
        """Test deleting a tag."""
        response = self.client.delete(f"/api/tags/{self.tag.tag_id}/")  # Use `tag_id`
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(tag_id=self.tag.tag_id).exists())  # Use `tag_id`

    def test_unauthenticated_create_tag(self):
        """
        Tests access control: unauthenticated users should receive either
        401 (Unauthorized) or 403 (Forbidden) when attempting to create a tag.
        """
        self.client.logout()  # Remove authentication
        data = {"name": "Node.js", "description": "JavaScript runtime"}
        response = self.client.post("/api/tags/", data)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )  # Accept both 401 and 403

    def test_invalid_name(self):
        """Test that creating a tag with no name returns an error."""
        data = {"name": "", "description": "Missing name"}
        response = self.client.post("/api/tags/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  # Ensure name field error is returned
