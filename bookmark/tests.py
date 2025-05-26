from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from resource_item.models import ResourceItem
from bookmark.models import Bookmark


class BookmarkAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create test users, resource, and samplae bookmark"""
        cls.user_1 = User.objects.create_user(username="testuser1", password="testpassword")
        cls.user_2 = User.objects.create_user(username="testuser2", password="testpassword")
        cls.resource = ResourceItem.objects.create(
            title="Test Resource", user=cls.user_1
        )
        cls.bookmark = Bookmark.objects.create(user=cls.user_1, resource=cls.resource)
        cls.resource2 = ResourceItem.objects.create(title="Another Resource", user=cls.user_2)
        cls.bookmark2 = Bookmark.objects.create(user=cls.user_2, resource=cls.resource2)
        
        cls.url = reverse("bookmark-list")
        cls.url_detail = reverse("bookmark-detail", args=[cls.bookmark.id])

    def test_create_bookmark_success(self):
        """Ensure authenticated user can create a new bookmark"""
        logged_in = self.client.login(username="testuser1", password="testpassword")
        self.assertTrue(logged_in, msg="Login failed for testuser1")
        new_resource = ResourceItem.objects.create(title="New Resource", user=self.user_1)
        data = {"resource": new_resource.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user_1.id)
        self.assertEqual(response.data["resource"], new_resource.id)

    def test_create_duplicate_bookmark(self):
        """Ensure user cannot bookmark the same resource twice"""
        logged_in = self.client.login(username="testuser1", password="testpassword")
        self.assertTrue(logged_in, msg="Login failed for testuser1")

        data = {"resource": self.resource.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_bookmark_unauthenticated(self):
        """Ensure unauthenticated user cannot create a bookmark"""
        data = {"resource": self.resource.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_bookmark_by_owner(self):
        """Ensure bookmark can be deleted by its owner"""
        logged_in = self.client.login(username="testuser1", password="testpassword")
        self.assertTrue(logged_in, msg="Login failed for testuser1")

        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_bookmark_by_other_user(self):
        """Ensure users cannot delete bookmarks they do not own"""
        logged_in = self.client.login(username="testuser2", password="testpassword")
        self.assertTrue(logged_in, msg="Login failed for testuser2")

        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_bookmarks(self):
        """Ensure bookmarks can be listed without authentication"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
                
        self.assertGreaterEqual(len(response.data), 2)
        
        for item in response.data:
            self.assertIn("id", item)
            self.assertIn("user", item)
            self.assertIn("resource", item)
            self.assertIn("created_at", item)

    def test_filter_bookmarks_by_user(self):
        """Ensure bookmarks can be filtered by user"""
        response = self.client.get(self.url, {"user": self.user_1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)
        for bookmark in response.data:
            self.assertEqual(bookmark["user"], self.user_1.id)
            
    def test_filter_bookmarks_by_resource(self):
        """Ensure bookmarks can be filtered by resource"""
        response = self.client.get(self.url, {"resource": self.resource.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)
        for bookmark in response.data:
            self.assertEqual(bookmark["resource"], self.resource.id)
            
    def test_ordering_by_created_at(self):
        """Ensure bookmarks are ordered by created_at descending by default"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        created_at_list = [item["created_at"] for item in response.data]
        self.assertEqual(created_at_list, sorted(created_at_list, reverse=True))

    def test_disallowed_update(self):
        """Ensure PATCH is blocked via validation in the serializer"""
        logged_in = self.client.login(username="testuser1", password="testpassword")
        self.assertTrue(logged_in, msg="Login failed for testuser1")

        response = self.client.patch(self.url_detail, {"resource": self.resource.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    


    


        

        
        